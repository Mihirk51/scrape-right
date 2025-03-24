from setuptools import find_packages, setup

setup(
    name="scrape-right",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "click",
        "selenium",
        "webdriver-manager",
        "beautifulsoup4",
        "requests",
        "python-dateutil",
        "lxml",
        "pyodbc",
        "pandas",
        "flask-pydantic",
    ],
    entry_points={
        "console_scripts": [
            "get_events_info=main:cli",
        ],
    },
)
