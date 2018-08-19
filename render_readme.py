#!/usr/bin/env python

import os

from jinja2 import Template

current_dir = os.path.dirname(os.path.abspath(__file__))

input_file = os.path.join(current_dir, 'README.tpl.md')
output_file = os.path.join(current_dir, 'README.md')


def get_file_content(relative_file_path):
    file_path = os.path.join(current_dir, relative_file_path)

    with open(file_path) as fd:
        return fd.read()


with open(input_file, encoding='utf_8') as input_fd, open(output_file, mode='w', encoding='utf_8') as output_fd:
    template = Template(input_fd.read())

    simple_usage_code = get_file_content('code_used_in_README/simple_usage.py')
    export_graphml_code = get_file_content('code_used_in_README/export_graphml.py')

    rendered_string = template.render(
        simple_usage_code=simple_usage_code,
        export_graphml_code=export_graphml_code
    )

    output_fd.write(rendered_string)
