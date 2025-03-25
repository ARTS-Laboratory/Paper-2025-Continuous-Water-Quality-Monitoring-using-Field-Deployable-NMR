import os
import pandas as pd

# Folder containing the CSV files
folder_path = "C:/Users/MK92/OneDrive - University of South Carolina/Paper-2025-Continuous-Water-Quality-Monitoring-using-Field-Deployable-NMR/data/creek_data/T2 Raw Data from creek/SPIE7"  # Update with the correct folder path

# Loop through all CSV files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".csv"):
        file_path = os.path.join(folder_path, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path, header=None)
        
        # Add the header
        df.columns = ["NMR signal (mV)", "time (s)"]
        
        # Save the updated CSV file
        df.to_csv(file_path, index=False)
        print(f"Updated: {filename}")

print("All files updated successfully.")
