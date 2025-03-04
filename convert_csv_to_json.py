import csv
import json

# Function to convert CSV to JSON
def csv_to_json(csv_file, json_file):
    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        
        # Remove any empty or None headers
        filtered_data = [
            {key: value for key, value in row.items() if key and key.strip()} 
            for row in csv_reader
        ]

    with open(json_file, 'w', encoding='utf-8') as file:
        json.dump(filtered_data, file, indent=4)

# Example usage
csv_to_json('fmp-data.csv', 'fmp-data.json')