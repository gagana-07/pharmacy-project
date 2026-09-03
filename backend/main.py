from fastapi import FastAPI
from datetime import date, datetime
from fastapi.middleware.cors import CORSMiddleware

from models import Pharmacy, User, Medicine
from auth import register_user, login_user

from database import (
    pharmacies_collection,
    medicines_collection,
    bills_collection
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Pharmacy AI Backend Running"}


# -------------------------
# PHARMACY APIs
# -------------------------

@app.post("/add-pharmacy")
def add_pharmacy(pharmacy: Pharmacy):

    pharmacies_collection.insert_one({
        "name": pharmacy.name,
        "city": pharmacy.city
    })

    return {"message": "Data inserted successfully"}


@app.get("/all-pharmacies")
def get_pharmacies():

    data = list(
        pharmacies_collection.find({}, {"_id": 0})
    )

    return data


# -------------------------
# USER AUTH APIs
# -------------------------

@app.post("/register")
def register(user: User):

    return register_user(
        user.username,
        user.password
    )


@app.post("/login")
def login(user: User):

    return login_user(
        user.username,
        user.password
    )


# -------------------------
# MEDICINE APIs
# -------------------------

@app.post("/add-medicine")
def add_medicine(medicine: Medicine):

    medicines_collection.insert_one({
        "name": medicine.name.lower(),
        "quantity": medicine.quantity,
        "price": medicine.price,
        "expiry_date": medicine.expiry_date,
        "manufacturer": medicine.manufacturer
    })

    return {"message": "Medicine added successfully"}


@app.get("/all-medicines")
def get_all_medicines():

    data = list(
        medicines_collection.find({}, {"_id": 0})
    )

    return data


@app.get("/search-medicine/{medicine_name}")
def search_medicine(medicine_name: str):

    medicine = medicines_collection.find_one(
        {
            "name": {
                "$regex": f"^{medicine_name}$",
                "$options": "i"
            }
        },
        {"_id": 0}
    )

    if medicine:
        return medicine

    return {"message": "Medicine not found"}


@app.put("/update-stock/{medicine_name}")
def update_stock(medicine_name: str, quantity: int):

    result = medicines_collection.update_one(
        {
            "name": {
                "$regex": f"^{medicine_name}$",
                "$options": "i"
            }
        },
        {
            "$set": {
                "quantity": quantity
            }
        }
    )

    if result.modified_count > 0:
        return {"message": "Stock updated successfully"}

    return {"message": "Medicine not found"}


@app.get("/low-stock")
def low_stock():

    medicines = list(
        medicines_collection.find(
            {"quantity": {"$lt": 10}},
            {"_id": 0}
        )
    )

    return medicines


@app.delete("/delete-medicine/{medicine_name}")
def delete_medicine(medicine_name: str):

    result = medicines_collection.delete_one(
        {
            "name": {
                "$regex": f"^{medicine_name}$",
                "$options": "i"
            }
        }
    )

    if result.deleted_count > 0:
        return {"message": "Medicine deleted successfully"}

    return {"message": "Medicine not found"}


@app.get("/expired-medicines")
def expired_medicines():

    medicines = list(
        medicines_collection.find(
            {},
            {"_id": 0}
        )
    )

    today = str(date.today())

    expired = []

    for medicine in medicines:

        if (
            "expiry_date" in medicine and
            medicine["expiry_date"] < today
        ):
            expired.append(medicine)

    return expired


# -------------------------
# BILLING APIs
# -------------------------

@app.post("/generate-bill")
def generate_bill(
    customer_name: str,
    medicine_name: str,
    quantity: int
):

    medicine = medicines_collection.find_one(
        {
            "name": {
                "$regex": f"^{medicine_name}$",
                "$options": "i"
            }
        }
    )

    if not medicine:
        return {"message": "Medicine not found"}

    if medicine["quantity"] < quantity:
        return {"message": "Insufficient stock"}

    total_amount = medicine["price"] * quantity

    medicines_collection.update_one(
        {"_id": medicine["_id"]},
        {
            "$set": {
                "quantity": medicine["quantity"] - quantity
            }
        }
    )

    bill = {
        "customer_name": customer_name,
        "medicine_name": medicine["name"],
        "quantity": quantity,
        "price_per_unit": medicine["price"],
        "total_amount": total_amount,
        "bill_date": str(datetime.now())
    }

    bills_collection.insert_one(bill)

    return {
        "message": "Bill generated successfully",
        "bill": bill
    }


@app.get("/all-bills")
def get_all_bills():

    bills = list(
        bills_collection.find(
            {},
            {"_id": 0}
        )
    )

    return bills