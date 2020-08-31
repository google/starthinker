# Development

Collection of commands to develop StarThinker in a local environment.

## Running Recipe Tests

```
git clone https://github.com/google/starthinker
cd starthinker
source install/deploy.sh
1) Dveloper Menu
4) Test Tasks
```

## Running UI / Worker Tests

```
git clone https://github.com/google/starthinker
cd starthinker
source install/deploy.sh
1) Dveloper Menu
3) Test UI
```

## Executing UI and Worker Locally

```
git clone https://github.com/google/starthinker
cd starthinker
source install/deploy.sh
1) Dveloper Menu
2) Test UI
```

In another terminal:

```
cd starthinker
source starthinker_assets/development.sh
python starthinker
python starthinker_ui/manage.py job_worker --jobs=1 --test --verbose
```

## Process For Debuging UI Recipes

### Get Recipe Status

Must be logged into one of the worker machines.

```
cd /home/starthinker
source starthinker_assets/development.sh
python starthinker_ui/manage.py recipe_status --recipe 116
```

### Get Recipe JSON And Run It Locally

Must be logged into one of the worker machines.

CAUTION: This has user credentials in it.
CAUTION: UI Machine is set to use low memory buffers, recipes will take a long time to run locally.

```
cd /home/starthinker
source starthinker_assets/development.sh
python starthinker_ui/manage.py recipe_to_json --recipe 116
python starthinker/all/run.py /home/starthinker/starthinker_cron/recipe_116.json
```

### Force Run A Recipe On Workers

Must be logged into one of the worker machines.

CAUTION: This removes all schedule from recipe and executes tasks sequentially.

```
cd /home/starthinker
source starthinker_assets/development.sh
python starthinker_ui/manage.py recipe_to_json --recipe 116 --remote --force
```

# Production

Collection of commands to manage production UI, workers, and database.

## Updating Production Database

```
cd /home/starthinker
git pull
source install/deploy.sh
3) Enterprise Menu
5) Migrate Database
```

## Logging Into Production Database

```
psql starthinker-ui --port 5432 --host=127.0.0.1 --user starthinker
```

## Updating UI And Workers

All code is pulled from the current working ST directory and copied to AppEngine and VM.

```
cd /home/starthinker
git pull
source install/deploy.sh
3) Enterprise Menu
1) Deploy UI
```
