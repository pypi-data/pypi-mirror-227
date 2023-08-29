from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'ogapi.py'
LONG_DESCRIPTION = 'Mi primer paquete de Python con una descripción ligeramente más larga'

setup(
        name="ogapi_py",
        version=VERSION,
        author="amplia-iiot",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'ogapi.py', 'opengate'],
        classifiers= [
            "Programming Language :: Python",
            "Programming Language :: Python :: 3.9",
        ]
)