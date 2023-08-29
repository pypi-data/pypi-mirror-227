from setuptools import setup, find_packages

setup(
    name='example_package_abdulmughni',
    version='0.1.0',
    description='An example Python package',
    author='Abdul Mughni',
    author_email='abdulmughni100@gmail.com',
    packages=find_packages(),
    install_requires=[
    'numpy',
    'tensorflow',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)