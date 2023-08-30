from setuptools import setup, find_packages

setup(
    name='MachineFailure',
    version='0.0.1',
    description='Random Forest model to predict machine failure',
    author='Kishore',
    packages=find_packages(),
    package_data={'': ['*.pkl']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)