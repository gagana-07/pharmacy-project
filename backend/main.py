from fastapi import FastAPI
from models import Pharmacy, User, Medicine
from database import pharmacies_collection, medicines_collection
from auth import register_user, login_user

app = FastAPI()


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
        "name": medicine.name,
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
        {"name": medicine_name},
        {"_id": 0}
    )

    if medicine:
        return medicine

    return {"message": "Medicine not found"}


@app.put("/update-stock/{medicine_name}")
def update_stock(medicine_name: str, quantity: int):

    result = medicines_collection.update_one(
        {"name": medicine_name},
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
        {"name": medicine_name}
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

    expired = []

    for medicine in medicines:
        expiry = medicine.get("expiry_date")

        if expiry and expiry < "2026-12-31":
            expired.append(medicine)

    return expired