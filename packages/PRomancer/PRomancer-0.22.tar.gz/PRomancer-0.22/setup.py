from setuptools import setup, find_packages

setup(
    name="PRomancer",
    version="0.22",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        'openai>=0.0,<1.0',
    ],
    entry_points={
        'console_scripts': [
            'promancer = main:main'
        ]
    },
)
