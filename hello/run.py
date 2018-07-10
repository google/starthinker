###########################################################################
#
#  Copyright 2017 Google Inc.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
###########################################################################

import pprint
from util.project import project 

def hello():
  if project.verbose: print 'HELLO'

  print ''
  print '-' * 80
  print "Tasks are just python, you can do whatever."
  print "This is a task being executed."
  print ''
  print 'SAY:', project.task['say']
  print ''
  print ''

  print '-' * 80
  print "Every task automatically gets a date parameter."
  print "The parameter can be passed in, or defaults to today."
  print ''
  print 'PROJECT DATE:', project.date
  print ''
  print ''

  print '-' * 80
  print "Most tasks operate on top of Google Cloud infrastructure." 
  print "Every task specifies an 'auth' parameter as 'user' or 'service'."
  print "Every project has its own credentails paths."
  print "If you provide 'client' credentials, the 'user' credentials will be populated as necessary."
  print "If you provde the 'user' credentails, the 'client' credentials are not necessary."
  print "If you use the 'service' credentials, you must add them manually." 
  print ''
  print 'PROJECT ID:', project.id
  print 'PROJECT CLIENT CREDENTIALS:', project.configuration['setup']['auth']['client']
  print 'PROJECT USER CREDENTIALS:', project.configuration['setup']['auth']['user']
  print 'PROJECT SERVICE CREDENTIALS:', project.configuration['setup']['auth']['service']
  print ''
  print ''

  print '-' * 80
  print "Your entire project definition is accessible as a dictionary."
  print "The task name must match a directory with a run.py inside it."
  print "For example, 'hello' is a task which will executed by 'hello/run.py'."
  print ''
  print 'PROJECT JSON:'
  pprint.PrettyPrinter(depth=20).pprint(project.configuration)
  print ''
  print ''

  print '-' * 80
  print "Each task is passed a nested subset of json."
  print "Different tasks should NOT share json. Security and readability reasons."
  print "Each task can execute as a service or a user independently."
  print "Access structure data within a task as..."
  print ''
  print 'PROJECT TASK:', project.task
  print 'PROJECT TASK AUTH:', project.task['auth']
  print 'PROJECT TASK SAY:', project.task['say']
  print ''
  print ''

  print '-' * 80
  print "Take a look inside 'hello/run.py'."
  print "Its a great skeleton for your first project."
  print ''
  print ''

if __name__ == "__main__":
  project.load('hello')
  hello()
