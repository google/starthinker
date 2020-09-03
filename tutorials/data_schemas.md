# List Of StarThinker Schema Definitions

Various StarThinker recipies use schemas to ensure data transfered into BigQuery or another database is stable.
This document gives a collective summary of most

### Why you should be using explicit schemas in all data moves...

Defining a schema explicitly removes ambiguity and flags errors early preventing down stream time sinks.  Data can change,
a column of NULLs can be and INTEGER or a STRING, but your down stream formula can only SUM one of them.

## List Of Schemas As Python Dictionaries
- [Campaign Manager - Report And DT Schema](https://github.com/google/starthinker/tree/master/starthinker/task/dt/schema) - Used by [dt](https://github.com/google/starthinker/tree/master/starthinker/task/dt) and [dcm](https://github.com/google/starthinker/tree/master/starthinker/task/dcm) task.
- [Campaign Manager - List Schema](https://github.com/google/starthinker/tree/master/starthinker/task/dcm_api/schema) - Used by [dcm_api](https://github.com/google/starthinker/tree/master/starthinker/task/dcm_api) task.
- [DV360 - Entity Read Schema](https://github.com/google/starthinker/tree/master/starthinker/task/entity/schema)- Used by [entity](https://github.com/google/starthinker/tree/master/starthinker/task/entity) task.
- [DV360 - SDF Files](https://github.com/google/starthinker/tree/master/starthinker/util/dcm/schema) - Used by [sdf](https://github.com/google/starthinker/tree/master/starthinker/task/sdf) task.

---
&copy; 2020 Google Inc. - Apache License, Version 2.0
