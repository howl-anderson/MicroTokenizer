#!/usr/bin/env python

import os

from jinja2 import Template

current_dir = os.path.dirname(os.path.abspath(__file__ ))

input_file = os.path.join(current_dir, 'README.tpl.md')
output_file = os.path.join(os.path.dirname(current_dir), 'README.md')

readme_variable_dir = 'code'


def get_file_content(relative_file_path):
    file_path = os.path.join(current_dir, relative_file_path)

    with open(file_path) as fd:
        return fd.read()


with open(input_file, encoding='utf_8') as input_fd, open(output_file, mode='w', encoding='utf_8') as output_fd:
    template = Template(input_fd.read())

    template_variable_dict = {}

    all_files = os.listdir(readme_variable_dir)
    for file_name in all_files:
        file_name_without_ext, _ = os.path.splitext(file_name)

        file_path = os.path.join(readme_variable_dir, file_name)

        template_variable_dict[file_name_without_ext] = get_file_content(file_path)

    rendered_string = template.render(**template_variable_dict)

    output_fd.write(rendered_string)
