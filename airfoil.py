"""Contains functions to manipulate airfoil data."""

import numpy as np
from math import radians, cos, sin

def twist_airfoil_ledge(df, angle_degrees):
    """
    Twist the airfoil about its leading edge by the specified angle in degrees.
    
    Args:
        df: pandas DataFrame with X and Y coordinates
        angle_degrees: Angle to twist in degrees (positive = clockwise)
    
    Returns:
        DataFrame with original and twisted coordinates
    """
    # Make a copy of the dataframe to avoid modifying the original
    result_df = df.copy()

    # Convert angle to radians
    angle_rad = radians(angle_degrees)
    
    # Create rotation matrix (https://en.wikipedia.org/wiki/Rotation_matrix)
    rotation_matrix = np.array([
        [cos(angle_rad), -sin(angle_rad)],
        [sin(angle_rad), cos(angle_rad)]
    ])
    
    # Apply rotation to each point of data set. Center of leading edge (0,0) is the rotation center.
    coords = np.column_stack((result_df['X'], result_df['Y']))
    rotated_coords = np.dot(coords, rotation_matrix.T)
    
    # Store the results
    result_df['X_twisted'] = rotated_coords[:, 0]
    result_df['Y_twisted'] = rotated_coords[:, 1]
    
    return result_df

def twist_airfoil_centroid(df, angle_degrees):
    """
    Twist the airfoil about its centroid by the specified angle in degrees.
    
    Args:
        df: pandas DataFrame with X and Y coordinates
        angle_degrees: Angle to twist in degrees (positive = clockwise)
    
    Returns:
        DataFrame with original and twisted coordinates
    """
    # Make a copy of the dataframe to avoid modifying the original
    result_df = df.copy()

    # Calculate centroid
    centroid_x = result_df['X'].mean()
    centroid_y = result_df['Y'].mean()

    # Convert angle to radians
    angle_rad = radians(angle_degrees)
    
    # Create rotation matrix (https://en.wikipedia.org/wiki/Rotation_matrix)
    rotation_matrix = np.array([
        [cos(angle_rad), -sin(angle_rad)],
        [sin(angle_rad), cos(angle_rad)]
    ])
    
    # Apply rotation to each point of data set. Centroid is the rotation center.
    coords = np.column_stack((result_df['X']-centroid_x, result_df['Y']-centroid_y))
    rotated_coords = np.dot(coords, rotation_matrix.T)
    
    # Store the results
    result_df['X_twisted'] = rotated_coords[:, 0] + centroid_x
    result_df['Y_twisted'] = rotated_coords[:, 1] + centroid_y
    
    return result_df

def scale_airfoil(df, scale_factor):
    """
    Scale the airfoil by a factor.
    
    Args:
        df: pandas DataFrame with X and Y coordinates
        scale_factor: Factor to scale the airfoil by
    
    Returns:
        DataFrame with scaled coordinates
    """
    # Make a copy of the dataframe to avoid modifying the original
    result_df = df.copy()
    
    # Calculate centroid
    centroid_x = result_df['X'].mean()
    centroid_y = result_df['Y'].mean()

    # Scale the plot
    result_df['X_scaled'] = centroid_x + (result_df['X'] - centroid_x) * scale_factor
    result_df['Y_scaled'] = centroid_y + (result_df['Y'] - centroid_y) * scale_factor
    
    return result_df
