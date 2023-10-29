import tkinter as tk
from tkinter import PhotoImage

# Initialize the main window
root = tk.Tk()
root.title("Notifications Display")
root.state('zoomed')  # Maximize the window

# Load the image
img_path = "C:\\Users\\stefa\\OneDrive\\Desktop\\site axes\\Icons\\Screenshot 2023-10-29 083355.png"
image = PhotoImage(file=img_path)
img_label = tk.Label(root, image=image)
img_label.pack(expand=True)

root.mainloop()
