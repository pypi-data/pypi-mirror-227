from setuptools import setup, find_packages

setup(
    name="PRomancer",
    version="0.23.1",
    packages=find_packages(),
    install_requires=[
        'openai>=0.0,<1.0',
    ],
    entry_points={
        'console_scripts': [
            'promancer=src.main:main'
        ]
    }
)
