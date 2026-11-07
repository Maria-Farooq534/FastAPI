from pydantic import BaseModel

# step 1: creating schema

# address ccan  have multiple components of it , like city, state, pin code etc, so, for this purpose, we will craete a seperte model for address and wil use it as a field in patient class. 

class Address(BaseModel):
    city: str
    state: str
    pin: int

class Patient(BaseModel):
    name: str
    age: int
    gender: str
    address: Address # then here, instead of values, we tell that this field belongs to address class.

# step 2: create pydantic object

address_info = {
    'city': 'Sargodha',
    'state': 'Punjab',
    'pin': 40600
}

address1 = Address(**address_info)

patient_info = {
    'name': 'Maria',
    'age': 24,
    'gender': 'Female',
    'address': address1
}

patient1 = Patient(**patient_info)

def insert_patient_info(patient_info):
    print(f"Patient info: {patient_info}")    


insert_patient_info(patient1)
insert_patient_info(patient1.address)
insert_patient_info(patient1.address.city)