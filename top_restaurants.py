import requests
import json
import os

# Get SerpAPI key from environment variable
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

def get_top_restaurants(city):
    query = f"restaurants in {city}"
    url = 'https://serpapi.com/search.json'

    params = {
        'engine': 'google_maps',
        'type': 'search',
        'q': query,
        'hl': 'en',
        'api_key': SERPAPI_API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"HTTP {response.status_code}: Failed to fetch data")

    data = response.json()

    if "error" in data:
        raise Exception(f"SerpAPI Error: {data['error']}")

    raw_results = data.get("local_results", [])
    if not raw_results:
        raise Exception("No local_results found. Check city name or API quota.")

    # Sort by rating and number of reviews
    sorted_results = sorted(
        raw_results,
        key=lambda r: (r.get("rating", 0), r.get("reviews", 0)),
        reverse=True
    )

    # Pick the top 10 sorted by rating + reviews
    restaurants = {}
    for place in sorted_results[:10]:
        name = place.get("title")
        rating = place.get("rating", "N/A")
        reviews = place.get("reviews", "N/A")
        address = place.get("address", "N/A")

        restaurants[name] = {
            "rating": rating,
            "reviews": reviews,
            "address": address
        }

    return restaurants

def main():
    city = input("Enter the name of a city: ").strip()
    print(f"\nFetching top restaurants in {city}...")

    try:
        top_restaurants = get_top_restaurants(city)
        if not top_restaurants:
            print("No restaurants found.")
            return

        # Save the results to JSON file
        with open("top_restaurants.json", "w") as f:
            json.dump(top_restaurants, f, indent=4)

        print(f"\nData saved successfully in 'top_restaurants.json'")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

