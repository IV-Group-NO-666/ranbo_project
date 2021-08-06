# ranbo_project

**Ranbo** is a social media platform for incredible insights.

## How to run

Follow the next steps to run **Ranbo**:

```bash
# remove database file if exists
rm -f db.sqlite3

# make migration
python manage.py makemigrations ranbo

# migrate
python manage.py migrate

# populate data
python population_script.py

# run server
python manage.py runserver
```

## How to test

Follow the next steps to run **tests**:

```bash
python manage.py test tests_model
```

## License

`ranbo-project` is licensed under the terms of the MIT license.
