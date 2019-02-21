import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='python-proxy-utils',
    version='0.1.0',
    author='Jeremy Storer',
    author_email='storerjeremy@gmail.com',
    description='Python Proxy Utils',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/storerjeremy/python-proxy-utils',
    packages=setuptools.find_packages(),
    install_requires=[
        'aiohttp',
        'lxml',
        'cssselect',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
