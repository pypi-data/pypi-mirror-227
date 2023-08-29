from setuptools import setup, find_namespace_packages

setup(
    name='{{ project_name }}',
    version='0.1',
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=[
        'jinja2',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            '{{ project_name }}={{ project_name }}:main',
        ],
    },
    description='{{ project_name }}',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
