from pydantic import BaseModel


class Pharmacy(BaseModel):

    name: str

    city: str


class User(BaseModel):

    username: str

    password: str

    company_code: str


class Company(BaseModel):

    company_name: str

    company_code: str


class Medicine(BaseModel):

    name: str

    quantity: int

    price: float

    expiry_date: str

    manufacturer: str