from setuptools import setup, find_packages
from setuptools import  find_namespace_packages
# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='thppred',
    version='1.1',
    description='A tool for prediction of therapeutic peptides',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license_files = ('LICENSE.txt',),
    url='https://github.com/raghavagps/thppred', 
    packages=find_namespace_packages(where="src"),
    package_dir={'':'src'},
    package_data={'thppred.model':['*']},
    entry_points={ 'console_scripts' : ['thppred = thppred.python_scripts.thppred:main']},
    include_package_data=True,
    python_requires='>=3.6',
    install_requires=[
        'numpy', 'pandas',  'argparse', 'onnxruntime' # Add any Python dependencies here
    ]
)
