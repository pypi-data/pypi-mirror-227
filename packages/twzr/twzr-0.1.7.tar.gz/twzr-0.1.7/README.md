# Tweezer
### teeny tiny tools for data processing :mag::space_invader:

`twzr` is a handful of microfunctions to help make `pandas` data transformation workflows faster. For example, Why type `df.filter(regex=re.compile('column',re.IGNORECASE))` when you can type `f(df,'column')`?

Ideally, analytical workflows will involve automated transformation pipelines and no-code tools for analysts. `twzr` is a practical set of functions for when that is not yet the case. :bowtie: And because laziness is a virtue in programming.

## Commands
Run `help()` for a current list of functions in `twzr`. 

## Installation
Run `pip install git+https://github.com/aspencage/twzr@main` on the command line. 

## Forthcoming
* Documentation
    * Functions described in this README file
    * Examples included in this README file 
* Packaging
    * Package distributed on PyPI
