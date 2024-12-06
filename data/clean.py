import pandas as pd
from pathlib import Path

# Define file paths
data_dir = Path('.')
combined_cleaned_file = data_dir / 'combined_cleaned.csv'

# Function to remove duplicate IDs in combined_cleaned.csv
def remove_duplicate_ids(file_path):
    try:
        # Load the CSV file
        df = pd.read_csv(file_path)

        # Create a set to track unique IDs
        seen_ids = set()
        unique_rows = []

        # Iterate over rows and keep only rows with unique IDs
        for _, row in df.iterrows():
            row_id = row['id']
            if row_id not in seen_ids:
                seen_ids.add(row_id)
                unique_rows.append(row)

        # Create a new DataFrame with unique rows
        unique_df = pd.DataFrame(unique_rows)

        # Save the deduplicated DataFrame back to the CSV
        unique_df.to_csv(file_path, index=False)
        print(f"Duplicates removed. Updated file saved: {file_path}")

    except Exception as e:
        print(f"Error processing {file_path}: {e}")

# Remove duplicate IDs in combined_cleaned.csv
remove_duplicate_ids(combined_cleaned_file)

# Print the updated file content for verification
updated_combined_df = pd.read_csv(combined_cleaned_file)
print(updated_combined_df.head(10))  # Print first 10 rows
