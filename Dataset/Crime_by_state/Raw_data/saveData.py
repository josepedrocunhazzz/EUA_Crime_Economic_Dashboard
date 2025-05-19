import os
import pandas as pd

# Define the directory path
final_dir = "C:/Users/marta/OneDrive - Universidade de Coimbra/Mestrado/1 ano/2 semestre/VAD/Projeto/Dataset/Crime_by_state"
dir = "C:/Users/marta/OneDrive - Universidade de Coimbra/Mestrado/1 ano/2 semestre/VAD/Projeto/Dataset/Crime_by_state/Raw_data"

# Get the list of folders
folders = [f for f in os.listdir(dir) if os.path.isdir(os.path.join(dir, f))]

for folder in folders:
    # List to store first rows
    first_rows = []
        
    folder_path = os.path.join(dir, folder)
    
    # Get all CSV files in the folder
    files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]

    for file in files:
        file_path = os.path.join(folder_path, file)
        
        # Read the first row only
        data = pd.read_csv(file_path, nrows=1)

        # Modify the first column to store the cleaned filename
        if not data.empty:
            clean_filename = file.replace("_03-02-2025", "").replace(".csv", "")  # Remove date & extension
            data.iloc[0, 0] = clean_filename  # Replace first column's value

        # Append to the list
        first_rows.append(data)

    # Combine all first rows into a single DataFrame
    final_df = pd.concat(first_rows, ignore_index=True)

    # csv has the name of the folder it's in
    output_name = folder + ".csv"

    # Save to a single CSV file
    output_path = os.path.join(final_dir, output_name)
    final_df.to_csv(output_path, index=False)

    print(f"Saved first rows from {len(files)} files to {output_path}")