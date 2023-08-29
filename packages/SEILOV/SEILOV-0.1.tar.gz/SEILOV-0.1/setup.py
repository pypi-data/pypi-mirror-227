from setuptools import setup, Extension
import pybind11

module = Extension(
    'SEILOV',
    sources=['SEILOV.cpp'],
    include_dirs=[pybind11.get_include()]
)

setup(
    name='SEILOV',
    version='0.1',
    description='My PyPI package',
    ext_modules=[module],
    options={'bdist_wheel': {'universal': '1', 'plat_name': 'manylinux2014_x86_64'}},
)

