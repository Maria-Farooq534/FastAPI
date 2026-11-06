from pydantic import BaseModel, computed_field, EmailStr, AnyUrl
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name: str
    age: int
    height: float
    weight: float
    email: EmailStr
    portfolio: AnyUrl
    allergies: List[str]
    contact: Dict[str,str]

    @computed_field()
    @property
    def bmi(self) -> float:
        return round((self.weight/self.height**2),2)

    
# 2: create pydantic object    

patient_info = {
    'name': 'alex',
    'age': 59,
    'height': 1.72,
    'weight': 60,
    'email': 'alex@ncc.com',
    'portfolio': 'https://www.google.com',
    'allergies': ['dust','pollen'],
    'contact': {
        'phone': '233333333',
        'email': 'abc@gmail.com',
        'address': 'xyz',
        'emergency': '2334243'
    }
}

# step 3 : pass the data to the function

#  create the function
def insert_patient_data(patient_data: Patient):
    print(f"Patient record: {patient_data} inserted successfully.")
    print("BMI: ", patient_data.bmi)

# pass data to tthe function

patient1 = Patient(**patient_info)
insert_patient_data(patient1)