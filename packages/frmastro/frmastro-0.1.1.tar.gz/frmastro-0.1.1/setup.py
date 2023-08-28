# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frmastro',
 'frmastro.filter_tracings.orig.jwst',
 'frmastro.filter_tracings.orig.uvot',
 'frmastro.psf']

package_data = \
{'': ['*'],
 'frmastro': ['filter_tracings/*',
              'filter_tracings/orig/*',
              'spec_mods/*',
              'spec_mods/bsl/*']}

install_requires = \
['astropy>=5.3.2,<6.0.0',
 'frmbase>=0.2.0,<0.3.0',
 'ipdb>=0.13.13,<0.14.0',
 'matplotlib>=3.7.2,<4.0.0',
 'numpy',
 'pandas',
 'pytest>=7.4.0,<8.0.0',
 'scipy']

setup_kwargs = {
    'name': 'frmastro',
    'version': '0.1.1',
    'description': "Fergal's astro related code in Python",
    'long_description': None,
    'author': 'Fergal',
    'author_email': 'fergal.mullally@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
