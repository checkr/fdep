Introduction
============

fdep is a framework-agnostic, transport-agnostic, extensible command line tool to shape workflows between machine learning experts and others. fdep is developed at Checkr_ to make a clean separation of two concerns: machine learning and deploying it as a service.

At Checkr_, we heavily use machine learning techniques to improve our accuracy of background checks. We frequently change, experiment, and deploy our models. We learned that maintaining the other aspects than the model itself becomes a huge cost in many angles. e.g. data scientists trying to set up AWS, copying around some service-related code, and so on. To tackle this problem, we separated the problem into two.

.. _Checkr: http://checkr.com/


The Two Concerns
----------------

1. Machine Learning
~~~~~~~~~~~~~~~~~~~

To solve business problems with machine learning, we not only need to work with other developers, but we need consistent collaboration with domain experts. This is how we are able to label, validate, and improve models. But, how do we collaborate with others efficiently?


2. Building A Service
~~~~~~~~~~~~~~~~~~~~~

It's not rocket science. You can make it rocket science, but keeping it
simple is always a better choice. Many of the current offerings require too
much work, especially if your expertise is data science.
There are many unresolved parts, if you see this just as an API service. For
example, how are we going to deploy our model's weights for a deep
convolutional neural network? Will it break the running services if I change the model's input shape?
What if I use a completely different framework now? Where do we upload our dataset?


Solution: fdep
--------------

Download Datasets and Models Anywhere
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you already have the fdep.yml file set up, the following command will install all the files you need:

.. code:: bash

   fdep install


Versioning Files
~~~~~~~~~~~~~~~~

You can upload your dataset, or model with a version tag by the following command:

.. code:: bash

   fdep commit data/dataset.dat


Support of More Popular Sources
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Google Sheets are supported.


Run Your Server with Just One Command
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Launching a XML-RPC server based on your python code `model.py` can be done by the following command:

.. code:: bash

   fdep serve --driver=xmlrpc model


Integrate with Third Party Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For instance, to set up Sentry, you just run the following command:

.. code:: bash

   export SENTRY_DSN=http://.....
   fdep serve --driver=xmlrpc
