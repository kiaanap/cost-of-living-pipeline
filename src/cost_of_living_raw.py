import os
import requests

API_KEY = os.getenv("APIVERVE_API_KEY")

if not API_KEY:
    raise EnvironmentError("APIVERVE_API_KEY not set")

BASE_URL = "https://api.apiverve.com/v1/costliving"


def fetch_cost_of_living_raw(location: str):
    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "location": location  # <-- correct param
    }

    response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    return response.json()

# LOCAL TEST

if __name__ == "__main__":
    print("Testing cost of living raw pull...")

    data = fetch_cost_of_living_raw("California") 

    print("Raw API response:")
    print(data)


    data = fetch_cost_of_living_raw(test_location)

    print("Raw API response:")
    print(data)
