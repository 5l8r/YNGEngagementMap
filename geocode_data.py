import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderServiceError
import ssl

class GeocodeData:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.geolocator = Nominatim(user_agent="yng_mapper", timeout=10, ssl_context=self.get_ssl_context())
        self.df = None

    def get_ssl_context(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def load_data(self):
        self.df = pd.read_csv(self.input_file, dtype={'Zip Code': str})  # Ensure zip codes are read as strings
        print("Data loaded successfully")

    def get_lat_long(self, zip_code):
        if not zip_code:
            return None, None
        try:
            location = self.geolocator.geocode({"postalcode": zip_code, "country": "USA"})
            if location:
                print(f"Geocoded {zip_code}: ({location.latitude}, {location.longitude})")
                return location.latitude, location.longitude
        except GeocoderServiceError as e:
            print(f"Geocoding error for zip code {zip_code}: {e}")
        return None, None

    def geocode_data(self):
        self.df['Latitude'], self.df['Longitude'] = zip(*self.df['Zip Code'].apply(self.get_lat_long))
        self.df.to_csv(self.output_file, index=False)
        print(f"Geocoded data saved to '{self.output_file}'")

# Run this part once to geocode and save the data
if __name__ == "__main__":
    input_file = 'data/yng_fake_members.csv'
    output_file = 'data/geocoded_yng_members.csv'
    geocode_data = GeocodeData(input_file, output_file)
    geocode_data.load_data()
    geocode_data.geocode_data()
