#!/usr/bin/env python

import argparse
import os

from ansible.plugins.loader import module_loader, fragment_loader
from ansible.utils.plugin_docs import get_docstring

ultisnips_play = '''
snippet play
- hosts: ${1:group}
  user: ${2:root}
  tasks:
endsnippet
'''

snipmate_play = '''
snippet play
\t- hosts: ${1:group}
\t  user: ${2:root}
\t  tasks:
'''

key_orders = [
  'id',
  'name',
  'path',
  'file',
  'src',
  'dest',
  'url',
  'state',
  'mode',
  'attributes',
  'owner',
  'group',
  'validate',
  'append',
  'copy',
  'backup',
  'force',
  ]
def reorder(opts):
    _before = [_ for _ in opts if _ in key_orders]
    before = [_ for _ in key_orders if _ in _before]
    after  = sorted([_ for _ in opts if _ not in key_orders])
    return before + after
def get_comment(item):
    if 'choices' in item:
        comment_str = " # [%s]" % ('|'.join(map(str, item['choices'])),)
    elif 'type' in item:
        comment_str = " # %s" % (item['type'],)
    else:
        comment_str = ""
    return comment_str
def generate(path, args, snippets):
    doc, examples, _, _ = get_docstring(path, fragment_loader)
    prefix = args.snipmate and '\t' or ''
    l = []
    if doc is not None:
        if 'module' not in doc:
          return
        name = doc['module']
        l.append(("snippet %s" % name))
        l.append(("%s- name: ${1:task_description}" % prefix))
        l.append(("%s  %s:" % (prefix, name)))

        count = 1
        if 'options' in doc:
            options = list(doc['options'].keys())
            options = reorder(options)
            # run two loops to put required keys at top
            for opt in options:
                item = doc['options'][opt]
                comment_str = get_comment(item)
                if 'required' in item and item['required']:
                    count += 1
                    if 'default' in item:
                        value = "${%d:%s:%s}" % (count, item['default'], comment_str)
                    else:
                        value = "${%d:%s}" % (count, comment_str)
                    l.append(("%s    %s: %s" % (prefix, opt, value)))
            for opt in options:
                item = doc['options'][opt]
                comment_str = get_comment(item)
                if 'required' not in item or item['required'] is False:
                    count += 1
                    if 'default' in item and item['default']:
                        value = "${%d:%s:%s}" % (count, item['default'], comment_str)
                    else:
                        value = "${%d:%s}" % (count, comment_str)
                    l.append(("%s    #%s: %s" % (prefix, opt, value)))
            if args.ultisnips:
                l.append('endsnippet')
            l.append('\n')
    snippets.append('\n'.join(l))


def main():
    parser = argparse.ArgumentParser(prog='snippet_generator.py')
    parser.add_argument('--ultisnips', action='store_true',
                        help='Generate snippets for UltiSnips')
    parser.add_argument('--snipmate', action='store_true',
                        help='Generate snippets for snipMate')
    parser.add_argument('modpath', type=str, nargs=1,
                        help="Path to Ansible's modules")
    args = parser.parse_args()

    if args.ultisnips:
        print(ultisnips_play)
    else:
        print(snipmate_play)

    snippets = []
    for root, _, files in os.walk(args.modpath[0]):
        for name in files:
            if name.endswith('.py'):
                generate(os.path.join(root, name), args, snippets)
    print(''.join(sorted(snippets)), end='')

if __name__ == '__main__':
        main()
