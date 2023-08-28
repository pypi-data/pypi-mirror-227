from setuptools import find_packages, setup

setup(
    name='django-custom-user-auth',
    version='1.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django==4.2.2',
        'djangorestframework==3.14.0',
    ],
)
