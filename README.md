## PROJECT AKY WITH DJANGO

# How to setup the project ?

- Clone the repository
- Create a virtual environment

```bash
python3 -m venv env
```

- Activate virtual environment

```bash
source env/bin/activate
```

- Install the requirements packages

```bash
pip3 install -r requirements.txt
```

- Sync database

```bash
python3 manage.py migrate
```

- Create admin user with the command below with username, password and email

```bash
python3 manage.py createsuperuser
```

# How to run the project ?

```bash
python3 manage.py runserver
```