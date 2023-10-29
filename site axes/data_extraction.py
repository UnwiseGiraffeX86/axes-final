import requests

API_KEY = "1f9efcb0ec1a3aa943411f550790af73"

def get_weather_icon(cloud_coverage):
    base_path = "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\Weather Icons\\"
    if cloud_coverage < 20:
        return base_path + "sunny.png"
    elif 20 <= cloud_coverage < 50:
        return base_path + "partly_cloudy.png"
    elif 50 <= cloud_coverage < 80:
        return base_path + "mostly_cloudy.png"
    else:
        return base_path + "cloudy.png"

def get_location():
    try:
        response = requests.get("http://www.geoplugin.net/json.gp")
        data = response.json()

        city = data.get("geoplugin_city", "Unknown city")
        region = data.get("geoplugin_regionName", "Unknown region")
        country = data.get("geoplugin_countryName", "Unknown country")
        latitude = data.get("geoplugin_latitude", "Unknown latitude")
        longitude = data.get("geoplugin_longitude", "Unknown longitude")

        return {
            "city": city,
            "region": region,
            "country": country,
            "latitude": latitude,
            "longitude": longitude
        }
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

location_info = get_location()
print(location_info)

def get_weather_forecast(latitude, longitude):
    endpoint = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,precipitation_probability,surface_pressure,cloudcover,uv_index&daily=temperature_2m_max,temperature_2m_min&timezone=Europe%2FMoscow&forecast_days=1"
    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    try:
        response = requests.get(endpoint, headers=headers)
        data = response.json()

        # Get cloud coverage percentage from the forecast data
        cloud_coverage = data["hourly"]["cloudcover"][0]
        weather_icon = get_weather_icon(cloud_coverage)
        print(f"The chosen weather icon based on cloud coverage is: {weather_icon}")

        return data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

forecast_data = get_weather_forecast(location_info["latitude"], location_info["longitude"])
print(forecast_data)


def extract_data_from_files():
    # Paths to the data files
    data_files = {
        "BMP": r"C:\Users\stefa\OneDrive\Desktop\site axes\DataFiles\BMP.TXT",
        "DHT": r"C:\Users\stefa\OneDrive\Desktop\site axes\DataFiles\DHT.TXT",
        "MPU": r"C:\Users\stefa\OneDrive\Desktop\site axes\DataFiles\MPU.TXT",
        "MQ131": r"C:\Users\stefa\OneDrive\Desktop\site axes\DataFiles\MQ131.TXT",
        "MQ135": r"C:\Users\stefa\OneDrive\Desktop\site axes\DataFiles\MQ135.TXT"
    }

    # Placeholder for extracted data
    extracted_data = {}

    # Extracting data from BMP file (temperature, pressure)
    with open(data_files["BMP"], 'r') as file:
        lines = file.readlines()
        temperatures, pressures = zip(*[map(float, line.split()) for line in lines])
        extracted_data["temperature"] = temperatures
        extracted_data["pressure"] = pressures

    # Extracting data from DHT file (humidity)
    with open(data_files["DHT"], 'r') as file:
        extracted_data["humidity"] = [float(line.strip()) for line in file.readlines()]

    # Extracting data from MPU file (acceleration, gyro, compass)
    with open(data_files["MPU"], 'r') as file:
        lines = file.readlines()
        values = [list(map(float, line.split())) for line in lines]
        extracted_data["acceleration"] = [val[:3] for val in values]
        extracted_data["gyro"] = [val[3:6] for val in values]
        extracted_data["compass"] = [val[6:] for val in values]

    # Extracting data from MQ131 file (ozone concentration)
    with open(data_files["MQ131"], 'r') as file:
        extracted_data["ozone_concentration"] = [float(line.strip()) for line in file.readlines()]

    # Extracting data from MQ135 file (air quality)
    with open(data_files["MQ135"], 'r') as file:
        extracted_data["air_quality"] = [float(line.strip()) for line in file.readlines()]

    return extracted_data

def compute_aqi(air_quality_data):
    positive_values = [value for value in air_quality_data if value > 0]
    average_aqi_raw = sum(positive_values) / len(positive_values)
    return int(average_aqi_raw / 6)

def get_aqi_color(aqi):
    # Define color for each segment
    dark_green = [0, 128, 0]
    light_green = [127, 255, 0]
    yellow = [255, 255, 0]
    orange = [255, 165, 0]
    red = [255, 0, 0]
    dark_red = [139, 0, 0]
    very_dark_red = [64, 0, 0]

    # Linear interpolation function
    def interpolate(color1, color2, t):
        return [int(color1[i] + (color2[i] - color1[i]) * t) for i in range(3)]

    if 10 <= aqi <= 50:
        t = (aqi - 10) / 40
        color = interpolate(dark_green, light_green, t)
    elif 51 <= aqi <= 100:
        t = (aqi - 51) / 49
        color = interpolate(light_green, yellow, t)
    elif 101 <= aqi <= 150:
        t = (aqi - 101) / 49
        color = interpolate(yellow, orange, t)
    elif 151 <= aqi <= 200:
        t = (aqi - 151) / 49
        color = interpolate(orange, red, t)
    elif 201 <= aqi <= 300:
        t = (aqi - 201) / 99
        color = interpolate(red, dark_red, t)
    elif 301 <= aqi <= 500:
        t = (aqi - 301) / 199
        color = interpolate(dark_red, very_dark_red, t)
    else:
        color = very_dark_red

    return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"

