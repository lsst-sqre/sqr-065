"""Sphinx configuration for technotes.

https://documenteer.lsst.io/technotes/configuration.html
"""

from documenteer.conf.technote import *

# Additional extensions
extensions += [
    "sphinx_diagrams",
]

# Additional intersphinx
intersphinx_mapping["nbconvert"] = (
    "https://nbconvert.readthedocs.io/en/latest/",
    None
)

# The reST default role (used for this markup: `text`)
default_role = "obj"
