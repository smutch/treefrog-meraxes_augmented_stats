from setuptools import setup, find_packages

setup(
    name="treefrog_meraxes_augmented_stats",
    version="0.1.0",
    author="Simon Mutch",
    author_email="smutch.astro@gmail.com",
    packages=find_packages(),
    install_requires=[
        "Click >= 7.0",
        "dask>=1.2.2",
        "toolz>=0.9.0",
        "h5py>=2.8",
        "numpy>=1.14",
        "pandas>=0.23",
        "pytest>=4.5.0",
        "cloudpickle>=1.1.1"
    ],
    scripts=[
        'bin/treefrog_test_forestinfo'
    ],
    entry_points={
        'console_scripts': [
            'treefrog_gen_alist=treefrog_meraxes_augmented_stats.generate_alist:cli',
            'treefrog_gen_forestinfo=treefrog_meraxes_augmented_stats.generate_forest_info:cli'
        ],
        'pytest11': [
            'augstats = treefrog_meraxes_augmented_stats._tests.augstats',
        ]
    }
)
