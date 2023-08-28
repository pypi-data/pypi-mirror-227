from setuptools import setup, find_packages

setup(
    name='mkproj',
    version='0.1',
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
)
