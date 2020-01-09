import json
from app import db
from app.models import Word

with open("app/resources/animals.json", "r") as json_file:
    data = json.load(json_file)
    for p in data['animals']:
        exist = Word.query.filter_by(name=p['word']).first()
        if not exist:
            animal = Word(name=p['word'], category='animals', description=p['description'])
            db.session.add(animal)
            db.session.commit()

with open("app/resources/countries.json", "r") as json_file:
    data = json.load(json_file)
    for p in data['countries']:
        exist = Word.query.filter_by(name=p['word']).first()
        if not exist:
            country = Word(name=p['word'], category='countries', img=p['img'])
            db.session.add(country)
            db.session.commit()

with open("app/resources/sport.json", "r") as json_file:
    data = json.load(json_file)
    for p in data['sport']:
        exist = Word.query.filter_by(name=p['word']).first()
        if not exist:
            country = Word(name=p['word'], category='sport', img=p['img'])
            db.session.add(country)
            db.session.commit()     