# ansible_snippet_generator

A small script to generate snipmate.vim and UltiSnips Ansible snippets.

## Requierements

- [Ansible source](http://github.com/ansible/ansible)
- [snipmate.vim](http://github.com/msanders/snipmate.vim) or [ultisnips](http://github.com/SirVer/ultisnips)
- PyYAML

## Run

```
source ~/ansible/lib/hacking/env-setup

./snippet_generator.py --ultisnips ~/ansible/lib/ansible/modules > ~/.vim/snippets/UltiSnips/yaml.snippets
```

## Credits

Forked from [bleader/ansible_snippet_generator](https://github.com/bleader/ansible_snippet_generator)
