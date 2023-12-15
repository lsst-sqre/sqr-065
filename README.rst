.. image:: https://img.shields.io/badge/sqr--065-lsst.io-brightgreen.svg
   :target: https://sqr-065.lsst.io/
.. image:: https://github.com/lsst-sqre/sqr-065/workflows/CI/badge.svg
   :target: https://github.com/lsst-sqre/sqr-065/actions/

#######################################################################################################
Design of Noteburst, a programatic JupyterLab notebook execution service for the Rubin Science Platform
#######################################################################################################

SQR-065
=======

Jupyter Notebooks are a widely used medium in Rubin Observatory for communicating through documentation and executable code. Until now, Jupyter Notebooks have only been accessible from the Notebook Aspect of the Rubin Science Platform (JupyterLab). There are applications where we can benefit from "headless" execution of Jupyter notebooks through a web API, such as preparing status dashboards (Times Square), and continuous integration of code samples in documentation. This technical note discusses the architectural design details of such a service, called Noteburst.

**Links:**

- Publication URL: https://sqr-065.lsst.io/
- Alternative editions: https://sqr-065.lsst.io/v
- GitHub repository: https://github.com/lsst-sqre/sqr-065
- Build system: https://github.com/lsst-sqre/sqr-065/actions/

Build this technical note
=========================

You can clone this repository and build the technote locally if your system has Python 3.11 or later:

.. code-block:: bash

   git clone https://github.com/lsst-sqre/sqr-065
   cd sqr-065
   make init
   make html

Repeat the ``make html`` command to rebuild the technote after making changes.
If you need to delete any intermediate files for a clean build, run ``make clean``.

The built technote is located at ``_build/html/index.html``.

Publishing changes to the web
=============================

This technote is published to https://sqr-065.lsst.io/ whenever you push changes to the ``main`` branch on GitHub.
When you push changes to a another branch, a preview of the technote is published to https://sqr-065.lsst.io/v.

Editing this technical note
===========================

The main content of this technote is in ``index.rst`` (a reStructuredText file).
Metadata and configuration is in the ``technote.toml`` file.
For guidance on creating content and information about specifying metadata and configuration, see the Documenteer documentation: https://documenteer.lsst.io/technotes.
