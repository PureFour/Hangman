import json
from app import db
from app.models import Word

with open("app/resources/animals.json", "r") as json_file:
    data = json.load(json_file)
    for p in data['animals']:
        animal = Word(name=p['word'], category='animals', description=p['description'])
        db.session.add(animal)
        db.session.commit()
