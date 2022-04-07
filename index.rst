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

Noteburst's architecture
========================

Noteburst's design resolves around the following constraints and requirements:

1. Notebooks must be executed in the Rubin Science Platform with a similar, if not identical, set up to how users interactively run notebooks.
   A notebook that a user can run in Nublado must also be runnable through the service.
2. The service must be accessible through a simple HTTP interface.
3. The service must account for the fact that notebooks can take a significant amount of time to execute (this is, it must employ an asynchronous queue architecture).

This section describes how Noteburst is designed to meet these needs.

.. diagrams:: deployment_diagram.py

Noteburst consists of two Kubernetes application deployments: an API deployment and the worker deployment.
The pods running in both deployments are drawn from the same codebase (`lsst-sqre/noteburst`_), but the API runs a FastAPI application, while the worker pods are arq_ worker instances.
Noteburst's only persistent storage is a Redis cluster that contains both queue jobs and the results from completed jobs.

API deployment
--------------

The Noteburst API deployment processes HTTP requests from clients.
Through the API, Noteburst receives notebook execution requests and creates notebook execution jobs through the arq_ library, which are stored in Redis.
The API can also retrieve results (generated by workers) from Redis, upon request.

Worker deployment
-----------------

Noteburst's workers are responsible for executing notebooks.
Each worker has a one-to-one relationship with a with a Nublado (JupyterLab) user pod.
When a worker pod starts up, it starts a JupyterLab pod under a bot user identity.
A connection to that JupyterLab pod is maintained for the lifetime of the worker pod.
When the Noteburst worker receives a job request (through arq_, from the Noteburst API deployment), it triggers a notebook execution via the `execution <https://github.com/lsst-sqre/rsp-jupyter-extensions/blob/main/rsp_jupyter_extensions/execution.py>`_ extension endpoint in `lsst-sqre/rsp-jupyter-extensions`_, which in turn runs nbconvert's `~nbconvert.preprocessors.ExecutePreprocessor`.

Redis deployment
----------------

Noteburst uses Redis as its sole persistent storage.
In the Phalanx deployment, Redis is deployed via a `Bitnami Helm chart <https://github.com/bitnami/charts/tree/master/bitnami/redis>`__ in high-availability mode with three nodes in total and persistent volumes for each node.

Noteburst uses Redis for two concerns:

1. As a global lock of claimed user identities for worker pods
2. As a storage backend for queued job submitted through the API pods and results submitted through the worker pods.

----

.. rubric:: References

.. Make in-text citations with: :cite:`bibkey`.

.. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
   :style: lsst_aa

.. Links

.. _arq: https://arq-docs.helpmanual.io
.. _FastAPI: https://fastapi.tiangolo.com
.. _lsst-sqre/noteburst: https://github.com/lsst-sqre/noteburst
.. _lsst-sqre/rsp-jupyter-extensions: https://github.com/lsst-sqre/rsp-jupyter-extensions
