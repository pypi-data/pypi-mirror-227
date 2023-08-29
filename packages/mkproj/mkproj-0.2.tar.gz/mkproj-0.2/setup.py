from setuptools import setup, find_namespace_packages

setup(
    name='mkproj',
    version='0.2',
    packages=find_namespace_packages(),
    include_package_data=True,
    install_requires=[
        'jinja2',
        'argparse',
    ],
    entry_points={
        'console_scripts': [
            'mkproj=mkproj:main',
        ],
    },
    description='A tool to generate scaffolding for C++ and Python projects',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
)
