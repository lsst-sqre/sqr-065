:tocdepth: 1

.. Please do not modify tocdepth; will be fixed when a new Sphinx theme is shipped.

.. sectnum::

Abstract
========

Jupyter Notebooks are a widely used medium in Rubin Observatory for communicating through documentation and executable code.
Until now, Jupyter Notebooks have only been accessible from the Notebook Aspect of the Rubin Science Platform (JupyterLab).
There are applications where we can benefit from "headless" execution of Jupyter notebooks through a web API, such as preparing status dashboards (Times Square, :sqr:`062`), and continuous integration of code samples in documentation.
This technical note discusses the architectural design details of such a service, called Noteburst.

Use cases
=========

There are not strict requirements on Noteburst, however, we can derive a basic notion of required functionality from our use cases.
These requirements can frame the subsequent design deliberation.

In the Times Square use case, users are visiting web pages in a browser, and those pages contain HTML renderings of executed Jupyter Notebooks.
Although Times Square will cache executed Jupyter Notebooks, if the user requests a novel parameterization of a notebook that isn't in Times Square's cache, that webpage visit will ultimately result in a request to Noteburst to execute a new notebook.
Furthermore multiple users may visit different novel pages, each requiring a different execution through Noteburst.

.. The front-end application will need to deal with delays in the notebook rendering.

An asynchronous noteburst API?
==============================

Is an asynchronous API and job queue required for Noteburst?

In a synchronous API, a client would request a notebook execution from noteburst and expect to receive the executed notebook as a response.
This synchronous API requires that the notebook can be returned within the period of an HTTP request, which is ideally less than a few seconds, and certainly no longer than 30 seconds.

Responding with an executed notebook can be delayed for a number of reasons:

1. The JupyterLab pod needs to spawn.
2. The notebook takes a certain duration to execute (the notebook may even make its own network requests, in addition to data processing and plotting).
3. The JupyterLab pod may already be in use by another noteburst client job (**note:** it is unknown whether it is possible to have

.. note::

   It is unclear whether noteburst can run multiple notebook executions on the same pod.
   This needs to be tested --- both with the websocket style of kernel execution and with the JupyterLab extension for notebook execution.

In an asynchronous API the client would follow these steps:

1. Request a notebook execution by sending the notebook to noteburst in a ``POST`` request.
   Noteburst would reply with a job ID.
2. The client would pole a job status endpoint until the status is marked as "done."
3. The client would request the executed notebook content from another endpoint.

A variation on this API is to use webhooks to bypass polling for clients that have their own web API:

1. Request a notebook execution by sending the notebook to noteburst in a ``POST`` request. Also send a webhook callback URL and a secret key.
2. Once noteburst executes the notebook, it sends a ``POST`` request to the registered webhook URL and includes the secret key for the client to validate.

The webhook model is ideal for Times Square since any Times Square API pod could receive the notebook and add it to its cache.
Times Square would need to provide an additional API for its front-end client though to indicate if the notebook is ready and the front-end would likely need to pole that endpoint unless websockets are used between the Times Square UI and Times Square API.

Overall, a synchronous API is much easier to implement.
However our experience with other systems that perform non-trivial work in a request handler is that these APIs can be fragile, and it's much better to design for the worst-case with an asynchronous API from the start.

.. .. rubric:: References

.. Make in-text citations with: :cite:`bibkey`.

.. .. bibliography:: local.bib lsstbib/books.bib lsstbib/lsst.bib lsstbib/lsst-dm.bib lsstbib/refs.bib lsstbib/refs_ads.bib
..    :style: lsst_aa
