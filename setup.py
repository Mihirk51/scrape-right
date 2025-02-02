from setuptools import setup, find_packages

setup(
    name='scrape-right',
    version='0.1',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'selenium',
        'webdriver-manager',
        'beautifulsoup4',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'get_events_info=main:main',
        ],
    },
)