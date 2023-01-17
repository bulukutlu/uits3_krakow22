from distutils.core import setup
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    author_email='berkin.ulukutlu@cern.ch',
    author='Berkin Ulukutlu',
    url='https://github.com/bulukutlu/uits3_krakow22',
    name='uits3_krakow22',
    version='v0.1', 
    packages=setuptools.find_packages(),
    license='MIT License',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=False,
    package_data={
    '': ['../*/*/*/*.ts']
    },
    install_requires=[
        'numpy',
        'pandas',
        ##---------------------   graphics  dependencies
        # ----------------------   jupyter notebook dependencies
        'ipywidgets',
        'runtime',
        'requests',
        "notebook>=6.4.10"
        "jupyter_contrib_nbextensions"
    ]
)