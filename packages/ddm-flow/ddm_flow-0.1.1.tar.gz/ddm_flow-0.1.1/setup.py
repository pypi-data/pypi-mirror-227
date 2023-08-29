from setuptools import setup, find_packages

setup(
    name="ddm_flow",
    version="0.1.1",
    packages=find_packages(),

    install_requires=[
        'contourpy>=1.1.0',
        'matplotlib>=3.7.2',
        'numpy>=1.25.2',
        'openpyxl>=3.1.2',
        'packaging>=23.1',
        'pandas>=2.0.3',
        'Pillow>=10.0.0',
        'python-dateutil>=2.8.2',
        'pytz>=2023.3',
        'tzdata>=2023.3'
    ],
    entry_points={
        'console_scripts': [
            'multisheet_aggregator=ddm_flow_scripts.multisheet_fov_aggregator:main',
            'csv_organizer=ddm_flow_scripts.csv_organizer:main',
            'plotter=ddm_flow_scripts.plotter:main'
        ],
    },

    author="Naz Ebrahimi",
    description="A toolset for processing, organizing, and visualizing data for individual FoVs from DDm analysis.",
    long_description=open('README.md').read(),
    url="https://github.com/NEbrahimi/ddm-flow",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)

