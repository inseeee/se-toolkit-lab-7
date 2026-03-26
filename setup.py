from setuptools import setup

setup(
    name="lms-bot",
    version="0.1",
    py_modules=["bot"],
    entry_points={
        'console_scripts': [
            'lms-bot = bot:main',
        ],
    },
)
