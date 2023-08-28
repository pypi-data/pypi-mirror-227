from setuptools import setup, find_packages

requirements = ['beautifulsoup4==4.12.2',
'Requests==2.31.0']

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='txts.py',
    author='smugay',
    description='Python wrapper for interacting with txts',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/txts-team/txts.py/',
    version="1.0",
    packages=find_packages(),
    install_requires=requirements,
classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.3'
)
