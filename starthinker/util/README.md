# The Rest Of This Document Is Pulled From Code Comments


# Python Scripts


## [/util/__init__.py](/util/__init__.py)

Generic utilities that do not belong in any specific sub module.

Add general utility functions that are used across many modules.  Do
not add classes here.



### flag_last(o):


  Flags the last loop of an iterator.

  Consumes an iterator, buffers one instance so it can look ahead.
  Returns True on last iteration.

  Args:
    * o: An iterator instance.

  Returns:
    * A tuple of ([True/False, iteration). Returns True on StopIteration.

  

# Launch In Google Cloud

Every code sample and JSON recipe listed here is immediately available for execution using Google Cloud Shell.  The Google Cloud Shell will launch a virtual box with StarThinker code already on it.  It will also display this documentation in the Google Cloud UI.  This is ideal for using StarThinker once to execute a task.  For longer running jobs see [Recipe Corn Job](/cron/README.md) or [Deployment Script](/deploy/README.md).

[![Open in Cloud Shell](http://gstatic.com/cloudssh/images/open-btn.svg)](https://console.cloud.google.com/cloudshell/editor?cloudshell_git_repo=https%3A%2F%2Fgithub.com%2Fgoogle%2Fstarthinker&cloudshell_print=%2FLAUNCH_RECIPE.txt&cloudshell_tutorial=%2Futil%2FREADME.md)
