from setuptools import setup, find_packages
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='networkh3',
    version='0.0.3',
    description='A package to return H3 hexagons based on an OSMnx network',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/callumscoby/networkh3',
    author='Callum Scoby',
    author_email='callumjamesscoby@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='OSMnx, H3, Routing, Network analysis',
    packages=find_packages(),
    install_requires=['pandas', 'geopandas', 'numpy', 'matplotlib', 'shapely', 'osmnx', 'h3', 'h3pandas', 'contextily']
)

