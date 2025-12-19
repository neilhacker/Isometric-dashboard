import os
import math
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def round_to_significant_figures(value, sig_figs=2):
    """Round a number to a specified number of significant figures."""
    if value == 0:
        return 0.0
    return round(value, sig_figs - int(math.floor(math.log10(abs(value)))) - 1)


ISOMETRIC_URL = "https://api.isometric.com/registry/v0/deliveries"
CLIENT_SECRET = os.getenv("ISOMETRIC_CLIENT_SECRET")

if not CLIENT_SECRET:
    raise ValueError("ISOMETRIC_CLIENT_SECRET environment variable is required. Please set it in your .env file.")

params = {"first": 10, "last": 10}
headers = {"x-client-secret": CLIENT_SECRET}

response = requests.get(ISOMETRIC_URL, headers=headers, params=params)
response.raise_for_status()  # fail fast if auth or request is wrong

data = response.json()
nodes = data["nodes"]


rows = []
for n in nodes:
    from_supplier = n["from_supplier"]["organisation"]["name"]
    to_organisation = n["to_organisation"]["name"]
    credits = n["credit_batch_size_total"]["credits"]
    
    if credits < 1:
        # Use credit_kgs if credits would round to 0
        credit_kgs = n["credit_batch_size_total"]["credit_kgs"]
        # Divide by 1000 and round to 2 significant figures
        value = round_to_significant_figures(credit_kgs / 1000, 2)
        rows.append(f'{from_supplier} ─({value}t)─▶ {to_organisation}')
    else:
        # Use credits as before
        rows.append(f'{from_supplier} ─({math.floor(credits):,}t)─▶ {to_organisation}')
for a in rows:
    print(a)


ISOMETRIC_URL = "https://api.isometric.com/registry/v0/retirements"
CLIENT_SECRET = os.getenv("ISOMETRIC_CLIENT_SECRET")

if not CLIENT_SECRET:
    raise ValueError("ISOMETRIC_CLIENT_SECRET environment variable is required. Please set it in your .env file.")

params = {"first": 10, "last": 10}
headers = {"x-client-secret": CLIENT_SECRET}

response = requests.get(ISOMETRIC_URL, headers=headers, params=params)
response.raise_for_status()  # fail fast if auth or request is wrong

data = response.json()
nodes = data["nodes"]

rows = []
for n in nodes:
    beneficiary_name = n["beneficiary"]["name"]
    credits = n["credit_batch_size_total"]["credits"]
    
    if credits < 1:
        # Use credit_kgs if credits would round to 0
        credit_kgs = n["credit_batch_size_total"]["credit_kgs"]
        # Divide by 1000 and round to 2 significant figures
        value = round_to_significant_figures(credit_kgs / 1000, 2)
        rows.append(f'{beneficiary_name}: ({value}t)')
    else:
        # Use credits as before
        rows.append(f'{beneficiary_name}: ({math.floor(credits):,}t)')
for a in rows:
    print(a)
