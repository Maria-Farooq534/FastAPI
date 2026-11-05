from pydantic import BaseModel, Field, EmailStr, AnyUrl
from typing import List, Dict, Annotated, Optional

# step 1 : make schema

class Patient(BaseModel):
    name: str = Annotated[str, Field(max_length='50', title="Name", description='Enter you name', examples=["Maria", "Khoula"])]
    age: Annotated[int, Field(gt=20, lt=120, title='Age', description='Enter your age in numbers', examples=[45, 67], strict=True)]
    weight: Annotated[float, Field(gt=30, lt=100, strict=True)]
    email: EmailStr
    portfolio: AnyUrl
    married: Annotated[Optional[bool], Field(default=None, title='Single or Married')]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5, title='Allergies')]
    contact_info: Annotated[Dict[str, str], Field(title='Contact Info')]
    
# step 2 : create pydantic object

patient_info = {
    'name': 'Maria',
    'age': 24,
    'weight': 48,
    'email': 'maria@gmail.com',
    'portfolio': 'https://linkedin.com/22',
    'allergies': ['dust allergy'],
    'contact_info': {
        'phone': '+92307-000000000',
        'address': 'xyz'
    }
}

# step 3: pass pydantic object to the function

# define function
def insert_patient_data(patient_record):
    print(f"Record: {patient_record} inserted successfully.")

# pass data to the function

patient1 = Patient(**patient_info)
insert_patient_data(patient1)