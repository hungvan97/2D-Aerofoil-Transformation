import pandas as pd
from plot import Plotting

if __name__ == '__main__': 
    df = pd.read_csv(filepath_or_buffer='Aerofoil.csv', sep=';')
    task_list = ['Task 1: Twist by Leading Edge', 'Task 2: Scale', 'Task 3: Twist by Centroid']
    plot_airfoil = Plotting(df=df, task_list=task_list)