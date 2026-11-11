from fastapi import FastAPI, HTTPException, Query, Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional, Literal
import json

app = FastAPI()

# functions
# load_data()
def load_data():
    with open('./patients.json', 'r') as file:
        return json.load(file)
    
    
# save data
def save_data(data):
    with open('./patients.json', 'w') as file:
        return json.dump(data, file)
    
    
    
# pydantic, step 1: define schema
class Patient(BaseModel):
    id: Annotated[str, Field(..., name='Patient ID', description="ID of the Patient", example='P003')]
    name: Annotated[str, Field(..., name='Patient Name', description='Name of the Patient', example='Maria')]
    city: Annotated[str, Field(..., title="City Name", description="Patient's residence", example='Sargodha')]
    age: Annotated[int, Field(..., title='Age', description="Patient's age", example='24', gt=0, lt=150)]
    gender: Annotated[Literal["female", "male", "others"], Field(..., title="Gender", description="Gender of the patient", examples=['female','male'])]
    height: Annotated[float, Field(..., title="Height", description='Height in meters', gt=0, example=1.62)]
    weight: Annotated[float, Field(..., title='Weight', description="Patient's weight in kgs", example=50, gt=0)]
    

    # bmi and verdict will be calculated on runtime using patient's given data. so these will be computed fields
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height**2), 2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi <= 18.5:
            return "Underweight"
        elif self.bmi <= 24.9:
            return "Normal"
        elif 25 <= self.bmi <= 29.9:
            return "Overweight"
        else:
            return "Obese"
        
        
class PatientUpdate(BaseModel):
    # i won't include id here, bcz id will be provided by the user to update record of that patient.
    name: Annotated[Optional[str], Field(default=None, name='Patient Name', description='Name of the Patient', example='Maria')]
    city: Annotated[Optional[str], Field(default=None, title="City Name", description="Patient's residence", example='Sargodha')]
    age: Annotated[Optional[int], Field(default=None, title='Age', description="Patient's age", example='24', gt=0, lt=150)]
    gender: Annotated[Optional[Literal["female", "male", "others"]], Field(default=None, title="Gender", description="Gender of the patient", examples=['female','male'])]
    height: Annotated[Optional[float], Field(default=None, title="Height", description='Height in meters', gt=0, example=1.62)]
    weight: Annotated[Optional[float], Field(default=None, title='Weight', description="Patient's weight in kgs", example=50)]
    

@app.get("/")
def home():
    return f"Patient Management System using FastAPI"

@app.get("/view")
def view_patients():
    return load_data()

@app.get('/patient/{patient_id}')
def view_patient(patient_id):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f'Patient {patient_id} not found!')
    
    return data[patient_id]

@app.get("/sort")
def sort_patients(sort_by:str = Query(..., title="Sort by weight, height or bmi", examples=['weight']), order:str = Query(default='asc', description='sort in asc or dsc')):
    sorting_fields = ['weight', 'height', 'bmi']
    if sort_by not in sorting_fields:
        raise HTTPException(status_code=400, detail=f'Invalid choice. Please select from {sorting_fields}')

    if order not in ['asc' ,'dsc']:
        raise HTTPException(status_code=400, detail=f"Invalid choice. Please select from {['asc','dsc']}")
    
    data = load_data()
    return sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=True if order=='dsc' else False)
  

@app.post("/create")
def create_patient(patient: Patient):
    # now i need to define a schema, what type of data will patient have.
    data = load_data()
    if patient.id in data:
        raise HTTPException(status_code=409, detail=f"Conflict, Patient {patient.id} already exists.")
    data[patient.id] = patient.model_dump(exclude='id')
    
    save_data(data)
    return JSONResponse(status_code=201, content={'message': f'Patient {patient.id} created successfully!'})
    
    
# update patient record: HTTP PUT method will be used

@app.put("/update/{patient_id}")
def update_record(patient_id:str, patient_updated_record:PatientUpdate):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f'Patient {patient_id} not found')
    
    if patient_id in data:
        existing_patient_record = data[patient_id]
        
        updated_record = patient_updated_record.model_dump(exclude_unset = True)
        
        # updating existing patient record
        for key,value in updated_record.items():
            existing_patient_record[key] = value
            
        existing_patient_record['id'] = patient_id 
        #record updated
        
        # once updated, now w eneed to pass it to Patient class for validation
        
        patient_pydantic_object = Patient(**existing_patient_record)
        patient_updated_info = patient_pydantic_object.model_dump(exclude='id')
        # exclude id, bcz id is the key.
        
        data[patient_id] = patient_updated_info
        save_data(data)
        return JSONResponse(status_code=200, content={'message':f"Patient {patient_id}'s record updated successfully."})
    

@app.delete("/delete/{patient_id}")
def delete_patient(patient_id):
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail=f'Patient {patient_id} not found.')
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200, content={'message':f'Patient {patient_id} deleted successfully.'})