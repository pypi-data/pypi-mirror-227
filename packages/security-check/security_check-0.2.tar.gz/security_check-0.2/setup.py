from setuptools import setup, find_packages

setup(
    name='security_check',
    version='0.2',
    description='Execute safety check with cvss scores',
    author='Claucio Rank',
    author_email='clauciorank@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'security_check=security_check.execute:run',
        ]
    },
    install_requires=[
        'requests',
        'beautifulsoup4',
        'safety',
        'numba'
    ]
)
