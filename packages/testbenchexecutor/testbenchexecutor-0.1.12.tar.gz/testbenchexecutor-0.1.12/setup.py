'''
Build with:
setup.py bdist_wheel
or install in editable mode with
Scripts\pip install -e path\to\testbenchexecutor
'''
from __future__ import absolute_import
from setuptools import setup

setup(
    name='testbenchexecutor',
    version='0.1.12',
    author='MetaMorph Software, Inc',
    author_email='adam.nagel@gmail.com',
    description='Executes the steps in a Test Bench manifest',
    packages=['testbenchexecutor', 'testbenchexecutor.templates', 'testbenchexecutor.progress_service', 'testbenchexecutor.progress_service.gen'],
    package_dir={'testbenchexecutor': 'testbenchexecutor'},
    package_data={'testbenchexecutor.templates': ['*.css', '*.html']},
    install_requires=[
        'python-dateutil>=2.5.0',
        'Jinja2>=2.10.0'],
    entry_points = {
        "console_scripts": [
            "testbenchexecutor = testbenchexecutor.__main__:main",
        ]
    },
    project_urls={
        'Source': 'https://github.com/metamorph-inc/testbenchexecutor',
    },
)
