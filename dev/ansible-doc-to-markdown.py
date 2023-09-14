#!/usr/bin/env python3

# Copyright 2023, Jonathan Kamens <jik@kamens.us>.
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

'''Convert output of ansible-doc --json into decent-looking markdown'''

import argparse
import json
import re
from textwrap import indent, wrap


def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert output of ansible-doc --json into decent-looking '
        'markdown')
    parser.add_argument('inputfile', nargs='?', type=argparse.FileType('r'),
                        help='Output of ansible-doc --json (default stdin)')
    parser.add_argument('outputfile', nargs='?', type=argparse.FileType('w'),
                        help='Where to put Markdown output (default stdout)')
    return parser.parse_args()


def main():
    args = parse_args()
    for name, docs in json.load(args.inputfile).items():
        convert_doc(args, name, docs)


def convert_doc(args, name, docs):
    def fprint(*msg):
        print(*msg, file=args.outputfile)

    fprint(f'# {markdown_quote(name)} Ansible module -- '
          f'{markdown_quote(docs["doc"]["short_description"])}\n')

    for paragraph in docs['doc']['description']:
        fprint('\n'.join(wrap(markdown_quote(paragraph))), "\n")

    print('## Requirements\n')
    for req in docs['doc']['requirements']:
        fprint('\n'.join(wrap(markdown_quote(req), initial_indent='- ',
                             subsequent_indent='  ')))
    fprint('')

    fprint('## Options\n')
    for name, params in docs['doc']['options'].items():
        constraints = []
        _type = params['type']
        if _type == 'list':
            _type += ' of ' + params['elements']
        constraints.append(_type)

        if 'choices' in params:
            constraints.append('one of ' + ', '.join(
                f'"{markdown_quote(c)}"' for c in params['choices']))

        text = f'**{name} [{", ".join(constraints)}]** -- {markdown_quote(params["description"])}'
        fprint('\n'.join(wrap(text, initial_indent='- ',
                              subsequent_indent='  ')))
    fprint('')

    if docs.get('return', None):
        fprint('## Return values\n')

        for name, params in docs['return'].items():
            constraints = []
            _type = params['type']
            if _type == 'list':
                _type += ' of ' + params['elements']
            constraints.append(_type)

            text = (f'**{name} [{", ".join(constraints)}]** -- '
                    f'{markdown_quote(params["description"])}')
            fprint('\n'.join(wrap(text, initial_indent='- ',
                                  subsequent_indent='  ')))

            if params.get('returned', None):
                fprint('\n'.join(
                    wrap(markdown_quote(f'Returned {params["returned"]}'),
                         initial_indent='  - ', subsequent_indent=('    '))))

            if params.get('sample', None):
                fprint('\n'.join(
                    wrap(markdown_quote(f'Example: {params["sample"]}'),
                         initial_indent='  - ', subsequent_indent=('    '))))
        fprint('')

    if docs.get('examples', None):
        fprint('## Examples\n')

        fprint(indent(docs['examples'].strip(), '    '))
        fprint('')

    if docs['doc'].get('author', None):
        fprint('## Author\n')
        for author in docs['doc']['author']:
            fprint(f'- {markdown_quote(author)}')
        fprint('')


def markdown_quote(text):
    fragments = re.split(r'C\(([^\)]*)\)', text)
    text = quote_fragment(fragments.pop(0))
    while fragments:
        text += f'`{fragments.pop(0)}`'
        text += quote_fragment(fragments.pop(0))
    return text


def quote_fragment(text):
    return text.replace('_', '\\_')


if __name__ == '__main__':
    main()
