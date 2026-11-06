from pydantic import BaseModel, model_validator, EmailStr, AnyUrl, Field
from typing import List, Optional, Dict, Annotated

# Step 1: define schema

class Patient(BaseModel):
    name: str
    age: int
    email: EmailStr
    portfolio: AnyUrl
    married: Annotated[Optional[bool], Field(default=None)]
    allergies : Optional[List[str]]
    contact: Dict[str, str]
    
    # i have to add a constraint on 2 fields, let say on age and contact. if the age is gt 60, there should be an emergency contact in contact  list(dict.). if not then do not add that patient record.
    # For this, i will use model validator.
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency' not in model.contact:
            raise ValueError("Patients older than 60 must have an emergency contact.")
        return model
    
    # now i will add another constraint, patient should be under 60 and a memebr of a specific organization.
    # this will use 2 fields, age and email
    
    @model_validator(mode='before')
    def validate_patient_organization(cls, model):
        valid_orgs = ['ncc.com', 'edu.com', 'edu.pk']
        patient_email = model['email']
        domain = patient_email.split('@')[-1].lower()
        if domain not in valid_orgs or model['age'] >= 60:
            raise ValueError(f"Patient should be under 60 if he/she is a member of a {domain.split('.')[0]} organization.")
        return model
    
    # here i used model['email'] and model['age'] bcz the mode is before. so its using raw data as provided.
    # if the mode is after, then i will use self.age or self.email as model.age or model.email.
    # {domain.split('.')[0]} will take the domain let say ncc.com , split by dot into ['ncc','com'] and take the first element which is ncc.
            
# step 2: craete pydantic object

patient_info = {
    'name': 'alex',
    'age': 59,
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
def insert_patient_data(patient_data):
    print(f"Patient record: {patient_data} inserted successfully.")

# pass data to tthe function

patient1 = Patient(**patient_info)
insert_patient_data(patient1)