import pandas as pd
import numpy as np

def calculate_metrics(file_path):
    # Load the dataset
    # Note: Update 'file_path' if your file name is different
    df = pd.read_csv(file_path)

    # --- 1. Define Columns ---
    # Deck 1 columns
    cols_1 = ['X', 'Y', 'Z', 'Qx', 'Qy', 'Qz', 'Qw']
    # Deck 2 columns
    cols_2 = ['X.1', 'Y.1', 'Z.1', 'Qx.1', 'Qy.1', 'Qz.1', 'Qw.1']
    
    # Label names for the output
    labels = ['X', 'Y', 'Z', 'Qx', 'Qy', 'Qz', 'Qw']

    # --- 2. Calculate WAPE (Weighted Absolute Percentage Error) ---
    wape_results = {}

    # Calculate WAPE per individual column
    for c1, c2, lbl in zip(cols_1, cols_2, labels):
        actual = df[c1].values
        forecast = df[c2].values
        
        numerator = np.sum(np.abs(actual - forecast))
        denominator = np.sum(np.abs(actual))
        
        # Handle division by zero
        if denominator == 0:
            wape_results[lbl] = np.nan 
        else:
            wape_results[lbl] = numerator / denominator

    # Calculate Aggregate Position WAPE (X, Y, Z combined)
    pos_act = df[['X', 'Y', 'Z']].values.flatten()
    pos_for = df[['X.1', 'Y.1', 'Z.1']].values.flatten()
    wape_pos = np.sum(np.abs(pos_act - pos_for)) / np.sum(np.abs(pos_act))

    # Calculate Aggregate Orientation WAPE (Qx, Qy, Qz, Qw combined)
    quat_act = df[['Qx', 'Qy', 'Qz', 'Qw']].values.flatten()
    quat_for = df[['Qx.1', 'Qy.1', 'Qz.1', 'Qw.1']].values.flatten()
    wape_quat = np.sum(np.abs(quat_act - quat_for)) / np.sum(np.abs(quat_act))

    # Store WAPE results in a DataFrame
    wape_df = pd.DataFrame(list(wape_results.items()), columns=['Component', 'WAPE'])
    # Add aggregates
    wape_df.loc[len(wape_df)] = ['Aggregate Position', wape_pos]
    wape_df.loc[len(wape_df)] = ['Aggregate Orientation', wape_quat]
    
    # Add a percentage column for easier reading
    wape_df['WAPE %'] = (wape_df['WAPE'] * 100).apply(lambda x: f"{x:.2f}%")

    # --- 3. Calculate Difference Margins (Euclidean Distance) ---
    # Position Margin: sqrt(diff_x^2 + diff_y^2 + diff_z^2)
    diff_p = df[['X', 'Y', 'Z']].values - df[['X.1', 'Y.1', 'Z.1']].values
    margin_p = np.linalg.norm(diff_p, axis=1)

    # Orientation Margin: sqrt(diff_qx^2 + ... + diff_qw^2)
    diff_q = df[['Qx', 'Qy', 'Qz', 'Qw']].values - df[['Qx.1', 'Qy.1', 'Qz.1', 'Qw.1']].values
    margin_q = np.linalg.norm(diff_q, axis=1)

    # Create a DataFrame for margins
    margin_df = pd.DataFrame({
        'Diff_X': diff_p[:, 0],
        'Diff_Y': diff_p[:, 1],
        'Diff_Z': diff_p[:, 2],
        'Position_Margin': margin_p,
        'Diff_Qx': diff_q[:, 0],
        'Diff_Qy': diff_q[:, 1],
        'Diff_Qz': diff_q[:, 2],
        'Diff_Qw': diff_q[:, 3],
        'Orientation_Margin': margin_q
    })

    return wape_df, margin_df

if __name__ == "__main__":
    # Replace with your actual CSV file name
    file_name = 'Untitled spreadsheet(1).xlsx - Sheet.csv'
    
    try:
        wape_table, margin_table = calculate_metrics(file_name)
        
        print("--- WAPE Analysis Results ---")
        print(wape_table)
        
        # Save results to CSV files
        wape_table.to_csv('WAPE_Analysis_Results.csv', index=False)
        margin_table.to_csv('Difference_Margins.csv', index=False)
        print("\nResults saved to 'WAPE_Analysis_Results.csv' and 'Difference_Margins.csv'")
        
    except FileNotFoundError:
        print(f"Error: File '{file_name}' not found. Please check the file path.")