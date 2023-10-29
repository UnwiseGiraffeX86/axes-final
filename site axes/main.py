import tkinter as tk
from tkinter import ttk, PhotoImage
from data_extraction import extract_data_from_files, get_location, get_weather_forecast, compute_aqi, get_aqi_color, get_weather_icon
from tkinter import Canvas


# Initialize the main window
root = tk.Tk()
root.title("Weather App")
root.state('zoomed')  # Maximize the window

# Function to create a frame with a gray border
def bordered_frame(parent, **kwargs):
    return ttk.Frame(parent, borderwidth=2, relief="solid", **kwargs)

def create_rounded_rectangle(canvas, x1, y1, x2, y2, r, **kwargs):
    """Draws a rounded rectangle on a given canvas."""
    points = [x1+r, y1,
              x2-r, y1,
              x2, y1, x2, y1+r,
              x2, y2-r, x2, y2,
              x2-r, y2, x1+r, y2,
              x1, y2, x1, y2-r,
              x1, y1+r, x1, y1]
    
    return canvas.create_polygon(points, **kwargs)


# Sidebar on the left
sidebar = ttk.Frame(root, width=150, relief="flat")
sidebar.grid(row=0, column=0, rowspan=6, sticky="nsew")

# Button icons
icons = {
    "Home": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\home.png",
    "Metrics": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\metrics.png",
    "Advanced View": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\advanced view.png",
    "Settings": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\settings.png",
    "Account": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\account.png",
    "Logout": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\logout.png"
}

# Sidebar buttons
buttons = ["Home", "Metrics", "Advanced View", "Settings"]
for idx, btn_text in enumerate(buttons):
    btn_icon = PhotoImage(file=icons[btn_text])
    btn = tk.Button(sidebar, image=btn_icon, compound="left", width=40, height=40, relief=tk.FLAT)
    btn.icon = btn_icon
    btn.pack(pady=25, padx=10)

# Account and Logout buttons at the bottom of the sidebar
bottom_buttons = ["Account", "Logout"]
for btn_text in bottom_buttons:
    btn_icon = PhotoImage(file=icons[btn_text])
    btn = tk.Button(sidebar, image=btn_icon, compound="left", width=40, height=40, relief=tk.FLAT)
    btn.icon = btn_icon
    btn.pack(side=tk.BOTTOM, pady=25, padx=10)

    
# Three columns for city illustrations
cities = ["C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\ilustrations\\illustration@2x.png", 
          "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\ilustrations\\illustration1@2x.png", 
          "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\ilustrations\\illustration2@2x.png"]
# Get the width of the first illustration after resizing
first_img = PhotoImage(file=cities[0])
first_img_width = first_img.width() * 0.6

# Three columns for city illustrations
for col, city in enumerate(cities, 1):
    img = PhotoImage(file=city)
    img = img.zoom(6)  # Zoom by 600%
    img = img.subsample(10)  # Subsample by 10% (or 0.1x) the zoomed size
    lbl = ttk.Label(root, image=img)
    lbl.image = img
    lbl.grid(row=0, column=col, pady=5)

    # Set the column width to the width of the illustration
    root.grid_columnconfigure(col, minsize=first_img_width)

# Daily Forecast section
forecast_frame = ttk.Frame(root, relief="flat", padding="5")
forecast_frame.grid(row=0, column=4, padx=10, sticky="nsew")

# Fetching data from data_extraction.py
location_info = get_location()
forecast_data = get_weather_forecast(location_info["latitude"], location_info["longitude"])

# Extracting the required forecast data
temperature = forecast_data["hourly"]["temperature_2m"][0]
humidity = forecast_data["hourly"]["relativehumidity_2m"][0]
pressure = forecast_data["hourly"]["surface_pressure"][0]
cloud_coverage = forecast_data["hourly"]["cloudcover"][0]
uv_index = forecast_data["hourly"]["uv_index"][0]
precipitation_chance = forecast_data["hourly"]["precipitation_probability"][0]

# Compute AQI
air_quality_data = extract_data_from_files()["air_quality"]
aqi_value = compute_aqi(air_quality_data)

# Get the weather icon path based on cloud coverage
weather_icon_path = get_weather_icon(cloud_coverage)

# Load the weather icon and display it
weather_icon = PhotoImage(file=weather_icon_path)
weather_icon = weather_icon.subsample(4, 4)  # Resize the icon to 25% of its original size
weather_icon_label = ttk.Label(forecast_frame, image=weather_icon)
weather_icon_label.pack(pady=5)

# Display the temperature centered beneath the weather icon
temperature_label = ttk.Label(forecast_frame, text=f"{temperature}°C", font=("Arial", 16))
temperature_label.pack(pady=5)

# Display forecast data in rounded rectangles
forecast_canvas = tk.Canvas(forecast_frame, width=350, height=275, bg="white")
forecast_canvas.pack(pady=10)

# Create the rounded rectangles for forecast data
create_rounded_rectangle(forecast_canvas, 10, 10, 80, 60, 10, fill="lightgray")
create_rounded_rectangle(forecast_canvas, 90, 10, 160, 60, 10, fill="lightgray")
create_rounded_rectangle(forecast_canvas, 170, 10, 240, 60, 10, fill="lightgray")
create_rounded_rectangle(forecast_canvas, 50, 75, 120, 125, 10, fill=get_aqi_color(aqi_value))
create_rounded_rectangle(forecast_canvas, 130, 75, 200, 125, 10, fill="#ffcc00")  # Example color for UV index

# Display the forecast data inside the rectangles
forecast_canvas.create_text(45, 35, text=f"{pressure:.2f} hPa")
forecast_canvas.create_text(125, 35, text=f"{humidity:.2f}%")
forecast_canvas.create_text(205, 35, text=f"{precipitation_chance:.2f}%")
forecast_canvas.create_text(85, 100, text=f"AQI: {aqi_value}")
forecast_canvas.create_text(165, 100, text=f"UV: {uv_index}")

# Interesting Videos section

videos_frame = ttk.Frame(root, relief="flat", padding="5")
videos_frame.grid(row=1, column=1, columnspan=3, pady=20, padx=10, sticky="nsew")


videos = ["C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\ilustrations\\image@2x.png", 
          "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\ilustrations\\image1@2x.png", 
          "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\ilustrations\\image2@2x.png"]

# Calculate the desired width for each video (assuming they all have the same original width)
first_img = PhotoImage(file=videos[0])
desired_width = first_img.width() * 0.6  # 60% of the original width

for idx, video in enumerate(videos):
    img = PhotoImage(file=video)
    
    # Resize the image proportionally to the desired width
    scale_factor = desired_width / img.width()
    img = img.zoom(int(scale_factor * 10))  # Multiply by 10 for precision
    img = img.subsample(10)  # Then subsample by 10 to offset the zoom
    
    lbl = ttk.Label(videos_frame, image=img)
    lbl.image = img
    lbl.grid(row=0, column=idx, padx=5)
    
    # Set the column width to the desired width
    videos_frame.grid_columnconfigure(idx, minsize=desired_width)   

# Notification bar at the bottom
notification_frame = bordered_frame(root, padding="5")
notification_frame.grid(row=1, column=4, pady=20, padx=10, sticky="nsew")

notification_label = ttk.Label(notification_frame, text="NOTIFICATIONS") 
notification_label.pack(expand=True, fill="both", pady=5)

# Button size in pixels
btn_width = 40
btn_height = 2

# First button anchored to the left
btn1 = tk.Button(notification_frame, text="0 errors reported in the past week.", command=lambda: print("Clicked Notification 1"),bg="#C5C5C5", fg="#5B5B5B", relief=tk.FLAT, activebackground="#C5C5C5", activeforeground="#5B5B5B",highlightthickness=0)
btn1.pack(anchor="w", pady=5, padx=1)  # Anchor set to "w" (west) for left alignment
btn1.config(width=btn_width, height=btn_height)

btn2 = tk.Button(notification_frame, text="Time Sensitive! Please check if your BME280 module is working as expected", command=lambda: print("Clicked Notification 2"),bg="#FFC0C0", fg="#B00000", relief=tk.FLAT, activebackground="#FFC0C0", activeforeground="#B00000",highlightthickness=0)
btn2.pack(anchor="w",pady=5, padx=1)
btn2.config(width=btn_width+30, height=btn_height)

# Configure rows and columns to expand
for i in range(3):  # 3 rows
    root.grid_rowconfigure(i, weight=1)
for j in range(5):  # 5 columns (including sidebar)
    root.grid_columnconfigure(j, weight=1)

root.mainloop()
