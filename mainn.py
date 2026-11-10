from fastapi import FastAPI, HTTPException, Path, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Annotated, Literal, Optional
from pydantic import BaseModel, Field, computed_field
import json

app = FastAPI()


# function to load dataset
def load_data():
    with open('./patients.json', 'r') as file:
        data = json.load(file)
        return data
    
# function to save data
def save_data(data_record):
    with open('./patients.json', 'w') as file:
        json.dump(data_record, file)

# step 1: create schema

class Patient(BaseModel):
    id: Annotated[str, Field(..., title="Patient ID", examples=['P001'])]
    name: Annotated[str, Field(..., max_length=50, title='Patient Name', description='Name of the patient', examples=['Maria', 'Farooq'])]
    city: Annotated[str, Field(..., title='City', description='City of residence', examples=['Sargodha','Shahpur'])]
    age: Annotated[int, Field(..., gt=0, lt=150, title="Age", description="Enter Patient Age")]
    gender: Annotated[Literal['male','female','others'], Field(..., title='Gender')]
    height: Annotated[float, Field(..., gt=0, title='Height', description='Height of the patient')]
    weight: Annotated[float, Field(..., gt=0, name='weight', description='Weight of the patient')]
    
    # rest , bmi and verdict are the computed fields that we will calculate on runtime froom user data. by using computed field
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height ** 2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <= 18.5:
            verdict = "Underweight"
        elif self.bmi <= 25:
            verdict = 'Normal'
        elif self.bmi <= 29:
            verdict = 'Overweight'
        else:
            verdict = "Obese"
        return verdict
    

# To update patient info, i need to make a new pydantic model, bcz the Patient model has all required fields, but when updating record, the client might not update all the records. so i need to make it optional.

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str],Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female','others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None)]
    weight: Annotated[Optional[float], Field(default=None)]
    
    

    
# step 2: create pydantic object

patient_info = {
    'id': 'P006',
    'name': 'Maria',
    'city': 'Sargodha',
    'age': 24,
    'gender': 'female',
    'height': 1.62,
    'weight': 48
}

# unpack dict
patient1 = Patient(**patient_info)



@app.get("/")
def home():
    return {'message': 'Patient management system'}

@app.get("/about")
def about():
    return {'message': 'This is about PMS using FastAPI'}

@app.get("/view")
def view_patients():
    data = load_data()
    return data

# endpoint to view patient by patient id

@app.get("/patient/{patient_id}")
def view_one_patient(patient_id:str=Path(...,title='Patient ID', description='Enter Patient ID', examples=['P001', 'P002'])):
    data = load_data()
    if patient_id not in data.keys():
        raise HTTPException(status_code=400, detail=f'Please select from {data.keys()}')
    
    return data[patient_id]
    
@app.get("/sort")
def sort_patient(sort_by:str = Query(..., description="Sort by weight, height or bmi"),
                 order: str = Query(description='Select sorting order asc or dsc')
                ):
    sorting_fields = ['weight', 'height', 'bmi']
    if sort_by not in sorting_fields:
        raise HTTPException(status_code=400, detail=f'Invalid choice! Please select from {sorting_fields}')
    
    data = load_data()
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=True if order=='dsc' else False)
    return sorted_data


# now, this time we are creating a patient data, not retriving, so, i'll use POST instead of get.

@app.post('/create')
def create_patient(patient: Patient):
    
    #load exisiting data
    data = load_data()
    
    # check if the new record already exists in previous record
    
    if patient.id in data:
        raise HTTPException(status_code=400, detail=f'{patient.id} already exists.')
    
    # if not exist, then add record in the database.
    data[patient.id] = patient.model_dump(exclude='id')
    
    #save data into json file
    save_data(data)
    
    # if everything done successfully, we will then send a json response to the client, which has status code 201 that shows resource created successfully. 
    
    return JSONResponse(status_code=201, content={'message': 'Patient created successfully.'})
    
    
    
    
# about create_patient function
# patient: Patient , here patient is parameter the function will receive,it will be the data , and, Patient is the class, it shows that patient belongs to Patient
# patient object/data will be redirected to Patient class. Patient class will validate the data, apply all rules and check if data is correct or not.
# if data validated successfully, then next steps will be perormed, otherwise it iwill raise error.
# data is a python dictionary, where patient is a pydantic object. so, to add patient into data, we first need to convert it into a dixtionary.
# once converted, we now have to add in the data file and save the file.
# we first create a save_data function for it.

    #save data into json file
    # save_data(data)
    
# if everything done successfully, we will then send a json response to the client, which has status code 201 that shows resource created successfully. 


# Update Endpoint, HTTP method used: PUT
@app.put("/edit/{patient_id}")
def edit_patient_record(patient_id: str, patient_updated_record: PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f'{patient_id} not found!')
    
    if patient_id in data:
        existing_patient_info = data[patient_id]
        
        updated_patient_info = patient_updated_record.model_dump(exclude_unset=True) # i need to convert this pydantic object into a dict.
        
        for key, value in updated_patient_info.items():
            existing_patient_info[key] = value
            
        # to update data, we need to convert it back into pydantic object
        
    existing_patient_info['id'] = patient_id        # patient id was missing from the data, so, we need to add it.
    
    patient_pydantic_object = Patient(**existing_patient_info)
    
    # now, this pydantic object has patient id as well, that we need to exclude
    
    existing_patient_info = patient_pydantic_object.model_dump(exclude='id')
        
    data[patient_id] = existing_patient_info               # update the record with new record
    
    save_data(data)
        
    return JSONResponse(status_code=200, content={'message': f'{patient_id} updated successfully'})
         
        
    