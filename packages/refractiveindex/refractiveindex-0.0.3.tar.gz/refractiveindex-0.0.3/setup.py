# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['refractiveindex']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0', 'scipy>=1.9.3,<2.0.0']

setup_kwargs = {
    'name': 'refractiveindex',
    'version': '0.0.3',
    'description': '',
    'long_description': "# Easy Python interface to RefractiveIndex database\n\nThe original database<br>\nhttps://github.com/polyanskiy/refractiveindex.info-database\n\nDatabase files parsing was made with a modified version of `refractiveIndex.py` from [PyTMM project](https://github.com/kitchenknif/PyTMM) by [Pavel Dmitriev](https://github.com/kitchenknif).\n\n## Installation\n\n```\npip install refractiveindex\n```\n\n## Usage\n\n\n```python\nfrom refractiveindex import RefractiveIndexMaterial\n\nSiO = RefractiveIndexMaterial(shelf='main', book='SiO', page='Hass')\n\nwavelength_nm = 600  # [nm]\n\nSiO.get_epsilon(wavelength_nm)\n# (3.8633404437869827+0.003931076923076923j)\n\nSiO.get_refractive_index(wavelength_nm)\n# (1.96553846)\n\nSiO.get_extinction_coefficient(wavelength_nm)\n# (0.001)\n```\n\nNotes: \n- here the time dependence is assumed to be $\\mathrm{e}^{-\\mathrm{i} \\omega t}$, so $\\operatorname{Im}\\varepsilon > 0$ is responsible for the losses.\n- if there is a space in the name, one should write underscore instead of it, i.e. not `page='Rodriguez-de Marcos'` but `page='Rodriguez-de_Marcos'`.\n\n\n## How to get material page names\n\nYou can find the proper “page” name by hovering your cursor on the link in the Data section\n\n![How to get page name](./fig/link.png)\n\nOr you can look up folders in this repository<br>\nhttps://github.com/polyanskiy/refractiveindex.info-database\n\n## Simular projects for Julia\n\nJulia interface to refractiveindex.info database<br>\nhttps://github.com/stillyslalom/RefractiveIndex.jl\n",
    'author': 'Ivan Toftul',
    'author_email': 'toftul.ivan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
