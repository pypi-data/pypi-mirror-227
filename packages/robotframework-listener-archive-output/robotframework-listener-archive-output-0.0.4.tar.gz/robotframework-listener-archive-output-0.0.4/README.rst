========
Overview
========

A Robot Framework listener for archiving the content of ./output in a ./%Y/%m/%d/fqdn_%H%M%S structure with optional
prefix path.

* Free software: Apache Software License 2.0

Installation
============

::

    pip install robotframework-listener-archive-output

You can also install the in-development version with::

    pip install https://gitlab.com/uhbs/robotframework-listener-archive-output/-/archive/main/robotframework-listener-archive-output-main.zip


Documentation
=============


To use the project:

.. code-block:: python

    import archive
    archive.longest()


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
