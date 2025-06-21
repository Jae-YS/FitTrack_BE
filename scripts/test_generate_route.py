import requests

# Set your local API URL
API_URL = "http://localhost:8000/api/routes/generate-route"

payload = {
    "user_id": 23,
    "start_lat": 40.7128,  # Example: New York City latitude
    "start_lng": -74.0060,  # Example: New York City longitude
}


def test_generate_route():
    try:
        print(f"Sending POST to {API_URL} with:")
        print(payload)
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            print("✅ Route generated successfully:")
            print("User ID:", data["user_id"])
            print("Distance (km):", data["distance_km"])
            print("Routes:", data["routes"])
        else:
            print(f"Failed with status {response.status_code}")
            print("Response:", response.text)

    except Exception as e:
        print("Exception during test:", e)


if __name__ == "__main__":
    test_generate_route()
