from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()
    

setup(
    name='pycalbi',
    version='0.0.8',
    description='This lib provides concurrent support to IntelMQ bots ',
    license='MIT',
    keywords=['python, package, distribution'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Federico Carrilao, Einar Lanfranco',
    url='https://github.com/csirtamericas/CALBI',
    packages=['pycalbi'],
    install_requires=['redis'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6'
)
