#!/usr/bin/env python2

from ansible.utils.module_docs import get_docstring
import os
import sys

modpath = os.environ["ANSIBLE_MODULE_PATH"]

def generate(path):
    doc, examples, _ = get_docstring(path)
    if doc != None:
        print "snippet %s" % doc['module']
        print "- name: ${1:task_description}"
        print "  %s: " % doc['module']

        if 'options' in doc:
            count = 1
            for opt in doc['options']:
                count += 1
                if 'required' in doc['options'][opt] and doc['options'][opt]['required']:
                    if 'default' in  doc['options'][opt]:
                        value = "${%d:%s}" % (count, doc['options'][opt]['default'])
                    else:
                        value = "${%d}" % (count)
                    print "    %s: %s" % (opt, value)

            for opt in doc['options']:
                if not 'required' in doc['options'][opt] or doc['options'][opt]['required'] == False:
                    count += 1
                    if 'default' in doc['options'][opt] and doc['options'][opt]['default']:
                        value = "${%d:%s}" % (count, doc['options'][opt]['default'])
                    else:
                        value = "${%d}" % (count)
                    print "    #%s: %s" % (opt, value)
                print 'endsnippet'
                print

print '''
snippet play
- hosts: ${1:group}
  user: ${2:root}
  tasks:
endsnippet
'''

for root, _, files in os.walk(modpath):
    for name in files:
        if name.endswith('.py'):
            generate(os.path.join(root, name))
