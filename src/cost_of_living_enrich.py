from statistics import mean

# Helper Function

def classify_cost(cost_index):
    if cost_index < 95:
        return "low"
    elif cost_index <= 105:
        return "average"
    else:
        return "high"


# Main Enrichment Function

def enrich_cost_of_living(validated_records):
    """
    Takes a list of validated cost-of-living records
    Returns enriched insights and optional comparisons
    """

    if not validated_records:
        return None

    enriched_records = []

    # Per-location
  
    for record in validated_records:
        enriched = record.copy()

        cost_index = record["cost_index"]
        cpi = record["cpi"]
        us_avg = record["us_avg_cpi"]

        # Relative to US average
        percent_above_us = ((cpi - us_avg) / us_avg) * 100

        enriched["percent_above_us_avg"] = round(percent_above_us, 2)
        enriched["cost_category"] = classify_cost(cost_index)

        enriched_records.append(enriched)

    # Multi-location comparison

    if len(enriched_records) > 1:
        most_expensive = max(enriched_records, key=lambda x: x["cost_index"])
        least_expensive = min(enriched_records, key=lambda x: x["cost_index"])

        avg_cost = mean(r["cost_index"] for r in enriched_records)

        comparison = {
            "most_expensive": most_expensive["location"],
            "least_expensive": least_expensive["location"],
            "cost_difference": most_expensive["cost_index"] - least_expensive["cost_index"],
            "average_cost_index": round(avg_cost, 2)
        }

        return {
            "locations": enriched_records,
            "comparison": comparison
        }

    # If only one location
    return enriched_records[0]


# Local Test

if __name__ == "__main__":
    from cost_of_living_validate import validate_cost_of_living
    from cost_of_living_raw import fetch_cost_of_living_raw

    print("Running enrichment test...")

    locations = ["California", "Texas", "Ohio"]

    validated_records = []

    for loc in locations:
        raw = fetch_cost_of_living_raw(loc)
        validated = validate_cost_of_living(raw)
        validated_records.append(validated)

    enriched = enrich_cost_of_living(validated_records)

    print("Enriched output:")
    print(enriched)
