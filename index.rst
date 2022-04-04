:tocdepth: 1

.. Please do not modify tocdepth; will be fixed when a new Sphinx theme is shipped.

.. sectnum::

Abstract
========

Jupyter Notebooks are a widely used medium in Rubin Observatory for communicating through documentation and executable code.
Until now, Jupyter Notebooks have only been accessible from the Notebook Aspect of the Rubin Science Platform (JupyterLab).
There are applications where we can benefit from "headless" execution of Jupyter notebooks through a web API, such as preparing status dashboards (Times Square, :sqr:`062` :cite:`SQR-062`), and continuous integration of code samples in documentation.
This technical note discusses the architectural design details of such a service, called Noteburst.

Use cases
=========

These are examples of applications that are either enabled by, or can benefit from, a headless Jupyter Notebook service co-located on the Rubin Science Platform.

Times Square
------------

In the Times Square (:sqr:`062`, :cite:`SQR-062`) use case, users are visiting web pages in a browser, and those pages contain HTML renderings of executed Jupyter Notebooks.
Although Times Square will cache executed Jupyter Notebooks, if the user requests a novel parameterization of a notebook that isn't in Times Square's cache, that webpage visit will ultimately result in a request to Noteburst to execute a new notebook.
Furthermore multiple users may visit different novel pages, each requiring a different execution through Noteburst.

Notebook-based technical notes
------------------------------

Rubin has a robust technical note platform (:sqr:`000` :cite:`SQR-000`), that empowers staff to share technical information quickly and widely with little overhead.
At the moment, technical notes are written either as Sphinx/reStructuredText or PDF (LaTeX) documents.
Jupyter Notebooks can be a compelling addition to this line-up for documentation applications that combine computational analysis and visualization with prose.
For example, a technical note could include an analysis of data available from the Rubin Science Platform, and all figures and tables presented in that technical note are the direct result of that computation.

Technotes are typically published through GitHub Actions, where we have upload credentials available and established workflow patterns.
Rubin data or software like the LSST Science Pipelines aren't typically available through GitHub Actions.
The naive workaround is to execute the notebook on the RSP and commit the result into the technote's GitHub repository.
There are at least two downsides to this.
First, the executed notebook takes more storage space because of its outputs and it generally harder to manage in a Git workflow.
Second, the technote is less reproducible since there are many manual steps between executing a notebook and publish it as a technote.

The solution could be to use a "headless notebook execution" web service hosted on the Rubin Science Platform.
The author commits a change to an (unexecuted) Jupyter Notebook-based technote, which triggers a GitHub Actions workflow.
That workflow makes a call to the service (noteburst) using an RSP token stored in the repository's GitHub Secrets.
Once the workflow gets the executed notebook back from the web service, it uses the local CI environment to convert the notebook into HTML and publish it through LSST the Docs (:sqr:`006` :cite:`SQR-006`).

Documentation testing
---------------------

Similar to the above use-case, the ability to test sample code and examples from documentation could benefit from a service that executes code on the RSP and packages the outputs in Jupyter Notebook format.
See :sqr:`032` :cite:`SQR-032` for additional ideas on this subject.

.. rubric:: References

.. Make in-text citations with: :cite:`bibkey`.

.. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
   :style: lsst_aa
