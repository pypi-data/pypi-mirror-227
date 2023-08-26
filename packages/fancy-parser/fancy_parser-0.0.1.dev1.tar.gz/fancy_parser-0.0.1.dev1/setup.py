from setuptools import setup, find_packages

setup(
    name='fancy_parser',
    version='0.0.1.dev1',
    description='A fancy parser for fancy people who like AI',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nannullna/fancy-parser',
    author='Sanghyun Kim',
    author_email='nannullna@kaist.ac.kr',
    license='Apache License 2.0',
    packages=['fancy_parser'],
    install_requires=[],
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
    ],
    python_requires='>=3.7',
)