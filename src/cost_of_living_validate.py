from datetime import datetime

# Definitions

REQUIRED_TOP_LEVEL_KEYS = {"status", "data"}

REQUIRED_DATA_FIELDS = {
    "searchedLocation",
    "costIndex",
    "cpi",
    "usAverageCPI",
    "period",
    "description"
}

# Helper Functions

def require_key(obj, key, context="object"):
    if key not in obj or obj[key] is None:
        raise ValueError(f"Missing required field '{key}' in {context}")


def validate_range(name, value, min_val=None, max_val=None):
    if value is None:
        raise ValueError(f"{name} is required")
    if not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    if min_val is not None and value < min_val:
        raise ValueError(f"{name} below minimum ({value})")
    if max_val is not None and value > max_val:
        raise ValueError(f"{name} above maximum ({value})")

# Main Function

def validate_cost_of_living(raw):
    # Validate top-level structure
    if not isinstance(raw, dict):
        raise ValueError("Payload must be a dictionary")

    for key in REQUIRED_TOP_LEVEL_KEYS:
        require_key(raw, key, "top-level payload")

    if raw.get("status") != "ok":
        raise ValueError(f"API returned non-ok status: {raw.get('status')}")

    data = raw["data"]

    if not isinstance(data, dict):
        raise ValueError("Field 'data' must be a dictionary")

    # Validate required data fields
    for field in REQUIRED_DATA_FIELDS:
        require_key(data, field, "data")


    validate_range("costIndex", data["costIndex"], 0, 300)
    validate_range("cpi", data["cpi"], 0, 1000)
    validate_range("usAverageCPI", data["usAverageCPI"], 0, 1000)

    if not isinstance(data["searchedLocation"], str):
        raise ValueError("searchedLocation must be a string")

    if not isinstance(data["description"], str):
        raise ValueError("description must be a string")

    # Validate period format (YYYY-MM)
    try:
        datetime.strptime(data["period"], "%Y-%m")
    except Exception:
        raise ValueError(f"Invalid period format: {data['period']} (expected YYYY-MM)")

    # Cleaned Output

    cleaned = {
        "location": data["searchedLocation"],
        "cost_index": data["costIndex"],
        "description": data["description"],
        "cpi": data["cpi"],
        "us_avg_cpi": data["usAverageCPI"],
        "period": data["period"],

        # optional fields (may be locked by API)
        "region": data.get("region"),
        "region_name": data.get("regionName"),
    }

    return cleaned

# Local Test

if __name__ == "__main__":
    print("Running cost of living validation...")

    from cost_of_living_raw import fetch_cost_of_living_raw

    raw = fetch_cost_of_living_raw("California")
    print("Raw data pulled")

    validated = validate_cost_of_living(raw)
    print("Validated output:")
    print(validated)
