# ocx-versioning
Utility python scripts for managing OCX xsdata databinding versioning according to PEP 440.
See [xsdata](https://xsdata.readthedocs.io/en/latest/) for details on python xml databindings.

## Installation

    pip install ocx_versioning

## Usage
    > python -m ocx_versioning --help
    Usage: ocx_versioning "module_name" "version_string"
    
    --help: Prints this message and exits.
    --version: Prints the version number and exits.
    >
    > python -m ocx 1.0.0
    Updating the configuration file xsdata.xml in module ocx
    New package name is ocx_100 with version: 1.0.0



    

