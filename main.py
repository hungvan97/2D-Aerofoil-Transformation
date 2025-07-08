import pandas as pd
from plot import Plotting
from tkinter import filedialog
import tkinter as tk
import os

if __name__ == '__main__': 
    # Create root window as parent and hide it
    root = tk.Tk()
    root.withdraw()

    # Open file dialog as child of the root window
    file_path = filedialog.askopenfilename(
        title='Select Airfoil Coordinates File',
        filetypes=[('Text Files', '*.txt'), 
                   ('CSV Files', '*.csv'),
                   ('All Files', '*.*')],
        initialdir=os.getcwd()  # Start in the current working directory
    )

    if file_path:
        # Read the selected file into a DataFrame
        df = pd.read_csv(filepath_or_buffer=file_path, sep=r'[ ;]+', header=0, engine='python')
        df.columns = ['X', 'Y']
        task_list = [
            'Task 1: Twist by Leading Edge', 
            'Task 2: Scale', 
            'Task 3: Twist by Centroid', 
            'Task 4: Translate'
        ]
        plot_airfoil = Plotting(df=df, task_list=task_list)
    else:
        print("No file selected. Exiting the program.")