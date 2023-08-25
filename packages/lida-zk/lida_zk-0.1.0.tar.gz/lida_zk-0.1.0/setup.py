from setuptools import setup, find_packages

setup(
    name='lida_zk',
    version='0.1.0',
    description='Added azure to the original foundation',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
    ],
    install_requires=[
        "llmx_zk",
        "pydantic",
        "uvicorn", 
        "typer",
        "fastapi", 
        "python-multipart", 
        "scipy", 
        "numpy",
        "pandas",
        "matplotlib",
        "altair", 
        "seaborn",
        "plotly", 
        "plotnine",
        "statsmodels", 
        "networkx",
        "geopandas",
        "matplotlib-venn",
        "wordcloud", 
        "basemap",
        "basemap-data-hires"
    ],
)
