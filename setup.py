from setuptools import setup, find_packages


setup(
    name='bitrise',
    version='1.0.1',
    description='Python bindings for Bitrise REST API',
    author='Brandon Blair',
    author_email='cbrandon.blair@gmail.com',
    url='https://github.com/brandonblair/bitrise',
    packages=find_packages(),
    install_requires=[
        "requests>=2.18.4",
        "slimpoint>=1.0.3",
        "certifi"
        ]
)