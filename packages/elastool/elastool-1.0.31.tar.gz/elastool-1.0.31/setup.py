"""
  Elastool -- Elastic toolkit for zero- and finite-temperature elastic constants and mechanical properties calculations

  Copyright (C) 2019-2024 by Zhong-Li Liu and Chinedu Ekuma

  This program is free software; you can redistribute it and/or modify it under the
  terms of the GNU General Public License as published by the Free Software Foundation
  version 3 of the License.

  This program is distributed in the hope that it will be useful, but WITHOUT ANY
  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
  PARTICULAR PURPOSE.  See the GNU General Public License for more details.

  E-mail: zl.liu@163.com and cekuma1@gmail.com
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

#Read in the README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
     long_description=fh.read()


py_m=["calc_elastic_constants", "calc_stress", "deform_cell_asess_strains", \
      "deform_cell_ohess_strains", "deform_cell_ulics", "extract_mean_values", \
      "equilibrium_md", "find_spg", "make_conv_cell", "optimize_initial_str", \
      "read_input", "relax_atoms_pos", "vasp_run", "sound_velocity", \
      "stability_criteria", "strain_matrix", "write_incar"]

setup(
      name="elastool",
      version="1.0.31",
      description="Elastic tool for zero and finite-temperature elastic constants and mechanical properties calculations",
      author="Zhong-Li Liu and Chinedu Ekuma",
      author_email="cekuma1@gmail.com",
      url="https://sourceforge.net/projects/elastool/",
      license="GNU GPL version 3",
      py_modules=py_m,
      package_dir = {'':'elastool'},
      scripts=["elastool/elastool"],
      long_description=long_description,
      long_description_content_type="text/markdown"
     # install_requires=[
     #     'numpy',
     #     'spglib',
     #     'ase',
     #     'pandas'
     # ]
      )
