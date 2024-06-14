import requests
from geopy.geocoders import Nominatim
import pandas as pd

# Initialize geolocator
geolocator = Nominatim(user_agent="kerala_hospitals_locator")

# Function to get OSM data for hospitals in the specified location
def get_osm_data_for_hospitals(location):
    query = (
        f'[out:json];'
        f'node["amenity"="hospital"]({location["south"]},{location["west"]},{location["north"]},{location["east"]});'
        'out body;'
    )
    url = f"https://overpass-api.de/api/interpreter?data={query}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['elements']

# Function to get detailed information of hospitals
def get_hospital_details(location):
    details = []
    osm_data = get_osm_data_for_hospitals(location)
    
    for element in osm_data:
        try:
            name = element['tags'].get('name', 'N/A')
            lat = element['lat']
            lon = element['lon']
            address = geolocator.reverse((lat, lon), exactly_one=True).address
            
            details.append({
                'Name': name,
                'Latitude': lat,
                'Longitude': lon,
                'Address': address
            })
        except Exception as e:
            print(f"Error fetching data for element {element['id']}: {e}")
    
    return details

# Define the location boundaries (latitude and longitude of Ernakulam district)
location = {
    'south': 9.85,  # Southern latitude
    'north': 10.2,  # Northern latitude
    'west': 76.2,   # Western longitude
    'east': 76.8    # Eastern longitude
}

# Collect detailed information for hospitals
print(f"Fetching details for hospitals in Ernakulam district...")
hospital_details = get_hospital_details(location)

# Convert the details to a DataFrame and save to an Excel file
df = pd.DataFrame(hospital_details)
df.to_excel("cif_hospitals.xlsx", index=False)

print(f"Total hospitals found: {len(df)}")
print("Hospital details saved to cif_hospitals.xlsx")
