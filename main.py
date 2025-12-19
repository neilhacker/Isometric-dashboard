#  type this into terminal to start the server: python3 -m uvicorn main:app --reload --port 8000
import os
import math
import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Allow your front-end origin (for local dev, allow localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten this later in prod
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

ISOMETRIC_ISSUANCES_URL = "https://api.isometric.com/registry/v0/issuances"
ISOMETRIC_RETIREMENTS_URL = "https://api.isometric.com/registry/v0/retirements"
ISOMETRIC_DELIVERIES_URL = "https://api.isometric.com/registry/v0/deliveries"
CLIENT_SECRET = os.getenv("ISOMETRIC_CLIENT_SECRET")

if not CLIENT_SECRET:
    raise ValueError("ISOMETRIC_CLIENT_SECRET environment variable is required. Please set it in your .env file.")

def round_to_significant_figures(value, sig_figs=2):
    """Round a number to a specified number of significant figures."""
    if value == 0:
        return 0.0
    return round(value, sig_figs - int(math.floor(math.log10(abs(value)))) - 1)


@app.get("/issuances")
def issuances():
    params = {"first": 10, "last": 10}
    headers = {"x-client-secret": CLIENT_SECRET}

    response = requests.get(ISOMETRIC_ISSUANCES_URL, headers=headers, params=params)
    response.raise_for_status()  # fail fast if auth or request is wrong

    data = response.json()
    nodes = data["nodes"]

    rows = [
        f'{n["supplier"]["organisation"]["name"]}: {math.floor(n["credit_batch_size_total"]["credits"]):,}t'
        for n in nodes
    ]
    return {"rows": rows}

@app.get("/credits")
def get_total_issued_credits():
    total_credits = 0.0
    after = None
    headers = {"x-client-secret": CLIENT_SECRET}


    while True:
        params = {
            "first": 50,  # max allowed per page
        }
        if after:
            params["after"] = after

        resp = requests.get(ISOMETRIC_ISSUANCES_URL, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()

        # Add this page’s credits
        for node in data["nodes"]:
            total_credits += node["credit_batch_size_total"]["credits"]

        page_info = data["page_info"]
        if not page_info["has_next_page"]:
            break

        after = page_info["end_cursor"]
    return total_credits

@app.get("/deliveries")
def deliveries():
    params = {"first": 10, "last": 10}
    headers = {"x-client-secret": CLIENT_SECRET}

    response = requests.get(ISOMETRIC_DELIVERIES_URL, headers=headers, params=params)
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
    
    return {"rows": rows}

@app.get("/retirements")    
def retirements():
    params = {"first": 10, "last": 10}
    headers = {"x-client-secret": CLIENT_SECRET}

    response = requests.get(ISOMETRIC_RETIREMENTS_URL, headers=headers, params=params)
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
            rows.append(f'{beneficiary_name}: {value}t')
        else:
            # Use credits as before
            rows.append(f'{beneficiary_name}: {math.floor(credits):,}t')

    return {"rows": rows}



if __name__ == "__main__":
    print(issuances())
    print(get_total_issued_credits())
    print(retirements())
    print(deliveries())