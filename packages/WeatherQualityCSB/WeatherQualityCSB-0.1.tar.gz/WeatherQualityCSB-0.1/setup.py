from setuptools import setup, find_packages

setup(
    name='WeatherQualityCSB',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'selenium',
        'tqdm'
    ],
    entry_points={
    },
    author='melihoverflow5',
    author_email='melihtaskin@pm.me',
    description='A utility to fetch weather quality data from the CSB website.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/melihoverflow5/WeatherQualityCSB',  # If you host it on GitHub
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)