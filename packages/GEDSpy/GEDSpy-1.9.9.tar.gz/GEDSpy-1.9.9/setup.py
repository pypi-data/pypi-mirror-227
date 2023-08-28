from setuptools import setup, find_packages

VERSION = '1.9.9' 
DESCRIPTION = 'GEDSpy'
LONG_DESCRIPTION = 'GEDSpy is the Python library for gene list enrichment with genes ontology, pathways, diseases, tissue and cellular specificity, and potential drugs. Package description  on https://github.com/jkubis96/GEDSpy'

# Setting up
setup(
        name="GEDSpy", 
        version=VERSION,
        author="Jakub Kubis",
        author_email="jbiosystem@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=['GEDSpy'],
        include_package_data=True,
        install_requires=['requests','pandas','tqdm','seaborn','matplotlib','scipy','networkx','pyvis','beautifulsoup4','numpy','adjustText', 'requests'],       
        keywords=['python', 'GO', 'pathways', 'drug', 'gene ontology', 'diseases', 'enrichment'],
        license = 'MIT',
        classifiers = [
            "Development Status :: 3 - Alpha",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
            "Operating System :: POSIX :: Linux",
        ],
        python_requires='>=3.6',
)


