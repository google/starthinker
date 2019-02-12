# StarThinker UI Reference Implementation

DISCLAIMER: This is only a reference implmentation.  We strongly recommend an internal
security and privacy review before using this code in production.

## Concepts

This code sample is a sample UI wrapped around the StartThinker solution deployment
framework. It illustrates:

- Connecting a UI to the JSON templates.
- Autheticating users and storing credentials in a recipe.
- Inserting service credentials into a recipe.
- Assembling custom recipes from basic task building blocks.

## UI Technology

This sample UI is built using open source [Django Open Source Framework](https://www.djangoproject.com/).
Thank you to the Django team for developing an amazing framework.

## Running The UI

For production servers please configure using NGINX/UWSGI. DO NOT USE the development runserver
in production, it is meant as a quick local deployment only per official Django documentation.

DISCLAIMER: This is only a reference implmentation.  We strongly recommend an internal
security and privacy review before using this code in production.

For production deployment, see: https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

For a non-production reference deployment, first set up the local SQLite database.

```
python manage.py makemigrations account --settings=ui.settings_open
python manage.py makemigrations project --settings=ui.settings_open
python manage.py makemigrations recipe --settings=ui.settings_open
python manage.py makemigrations storage --settings=ui.settings_open
python manage.py makemigrations website --settings=ui.settings_open
python manage.py migrate --settings=ui.settings_open
```

Then run the non-production local server. 

```
source setup.sh
python ui/manage.py runserver localhost:8000 --settings=ui.settings_open
```

If you are using a Google Cloud machine, you will have to access http:[IP ADDRESS]:8000 in your browser.

See [Django 1.11 Configuration](https://docs.djangoproject.com/en/1.11/intro/tutorial01/) for instructions on running your first application.

# The Rest Of This Document Is Pulled From Code Comments
