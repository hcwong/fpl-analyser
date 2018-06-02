from distutils.core import setup

setup(
    name='FPL Analyzer',
    version='0.10dev',
    author='Joshua Wong',
    author_email='',
    packages=['fplanalyzer'],
    license='LICENSE.txt',
    description='Analyze FPL Leagues',
    install_requires=[
        "requests",
        "pylint",
        "python-dotenv"
    ],
)