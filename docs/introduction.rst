Introduction
============

fdep is a framework-agnostic, transport-agnostic, extensible command line tool to shape workflows between machine learning experts and others. fdep is developed at Checkr_ to make a clean separation of two concerns: machine learning and deploying it as a service.

At Checkr_, we heavily use machine learning techniques to improve our accuracy of background checks. We frequently change, experiment, and deploy our models. We learned that maintaining the other aspects than the model itself becomes a huge cost in many angles. e.g. data scientists trying to set up AWS, copying around some service-related code, and so on. To tackle this problem, we separated the problem into two.

.. _Checkr: http://checkr.com/


The Two Concerns
----------------

1. Machine Learning
~~~~~~~~~~~~~~~~~~~

It's probably the meat for your current project. Developing a successful machine learning model for business requires lots of science, and sometimes inter-department collaborations/communications in order to validate, and improve the model. Many critical insights about the data come from domain experts of the business, and it is essential to keep them in the loop, build a ground-truth data, and validate the result in a collaborative manner. How do we collaborate wit them efficiently?


2. Building A Service
~~~~~~~~~~~~~~~~~~~~~

Let's say this, It's not a rocket science. You could make this as a rocket science, but keeping it simple, stupid is always a better choice. While there are many good tools out there, it requires a lot of work. Even more so if you know that it's a little different area of expertise than data science. There are many unresolved parts, if you see this just as an API service. For example, how are we going to deploy the weights numpy file for a deep convolutional neural network? Will it break the running services if I change the model's input shape? What if I use a completely different framework now? Where do we upload our dataset?


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

Google Spreadsheet is supported.


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
