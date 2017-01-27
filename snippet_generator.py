#!/usr/bin/env python2

import argparse
from ansible.utils.module_docs import get_docstring
import os
import sys

ultisnips_play = '''
snippet play
- hosts: ${1:group}
  user: ${2:root}
  tasks:
endsnippet
'''

snipmate_play = '''
snippet play
- hosts: ${1:group}
  user: ${2:root}
  tasks:
'''

def generate(path, args):
    doc, examples, _ = get_docstring(path)
    prefix = args.snipmate and '\t' or ''
    if doc != None:
        print "snippet %s" % doc['module']
        print "%s- name: ${1:task_description}" % prefix
        print "%s  %s: " % (prefix, doc['module'])

        count = 1
        if 'options' in doc:
            for opt in doc['options']:
                count += 1
                optional = not doc['options'][opt].get('required', False)
                if 'default' in  doc['options'][opt]:
                    value = "${%d:%s}" % (count, doc['options'][opt]['default'])
                else:
                    value = "${%d}" % (count)
                print "%s    %s%s: %s" % (prefix, optional and '#' or '', opt, value)
            if args.ultisnips:
                print 'endsnippet'
            print


def main():
    parser = argparse.ArgumentParser(prog='snippet_generator.py')
    parser.add_argument('--ultisnips', action='store_true',
    	help='Generate snippets for UltiSnips')
    parser.add_argument('--snipmate', action='store_true',
    	help='Generate snippets for snipMate')
    parser.add_argument('modpath', type=str, nargs=1,
        help="Path to Ansible's modules, i.e.:/<ansible_source>/lib/ansible/modules")
    args = parser.parse_args()

    for root, _, files in os.walk(args.modpath[0]):
        for name in files:
            if name.endswith('.py'):
                generate(os.path.join(root, name), args)

if __name__ == '__main__':
        main()
