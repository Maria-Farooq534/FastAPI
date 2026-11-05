from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional

# Step 1: Creating schema

class Patient(BaseModel):
    
    name: str = Field(max_length = 50)
    email: EmailStr
    profile_link: AnyUrl
    age: int = Field(gt=10, lt=100)
    weight: float = Field(gt=30, ls=100)
    married: Optional[bool] = None
    allergies: Optional[List[str]] = None
    contact: Dict[str, str]


# Step 2: Creating Pydantic object
# i haven't added married details, so by default, pydantic will set it to None.
patient_details = {
    'name': 'Alex',
    'email': 'alex@gmail.com',
    'profile_link': 'https://linkedin.com/22',
    'age': '20',
    'weight': 60, 
    'allergies': ['pollen','dust'],
    'contact': {
        'phone': '+923030000000',
        'email': 'abc@gmail.com'
    }
}

patient1 = Patient(**patient_details)

# Step 3: Passing Object to the function, first create the function

# creating function
def insert_patient_record(record):
    print(f'The record "{record}" inserted successfully.')
    
    
# passing data to the function
insert_patient_record(patient1)