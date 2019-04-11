# The Rest Of This Document Is Pulled From Code Comments


# Python Scripts


## [/task/dynamic_costs/run.py](/task/dynamic_costs/run.py)



### view_combine(name, combos_table, main_table, shadow_table):


    query = 
      SELECT
        combos.*,
        (combos.Impressions / main.Impressions) * shadow.Dbm_Cost_Account_Currency AS Scaled_Dbm_Cost_Account_Currency
      FROM `%(project)s.%(dataset)s.%(combos_table)s` combos
      JOIN `%(project)s.%(dataset)s.%(main_table)s` main
      ON combos.Placement_Id = main.Placement_Id
      JOIN `%(project)s.%(dataset)s.%(shadow_table)s` shadow
      ON STARTS_WITH(shadow.Placement, combos.Placement)
       % {
    query = 
      SELECT
        combos.*,
        (combos.Impressions / main.Impressions) * main.Dbm_Cost_Account_Currency AS Scaled_Dbm_Cost_Account_Currency
      FROM `%(project)s.%(dataset)s.%(combos_table)s` combos
      JOIN `%(project)s.%(dataset)s.%(main_table)s` main
      ON combos.Placement_Id = main.Placement_Id
       % {

# Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Ftask%2Fdynamic_costs%2FREADME.md)
