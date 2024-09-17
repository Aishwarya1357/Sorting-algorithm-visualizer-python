from tkinter import *
from tkinter import ttk, messagebox
import random
import time

# Initialize the window
root = Tk()
root.title('Sorting Algorithm Visualization')
root.geometry("900x600")
root.config(bg='#F0F0F0')  # Light background

# Global variables
selected_alg = StringVar()
data = []
error_label = None  # Initialize error label to None

# Function for bubble sort
def bubble_sort(data, drawData, timeTick):
    for _ in range(len(data)-1):
        for j in range(len(data)-1):
            if data[j] > data[j+1]:
                data[j], data[j+1] = data[j+1], data[j]
                drawData(data, ['#00BFFF' if x == j or x == j+1 else '#FF4500' for x in range(len(data))])
                root.update()
                time.sleep(timeTick)
    drawData(data, ['#228B22' for x in range(len(data))])  # green when sorted

# Function for merge sort
def merge_sort(data, drawData, timeTick):
    merge_sort_alg(data, 0, len(data) - 1, drawData, timeTick)

def merge_sort_alg(data, left, right, drawData, timeTick):
    if left < right:
        middle = (left + right) // 2
        merge_sort_alg(data, left, middle, drawData, timeTick)
        merge_sort_alg(data, middle + 1, right, drawData, timeTick)
        merge(data, left, middle, right, drawData, timeTick)

def merge(data, left, middle, right, drawData, timeTick):
    left_part = data[left:middle + 1]
    right_part = data[middle + 1:right + 1]

    left_idx = right_idx = 0
    for i in range(left, right + 1):
        if left_idx < len(left_part) and (right_idx >= len(right_part) or left_part[left_idx] <= right_part[right_idx]):
            data[i] = left_part[left_idx]
            left_idx += 1
        else:
            data[i] = right_part[right_idx]
            right_idx += 1

        drawData(data, ['#00BFFF' if x >= left and x <= right else '#FF4500' for x in range(len(data))])
        root.update()
        time.sleep(timeTick)

# Function to draw data on the canvas
def drawData(data, colorArray):
    canvas.delete("all")
    c_height = 380
    c_width = 600
    x_width = c_width / (len(data) + 1)
    offset = 30
    spacing = 10
    normalizedData = [i / max(data) for i in data]

    for i, height in enumerate(normalizedData):
        x0 = i * x_width + offset + spacing
        y0 = c_height - height * 340
        x1 = (i + 1) * x_width + offset
        y1 = c_height
        canvas.create_rectangle(x0, y0, x1, y1, fill=colorArray[i], outline='')
        canvas.create_text(x0 + 2, y0, anchor=SW, text=str(data[i]), font=("Arial", 8))

# Function to generate random data without repetition
def Generate():
    global data
    minVal = int(minEntry.get())
    maxVal = int(maxEntry.get())
    size = int(sizeEntry.get())

    # Check if the range can accommodate the size of the data
    if maxVal - minVal + 1 < size:
        show_error("Error: The range is too small for the data size.")
        return

    # Hide error message if range is correct
    hide_error()

    # Generate unique random numbers using random.sample()
    data = random.sample(range(minVal, maxVal + 1), size)
    drawData(data, ['#FF4500' for x in range(len(data))])

# Function to show error on the GUI
def show_error(message):
    global error_label
    if error_label is None:
        error_label = Label(UI_frame, text=message, fg="red", bg='#F0F0F0', font=("Arial", 10, "bold"))
        error_label.grid(row=2, column=0, columnspan=4, padx=5, pady=5)
    else:
        error_label.config(text=message)

# Function to hide error message
def hide_error():
    global error_label
    if error_label is not None:
        error_label.config(text="")

# Function to start the sorting algorithm
def StartAlgorithm():
    global data
    if algMenu.get() == 'Bubble Sort':
        bubble_sort(data, drawData, speedScale.get())
    elif algMenu.get() == 'Merge Sort':
        merge_sort(data, drawData, speedScale.get())

# Function to update the window
def update_window():
    root.update_idletasks()
    root.after(10, update_window)

# Layout setup
UI_frame = Frame(root, width=600, height=200, bg='#F0F0F0')
UI_frame.grid(row=0, column=0, padx=10, pady=5)

canvas = Canvas(root, width=600, height=380, bg='white', bd=0, highlightthickness=0)
canvas.grid(row=1, column=0, padx=10, pady=5)

# User Interface (UI) setup with ttk widgets
Label(UI_frame, text="Algorithm: ", bg='#F0F0F0', font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
algMenu = ttk.Combobox(UI_frame, textvariable=selected_alg, values=['Bubble Sort', 'Merge Sort'], font=("Arial", 10))
algMenu.grid(row=0, column=1, padx=5, pady=5)
algMenu.current(0)

speedScale = Scale(UI_frame, from_=0.1, to=2.0, length=200, digits=2, resolution=0.2, orient=HORIZONTAL, label="Select Speed [s]", font=("Arial", 10), bg='#F0F0F0')
speedScale.grid(row=0, column=2, padx=5, pady=5)

ttk.Style().configure("TButton", font=("Arial", 10), padding=6)
Button(UI_frame, text="Start", command=StartAlgorithm, bg='#00BFFF', fg='white', font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=0, column=3, padx=5, pady=5)

# Row 1 (Data Entry)
sizeEntry = Scale(UI_frame, from_=3, to=25, resolution=1, orient=HORIZONTAL, label="Data Size", font=("Arial", 10), bg='#F0F0F0')
sizeEntry.grid(row=1, column=0, padx=5, pady=5)

minEntry = Scale(UI_frame, from_=0, to=10, resolution=1, orient=HORIZONTAL, label="Min Value", font=("Arial", 10), bg='#F0F0F0')
minEntry.grid(row=1, column=1, padx=5, pady=5)

maxEntry = Scale(UI_frame, from_=10, to=100, resolution=1, orient=HORIZONTAL, label="Max Value", font=("Arial", 10), bg='#F0F0F0')
maxEntry.grid(row=1, column=2, padx=5, pady=5)

Button(UI_frame, text="Generate", command=Generate, bg='#00BFFF', fg='white', font=("Arial", 10, "bold"), padx=10, pady=5).grid(row=1, column=3, padx=5, pady=5)

# Start the update loop
update_window()

# Start the Tkinter main loop
root.mainloop()


