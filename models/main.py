from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel
from typing import Optional

import json

app = FastAPI()

class Person(BaseModel):
    id: Optional[int] = None
    name: str
    age: int
    gender: str

with open('people.json', 'r') as f:
    people = json.load(f)

@app.get('/person/{p_id}')
def get_person(p_id: int):
    try:
        person = [p for p in people if p['id'] == p_id]
        if len(person) > 0:
            return Person(**person[0])
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid p_id")

@app.get("/search", status_code=200)
async def search_person(name: Optional[str] = None, age: Optional[int] = None):
    """
    Search for people based on name and/or age.

    Args:
        name (str, optional): The name to search for. Defaults to None.
        age (int, optional): The age to search for. Defaults to None.

    Returns:
        list: A list of matching people.
    """
    results = people
    if name:
        results = [p for p in results if name.lower() in p['name'].lower()]
    if age:
        results = [p for p in results if p['age'] == age]
    return [Person(**p) for p in results]

@app.post('/addPerson', status_code=201)
def add_person(person: Person):
    p_id = max([p['id'] for p in people]) + 1
    new_person = {
        "id": p_id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender
    }
    
    people.append(new_person)
    
    with open('people.json','w') as f:
        json.dump(people, f) 
        
    return new_person

@app.put('/changePerson', status_code=204)
def change_person(person: Person):
    new_person = {
        "id": person.id,
        "name": person.name,
        "age": person.age,
        "gender": person.gender
    }
    
    person_list = [p for p in people if p['id'] == person.id]
    if len(person_list) > 0:
        people.remove(person_list[0])
        people.append(new_person)
        with open('people.json', 'w') as f:
            json.dump(people, f)
        return new_person
    else:
        return HTTPException(status_code=404, detail=f"Person with id {person.id} does not exist")
    
@app.delete('/deletePerson/{p_id}', status_code=204)
def delete_person(p_id: int):
    person = [p for p in people if p['id'] == p_id]
    if len(person) > 0:
        people.remove(person[0])
        with open('people.json', 'w') as f:
            json.dump(people, f)
    else:
        raise HTTPException(status_code=404, detail=f"There is no person with id {p_id}")