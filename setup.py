from setuptools import setup, find_packages

setup(
    name='dup-search',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['Pillow'],
    entry_points={
        'console_scripts': [
            'dup-search=dup_search.main:main',
        ],
    },
    author='Your Name',
    description='A CLI tool to find duplicate images using Pillow.',
    license='MIT',
)