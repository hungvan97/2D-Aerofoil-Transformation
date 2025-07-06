import pandas as pd
from plot import Plotting

if __name__ == '__main__': 
    df = pd.read_csv(filepath_or_buffer='IEA-15-240-RWT_AF38_Coords.txt', sep=r'[ ;]+', header=0, engine='python')
    df.columns = ['X', 'Y']  # Rename columns for easy access later
    task_list = ['Task 1: Twist by Leading Edge', 'Task 2: Scale', 'Task 3: Twist by Centroid', 'Task 4: Translate']
    plot_airfoil = Plotting(df=df, task_list=task_list)