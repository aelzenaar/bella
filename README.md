Bella
=====

Bella (short for BeLimDra, 'Better Limit set Drawer') will be an improvement over my
older [Riley computational package](https://github.com/aelzenaar/riley). New features will include:

 - faster group enumeration algorithms
 - more fancy limit set algorithms including the specialised limit set tracing algorithms found in _Indra's Pearls_
 - closer integration with [pandas](https://pandas.pydata.org/)
 - better visualisation tools using [HoloViews](https://holoviews.org/)

Examples
--------
Install the python packages `holoview`, `bokeh`, `panel`, `pandas` installed to try the examples. Then run

    panel serve <filename.py>

to start the HoloViews/Bokeh server.

The `limits.py` file contains an example to dynamically show limit sets for elliptic Riley groups.

The `peripherals.py` file shows the peripheral subgroups of the parabolic Riley groups of the form $ \langle X, W_{p/q} \rangle $ for $ W_{p/q} $ a Farey word.
This shows the power of having HoloViews as a graphics frontend: we can compose two different limit sets with no pain.
