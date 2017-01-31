A Software Engineer
===================

Test what your data scientist developed and extend fdep.

Install Their Machine Learning Project and Get It Running
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

   git clone git@github.com:foo/bar.git; cd bar
   fdep install
   fdep serve run_ml

Extend fdep
~~~~~~~~~~~

You can extend fdep to use different protocols to serve the model.

.. autoclass:: fdep.servers.RPCServer
    :members: register_functions, serve_forever

Extend the above class in your project and simply do the following:

.. code:: bash

   fdep serve --driver=your.project.driver.JSONRPCServer some_module

fdep will pick up your driver and use it to serve the model.

.. note::
   fdep has built-in support for XMLRPC and JSONRPC.
   ``fdep serve --driver=xmlrpc some_module`` or ``fdep serve --driver=jsonrpc some_module``
