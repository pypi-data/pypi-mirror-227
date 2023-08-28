from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='networkh3',
    version='0.0.1',
    description='A package to return H3 polygons based on an OSMnx network',
    Long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Callum Scoby',
    author_email='callumjamesscoby@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='OSMnx, H3, Routing, Network analysis',
    packages=find_packages(),
    install_requires=['pandas', 'geopandas', 'numpy', 'matplotlib', 'shapely', 'osmnx', 'h3', 'h3pandas', 'contextily']
)