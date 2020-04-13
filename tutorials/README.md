# StarThinker Tutorials

Samples and references for using the StarThinker code base. Use these to deploy and maintain 
a StarThinker instance.

## Deployment

- [Enterprise](deploy_enterprise.md) - Full browser based UI with multiple user login.
- [AirFlow](deploy_airflow.md) - Run recipes usng cloud compoer / airflow framework.
- [Colab](deploy_colab.md) - For Workshops, Data Pill deployment using Google Collaboratory.
- [Developer](deploy_developer.md) - Command line recipe creation, editing, and testing.
- [Package](deploy_package.md) - Use StarThinker as a library.

## UI

- [Running A Recipe](https://google.github.io/starthinker/help/) - How to set up and deploy a recipe using the UI.
- [Recipe Gallery](https://google.github.io/starthinker/) - List of packaged solutions. 
- [Logging](logging.md) - All logs are written to StackDriver, you can build dashboards on them.
- [Testing](testing_ui.md) - How to test the UI and worker.

## Development

- [Running A Recipe](running.md) - How to execute a recipe or solution from the command line.
- [Creating A Task](task.md) - How to code up a task that can be used by scripts.
- [Creating A Recipe](recipe.md) - How to create JSON task parameters and add them to the UI.
- [Command Line Helpers](helpers.md) - Utilities that speed up development at the command line.
- [Testing](testing.md) - How to test the UI, worker, and various recipes.

## Credentials

- [Cloud Project ID](cloud_project.md) - How to get cloud project ID.
- [Service Credentials](cloud_service.md) - How to get service credentials.
- [Client UI Credentials](cloud_client_web.md) - How to get client credentials ( web ).
- [Client Command Line Credentials And User Credentials](cloud_client_installed.md) - How to get client and user credentials ( other ).

## General

- [Architecture](architecture.md) - All the components of this repository explained.
- [Frequently Asked Questions](faq.md) - Common Google Cloud and StarThinker questions.
- [Useful Utilities](cheat_sheet.md) - List of common development and production commands.
- [Data Schemas](data_schemas.md) - Schemas used by various tasks.
- [Estimated Costs](cost_sheet.md) - Operating expense estimates for StarThinker UI and Workers.

---
&copy; 2020 Google LLC - Apache License, Version 2.0
