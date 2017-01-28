A Data Scientist
================

Train your model and ship products really quickly! No chores needed, you can start with just one Python source code.


Set Up Your Machine Learning Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose you have a project version controlled with Git. Let's start using fdep.

.. code:: bash

   cd project
   fdep init development production
   git add fdep.yml
   git commit -m "Initialize fdep"

Now you have two environments ``development``, and ``production`` set up for your machine learning project.


Upload Your Dataset
~~~~~~~~~~~~~~~~~~~

Let's use S3 as our storage backend. You can add your file to the fdep.yml and manage it there by:

.. code:: bash

   fdep add data/labeled_data.csv s3://my-nlp-project/labeled_data.csv

But note that the above command doesn't upload the file itself. Let's upload the file to our infrastructure.

.. code:: bash

   fdep commit data/labeled_data.csv

Done! Make sure you commit your ``fdep.yml`` on git, so that the version you just uploaded can be tracked properly on git, or whatever version control system you use.

.. code:: bash

   git commit -m "Update the labeled data" fdep.yml

From this on, you can follow the software practice you normally do or your company does, such as making a pull request on Github for code review, etc.

.. note::

   If you are getting errors, probably you haven't set up ``aws-cli`` on your machine. You can go to this webpage and learn how to set up ``aws-cli``: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html

.. note::

   You can also use ``fdep upload``, but using ``fdep commit`` is highly recommended. By doing so, all changes to the data can be tracked nicely on your version control system.

Testing Your Model
~~~~~~~~~~~~~~~~~~

If you have a function defined in your Python source code that takes a string as an input, you can try out your functions, test your models, etc.

.. code:: bash

   fdep serve --func classify my_nlp_classifier
