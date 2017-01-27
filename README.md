# ansible_snippet_generator

A small script to generate snipmate.vim and UltiSnips Ansible snippets.

## Requierements

- [Ansible source](/ansible/ansible)
- [snipmate.vim](/msanders/snipmate.vim) or [ultisnips](/SirVer/ultisnips)

## Run

```
./ansible_snippet_generator.py --ultisnips ~/ansible/lib/ansible/modules > ~/.vim/snippets/UltiSnips/yaml.snippets
```

## Credits

Forked from [bleader/ansible_snippet_generator](/bleader/ansible_snippet_generator)
