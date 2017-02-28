A Data Scientist
================

Train your model and ship products at the speed of light! No chores needed,
you can start with just one Python file.


Set Up Your Machine Learning Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suppose you have a project version controlled with Git. Let's start using fdep.

.. code:: bash

   cd project
   fdep init development production
   git add fdep.yml
   git commit -m "Initialize fdep"

Now you have two environments ``development``, and ``production`` set up for your machine learning project.


Example: English Word Checker
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's work on a really trivial example to help you understand how to use fdep.
How about building a word list from a book and determining if the
given word is in the book?

First, let's add a plain-text English book from Gutenberg_.

.. _Gutenberg: https://www.gutenberg.org/

.. code:: bash

   fdep add data/pride-and-prejudice.txt https://www.gutenberg.org/files/1342/1342-0.txt

And write a simple Python program:

.. code-block:: python
   :linenos:
   :caption: build_wordlist.py

   from nltk import word_tokenize
   import re

   wordlist = set()
   with open('data/pride-and-prejudice.txt') as f:
       for word in word_tokenize(f.read()):
           word = word.lower()
           word = re.sub('[^a-z0-9]', '', word)
           wordlist.add(word)

   with open('data/wordlist.txt', 'w') as f:
       for word in wordlist:
           f.write(word + '\n')

This simple code will build the file ``data/wordlist.txt``.
Let's go ahead and build the wordlist with
.. code:: bash

   python build_wordlist.py


Now, let's build a function that checks if a given word is in our set.

.. code-block:: python
   :linenos:
   :caption: word_checker.py

   with open('data/wordlist.txt') as f:
        wordlist = set(f.read().split('\n'))

   def check(word):
       return word in wordlist

Wait, this is just a function, though. How do we test this? It's easy!

.. code:: bash

   fdep serve --func check word_checker


.. note::

    If you have a function defined in your Python source code that takes a string as an input, you can try out your functions, test your models, etc.

    .. code:: bash

       fdep serve --func classify my_nlp_classifier


Upload Your Dataset
~~~~~~~~~~~~~~~~~~~

Now that we built the wordlist, we probably want to save it somewhere.
Let's use S3 as our storage backend. You can add your file to the ``fdep.yml`` file and manage it there by:

.. code:: bash

   fdep add data/wordlist.txt s3://my-nlp-project/wordlist.txt

But note that the above command doesn't upload the file itself. Let's upload the file to our infrastructure.

.. code:: bash

   fdep commit data/wordlist.txt

Done! Commit both adds the sha1 hash to ``fdep.yml`` and uploads the file to its specified storage location. Make sure you commit your ``fdep.yml`` on git, so that the version you just uploaded can be tracked properly on git, or whatever version control system you use.

.. code:: bash

   git commit -m "Update the wordlist file" fdep.yml

From here, you can follow the software practice you normally do or your company does, such as making a pull request on Github for code review, etc.

.. note::

   If you're getting errors, you probably haven't set up ``aws-cli`` on your machine. You can go to this webpage and learn how to set up ``aws-cli``: http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-set-up.html

.. note::

   You can also use ``fdep upload``, but using ``fdep commit`` is highly recommended. By doing so, all changes to the data can be tracked nicely on your version control system.

Set Up Production
~~~~~~~~~~~~~~~~~

You can have a different set of files for development and production, or you can choose to have the same.

For our exercise above, it probably doesn't make sense to have a different ``wordlist.txt`` for production.
And also, for production, it doesn't make sense to have the English book there.

.. code:: bash

   fdep link development:data/wordlist.txt production:data/wordlist.txt

The above command will link the two different environments and make them use the same ``data/wordlist.txt``.
So as a result, your ``fdep.yml`` will look like this:

.. code-block:: yaml

   development:
     data/pride-and-prejudice.txt: https://www.gutenberg.org/files/1342/1342-0.txt
     data/wordlist.txt: &id001
       source: s3://my-nlp-project/wordlist.txt
       version: ca79894f4bbdc6a5389a48f48dcb1194
   production:
     data/wordlist.txt: *id001


Now, both your development and production environments will get their
wordlist from s3://my-nlp-project/wordlist.txt.  The command line
below will install ``data/wordlist.txt``, but not
``data/pride-and-prejudice.txt``.

.. code:: bash

   ENV=production fdep install
