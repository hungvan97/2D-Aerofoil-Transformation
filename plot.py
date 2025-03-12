"""Contains functions for plotting the airfoil data."""

import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons, Slider
from airfoil import twist_airfoil_ledge, twist_airfoil_centroid, scale_airfoil

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
        
        self.ax_scale = plt.axes([0.85, 0.2, 0.03, 0.6])
        self.scale_slider = Slider(ax=self.ax_scale, label='Scale Factor', valmin=0.1, valmax=2.0, valinit=0, orientation='vertical')
        self.scale_slider.set_active(False)

        # Update plot when sliders are changed
        self.angle_slider.on_changed(func=lambda _: self.update_plot(task=radio.value_selected))
        self.scale_slider.on_changed(func=lambda _: self.update_plot(task=radio.value_selected))

        # Show initial plot (Task 1 by default)
        self.update_plot(task=self.task_list[0])
        plt.show()

    def plot_twisted_airfoil(self, df, angle_degrees, ledge=True, centroid=False) -> None:
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
            result_df = twist_airfoil_ledge(df=df, angle_degrees=angle_degrees)
        else:
            result_df = twist_airfoil_centroid(df=df, angle_degrees=angle_degrees)
        
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

    def plot_scale_airfoil(self, df, scale_factor) -> None:
        """
        Plot the original and scaled airfoil.
        
        Args:
            df: pandas DataFrame with X and Y coordinates
            scale_factor: Factor to scale the airfoil by
        """
        plt.sca(self.ax)  # Set the main axes as current
        plt.cla()       # Clear the main axes only
        
        # Apply scale
        result_df = scale_airfoil(df, scale_factor)
        
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

    def update_plot(self, task) -> None:
        plt.sca(self.ax)
        plt.cla()
        if task == 'Task 1: Twist by Leading Edge':
            self.ax_angle.set_visible(True)
            self.angle_slider.set_active(True)
            self.ax_scale.set_visible(False)
            self.scale_slider.set_active(False)
            self.plot_twisted_airfoil(df=self.df, angle_degrees=self.angle_slider.val, ledge=True, centroid=False)
        elif task == 'Task 2: Scale':
            self.ax_angle.set_visible(False)
            self.angle_slider.set_active(False)
            self.ax_scale.set_visible(True)
            self.scale_slider.set_active(True)
            self.plot_scale_airfoil(df=self.df, scale_factor=self.scale_slider.val)
        else:
            self.ax_angle.set_visible(True)
            self.angle_slider.set_active(True)
            self.ax_scale.set_visible(False)
            self.scale_slider.set_active(False)
            self.plot_twisted_airfoil(df=self.df, angle_degrees=self.angle_slider.val, ledge=False, centroid=True)
        plt.draw()
