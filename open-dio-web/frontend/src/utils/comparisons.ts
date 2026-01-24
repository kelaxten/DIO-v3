/**
 * Generate contextual comparisons for environmental impacts
 */

/**
 * Format large numbers for display
 */
export function formatNumber(value: number): string {
  if (value >= 1_000_000_000) {
    return (value / 1_000_000_000).toFixed(2) + 'B';
  } else if (value >= 1_000_000) {
    return (value / 1_000_000).toFixed(2) + 'M';
  } else if (value >= 1_000) {
    return (value / 1_000).toFixed(2) + 'K';
  } else if (value >= 1) {
    return value.toFixed(2);
  } else {
    return value.toExponential(2);
  }
}

export function getGHGComparisons(ghgKg: number): string[] {
  const comparisons: string[] = [];

  // Convert to metric tons
  const metricTons = ghgKg / 1000;

  // Cars (avg 4.6 MT CO2/year)
  const cars = Math.round(metricTons / 4.6);
  if (cars > 0) {
    comparisons.push(`Equivalent to ${cars.toLocaleString()} cars driven for one year`);
  }

  // Homes (avg 8 MT CO2/year)
  const homes = Math.round(metricTons / 8);
  if (homes > 0) {
    comparisons.push(`Equivalent to ${homes.toLocaleString()} homes' energy use for one year`);
  }

  // Flights NYC-LA (0.9 MT CO2/flight)
  const flights = Math.round(metricTons / 0.9);
  if (flights > 0) {
    comparisons.push(`Equivalent to ${flights.toLocaleString()} one-way flights from NYC to LA`);
  }

  return comparisons;
}
