import setuptools
import pathlib

import zerofun


setuptools.setup(
    name='zerofun',
    version=zerofun.__version__,
    author='Danijar Hafner',
    author_email='mail@danijar.com',
    description='Remote function calls for array data using ZMQ',
    url='http://github.com/danijar/zerofun',
    long_description=pathlib.Path('README.md').read_text(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=['numpy', 'msgpack', 'pyzmq'],
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
