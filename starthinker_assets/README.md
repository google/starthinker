# StarThinker Assets

This directory will hold all assets for a starthinker configuration.

All assets are created using:

```source starthinker/install/deploy.sh```

Assets include...

 - production.sh - all paths and cloud project variables.
 - development.sh - all paths and cloud project variables.
 - client.json - client credentials.
 - service.josn - service credentials.
 - env - virtual environment configuration.

If running developer deployment, load a StarThinker environment using:

```
source starthinker_assets/development.sh
```

For production, load a StarThinker environment using:

```
source starthinker_assets/development.sh
```

You are ready to start creating StarThinker recipes.

In production to access the database try:

psql -h localhost -d $STARTHINKER_UI_DATABSE_NAME -U $STARTHINKER_UI_DATABASE_USER

---
&copy; 2019 Google Inc. - Apache License, Version 2.0
