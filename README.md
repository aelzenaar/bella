Bella
=====

Bella (short for BeLimDra, 'Better Limit set Drawer') will be an improvement over my
older [Riley computational package](https://github.com/aelzenaar/riley). New features will include:

 - faster group enumeration algorithms
 - more fancy limit set algorithms including the specialised limit set tracing algorithms found in _Indra's Pearls_
 - closer integration with [pandas](https://pandas.pydata.org/)
 - better visualisation tools using [HoloViews](https://holoviews.org/)

Installation
------------
Run `pip install .` to install.

Examples
--------
Install the python packages `holoview`, `bokeh`, `panel`, `pandas` to try the examples in the `examples` directory.

 - `panel serve limits.py` - dynamically show limit sets for elliptic Riley groups.
 - `panel serve peripherals.py` - dynamically show peripheral subgroups for the parabolic Riley groups.
 - `python padictest.py` - plot the limit set of a $`p`$-adic group.
 - `python test.py` - run profiler for both `GroupCache.free_cayley_graph_mc` and `GroupCache.cayley_graph_mc`.

