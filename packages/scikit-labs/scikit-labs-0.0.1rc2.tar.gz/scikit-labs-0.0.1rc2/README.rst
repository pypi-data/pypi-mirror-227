===========================================================
``scikit-labs``: Linear-time Adaptive Best-subset Selection
===========================================================

|pypi| |pyversion| |downloads| |issues| |license|

.. |pypi| image:: https://img.shields.io/pypi/v/scikit-labs
.. |pyversion| image:: https://img.shields.io/pypi/pyversions/scikit-labs
.. |downloads| image:: https://img.shields.io/pypi/dm/scikit-labs
.. |issues| image:: https://img.shields.io/github/issues/abess-team/scikit-labs
.. |license| image:: https://img.shields.io/pypi/l/scikit-labs

Overview
========

Best-subset selection plays a vital role in regression analysis, aiming to identify a parsimonious subset of variables that maximizes prediction accuracy within the resulting linear model. This process is important in various scientific fields, including physics, biology, and medicine, where extensive datasets are routinely generated. Nevertheless, the computational complexity of selecting the best subset from massive datasets presents a formidable challenge, given the problem's well-known NP-hard nature.

To address this challenge, we introduce a new tuning-free iterative algorithm ``scikit-labs`` that capitalizes on a novel subset splicing procedure. Remarkably, under mild conditions, our algorithm demonstrates provable identification of the best subset while maintaining a linear time complexity, achieving optimality in computation and statistics simultaneously. The power of ``scikit-labs`` is numerically certified by extensive test cases.

Quick Start
===========

Installation
------------

Install the stable ``scikit-labs`` Python package from Pypi:

.. code-block:: bash

    pip install scikit-labs


And then the package can be imported as:

.. code-block:: python

    import sklabs


Example
-------

Best subset selection for linear regression on a simulated dataset in Python:

.. code-block:: python

    from sklabs.datasets import make_glm_data
    from sklabs.linear import LinearRegression
    sim_dat = make_glm_data(n = 350, p = 500, k = 6, family = "gaussian")
    model = LinearRegression()
    model.fit(sim_dat.x, sim_dat.y)


Open source software
====================

``scikit-labs`` is a free software and its source code are publicly available in Github. The core framework is programmed in C++, and user-friendly Python interfaces are offered. You can redistribute it and/or modify it under the terms of the GPL-v3 License. We welcome contributions for ``scikit-labs``, especially stretching ``scikit-labs`` to the other best subset selection problems.

Citation
========

If you use ``scikit-labs`` or reference our tutorials in a presentation or publication, we would appreciate citations of our library.

.. code-block:: latex

    @article{scikit-labs,
        title   = {Selecting the Best Subset in Regression in Linear Time},
        author  = {Jin Zhu and Junxian Zhu and Junhao Huang and Xueqin Wang and Heping Zhang},
        journal = {Submitted},
        year    = {2023},
    }

.. References
.. ==========
