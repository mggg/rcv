===
rcv
===

.. image:: https://travis-ci.com/mggg/rcv.svg?branch=master
    :target: https://travis-ci.com/mggg/rcv
    :alt: Build Status
.. image:: https://codecov.io/gh/mggg/rcv/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/mggg/rcv
    :alt: Code Coverage
.. image:: https://readthedocs.org/projects/rcv-py/badge/?version=latest
    :target: https://rcv-py.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://badge.fury.io/py/rcv.svg
    :target: https://https://pypi.org/project/rcv/
    :alt: PyPI Package

``rcv`` is a Python library for tabulating ballots from ranked-choice elections.
The package is distributed under the BSD 3-Clause License.

Examples
========

.. code-block:: python

    from rcv import FractionalSTV, PreferenceSchedule

    schedule = PreferenceSchedule.from_ballots([
        ("A", "B", "C"),
        ("A", "C", "B"),
        ("A", "C", "B"),
    ])

    stv = FractionalSTV(schedule, seats=2)
    winners = stv.elect()

    assert winners == {"A", "C"}
