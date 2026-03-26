from setuptools import setup, find_packages

setup(
    name="lms-bot",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'lms-bot = bot:main',
        ],
    },
)
