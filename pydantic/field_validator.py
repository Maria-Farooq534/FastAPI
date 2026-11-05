from pydantic import BaseModel, Field, field_validator, EmailStr, AnyUrl
from typing import List, Dict, Optional

# step 1 : create schema

class Patient(BaseModel):
    name: str
    age: int
    weight: float
    email: EmailStr
    portfolio: AnyUrl
    married: Optional[bool] = None
    allergies: List[str]
    contact: Dict[str, str]
    
    # field validation
    
    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['edu.com', 'ncc.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError(f"{domain_name} is not a valid company domain.")
        return value
    
    @field_validator('name', mode='after') # by default, after mode
    @classmethod
    def transform_name(cls, value):
        transformed_name = value.upper()
        # if value != transformed_name:
        #     raise ValueError("Name should be upper case.")
        return transformed_name

    
# step 2: craete pydantic object

patient_info = {
    'name': 'Alex',
    'age': 34,
    'weight': 49,
    'email': 'alex@ncc.com',
    'portfolio': 'https://google.com',
    'allergies': ['dust'],
    'contact': {
        'phone': '+92309999999',
        'address': 'xyz',
        'email': 'alex@gmail.com'
    }
}

# step 3: pass pydantic object to the function

# create function

def insert_patient_data(patient_record):
    print(f"Patient record: {patient_record} inserted successfully.")
    
# pass object to the function

patient1 = Patient(**patient_info)
insert_patient_data(patient1)