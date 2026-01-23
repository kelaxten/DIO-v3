# Extract DIO Model to JSON for Web Application
# This script loads the pre-built DIO v2.0 model and exports key components to JSON

library(jsonlite)

cat("Loading DIO model...\n")

# Load the pre-built DIO model
DIO <- readRDS("EPA-DIO-original/model/DIO.rds")

cat("Model loaded successfully!\n")
cat("Sectors:", nrow(DIO$A), "\n")
cat("Flows:", nrow(DIO$B), "\n\n")

# Create output directory
output_dir <- "open-dio-web/data"
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Helper function to convert matrix to JSON-friendly format
matrix_to_json <- function(mat, filename) {
  if (!is.null(mat)) {
    df <- as.data.frame(as.matrix(mat))
    df$rownames <- rownames(mat)
    write_json(df, file.path(output_dir, filename),
               pretty = TRUE, digits = 10, auto_unbox = FALSE)
    cat(paste("✓ Exported:", filename, "\n"))
  } else {
    cat(paste("✗ Skipped:", filename, "(NULL)\n"))
  }
}

cat("\nExporting matrices...\n")

# Export key matrices (reduced precision for web app)
# For a web demo, we'll export a subset to keep file sizes manageable

# 1. Impact multipliers (N matrix) - most important for calculations
if (!is.null(DIO$N)) {
  matrix_to_json(DIO$N, "N_matrix.json")
}

# 2. Sector metadata
if (!is.null(DIO$Commodities)) {
  sectors_df <- as.data.frame(DIO$Commodities)
  write_json(sectors_df, file.path(output_dir, "sectors.json"),
             pretty = TRUE, auto_unbox = FALSE)
  cat("✓ Exported: sectors.json\n")
}

# 3. Impact category metadata
if (!is.null(DIO$Indicators) && !is.null(DIO$Indicators$meta)) {
  indicators_df <- as.data.frame(DIO$Indicators$meta)
  write_json(indicators_df, file.path(output_dir, "indicators.json"),
             pretty = TRUE, auto_unbox = FALSE)
  cat("✓ Exported: indicators.json\n")
}

# 4. Model info
model_info <- list(
  model_name = "DIO v2.0",
  io_year = DIO$specs$IOYear,
  sectors = nrow(DIO$A),
  satellite_flows = nrow(DIO$B),
  impact_categories = nrow(DIO$C),
  description = "Defense Input-Output Model v2.0 from EPA",
  source = "https://github.com/USEPA/DIO"
)

write_json(model_info, file.path(output_dir, "model_info.json"),
           pretty = TRUE, auto_unbox = TRUE)
cat("✓ Exported: model_info.json\n")

# 5. Create a simplified sector list for UI (defense-relevant sectors)
# Extract key defense sectors for the demo
defense_sector_codes <- c(
  "336411", "336414", "336413", "336611", "336992",
  "541330", "541512", "541715", "237990", "324110"
)

if (!is.null(DIO$Commodities)) {
  all_sectors <- as.data.frame(DIO$Commodities)

  # Try to find defense sectors by code
  defense_sectors <- all_sectors[all_sectors$Code %in% defense_sector_codes, ]

  # If no matches, take first 20 sectors as sample
  if (nrow(defense_sectors) == 0) {
    cat("Note: Using sample sectors (defense codes not found in exact match)\n")
    defense_sectors <- head(all_sectors, 20)
  }

  write_json(defense_sectors, file.path(output_dir, "defense_sectors.json"),
             pretty = TRUE, auto_unbox = FALSE)
  cat("✓ Exported: defense_sectors.json (", nrow(defense_sectors), "sectors)\n")
}

cat("\n========================================\n")
cat("Export complete!\n")
cat("Files created in:", output_dir, "\n")
cat("========================================\n")

# List all exported files with sizes
files <- list.files(output_dir, full.names = TRUE)
for (f in files) {
  size <- file.size(f)
  size_kb <- round(size / 1024, 1)
  cat(paste("  -", basename(f), ":", size_kb, "KB\n"))
}
