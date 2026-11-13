from pydantic import BaseModel

# step 1: creating schema

class Address(BaseModel):
    city: str
    state: str
    pin: int

class Patient(BaseModel):
    name: str
    age: int
    gender: str = 'Female'
    address: Address 

address_info = {
    'city': 'Sargodha',
    'state': 'Punjab',
    'pin': 40600
}

address1 = Address(**address_info)

patient_info = {
    'name': 'Alia',
    'age': 24,
    # 'gender': 'Female',
    'address': address1
}

patient1 = Patient(**patient_info)

def insert_patient_info(patient_info):
    print(f"Patient info: {patient_info}")    

insert_patient_info(patient1)
insert_patient_info(patient1.address)
insert_patient_info(patient1.address.city)

# model_dump() : it converts existing pydantic model object into a dictionary.

info = patient1.model_dump()
print(info)
print(type(info))

# we can specify the fields we have to export.

info = patient1.model_dump(include=['name', 'age'])
print(info)

# to exclude some/any field
info = patient1.model_dump(exclude=['name', 'age'])
print(info)

# to exclude anything from address
info = patient1.model_dump(exclude={'address':['state']})
print(info)

# exclude_unset=True, when used, it will export only the fields given. for example, let say gender has default value Female,and we dont give a value to gender field , by defult it will hav male. which is wrong. so , when exporting data, we dont want to export it, so we will use exclude_unset = True. it will export only the fields provided. 

info = patient1.model_dump(exclude_unset=True)
print(info)

# for json: model_dump_json()

json_info = patient1.model_dump_json()
print(json_info)
print(type(json_info))