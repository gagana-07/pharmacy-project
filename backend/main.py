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
        "price": medicine.price
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