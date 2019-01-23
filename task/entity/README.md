# The Rest Of This Document Is Pulled From Code Comments

### Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=LAUNCH_RECIPE.txt&cloudshell_tutorial=task%2Fentity%2FREADME.md)


# Python Scripts


## [/task/entity/run.py](/task/entity/run.py)

Script that executes { "entity":{...}} task.

This script translates JSON instructions into operations on Entity Read File
transfer to BigQuery.  

### CAUTION 

ONLY PARTNER LEVEL LOG FILES ARE MOVED, no advertiser filters in 
this script. To filter by advertiser, add queries within BigQuery to create
additional tables.

See: https://developers.google.com/bid-manager/guides/entity-read/format-v2

### Table Names And Entities

The prefix value specified in JSON is used to name each table and avoid 
collisions.  All tables will be prefixed with "Entity_" by default. For
example 'Campaign' Entity Read becomes, 'Entity_Campaign'. You can
modify the preifx in the JSON script.

The following Entity Read Files Can Be Specified:

- Campaign 
- LineItem
- Creative
- UserList
- Partner
- Advertiser
- InsertionOrder
- Pixel
- InventorySource
- CustomAffinity
- UniversalChannel
- UniversalSite
- SupportedExchange
- DataPartner
- GeoLocation
- Language
- DeviceCriteria
- Browser
- Isp

### Notes

- Files are moved using an in memory buffer, controlled by BUFFER_SCALE in setup.py. 
- Bigger buffer means faster move but needs a machine with more memory.
- These transfers take a long time, two jobs can write over each other.
- The tables are filled over time, if you need instant data switch, use table copy after job.


