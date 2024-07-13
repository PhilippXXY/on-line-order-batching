from setuptools import setup, find_packages

setup(
    name='online_order_batching',
    version='1.0.0',
    description='Implementation of algorithms for on-line order batching in an order picking warehouse',
    author='Philipp Schmidt',
    license='Apache-2.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'click==8.1.7',
        'inquirerpy==0.3.4',
        'pandas==2.2.2',
        'tabulate==0.9.0',
        'keyboard==0.13.5',
    ],
    entry_points={
        'console_scripts': [
            'online_order_batching=main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
