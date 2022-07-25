from setuptools import find_packages, setup


setup(
    name='flaskr',
    version='1.0.0',
    packages=find_packages(),  # Finds these directories automatically
    include_package_data=True,  # To include other files such as static and templates directory
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)
