import os
import requests

# API keys
API_KEY = os.getenv("APIVERVE_API_KEY")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

BASE_URL = "https://api.apiverve.com/v1/costliving"


def fetch_cost_of_living_raw(location: str):
    if not API_KEY:
        raise EnvironmentError("APIVERVE_API_KEY not set")

    headers = {
        "x-api-key": API_KEY
    }

    params = {
        "location": location
    }

    response = requests.get(BASE_URL, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def fetch_gas_price_raw(state_code):
    if not RAPIDAPI_KEY:
        raise EnvironmentError("RAPIDAPI_KEY not set")

    url = "https://gas-price.p.rapidapi.com/state"

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "gas-price.p.rapidapi.com"
    }

    params = {
        "code": state_code  # e.g. "CA"
    }

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()

    return response.json()


def fetch_all_raw(location, state_code):
    cost_data = fetch_cost_of_living_raw(location)
    gas_data = fetch_gas_price_raw(state_code)

    return {
        "cost_of_living": cost_data,
        "gas_price": gas_data
    }


# LOCAL TEST
if __name__ == "__main__":
    print("Testing combined raw pull...")

    raw = fetch_all_raw("California", "CA")

    print("Raw API response:")
    print(raw)
