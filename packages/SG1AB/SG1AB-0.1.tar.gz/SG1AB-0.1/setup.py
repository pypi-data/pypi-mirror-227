from setuptools import setup, Extension
import pybind11

module = Extension(
    'SG1AB',
    sources=['SG1AB.cpp'],
    include_dirs=[pybind11.get_include()]
)

setup(
    name='SG1AB',
    version='0.1',
    description='My PyPI package',
    ext_modules=[module],
    options={'bdist_wheel': {'universal': '1', 'plat_name': 'manylinux2014_x86_64'}},
)

