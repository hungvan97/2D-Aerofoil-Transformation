"""Contains functions for plotting the airfoil data."""
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider, TextBox
from airfoil import *
import asyncio
import pandas as pd
from tkinter import filedialog

class Plotting():
    def __init__(self, df, task_list) -> None:
        self.df = df
        self.task_list = task_list
        # Create the main figure
        fig = plt.figure(figsize=(12, 8))
        
        # Create main plot area with radio buttons
        self.ax = plt.axes(arg=[0.1, 0.1, 0.7, 0.8])  
        rax = plt.axes(arg=[0.85, 0.85, 0.15, 0.15], frameon=False)  
        radio = RadioButtons(ax=rax, labels=self.task_list)
        radio.on_clicked(func=self.update_plot)

        # Create sliders
        self.ax_angle = plt.axes([0.85, 0.2, 0.03, 0.6])
        self.angle_slider = Slider(ax=self.ax_angle, label='Angle Twist', valmin=-180, valmax=180, valinit=0, orientation='vertical')
        self.angle_slider.set_active(True)
        
        self.ax_scale = plt.axes([0.90, 0.2, 0.03, 0.6])
        self.scale_slider = Slider(ax=self.ax_scale, label='Scale Factor', valmin=0.1, valmax=2.0, valinit=0, orientation='vertical')
        self.scale_slider.set_active(False)

        # Update plot when sliders are changed
        self.angle_slider.on_changed(func=lambda _: self.update_plot(task=radio.value_selected))
        self.scale_slider.on_changed(func=lambda _: self.update_plot(task=radio.value_selected))

        # Add text boxes for X and Y coordinates
        self.ax_x = plt.axes([0.85, 0.1, 0.1, 0.03])
        self.ax_y = plt.axes([0.85, 0.05, 0.1, 0.03])
        self.x_textbox = TextBox(self.ax_x, 'X:', initial='0')
        self.y_textbox = TextBox(self.ax_y, 'Y:', initial='0')
        self.x_textbox.on_submit(lambda _: self.update_plot(task=radio.value_selected))
        self.y_textbox.on_submit(lambda _: self.update_plot(task=radio.value_selected))
        self.ax_x.set_visible(False)
        self.ax_y.set_visible(False)

        # Add button to store results
        self.save_button_ax = plt.axes([0.85, 0.01, 0.1, 0.03])
        self.save_button = plt.Button(self.save_button_ax, 'Save Results')
        self.save_button_ax.set_visible(False)
        self.save_button.on_clicked(self.save_results)
        self.save_results_concat = None  # Placeholder for concatenated results

        # Show initial plot (Task 1 by default)
        self.update_plot(task=self.task_list[0])
        plt.show()

    async def plot_twisted_airfoil(self, df, angle_degrees, ledge=True, centroid=False) -> None:
        """
        Plot the original and twisted airfoil
        
        Args:
            df: pandas DataFrame with X and Y coordinates
            angle_degrees: Angle of twist in degrees
            ledge: If True, twist about the leading edge. If False, twist about the centroid
            centroid: If True, twist about the centroid. If False, twist about the leading edge
        """
        plt.sca(self.ax)  # Set the main axes as current
        plt.cla()            # Clear the main axes only
        
        # Apply twist
        if ledge:
            result_df = await twist_airfoil_ledge(df=df, angle_degrees=angle_degrees)
        else:
            result_df = await twist_airfoil_centroid(df=df, angle_degrees=angle_degrees)
        
        # Plot original airfoil 
        plt.plot(result_df['X'], result_df['Y'], 'b-', linewidth=2, label='Original')
        
        # Plot twisted airfoil
        plt.plot(result_df['X_twisted'], result_df['Y_twisted'], 'r--', linewidth=2, 
                label=f'Twisted ({angle_degrees}°)')
        
        # Add reference point at the leading edge
        if ledge:
            plt.plot(0, 0, 'ko', markersize=6)
        else:
            plt.plot(result_df['X'].mean(), result_df['Y'].mean(), 'ko', markersize=6)
        
        # Setup plot
        plt.grid(visible=True, linestyle='--')
        plt.xlabel(xlabel='X', fontsize=12)
        plt.ylabel(ylabel='Y', fontsize=12)
        plt.title(label=f'Airfoil twisted by {angle_degrees}° about its leading edge', fontsize=14)
        plt.axis('equal')
        plt.legend()

    async def plot_scale_airfoil(self, df, scale_factor) -> None:
        """
        Plot the original and scaled airfoil.
        
        Args:
            df: pandas DataFrame with X and Y coordinates
            scale_factor: Factor to scale the airfoil by
        """
        plt.sca(self.ax)  # Set the main axes as current
        plt.cla()            # Clear the main axes only
        
        # Apply scale
        result_df = await scale_airfoil(df, scale_factor)
        
        # Plot original airfoil 
        plt.plot(result_df['X'], result_df['Y'], 'b-', linewidth=2, label='Original')
        
        # Plot scaled airfoil
        plt.plot(result_df['X_scaled'], result_df['Y_scaled'], 'r--', linewidth=2, 
                label=f'Scaled (Factor = {scale_factor})')
        
        # Setup plot
        plt.grid(visible=True, linestyle='--')
        plt.xlabel(xlabel='X', fontsize=12)
        plt.ylabel(ylabel='Y', fontsize=12)
        plt.title(label=f'Airfoil scaled by factor of {scale_factor}', fontsize=14)
        plt.axis('equal')
        plt.legend()

    async def plot_translated_airfoil(self, df, centroid_x, centroid_y):
        """
        Plot the original and translated airfoil.
        
        Args:
            df: pandas DataFrame with X and Y coordinates
            centroid_x: X coordinate of the translation
            centroid_y: Y coordinate of the translation
        """
        plt.sca(self.ax)  # Set the main axes as current
        plt.cla()            # Clear the main axes only

        # Apply translation
        result_df_translated = await translate_airfoil(df=df, x_center=centroid_x, y_center=centroid_y)
        result_df_twisted = await twist_airfoil_centroid(df=result_df_translated[['X_translated', 'Y_translated']], angle_degrees=self.angle_slider.val)
        result_df_scale = await scale_airfoil(df=result_df_twisted[['X_twisted', 'Y_twisted']], scale_factor=self.scale_slider.val)

        # Store results in the DataFrame
        self.save_results_concat = pd.concat(
            [result_df_translated, 
             result_df_twisted[['X_twisted', 'Y_twisted']], 
             result_df_scale[['X_scaled', 'Y_scaled']]
            ], axis=1)

        # Plot original and transformed airfoils
        plt.plot(result_df_translated['X'], result_df_translated['Y'], 'b-', linewidth=2, label='Original')
        plt.plot(result_df_translated['X_translated'], result_df_translated['Y_translated'], 'r--', linewidth=2, label=f'Translated by ({centroid_x}, {centroid_y})')
        plt.plot(result_df_twisted['X_twisted'], result_df_twisted['Y_twisted'], 'g-.', linewidth=2, label=f'Twisted by {self.angle_slider.val}°')
        plt.plot(result_df_scale['X_scaled'], result_df_scale['Y_scaled'], 'm:', linewidth=2, label=f'Scaled by {self.scale_slider.val}')

        # Setup plot
        plt.grid(visible=True, linestyle='--')
        plt.xlabel(xlabel='X', fontsize=12)
        plt.ylabel(ylabel='Y', fontsize=12)
        plt.title(label=f'Airfoil transformed', fontsize=14)
        plt.axis('equal')
        plt.legend()

    def update_plot(self, task) -> None:
        plt.sca(self.ax)
        plt.cla()
        if task == 'Task 1: Twist by Leading Edge':
            self.ax_angle.set_visible(True)
            self.angle_slider.set_active(True)
            self.ax_scale.set_visible(False)
            self.scale_slider.set_active(False)
            self.ax_x.set_visible(False)
            self.ax_y.set_visible(False)
            asyncio.run(self.plot_twisted_airfoil(
                df=self.df, 
                angle_degrees=self.angle_slider.val, 
                ledge=True, 
                centroid=False
                )
            )
        elif task == 'Task 2: Scale':
            self.ax_angle.set_visible(False)
            self.angle_slider.set_active(False)
            self.ax_scale.set_visible(True)
            self.scale_slider.set_active(True)
            self.ax_x.set_visible(False)
            self.ax_y.set_visible(False)
            asyncio.run(self.plot_scale_airfoil(
                df=self.df, 
                scale_factor=self.scale_slider.val
                )
            )
        elif task == 'Task 3: Twist by Centroid':
            self.ax_angle.set_visible(True)
            self.angle_slider.set_active(True)
            self.ax_scale.set_visible(False)
            self.scale_slider.set_active(False)
            self.ax_x.set_visible(False)
            self.ax_y.set_visible(False)
            asyncio.run(self.plot_twisted_airfoil(
                df=self.df, 
                angle_degrees=self.angle_slider.val, 
                ledge=False, 
                centroid=True
                )
            )
        else:
            self.ax_angle.set_visible(True)
            self.angle_slider.set_active(True)
            self.ax_scale.set_visible(True)
            self.scale_slider.set_active(True)
            self.ax_x.set_visible(True)
            self.ax_y.set_visible(True)
            self.save_button_ax.set_visible(True)
            asyncio.run(self.plot_translated_airfoil(
                df=self.df, 
                centroid_x=float(self.x_textbox.text), 
                centroid_y=float(self.y_textbox.text)
                )
            )
        plt.draw()
    
    def save_results(self, event) -> None:
        """Save the transformed results to a file."""
        file_path = filedialog.asksaveasfilename(
            title='Save Transformed Airfoil Coordinates',
            defaultextension='.txt',
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )
        if file_path:
            self.save_results_concat.to_csv(file_path, sep='\t', index=False, float_format='%.6f')
