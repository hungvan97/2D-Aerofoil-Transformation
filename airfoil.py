"""Contains functions to manipulate airfoil data."""

import numpy as np
from math import radians, cos, sin

async def twist_airfoil_ledge(df, angle_degrees):
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
    res_x = result_df.iloc[:, 0]  # Access X column
    res_y = result_df.iloc[:, 1]  # Access Y column
    coords = np.column_stack((res_x, res_y))
    rotated_coords = np.dot(coords, rotation_matrix.T)
    
    # Store the results
    result_df['X_twisted'] = rotated_coords[:, 0]
    result_df['Y_twisted'] = rotated_coords[:, 1]
    
    return result_df

async def twist_airfoil_centroid(df, angle_degrees):
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
    res_x = result_df.iloc[:, 0]  # Access X column
    res_y = result_df.iloc[:, 1]  # Access Y column
    centroid_x = res_x.mean()        
    centroid_y = res_y.mean()        

    # Convert angle to radians
    angle_rad = radians(angle_degrees)
    
    # Create rotation matrix (https://en.wikipedia.org/wiki/Rotation_matrix)
    rotation_matrix = np.array([
        [cos(angle_rad), -sin(angle_rad)],
        [sin(angle_rad), cos(angle_rad)]
    ])
    
    # Apply rotation to each point of data set. Centroid is the rotation center.
    coords = np.column_stack((res_x-centroid_x, res_y-centroid_y))
    rotated_coords = np.dot(coords, rotation_matrix.T)
    
    # Store the results
    result_df['X_twisted'] = rotated_coords[:, 0] + centroid_x
    result_df['Y_twisted'] = rotated_coords[:, 1] + centroid_y
    
    return result_df

async def scale_airfoil(df, scale_factor):
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
    res_x = result_df.iloc[:, 0]  # Access X column
    res_y = result_df.iloc[:, 1]  # Access Y column
    centroid_x = res_x.mean()
    centroid_y = res_y.mean()

    # Scale the plot
    result_df['X_scaled'] = centroid_x + (res_x - centroid_x) * scale_factor
    result_df['Y_scaled'] = centroid_y + (res_y - centroid_y) * scale_factor
    
    return result_df

async def translate_airfoil(df, x_center, y_center):
    """
    Translate the points in space as per the new center of aerofoil defined by the user.
    
    Args:
        df: pandas DataFrame with X and Y coordinates
        x_center: New X coordinate for the center
        y_center: New Y coordinate for the center

    Returns:
        DataFrame with translated coordinates
    """

    # Make a copy of the dataframe to avoid modifying the original
    result_df = df.copy()

    # Calculate current centroid by taking average of extreme points
    current_centroid_x = (max(result_df['X']) + min(result_df['X'])) / 2
    current_centroid_y = (max(result_df['Y']) + min(result_df['Y'])) / 2
    
    # Translate the points using the difference between the new center and current centroid
    result_df['X_translated'] = result_df['X'] + (x_center - current_centroid_x)
    result_df['Y_translated'] = result_df['Y'] + (y_center - current_centroid_y)

    return result_df