# Operating Costs For StarThinker UI and Workers At Scale 

StarThinker UI and Job Workers use Google Cloud resources in the form a database, virtual machines, and appengine.
Althought we cannot provide specific guranteed pricing due to pricing variations in your specific Google contract,
the rough cost of StarThinker UI and Job workers scales as follows...

## Data Costs

StarThinker runs jobs that transfer data.  Those jobs are connected to service accounts from Google Cloud Projects and are billed
for all data transfer independently of the Google CLoud Project where StarThinker is deployed.  We strongly discourage using the
Google Project running StarThinker as the project hosting recipe data for security and confusing cost reasosns.

= **$0 - All data costs are billed to recipe owner.**

## Fixed Costs 

The UI web server and database are roughly fixed in cost, for most trading desks or client deployments, these costs will be minimal.
If your databse grows or you request increased availability, your costs will vary...

$85 [App Engine UI](https://cloud.google.com/appengine/pricing) - Monthly cost of scaled web server.  
$95 [Cloud SQL](https://cloud.google.com/appengine/pricing) - Monthly cost of backed up database.
$1 [Cloud Storage](https://cloud.google.com/storage/pricing) - Monthly cost of storing credential data.

= **$180 / month total fixed costs**

## Scaled Costs

StarThinker requires more Job Workers as the number of recipes increases.  The number of recipes increases as the number of users increases.

### Job Resource Use

StarThinker executes jobs that consume both memory and time.  A single recipe may execute several jobs in series,
and several recipes may execute jobs in parallel.  Thus choosing the number of workers depends on both the length
of the average job, as well as the number of concurrent recipes scheduled by users.

### Memory Scaling

By default, StarThinker memory is configured by [BUFFER_SCALE inside config.py](https://github.com/google/starthinker/blob/master/starthinker/config.py).
The value multiplies all internal memory buffers, to scale StarThinker memory usage on small and large machines.
In development this is set to 1 equating roughly to 1 GB buffers, and in production it is set to 5 equating to 5 GB buffers.
Note that each module in StarThinker adjusts and caps its memory using this buffer but may limit it to lower value if necessary.
For advanced tunning of costs you may adjust this value to run more or fewer jobs per virtual machine.

### Machine Scaling

On Google Cloud StarThinker deploys with BUFFER_SCALE=5, allowing 5 GB for upload and another 5 GB download for a total of 10 GB memory per job. With
the instances chosen, thats 2 jobs on the n1-highmem-4 ( 26 GB ) machines, and 4 jobs on n1-highmem-8 ( 52 GB ) machines.  You can adjust the
[BUFFER_SCALE inside config.py](https://github.com/google/starthinker/blob/master/starthinker/config.py) and 
[Worker Deployment Script](https://github.com/google/starthinker/blob/master/install/worker.sh#L293) to tune this for your needs.

### Time Scaling

Conservitvely, if the average job takes 6 minutes, and the average recipe has 10 jobs, then each job handler on a machine can execute 24 recipes in a day.
Thus, a machine with two job handlers can execute 48 recipes, and so on. Your pricing for [Google Virtual Machines](https://cloud.google.com/compute/docs/machine-types) may vary...

$37 / month at 1   - 50 Recipes  = 1 x n1-highmem-4 x 2 jobs = 48 recipe hours  
$73 / month at 50  - 100 Recipes = 2 x n1-highmem-4 x 2 jobs = 96 recipe hours  
$110 / month at 100 - 200 Recipes = 3 x n1-highmem-4 x 2 jobs = 144 recipe hours  
$146 / month at 200 - 300 Recipes = 4 x n1-highmem-4 x 2 jobs = 192 recipe hours  
$182 / month at 300 - 400 Recipes = 5 x n1-highmem-4 x 2 jobs = 240 recipe hours  
$292 / month at 400 - 500 Recipes = 4 x n1-highmem-8 x 3 jobs = 288 recipe hours  
$365 / month at 500 - 600 Recipes = 5 x n1-highmem-8 x 3 jobs = 360 recipe hours  
$438 / month at 600 - 700 Recipes = 6 x n1-highmem-8 x 3 jobs = 432 recipe hours

**$37 - $438 / month scaled worker costs**

For most installs we recommend at least two machines running 2 jobs each.  In practice, most jobs take seconds to execute, at Google we have run 1,000
recipes per day for hundreds of users from 4 machines with 2 jobs each.

## Signs You Need To Increase Workers

- Users are waiting 3 minutes or more for their recipe to run when using "Run Now".
- Not all your jobs finish at the end of the day, see [logging](logging.md).

---
&copy; 2020 Google Inc. - Apache License, Version 2.0
