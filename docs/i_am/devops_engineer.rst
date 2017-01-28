A DevOps Engineer
=================

Deploy their fancy machine learning project, without having to understand its content.


Heroku
~~~~~~

Using Heroku is almost zero-configuration. The following is an example ``Procfile``:

.. code::

   web: fdep serve --driver=xmlrpc app

Done!

Dockerfile
~~~~~~~~~~

A simple example ``Dockerfile`` would be like this:

.. code:: dockerfile

   FROM ubuntu:latest

   RUN apt-get update && \
       apt-get install python python-dev python-pip
   ADD requirements.txt /tmp/requirements.txt
   RUN pip install -r /tmp/requirements.txt

   WORKDIR /src
   ADD . /src/
   RUN fdep install
   CMD fdep serve --driver=xmlrpc app


Build the docker image by:

.. code:: bash

   docker build -t foo/bar .


Running the server on a docker host can be done by the following command:

.. code:: bash

   docker run \
      -e SENTRY_DSN=http://... \
      -e FLUENTD_HTTP_URL=http://... \
      -e RPC_USERNAME=admin \
      -e RPC_PASSWORD=foobar \
      foo/bar

Now you can deploy your app to your Kubernetes cluster, Docker Swarm, etc.
