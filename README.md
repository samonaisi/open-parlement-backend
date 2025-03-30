# open-parlement API

## Usage

### Clone the repository

```bash
git clone git@github.com:samonaisi/open-parlement-backend.git
cd open-parlement
```


### Create and populate your .env file

```bash
cp .env.example .env
```

### Run the stack

```bash
docker compose up
```

**Get a shell access to the backend container**
```bash
make bash
```

**Setup the backend**
```bash
python manage.py migrate
python manage.py collectstatic
python manage.py compilemessages
```
