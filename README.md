# Spy Cats 

**Spy Cats** is a REST API for managing spy missions, targets and agents (cats). The project was created on the Django REST Framework.

---

##  Functional

1. **Managing agents (cats)**:
 - Add, update, delete and view agent data.
 - Updating the agent's salary.

2. **Goal management**:
 - Add, update, delete and view target data.

3. **Mission management**:
 - Added mission with binding to agent and objectives.
 - Update mission status and objectives.
 - Assigning an agent to a mission.

---

## Technologies

- Python 
- Django 
- Django REST Framework
- SQLite

---

## Installation and launch

### **Repository cloning**
```bash
git clone https://github.com/Rygos/spycats.git
cd spycats
```

## virtual enviroment creation
```bash
python -m venv venv
source venv/bin/activate # Linux/Mac
venv\Scripts\activate    # Windows
```

## modules installation 
```bash
pip install -r requirements.txt
```

## Make migrations 
```bash
python manage.py makemigrations
python manage.py migrate
```

## Run server
```bash
python manage.py runserver
```

Postman tests you can check in SpyCats.postman_collection.json
or here https://ua.files.fm/u/nqyb7e9nap
