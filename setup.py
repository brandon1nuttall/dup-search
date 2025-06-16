from setuptools import setup

setup(
    name='dup-search',
    version='0.1.0',
    py_modules=['dup_search'],
    install_requires=['Pillow'],
    entry_points={
        'console_scripts': [
            'dup-search=dup_search:main',
        ],
    },
    author='Your Name',
    description='A CLI tool to find duplicate images using Pillow.',
    license='MIT',
)