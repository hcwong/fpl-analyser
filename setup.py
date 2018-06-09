from distutils.core import setup

setup(
    name='fplanalyzer',
    version='0.20dev',
    author='Joshua Wong',
    author_email='',
    packages=['fplanalyzer'],
    license='LICENSE.txt',
    description='See your FPL league in graphs',
    install_requires=[
        "requests",
        "pylint",
        "python-dotenv"
        "pandas",
        "matplotlib"
    ],
)