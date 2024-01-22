import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
DATA_PATH = os.environ.get("DATA_PATH")
os.makedirs(DATA_PATH, exist_ok=True)

# Function to load datasets
def load_data():
    # Donation retention data
    with open(f"{DATA_PATH}/blood_donation_retention.parquet", "wb") as file:
        res = requests.get("https://storage.data.gov.my/healthcare/blood_donation_retention_2024.parquet", allow_redirects=True)
        file.write(res.content)

    # Aggregate data 
    aggregate_data_links = [
        "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_facility.csv",
        "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/donations_state.csv",
        "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_facility.csv",
        "https://raw.githubusercontent.com/MoH-Malaysia/data-darah-public/main/newdonors_state.csv"
    ]

    for link in aggregate_data_links:
        res = requests.get(link)
        filename = link.split("/")[-1]
        with open(f"{DATA_PATH}/{filename}", "wb") as file:
            file.write(res.content)


if __name__ == "__name__":
    load_data()