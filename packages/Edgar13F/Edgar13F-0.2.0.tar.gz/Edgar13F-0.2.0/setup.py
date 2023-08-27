from setuptools import setup

setup(
    name='Edgar13F',
    version='0.2.0',
    author='Jack Brown',
    author_email='jackabrown21@gmail.com',
    packages=['Edgar13F'],
    description='A Python package for scraping 13F filings from the SEC Edgar database.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url="https://pypi.org/project/Edgar13F/",
    install_requires=[
        'requests',
        'beautifulsoup4',
        'python-dotenv'
    ],
)
