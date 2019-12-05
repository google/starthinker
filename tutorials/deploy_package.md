# Using StarThinker As A Python Package

You can use the starthinker module directly in any python project to run a recipe. The following
example will execute two tasks in sequence in a single process.

```
pip install git+https://github.com/google/starthinker
```
```
from starthinker.util.project import project
  
if __name__ == "__main__":
  var_service = '[SERVICE CREDENTIALS JSON STRING OR PATH]'
  var_user = '[USER CREDENTIALS JSON STRING OR PATH]'
  var_cloud_id = '[GOOGLE CLOUD PROJECT ID]'
  var_recipe = {
    "setup":{
      "id":var_cloud_id
    },
    "tasks":[
      { "hello":{
        "auth":"user",
        "say":"Hello World"
      }},
      { "dataset":{
        "auth":"service",
        "dataset":"Test_Dataset"
      }}
    ]
  }

  project.initialize(_recipe=var_recipe, _user=var_user, _service=var_service, _verbose=True)
  project.execute()
```

  1. **SERVICE CREDENTIALS JSON STRING OR PATH** - Get [service credententials](cloud_service.md) 
  1. **[USER CREDENTIALS JSON STRING OR PATH]** - Optional, get [user credententials](cloud_client_installed.md) 
  1. **[GOOGLE CLOUD PROJECT ID]** - Get the Cloud Project ID fto be billed ( use the ID, not the Name, not the Number )


[![Try It In Google Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_tutorial=tutorials/deploy_package.md)

Next, review list of available tasks in the [Recipe Gallery](https://google.github.io/starthinker/code/#code-tasks) or [GIT Scripts Folder](../scripts/).

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
