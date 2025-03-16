import os

dataset_path = "sign_language_data/datasets"

# Ensure the dataset folder exists
if not os.path.exists(dataset_path):
    print(f"⚠️ Warning: Dataset path '{dataset_path}' not found. Creating it now...")
    os.makedirs(dataset_path, exist_ok=True)  # Creates the directory if missing

def list_datasets():
    return [dataset for dataset in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, dataset))]

print("Available datasets:", list_datasets())
