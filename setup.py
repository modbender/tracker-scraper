import setuptools
from readme_renderer import rst

README = open('README.md').read()

setuptools.setup(
    name='tracker-scraper',
    version='1.0.1',
    url='https://github.com/modbender/tracker-scraper',
    description='A simple torrent tracker scraper',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Yashas H R',
    author_email='rameshmamathayashas@gmail.com',
    install_requires=[
        'bencode.py',
        'requests',
    ],
    python_requires='>=3.5',
    platforms=['any'],
    packages=setuptools.find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
