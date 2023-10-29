import tkinter as tk
from tkinter import ttk, PhotoImage
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import datetime

# Button icons
icons = {
    "Home": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\home.png",
    "Metrics": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\metrics.png",
    "Advanced View": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\advanced view.png",
    "Settings": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\settings.png",
    "Account": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\account.png",
    "Logout": "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\logout.png"
}
def add_text_and_number(master, text):
    """Add a small text box and a number above it to a given master widget."""
    frame = tk.Frame(master, bg='#FFFFFF')
    frame.pack(side=tk.LEFT, padx=5)
    
    # Set borderwidth and highlightthickness to 0 to remove border
    textbox = tk.Text(frame, height=3, width=10, borderwidth=0, highlightthickness=0)
    textbox.insert(tk.END, text)
    textbox.pack()
    
    return frame

current_month_idx = datetime.datetime.now().month - 1

def get_bar_colors(data_length, current_idx, vibrant_color, desaturated_color):
    return [vibrant_color if i == current_idx else desaturated_color for i in range(data_length)]


# Initialize the main window
root = tk.Tk()
root.title("Graphs Page")
root.state('zoomed')  # Maximize the window

root.grid_rowconfigure(0, weight=1)  # This ensures that the row containing the metrics expands as needed
root.grid_columnconfigure(1, weight=1) 

# Sidebar on the left
sidebar = ttk.Frame(root, width=150, relief="flat")
sidebar.grid(row=0, column=0, rowspan=6, sticky="nsew")

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
    


# Advanced Metrics Content Area
adv_metrics_frame = tk.Frame(root, bg='#FFFFFF')
adv_metrics_frame.grid(row=0, column=1, sticky='nsew', rowspan=4, columnspan=2)

# Header Frame for labels
header_frame = tk.Frame(adv_metrics_frame, bg='#FFFFFF')
header_frame.grid(row=0, column=0, columnspan=2, sticky='nsew')

effect_label = tk.Label(header_frame, text="Air Pollution Effect Report", font=('Arial', 16, 'bold'), bg='#FFFFFF')
effect_label.pack(side=tk.LEFT, padx=5, pady=5)

cause_label = tk.Label(header_frame, text="Air Pollution Cause Report", font=('Arial', 16, 'bold'), bg='#FFFFFF')
cause_label.pack(side=tk.RIGHT, padx=5, pady=5)

# Adjusted the row weight for the header
adv_metrics_frame.grid_rowconfigure(0, weight=0) 
for i in range(1, 4):
    adv_metrics_frame.grid_rowconfigure(i, weight=1)
for i in range(2):  
    adv_metrics_frame.grid_columnconfigure(i, weight=1)

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
pressure_data = [1012, 1015, 1014, 1010, 1011, 1013, 1016, 1015, 1013, 1014, 1012, 1014]
temperature_data = [10, 12, 15, 18, 20, 39, 34, 22, 20, 17, 14, 4]
x = np.linspace(0, 2 * np.pi, 12)
rainfall_data = -40 * np.sin(x) + 50 
aqi_data = [50, 60, 70, 65, 75, 90, 85, 70, 68, 72, 80, 78]
uvi_data = [2, 3, 5, 7, 8, 10, 9, 9, 7, 5, 3, 2]
o3i_data = [30, 32, 35, 37, 40, 42, 45, 44, 40, 38, 36, 35]

# Create a 2x3 grid layout for the metrics
for row in range(1, 4):
    for col in range(2):
        metric_frame = tk.Frame(adv_metrics_frame, bg='#FFFFFF', width=260, height=125) 
        metric_frame.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        #Pressure Graph
        if row == 1 and col == 0:
            add_text_and_number(metric_frame, "1014 hPa")
            fig, ax = plt.subplots()  # Make sure you have this line to define 'ax'

            y_min = min(pressure_data) - 1  # Slightly below the minimum value in the data
            y_max = max(pressure_data) + 1  # Slightly above the maximum value in the data

            ax.set_ylim(y_min, y_max)  
            
            
            fig, ax = plt.subplots(figsize=(5, 2.5))
            ax.plot(months, pressure_data, color='dodgerblue', marker='o')
            ax.fill_between(months, pressure_data, color='dodgerblue', alpha=0.1)
            ax.set_title("Average Pressure This Year")
            ax.set_ylabel("Pressure (hPa)")
            ax.grid(True, which="both", ls="--", c='gray', alpha=0.2)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            canvas = FigureCanvasTkAgg(fig, master=metric_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        

        #Temp Graph
        if row == 2 and col == 0:  # Adjust this to place the graph in metric 3
            add_text_and_number(metric_frame, "22.2°C")
            fig, ax = plt.subplots(figsize=(5, 3))  # Adjust size as needed

            # Plotting the data
            ax.plot(months, temperature_data, marker='', linestyle='--', color='blue')

            # Styling
            ax.set_title('Average Temperature Over the Year')
            ax.set_xlabel('Month')
            ax.set_ylabel('Temperature (°C)')
            ax.grid(True, which="both", ls="--", c='gray', alpha=0.2)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.set_facecolor('#E6E6E6')  # Light gray background

            # Set y-axis limits to emphasize differences in data
            y_min_temp = min(temperature_data) - 2
            y_max_temp = max(temperature_data) + 2
            ax.set_ylim(y_min_temp, y_max_temp)

            # Embed the plot in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=metric_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
        #Precipitation Graph
        if row == 3 and col == 0:  # Adjust this to place the graph in the desired metric slot
            add_text_and_number(metric_frame, "33%")
            fig, ax = plt.subplots(figsize=(5, 3))  # Adjust size as needed

            # Plotting the data
            ax.plot(months, rainfall_data, color='blue', alpha=0.7)

            # Styling
            ax.set_title('Average Monthly Rainfall')
            ax.set_xlabel('Month')
            ax.set_ylabel('Rainfall (%)')
            ax.grid(True, which='both', linestyle='--', linewidth=0.5, axis='y')
            ax.axhline(0, color='black', linewidth=0.5)
            ax.set_facecolor('#E6E6E6')  # Light gray background
            ax.set_ylim(0, 100)  # Limiting the y-axis from 0 to 100%

            # Embed the plot in the Tkinter window
            canvas = FigureCanvasTkAgg(fig, master=metric_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)
        # AQI Bar Graph
        if row == 1 and col == 1:
            add_text_and_number(metric_frame, "AQI 67")
            vibrant_color = 'blue'
            desaturated_color = 'lightblue'
            colors = get_bar_colors(len(aqi_data), current_month_idx, vibrant_color, desaturated_color)
    
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(months, aqi_data, color=colors, label='AQI')
            ax.set_title('Average Monthly AQI')
            canvas = FigureCanvasTkAgg(fig, master=metric_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # UVI Bar Graph
        elif row == 2 and col == 1:
            add_text_and_number(metric_frame, "UVI 3")
            vibrant_color = 'green'
            desaturated_color = 'lightgreen'
            colors = get_bar_colors(len(uvi_data), current_month_idx, vibrant_color, desaturated_color)
    
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(months, uvi_data, color=colors, label='UVI')
            ax.set_title('Average Monthly UVI')
            canvas = FigureCanvasTkAgg(fig, master=metric_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


        # O3I Bar Graph
        elif row == 3 and col == 1:
            add_text_and_number(metric_frame, "2.5 ppm")
            vibrant_color = 'red'
            desaturated_color = 'lightsalmon'
            colors = get_bar_colors(len(o3i_data), current_month_idx, vibrant_color, desaturated_color)
    
            fig, ax = plt.subplots(figsize=(5, 3))
            ax.bar(months, o3i_data, color=colors, label='O3I')
            ax.set_title('Average Monthly O3I')
            canvas = FigureCanvasTkAgg(fig, master=metric_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
root.mainloop()
