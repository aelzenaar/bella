# Bella: A computational package for Kleinian groups

This is a computational package for dealing with Kleinian groups, particularly aspects related to visualisation and moduli spaces. It is meant to
superceed the earlier [Riley computational package](https://github.com/aelzenaar/riley). Advantages over that software already include speed and ease
of use. New features will include:

 - alternative group enumeration algorithms and limit set algorithms including the specialised limit set tracing algorithms found in _Indra's Pearls_
 - closer integration with [pandas](https://pandas.pydata.org/)
 - better visualisation tools using [HoloViews](https://holoviews.org/)
 - support of $`p`$-adic groups, for which we use the [pyadic](https://pypi.org/project/pyadic/) library; see also the [interesting work of Ari Markowitz](https://github.com/ariymarkowitz/Bruhat-Tits-Tree-Visualiser)


## Background material on Kleinian groups
A Kleinian group is a discrete subgroup of $` \mathrm{PSL}(2,\mathbb{C}) `$. These groups are the holonomy groups of complete hyperbolic 3-orbifolds,
so every complete hyperbolic 3-orbifold is of the form $` \mathbb{H}^3/G `$ for $` G `$ a Kleinian group. For background material in Kleinian groups, see [[B83](#B83),[M87](#M87)].

We are particularly interested in studying a particular moduli space of Kleinian groups, the Riley slice of Schottky space [[KS94](#KS94), [KS98](#KS98)], together with its elliptic
generalisations. Background specific to the Riley slice may be found in the proceedings article [[EMS22b](#EMS22b)] and in my MSc thesis [[Elz22](#Elz22)]. For a more practical
introduction to some of the computational geometry and some very nice pictures, see [[MSW02](#MSW02)] and [its associated website](http://klein.math.okstate.edu/IndrasPearls/).
Many of the computations in this direction are done using the results obtained in our paper [[EMS22a](#EMS22a)].
We also have some further recent results on the Riley slice which are of interest from a computational point of view [[EMS21](#EMS21)]; in a later version of this software we will incorporate some of the insights
from this paper.

The visualisation software was inspired by the [schottky](https://github.com/dannycalegari/schottky) software written by Danny Calegari and Alden Walker.


## Installation
We use the `setuptools` package for ease of installation. Simply run `pip install .` to install.

## The software included

### Python library
The library is called `bella` (so after installing run `import bella` in Python) and includes the following modules:
 * [cayley.py](bella/cayley.py) -- methods for computing with general matrix groups via their Cayley graph (e.g. reducing words, computing limit sets)
 * [farey.py](bella/farey.py) -- methods for working with Farey words and polynomials
 * [riley.py](bella/riley.py) -- methods for working with the Riley slices
 * [chistyakov.py](bella/chistyakov.py) -- methods for embedding elements of $` \mathbb{Q}_p `$ into $` \mathbb{C} `$.


### Examples
Install the python packages `holoview`, `bokeh`, `panel`, `pandas` to try the examples in the `examples` directory.

 - `panel serve limits.py` - dynamically show limit sets for elliptic Riley groups.
 - `panel serve peripherals.py` - dynamically show peripheral subgroups for the parabolic Riley groups.
 - `python padictest.py` - plot the limit set of a $`p`$-adic group.
 - `python test.py` - run profiler for both `GroupCache.free_cayley_graph_mc` and `GroupCache.cayley_graph_mc`.

