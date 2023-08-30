#  Copyright (c) 2023. OCX Consortium https://3docx.org. See the LICENSE
"""Script to update the xsdata package name from the schema version."""
# System imports
from pathlib import Path
import sys
from typing import Optional, Tuple
# Third party packages
import packaging.version
from packaging.version import Version, parse
from xsdata.models.config import GeneratorConfig
# Project imports
from ocx_versioning import __version__

CONFIG_FILE = 'xsdata.xml'

# The new package version


def usage():
    """Print the usage message and exit"""
    print('Usage: ocx_versioning "module_name" "version_string"\n')
    print('--help: Prints this message and exits.')
    print('--version: Prints the version number and exits.\n')


def cli():
    """Update the package name for python data bindings.

    Usage:

        > python -m ocx_versioning --help
        Usage: ocx_versioning "module_name" "version_string"

        --help: Prints this message and exits.
        --version: Prints the version number and exits.

    """

    if len(sys.argv) == 3:
        new_version = sys.argv[2]
        package = sys.argv[1]
        insert_package_name(package,new_version)
    else:
        arg = sys.argv.pop()
        if arg == '--version':
            print(__version__)
            exit(0)
        else:
            usage()
        exit(0)


def insert_package_name(package:str, version: str):
    """ Update the package name in xsdata.xml, see  https://xsdata.readthedocs.io/en/latest/
        If the config file xsdata.xml does not exist, it will be created with the following values set:

       Arguments:
            package: name of package
            version: The new version string

    Example:

           > python -m ocx_version ocx 1.0.0
            Updating the configuration file xsdata.xml in module ocx
            New package name is ocx_100 with version: 1.0.0

    """
    # parse new_version
    try:
        v= parse(version)
        if v.is_prerelease:
            pr1, pr2 = v.pre
            package_dir = f'{package}_{v.major}{v.minor}{v.micro}{pr1}{pr2}'
        else:
            package_dir = f'{package}_{v.major}{v.minor}{v.micro}'
        file_path = Path(CONFIG_FILE)
        if file_path.exists():
            config = GeneratorConfig.read(file_path)
            print(f'Updating the configuration file {CONFIG_FILE} in module {package}')
        else:
            print(f'Initializing configuration file {CONFIG_FILE}')
            config = GeneratorConfig.create()
        # OCX databindings defaults
        config.output.docstring_style = 'Google'
        # The package name
        config.output.package = package_dir
        config.output.structure_style = 'single-package'
        print(f'New package name is {package_dir} with version: {version}')
        with file_path.open("w") as fp:
            config.write(fp, config)
    except packaging.version.InvalidVersion as e:
        print(e)
        exit(1)

if __name__ == "__main__":
    insert_package_name()
