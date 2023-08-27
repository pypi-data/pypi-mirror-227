from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Pattern expression'
LONG_DESCRIPTION = 'A pattern expression package'

# Setting up
setup(
       
        name="patex", 
        version=VERSION,
        author="Aidin T.",
        author_email="at.aidin@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)