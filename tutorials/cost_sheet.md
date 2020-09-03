# Operating Costs For StarThinker UI and Workers At Scale

StarThinker UI and Job Workers use Google Cloud resources in the form a database, virtual machines, and appengine.
Although we cannot provide specific guaranteed pricing due to pricing variations in your specific Google contract,
the rough cost of StarThinker UI and Job workers scales as follows...

## Data Costs

StarThinker runs jobs that transfer data.  Those jobs are connected to service accounts from Google Cloud Projects and are billed
for all data transfer independently of the Google Cloud Project where StarThinker is deployed.  We strongly discourage using the
Google Project running StarThinker as the project hosting recipe data for security and confusing cost reasons.

= **$0 - All data costs are billed to recipe owner.**

## Costs

The UI web server and database are roughly fixed in cost, for most add operations teams, these costs will be minimal.
If your database grows past 100 users or 1000 recipes or you request increased availability, your costs will vary...

- $85 [App Engine UI](https://cloud.google.com/appengine/pricing) - Monthly cost of scaled web server.
- $95 [Cloud SQL](https://cloud.google.com/appengine/pricing) - Monthly cost of backed up database.
- $1 [Cloud Storage](https://cloud.google.com/storage/pricing) - Monthly cost of storing credential data.

= **$181 / month fixed costs**

## Scaled Costs

StarThinker [autoscales the number of workers](../starthinker_ui/recipe/views.py) based on the number of pending recipe tasks.  A
[cron job](../cron.yaml) brings new workers up every 3 minutes and [workers fall of if idle](../starthinker_ui/recipe/management/commands/job_worker.py)
 for 5 minutes.  This allows the system to scale to zero workers when no recipe tasks are scheduled for that time.

Currently StarThinker uses [n1-highmem-4 instances at $0.2368 / hour](https://cloud.google.com/compute/vm-instance-pricing#n1_predefined)
 with 4 concurrent tasks per machine.  Which reduces to roughly a cost of $0.059225 / task / hour = $0.000987083333333 / task / minute.

This makes the cost proportional to the number of minutes all recipes take to execute per day. A few examples....

- Small Recipe ( move data to Bigquery from DV360 ) ~ 3 minutes x 1 per day x 30 days / month =  $0.09 per month
- Large Recipe ( CM User Audit ) ~ 45 minutes x 1 per day x 30 days / month =  $1.33 per month

Most recipes run in the 10 minute range making the median recipe cost around $0.30 per month.  Scaling that up to 4 recipes per
client at 50 clients gives an order of magnitude cost of $60 per month for a mid sized ad operations team.

= **$30 ( small ) - $60 ( medium ) - $300 ( very large ) / month scaled costs**

### Memory Scaling

For advanced tunning of costs you may adjust this value to run more or fewer jobs per virtual machine.
By default, StarThinker memory is configured by [BUFFER_SCALE inside config.py](https://github.com/google/starthinker/blob/master/starthinker/config.py).
The value multiplies all internal memory buffers, to scale StarThinker memory usage on small and large machines.
In development this is set to 1 equating roughly to 1 GB buffers, and in production it is set to 5 equating to 5 GB buffers.
Note that each module in StarThinker adjusts and caps its memory using this buffer but may limit it to lower value if necessary.


---
&copy; 2020 Google LLC - Apache License, Version 2.0
