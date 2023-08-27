from setuptools import setup

setup(
    name='geneplore_bare_api',
    version='0.2.5',
    install_requires=[
        'requests',
        'pandas',
        'tiktoken',
        'google-api-python-client',
        'google-api-core',
        'python-dotenv'
    ],
)