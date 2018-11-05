# The Rest Of This Document Is Pulled From Code Comments

# Python Scripts


# util/__init__.py

Generic utilities that do not belong in any specific sub module.

Add general utility functions that are used across many modules.  Do
not add classes here.



### function flag_last(o):


  Flags the last loop of an iterator.

  Consumes an iterator, buffers one instance so it can look ahead.
  Returns True on last iteration.

  Args:
    o: An iterator instance.

  Returns:
    A tuple of ([True/False, iteration). Returns True on StopIteration.
  
