
from setuptools import setup, find_packages

# this is to be used locally by the dev, and not from the module
from long_description import LONG_DESCRIPTION

from rewrite_readme import rewrite_readme

VERSION = '0.0.3' 

DESCRIPTION = 'Simple tools to practice with opencv on VScode in place of Jupyter Notebooks.'

rewrite_readme()

# Setting up
setup(
        name="sottopoco_vscode", 
        version=VERSION,
        author="tms1991",
        author_email="<youremail@email.com>",
        description=DESCRIPTION,
        long_description_content_type='text/markdown',
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["numpy", "opencv-python", "matplotlib"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['opencv', 'vscode'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)

# deploy
#--------

# python setup.py sdist bdist_wheel

# twine upload dist/sottopoco_vscode-0.0.0*
# __token__
# api key

# pip install sottopoco_vscode==0.0.0*