from fastapi import FastAPI
from fastapi import Path, HTTPException, Query
import json

# using Path parameters, i can enhance the readability of path parameters.

app = FastAPI()


# i have to make view interaction, when someone perform view interaction with software or website, it should show all the patients records.
# Ss, its a repeating operation, i will make a function for it.

def load_data():
    with open('patients.json', 'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def home():
    return {"message": "Patient Management System API"}


@app.get("/about")
def about():
    return {"message": "API to manage patient records."}


# i have a create a new endpoint name: view , and its route will be ('/view')
# when someone try to view, i first need to fetch the data, for that i will use load_data function that i have created now.

@app.get('/view')
def view():
    data = load_data()
    return data

# now i have to view one patient instead of all.

@app.get("/patient")
def patients():
    return view()

@app.get("/patient/{patient_id}")

def view_patient(patient_id: str=Path(..., description="ID of the patient", example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    
    raise HTTPException(status_code= 404 , detail = 'Patient not found') # now if client enters correct patient id, then ok, otherwise it will raise 404 error.
    
    # return {"error": "Patient not found"} # whenever client enter a patient id that does not exist, the program return this dictionary/json format. 
# so, there will be no error, and http request status code will be 200 that shows success. Ideally, its not true. clint is searching for a patient that does not exist , so it should return 404 error that indicates that a resource does not exist.
# so, for this we will use HTTPException. its a built in fastapi exception that raise error and show details and status code.

@app.get("/sort")
def sort_patients(sort_by: str = Query(..., description='Sort by weight, height, bmi'), order: str = Query('asc' , description='Sort in asc or dsc')):
    valid_fields = ["weight", "height", "bmi"]
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400 , detail=f'Invalid field! Select from {valid_fields}')
    
    if order not in ['asc' , 'dsc']:
        raise HTTPException(status_code=400, detail="Select valid order asc or dsc.")
    
    data = load_data()
        
    sorted_data = sorted(data.values(), key=lambda x: x.get(sort_by, 0), reverse=True if order=='dsc' else False)
    
    return sorted_data

# sort_function

# sort_by has ... , it means its required, the other parameter, order is optional, so when client do not give any value, by default we set it to ascending.

# key=lambda x: x.get(sort_by, 0) ::  x is one patient's dictionary. 
# sort_by :: the field selected by the user, the user may select weight , height, bmi 
# 0  is the default value, if there is no value exist for that field in any patient