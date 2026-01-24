#!/usr/bin/env Rscript
# Extract DIO Multipliers for Open DIO Backend
#
# This script:
# 1. Builds or loads the DIO v2.0 model using Cornerstone useeior
# 2. Extracts N matrix (total environmental multipliers)
# 3. Identifies defense-relevant sectors
# 4. Exports in JSON format for the backend API
#
# Usage: Rscript extract_multipliers_for_backend.R

library(jsonlite)

cat("\n")
cat("================================================================\n")
cat("  EXTRACTING DIO MULTIPLIERS FOR OPEN DIO BACKEND\n")
cat("================================================================\n\n")

# Step 1: Check if model already exists
cat("[1/6] Checking for existing DIO model...\n")

model_file <- "DIO-updated/model/DIO_Cornerstone.rds"
use_existing <- FALSE

if (file.exists(model_file)) {
  cat("  Found existing model:", model_file, "\n")
  cat("  Use existing model? (y/n, default=y): ")

  # For automated runs, default to yes
  use_existing <- TRUE
  cat("yes (automated)\n")
} else {
  cat("  No existing model found\n")
}

# Step 2: Load or build model
cat("\n[2/6] Loading DIO model...\n")

if (use_existing && file.exists(model_file)) {
  DIO <- readRDS(model_file)
  cat("  ✓ Model loaded from:", model_file, "\n")
} else {
  cat("  Building model from scratch...\n")
  cat("  NOTE: This will take 15-30 minutes\n\n")

  # Install dependencies if needed
  if (!"devtools" %in% installed.packages()[, "Package"]) {
    install.packages("devtools")
  }
  if (!"useeior" %in% installed.packages()[, "Package"]) {
    library(devtools)
    devtools::install_github("cornerstone-data/useeior@v1.8.0", upgrade = "never")
  }

  library(useeior)

  # Build model
  modelname <- "DIOv2.0"
  configpaths <- file.path("DIO-updated/data", c("DIOv2.0.yml", "DIOProcesses.yml"))

  DIO <- useeior::buildModel(modelname, configpaths)

  # Save for future use
  dir.create("DIO-updated/model", showWarnings = FALSE, recursive = TRUE)
  saveRDS(DIO, model_file)
  cat("  ✓ Model built and saved\n")
}

cat("  Sectors:", nrow(DIO$A), "\n")
cat("  Satellite flows:", nrow(DIO$B), "\n")
cat("  Impact categories:", nrow(DIO$C), "\n")

# Step 3: Extract sector information
cat("\n[3/6] Extracting sector information...\n")

sectors_df <- as.data.frame(DIO$Commodities)
n_sectors <- nrow(sectors_df)

cat("  Total sectors:", n_sectors, "\n")
cat("  Columns:", paste(colnames(sectors_df), collapse=", "), "\n")

# Step 4: Identify defense-relevant sectors
cat("\n[4/6] Identifying defense-relevant sectors...\n")

# Defense sector NAICS codes
defense_naics <- c(
  "336411",  # Aircraft Manufacturing
  "336412",  # Aircraft Engine and Engine Parts Manufacturing
  "336413",  # Other Aircraft Parts and Auxiliary Equipment Manufacturing
  "336414",  # Guided Missile and Space Vehicle Manufacturing
  "33641A",  # Aircraft/Guided missile related (aggregated)
  "336611",  # Ship Building and Repairing
  "336992",  # Military Armored Vehicle, Tank, and Tank Component Manufacturing
  "332993",  # Ammunition (except Small Arms) Manufacturing
  "332994",  # Small Arms Ammunition Manufacturing
  "33299A",  # Ammunition, arms, ordnance and accessories manufacturing (aggregated)
  "334220",  # Radio and Television Broadcasting and Wireless Communications Equipment
  "334290",  # Other Communications Equipment Manufacturing
  "334511",  # Search, Detection, and Navigation Instrument Manufacturing
  "334519",  # Other Measuring and Controlling Device Manufacturing
  "334413",  # Semiconductor and Related Device Manufacturing
  "541330",  # Engineering Services
  "541512",  # Computer Systems Design Services
  "541715",  # R&D in the Physical, Engineering, and Life Sciences
  "237310",  # Highway, Street, and Bridge Construction
  "237990",  # Other Heavy and Civil Engineering Construction
  "541610",  # Management Consulting Services
  "561210",  # Facilities Support Services
  "561499",  # All Other Business Support Services
  "721"      # Accommodation
)

# Keywords for sector names
defense_keywords <- c(
  "aircraft", "missile", "ship", "vessel", "naval", "marine",
  "ammunition", "arms", "ordnance", "weapon", "military",
  "defense", "armored", "tank", "radar", "navigation",
  "aerospace", "guided missile"
)

# Mark defense-relevant sectors
sectors_df$is_defense_relevant <- FALSE

# Match by code
if ("Code" %in% colnames(sectors_df)) {
  code_matches <- sectors_df$Code %in% defense_naics
  sectors_df$is_defense_relevant[code_matches] <- TRUE
  cat("  Matched by code:", sum(code_matches), "sectors\n")
}

# Match by name (case-insensitive)
if ("Name" %in% colnames(sectors_df)) {
  for (keyword in defense_keywords) {
    name_matches <- grepl(keyword, sectors_df$Name, ignore.case = TRUE)
    sectors_df$is_defense_relevant[name_matches] <- TRUE
  }
}

n_defense <- sum(sectors_df$is_defense_relevant)
cat("  Total defense-relevant sectors:", n_defense, "\n")

if (n_defense > 0) {
  cat("\n  Defense sectors identified:\n")
  defense_sectors <- sectors_df[sectors_df$is_defense_relevant, c("Code", "Name")]
  print(head(defense_sectors, 20))
}

# Step 5: Extract N matrix (total environmental multipliers)
cat("\n[5/6] Extracting environmental multipliers (N matrix)...\n")

if (is.null(DIO$N)) {
  stop("ERROR: N matrix not found in model. Model may not have built correctly.")
}

N_matrix <- as.matrix(DIO$N)
cat("  N matrix dimensions:", nrow(N_matrix), "×", ncol(N_matrix), "\n")
cat("  Impact categories:", nrow(N_matrix), "\n")
cat("  Sectors:", ncol(N_matrix), "\n")

# Get indicator metadata
indicators_df <- as.data.frame(DIO$Indicators$meta)
cat("  Indicators available:", nrow(indicators_df), "\n")

# Map indicators to our categories
# GHG, Energy, Water, Land
category_mapping <- list(
  GHG = c("Greenhouse Gases", "GHG", "Climate Change", "Global Warming"),
  Energy = c("Energy", "Primary Energy", "Total Energy"),
  Water = c("Water", "Freshwater", "Water Withdrawal", "Water Consumption"),
  Land = c("Land", "Land Use", "Land Occupation")
)

# Find matching indicators
find_indicator <- function(category_keywords, indicator_names) {
  for (keyword in category_keywords) {
    matches <- grepl(keyword, indicator_names, ignore.case = TRUE)
    if (any(matches)) {
      return(which(matches)[1])  # Return first match
    }
  }
  return(NA)
}

indicator_indices <- list(
  GHG = find_indicator(category_mapping$GHG, rownames(N_matrix)),
  Energy = find_indicator(category_mapping$Energy, rownames(N_matrix)),
  Water = find_indicator(category_mapping$Water, rownames(N_matrix)),
  Land = find_indicator(category_mapping$Land, rownames(N_matrix))
)

cat("\n  Mapped indicators:\n")
for (cat_name in names(indicator_indices)) {
  idx <- indicator_indices[[cat_name]]
  if (!is.na(idx)) {
    cat("    ", cat_name, "→", rownames(N_matrix)[idx], "\n")
  } else {
    cat("    ", cat_name, "→ NOT FOUND\n")
  }
}

# Step 6: Export to JSON
cat("\n[6/6] Exporting to JSON for backend...\n")

output_dir <- "backend/app/data"
dir.create(output_dir, showWarnings = FALSE, recursive = TRUE)

# Create multipliers output structure
multipliers_output <- list(
  description = "DIO v2.0 environmental impact multipliers from Cornerstone useeior",
  note = "Total multipliers including direct and indirect (supply chain) effects",
  methodology = "Based on EEIO analysis: M = B * L, where B is environmental satellite matrix and L is Leontief inverse",
  data_sources = paste(
    "EPA GHG Inventory (2016), USGS Water Use (2015),",
    "USDA/BLM/EIA Land Use (2012), USEEIO Energy (2014)"
  ),
  model_version = "DIO v2.0",
  useeior_version = as.character(packageVersion("useeior")),
  build_date = as.character(Sys.Date()),
  units = list(
    GHG = "kg CO2 eq per $ spending",
    Energy = "MJ per $ spending",
    Water = "m3 per $ spending (multiply by 264.172 for gallons)",
    Land = "m2*yr per $ spending"
  ),
  sectors = list()
)

# Extract multipliers for each sector
sector_codes <- if ("Code" %in% colnames(sectors_df)) sectors_df$Code else rownames(sectors_df)
sector_names <- if ("Name" %in% colnames(sectors_df)) sectors_df$Name else sector_codes

for (i in 1:n_sectors) {
  code <- sector_codes[i]
  name <- sector_names[i]

  # Extract multipliers (in per-dollar terms)
  mult_ghg <- if (!is.na(indicator_indices$GHG)) N_matrix[indicator_indices$GHG, i] else 0
  mult_energy <- if (!is.na(indicator_indices$Energy)) N_matrix[indicator_indices$Energy, i] else 0
  mult_water <- if (!is.na(indicator_indices$Water)) N_matrix[indicator_indices$Water, i] else 0
  mult_land <- if (!is.na(indicator_indices$Land)) N_matrix[indicator_indices$Land, i] else 0

  # Convert to per-$1000 for better readability
  multipliers_output$sectors[[code]] <- list(
    name = name,
    GHG = round(mult_ghg * 1000, 2),      # kg CO2 per $1000
    Energy = round(mult_energy * 1000, 2), # MJ per $1000
    Water = round(mult_water * 1000 * 264.172, 2), # gallons per $1000
    Land = round(mult_land * 1000, 2)      # m2-year per $1000
  )
}

# Save multipliers
mult_file <- file.path(output_dir, "multipliers.json")
write_json(multipliers_output, mult_file, pretty = TRUE, auto_unbox = TRUE)
cat("  ✓ Multipliers saved:", mult_file, "\n")
cat("    Total sectors:", length(multipliers_output$sectors), "\n")

# Save sector list
sectors_output <- lapply(1:n_sectors, function(i) {
  list(
    code = sector_codes[i],
    name = sector_names[i],
    is_defense_relevant = sectors_df$is_defense_relevant[i]
  )
})

sectors_file <- file.path(output_dir, "sectors_full.json")
write_json(sectors_output, sectors_file, pretty = TRUE, auto_unbox = TRUE)
cat("  ✓ Sectors saved:", sectors_file, "\n")

# Save defense sectors separately
defense_output <- sectors_output[sectors_df$is_defense_relevant]
defense_file <- file.path(output_dir, "sectors_defense.json")
write_json(defense_output, defense_file, pretty = TRUE, auto_unbox = TRUE)
cat("  ✓ Defense sectors saved:", defense_file, "\n")
cat("    Count:", length(defense_output), "\n")

# Save model info
model_info <- list(
  model = "DIO v2.0",
  useeior_version = as.character(packageVersion("useeior")),
  repository = "cornerstone-data/useeior",
  build_date = as.character(Sys.Date()),
  io_year = DIO$specs$IOYear,
  total_sectors = n_sectors,
  defense_sectors = n_defense,
  satellite_flows = nrow(DIO$B),
  impact_categories = nrow(DIO$C)
)

info_file <- file.path(output_dir, "model_info.json")
write_json(model_info, info_file, pretty = TRUE, auto_unbox = TRUE)
cat("  ✓ Model info saved:", info_file, "\n")

# Print summary statistics
cat("\n")
cat("================================================================\n")
cat("  EXTRACTION COMPLETE\n")
cat("================================================================\n\n")

cat("Summary:\n")
cat("  Total sectors:", n_sectors, "\n")
cat("  Defense sectors:", n_defense, "\n")
cat("  Output directory:", output_dir, "\n")

# Show sample multipliers
cat("\nSample multipliers (per $1000 spending):\n")
sample_codes <- head(sector_codes[sectors_df$is_defense_relevant], 5)
if (length(sample_codes) == 0) {
  sample_codes <- head(sector_codes, 5)
}

for (code in sample_codes) {
  mult <- multipliers_output$sectors[[code]]
  cat(sprintf("  %s (%s):\n", code, substr(mult$name, 1, 60)))
  cat(sprintf("    GHG: %.1f kg CO2  |  Energy: %.0f MJ  |  Water: %.0f gal  |  Land: %.1f m2-yr\n",
              mult$GHG, mult$Energy, mult$Water, mult$Land))
}

cat("\nNext steps:\n")
cat("  1. Restart backend API to load new multipliers\n")
cat("  2. Test calculations with real data\n")
cat("  3. Validate results against EPA documentation\n")
cat("  4. Update frontend with data quality indicator\n\n")
