from setuptools import setup, find_packages


setup(
    name="riskhub",
    version="0.1",
    author='sabarish',
    author_email="sabarishbugbounty@gmail.com",
    description="fetching URLs to any domains",
    packages=find_packages(),
    readme = "README.md",
    install_requires=[
        'requests==2.27.1',
        'argparse==1.4.0',
        'apscheduler==3.9.1',
        'pause==0.3',
        'urllib3==1.24.2',
        'multiprocessing',
    ],
    entry_point= {
        'console_scripts': [
            'riskhub=riskhub.riskhub:main',
        ],
    },
)
