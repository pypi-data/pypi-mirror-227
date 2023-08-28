from setuptools import setup, find_packages

setup(
    name='mkproj',
    version='0.1.1',
    packages=find_packages(),
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
