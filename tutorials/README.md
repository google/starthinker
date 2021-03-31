# StarThinker Tutorials

Samples and references for using the StarThinker code base. Use these to deploy and maintain
a StarThinker instance.

## Deployment

- [AppEngine](deploy_enterprise.md) - Full browser based UI with multiple user login.
- [Cloud Function](deploy_cloudfunction.md) - Serverless deployment to Google Cloud Functions.
- [AirFlow](deploy_airflow.md) - Run recipes using cloud composer / airflow framework.
- [Colab](deploy_colab.md) - For Workshops, Data Pill deployment using Google Collaboratory.
- [Developer](deploy_developer.md) - Full test suite in a local development machine.
- [Command Line](deploy_commandline.md) - Quick easy to install utility for runnning recipes.
- [PIP Package](deploy_package.md) - Use StarThinker as a Python module.

## UI

- [Running A Recipe](https://google.github.io/starthinker/help/) - How to setup and deploy a recipe using the UI.
- [Recipe Gallery](https://google.github.io/starthinker/) - List of packaged solutions.
- [Logging](logging.md) - All logs are written to StackDriver, you can build dashboards on them.
- [Testing](testing_ui.md) - How to test the UI and worker.

## Development

- [Running A Recipe](running.md) - How to execute a recipe or solution from the command line.
- [Creating A Task](task.md) - How to code up a task that can be used by scripts.
- [Creating A Recipe](recipe.md) - How to create JSON task parameters and add them to the UI.
- [Internationalization / Localization / Accessability](i18n_l10n_a11y.md) - How to test the UI and worker.
- [Command Line Helpers](helpers.md) - Utilities that speed up development at the command line.
- [Testing](testing.md) - How to test the UI, worker, and various recipes.
- [Contributing](../CONTRIBUTING.md) - How to set up a forked repository, pull, and/or contribute changes.

## Credentials

- [Cloud Project ID](cloud_project.md) - How to get cloud project ID.
- [Service Credentials](cloud_service.md) - How to get service credentials.
- [Client UI Credentials](cloud_client_web.md) - How to get client credentials ( web ).
- [Client Command Line Credentials And User Credentials](cloud_client_installed.md) - How to get client and user credentials ( other ).

## General

- [Architecture](architecture.md) - All the components of this repository explained.
- [Developer Training Resources](developer_training.md) - Relevant online training courses for developers.
- [Frequently Asked Questions](faq.md) - Common Google Cloud and StarThinker questions.
- [Useful Utilities](cheat_sheet.md) - List of common development and production commands.
- [Data Schemas](data_schemas.md) - Schemas used by various tasks.
- [Estimated Costs](cost_sheet.md) - Operating expense estimates for StarThinker UI and Workers.
- [White Label](white_label.md) - Instructions on how to re-brand StarThinker.

## Table Of Contents

- [/install](../install/) - Scripts for installing and deploying StarThinker.
- [/tutorials](../tutorials/) - Tutorials for using StarThinker code base.
- [/scripts](../scripts/) - Complete solution templates provided by Google that you can deploy.
- [/dags](../dags/) - Deploy solutions using Cloud Composer and Airflow.
- [/colabs](../colabs/) - Deploy solutions using Google Collaboratory.
- [/tests](../tests/) - Complete testing harness for all solutions provided by Google that you can use.
- [/starthinker/util](../starthinker/util/) - Low level library wrappers around Google API with helpers to handle common errors.
- [/starthinker/task](../starthinker/task/) - Handlers for each task specified in a JSON recipe.
- [/starthinker/script](../starthinker/script/) - Command line for converting a recipe template into a client specific executable recipe.
- [/starthinker/all](../starthinker/all/) - Developer command line for executing a recipe in its entirety.
- [/starthinker/cron](../starthinker/cron/) - Quick command line for executing recipes on a schedule.
- [/starthinker/auth](../starthinker/auth/) - Developer command line for testing user credential setup.
- [/starthinker_ui](../starthinker_ui/) - UI code deployed on AppEngine powered by Django.
- [/starthinker_assets](../starthinker_assets/) - Holds all configuration files when you launch StarThinker.
- [/starthinker/airflow](../starthinker/airflow/) - Factory for airflow.
- starthinker_virtualenv/ - After deploy, holds virtual environment libraries on setup.
- starthinker_database/ - After deploy, holds local development database on setup.
- starthinker_cron/ - After deploy, holds recipes executing using local cron on setup.

---
&copy; 2020 Google LLC - Apache License, Version 2.0
