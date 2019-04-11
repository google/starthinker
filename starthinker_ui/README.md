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

First, install StarThinker development environment...

```
git clone https://github.com/google/starthinker
cd starthinker
source install/developer.sh --instance
Choose Option 1) Full Install
```

Second, activate environment and deploy UI...

```
source starthinker_assets/config.sh 
python starthinker_ui/manage.py makemigrations 
python starthinker_ui/manage.py migrate
python starthinker_ui/manage.py runserver localhost:8000
```

If you are using a Google Cloud machine, you will have to access http:[IP ADDRESS]:8000 in your browser.

See [Django 1.11 Configuration](https://docs.djangoproject.com/en/1.11/intro/tutorial01/) for instructions on running your first application.

# The Rest Of This Document Is Pulled From Code Comments
