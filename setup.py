from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='nadia-proof',
    version='0.1.9',
    license='MIT',
    author="Davi Romero de Vasconcelos",
    author_email='daviromero@ufc.br',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/daviromero/nadia',
    description='''NADIA is a proof assistant for teaching natural deduction to computer science students. NADIA allows students to write their proofs and automatically checks whether the proofs are correct and, if not, displays any errors found.''',
    long_description=long_description,
    long_description_content_type='text/markdown',
    keywords='Natural Deduction, Teaching Logic, Educational Software', 
    install_requires=[
        'rply',
        'ipywidgets',
      ],
    entry_points={'console_scripts': ['nadia=nadia.__main__:main', ], },    
    
)
