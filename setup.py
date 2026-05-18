from setuptools import setup, find_packages

setup (
    name ='Parrot Proxy',
    version = '0.1.0',
    description = 'Parrot Proxy - HTTP Request Analyzer and Replay Tool',
    author = 'Dave Palombo',
    author_email = 'david.palombo5@gmail.com',
    url = 'https://github.com/DavidPalombo/parrot-proxy.git',

    packages = find_packages(where='src'),
    package_dir = {'': 'src'},

    python_requires = '>=3.8',

    install_requires = [
        'requests>=2.31.0',
        'beautifulsoup4>=4.12.0',
        'click>=8.1.0',
        'rich>=13.0.0',
        'sqlalchemy>=2.0.0',
    ],

    entry_points = {
        'console_scripts': [
            'http-analyzer=request_analyzer.main:cli',
        ],        
    },

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)