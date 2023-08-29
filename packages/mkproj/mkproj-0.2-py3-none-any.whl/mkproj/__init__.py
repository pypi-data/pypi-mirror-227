import os
import re
import argparse
from jinja2 import Environment, FileSystemLoader

def to_sentinel(filename):
    # print(f'filename={filename}')
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

def render(template_dir, variables):
    # create project directory
    # project_dir = os.path.join(os.getcwd(), variables['project_name'])
    # os.makedirs(project_dir, exist_ok=True)

    # set up jinja2 environment
    template_dir = os.path.join(os.path.dirname(__file__), template_dir)
    env = Environment(loader=FileSystemLoader(template_dir))

    # iterate through all files in the templates/cpp directory and its subdirectories
    for root, _dirs, files in os.walk(template_dir):
        for file in files:
            # get the relative path of the file
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, template_dir)

            if '__pycache__' in rel_path:
                continue

            rendered_file_name = env.from_string(file).render(variables)
            variables['sentinel'] = to_sentinel(rendered_file_name)

            # print(f'rel_path={rel_path}')

            file_permissions = os.stat(full_path).st_mode

            # print(f'variables={variables}')

            # render the file name and file content
            rendered_rel_path = env.from_string(rel_path).render(variables)
            template = env.get_template(rel_path)
            rendered_template = template.render(variables)

            # create the output file
            # output_file = os.path.join(project_dir, rendered_rel_path)
            output_file = rendered_rel_path
            output_dir = os.path.dirname(output_file)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)
            with open(output_file, 'w') as f:
                f.write(rendered_template)

            os.chmod(output_file, file_permissions)


def create_scaffolding(project_name, project_type):
    variables = {
        'project_name': project_name,
        'project_type': project_type,
    }
    render(f"templates/{project_type}", variables)
    print(f'Project "{project_name}" created successfully!')

def main():
    parser = argparse.ArgumentParser(description='Create project scaffolding.')
    parser.add_argument('project_type', choices=['cpp', 'python', 'bash'], help='The type of the project.')
    parser.add_argument('project_name', help='The name of the project.')
    args = parser.parse_args()

    project_type = args.project_type
    project_name = args.project_name

    create_scaffolding(project_name, project_type)

if __name__ == '__main__':
    main()