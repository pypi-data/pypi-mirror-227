import os
import re
import argparse
from jinja2 import Environment, FileSystemLoader

def to_sentinel(filename):
    print(f'filename={filename}')
    # remove the file extension
    name, ext = os.path.splitext(filename)

    # replace non-alphanumeric characters with underscores
    name = re.sub(r'\W+', '_', name)
    ext = re.sub(r'\W+', '_', ext)

    # convert to uppercase
    name = name.upper()
    ext = ext.upper()

    # compose name
    name = f'__{name}{ext}__'
    return name

def create_cpp_scaffolding(project_name):
    # create project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir, exist_ok=True)

    # set up jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'cpp')
    env = Environment(loader=FileSystemLoader(template_dir))

    variables = {'project_name': project_name}

    # iterate through all files in the templates/cpp directory and its subdirectories
    for root, _dirs, files in os.walk(template_dir):
        for file in files:
            rendered_file_name = env.from_string(file).render(variables)
            variables['sentinel'] = to_sentinel(rendered_file_name)

            # get the relative path of the file
            file_path = os.path.relpath(os.path.join(root, file), template_dir)

            print(f'variables={variables}')

            # render the file name and file content
            rendered_file_path = env.from_string(file_path).render(variables)
            template = env.get_template(file_path)
            rendered_template = template.render(variables)

            # create the output file
            output_file = os.path.join(project_dir, rendered_file_path)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(rendered_template)

    print(f'C++ scaffolding for project "{project_name}" created successfully!')


def create_python_scaffolding(project_name):
    # create project directory
    project_dir = os.path.join(os.getcwd(), project_name)
    os.makedirs(project_dir, exist_ok=True)

    # set up jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), 'templates', 'python')
    env = Environment(loader=FileSystemLoader(template_dir))

    # create a dictionary with the variables
    variables = {'project_name': project_name}

    # iterate through all files in the templates/python directory and its subdirectories
    for root, dirs, files in os.walk(template_dir):
        for file in files:
            # get the relative path of the file
            file_path = os.path.relpath(os.path.join(root, file), template_dir)

            # render the file name and file content
            rendered_file_path = env.from_string(file_path).render(variables)
            template = env.get_template(file_path)
            rendered_template = template.render(variables)

            # create the output file
            output_file = os.path.join(project_dir, rendered_file_path)
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(rendered_template)

    print(f'Python scaffolding for project "{project_name}" created successfully!')

def main():
    parser = argparse.ArgumentParser(description='Create project scaffolding.')
    parser.add_argument('project_type', choices=['cpp', 'python'], help='The type of the project.')
    parser.add_argument('project_name', help='The name of the project.')
    args = parser.parse_args()

    project_type = args.project_type
    project_name = args.project_name

    if project_type == 'cpp':
        create_cpp_scaffolding(project_name)
    elif project_type == 'python':
        create_python_scaffolding(project_name)

if __name__ == '__main__':
    main()