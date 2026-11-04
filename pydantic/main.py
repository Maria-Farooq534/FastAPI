from pydantic import BaseModel

# def insert_patient_record(name:str , age:int):
    
#     if type(name)==str and type(age)==int:
#         print(name)
#         print(age)
#         print("record inserted.")
#     else:
#         raise TypeError("Invalid data type.")
    
# insert_patient_record("Maria", '24')

# Thats the problem, we need to do a lot of code to manually do type validation and data validation. to prevent this, i will use pydantic.


# Step 1
# first create a model/class and define the schema/rules for the data

class Patient(BaseModel):
    name: str
    age: int
    

# step 2
# validate the model by creating its object

patient1 = {"name": "elon", "age": 30}
patient1_record = Patient(**patient1)
# print(patient1_record)

# step 3
# pass the object to the function

# creating function first
def insert_patient_record(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("inserted")
    

def update_patient_record(patient: Patient):
    print(patient.name)
    print(patient.age)
    print("updated")
    
    
insert_patient_record(patient1_record)
update_patient_record(patient1_record)