import exifread
import json
import numpy as np
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from keras.applications import MobileNet
from keras.applications.mobilenet import preprocess_input, decode_predictions
import matplotlib.pyplot as plt
import folium
import seaborn as sns

# Define the functions for extracting GPS info, geolocation, and map visualization
def extract_gps_info(image_path):
    img = Image.open(image_path)
    exif_data = img._getexif()
    
    if 34853 in exif_data:
        gps_info = exif_data[34853]
        return {
            'Latitude': gps_info[2],
            'Longitude': gps_info[4]
        }
    else:
        return None

def get_geolocation(latitude, longitude, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?key={api_key}&q={latitude}+{longitude}&pretty=1"
    response = requests.get(url)
    geolocation_data = json.loads(response.text)
    return geolocation_data

def display_location_on_map(latitude, longitude, geolocation_data):
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    popup_text = f"<b>Location:</b> {geolocation_data['results'][0]['formatted']}"
    folium.Marker([latitude, longitude], popup=popup_text).add_to(m)
    return m

def display_image_with_location(image_path, m):
    img = Image.open(image_path)
    plt.figure(figsize=(8, 8))
    plt.imshow(img)
    plt.title("Image with Location")
    plt.show()

if __name__ == '__main__':
    image_path = "your_image.jpg"
    api_key = "your_opencage_api_key"
    
    gps_info = extract_gps_info(image_path)
    
    if gps_info:
        latitude, longitude = gps_info['Latitude'], gps_info['Longitude']
        geolocation_data = get_geolocation(latitude, longitude, api_key)
        
        # Display location on map
        m = display_location_on_map(latitude, longitude, geolocation_data)
        
        # Display image with location
        display_image_with_location(image_path, m)
        
        # Print structured location details
        location_details = geolocation_data['results'][0]
        print("\nLocation Details:")
        print(f"Formatted Address: {location_details['formatted']}")
        print(f"Country: {location_details['components']['country']}")
        print(f"City: {location_details['components']['city']}")
    else:
        print("No GPS information found in the image.")
