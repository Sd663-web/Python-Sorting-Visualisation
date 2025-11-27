
import tkinter as tk
from tkinter import ttk
import random
import time
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Utility Functions


def draw_bars(data, color_array, ax, canvas):
    ax.clear()
    ax.bar(range(len(data)), data, color=color_array)
    ax.set_title("Sorting Visualization")
    canvas.draw()


# Sorting Algorithms (Generators for animation)


def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
            yield data, ["red" if x == j or x == j + 1 else "blue" for x in range(len(data))]

def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            yield data, ["red" if x == j or x == j + 1 else "blue" for x in range(len(data))]
        data[j + 1] = key
        yield data, ["green" if x == i else "blue" for x in range(len(data))]

def merge_sort(data, left=0, right=None):
    if right is None:
        right = len(data) - 1
    if left >= right:
        return

    mid = (left + right) // 2
    yield from merge_sort(data, left, mid)
    yield from merge_sort(data, mid + 1, right)
    yield from merge(data, left, mid, right)

def merge(data, left, mid, right):
    merged = []
    left_idx = left
    right_idx = mid + 1

    while left_idx <= mid and right_idx <= right:
        if data[left_idx] < data[right_idx]:
            merged.append(data[left_idx])
            left_idx += 1
        else:
            merged.append(data[right_idx])
            right_idx += 1

        temp = data[:]
        temp[left:right+1] = merged + data[left_idx:mid+1] + data[right_idx:right+1]
        yield temp, ["red" if left <= x <= right else "blue" for x in range(len(data))]

    merged += data[left_idx:mid+1]
    merged += data[right_idx:right+1]
    data[left:right+1] = merged
    yield data, ["green" if left <= x <= right else "blue" for x in range(len(data))]

def quick_sort(data, low=0, high=None):
    if high is None:
        high = len(data) - 1
    if low < high:
        p, states = yield from partition(data, low, high)
        yield from quick_sort(data, low, p - 1)
        yield from quick_sort(data, p + 1, high)

def partition(data, low, high):
    pivot = data[high]
    i = low - 1

    for j in range(low, high):
        if data[j] < pivot:
            i += 1
            data[i], data[j] = data[j], data[i]

        yield data, ["red" if x == j or x == i else "blue" for x in range(len(data))]

    data[i + 1], data[high] = data[high], data[i + 1]
    yield data, ["green" if x == i + 1 else "blue" for x in range(len(data))]
    return i + 1, data


# Tkinter GUI Framework


class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        root.title("Sorting Algorithm Visualizer")

        # Sorting Data
        self.data = []
        self.speed = tk.DoubleVar(value=0.1)

        # UI Layout
        self.setup_ui()

        # Matplotlib Figure
        self.figure, self.ax = plt.subplots(figsize=(7, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Algorithm: ").grid(row=0, column=0)

        self.algorithm_menu = ttk.Combobox(control_frame, values=[
            "Bubble Sort", "Insertion Sort", "Merge Sort", "Quick Sort"
        ])
        self.algorithm_menu.grid(row=0, column=1)
        self.algorithm_menu.current(0)

        ttk.Label(control_frame, text="Speed: ").grid(row=0, column=2)
        ttk.Scale(control_frame, from_=0.001, to=0.5, orient='horizontal',
                  variable=self.speed).grid(row=0, column=3)

        ttk.Button(control_frame, text="Generate Data",
                   command=self.generate_data).grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(control_frame, text="Start Sorting",
                   command=self.start_sorting).grid(row=1, column=2, columnspan=2, pady=10)

        # Time display
        self.time_label = ttk.Label(self.root, text="Execution Time: 0.0 sec", font=("Arial", 12))
        self.time_label.pack()

    def generate_data(self):
        self.data = [random.randint(5, 100) for _ in range(60)]
        draw_bars(self.data, ["blue"] * len(self.data), self.ax, self.canvas)

    def start_sorting(self):
        if not self.data:
            return

        algo = self.algorithm_menu.get()

        algorithms = {
            "Bubble Sort": bubble_sort,
            "Insertion Sort": insertion_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort
        }

        sort_generator = algorithms[algo](self.data.copy())

        def run_sort():
            start_time = time.time()

            for data, color in sort_generator:
                draw_bars(data, color, self.ax, self.canvas)
                time.sleep(self.speed.get())

            end_time = time.time()
            self.time_label.config(text=f"Execution Time: {round(end_time - start_time, 3)} sec")

        threading.Thread(target=run_sort).start()


# Run Application


root = tk.Tk()
SortingVisualizer(root)
root.mainloop()
