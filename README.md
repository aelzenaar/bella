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
We also have some further recent results on the Riley slice which are of interest from a computational point of view [[EMS21](#EMS21)]; our construction of pleating ray neighbourhoods
is used by the function `riley.RileyGroup.guess_radial_coordinate' to approximate the pleating coordinate of an input Riley group.

The visualisation software was inspired by the [schottky](https://github.com/dannycalegari/schottky) software written by Danny Calegari and Alden Walker.


## Installation
We use the `setuptools` package for ease of installation. Simply run `pip install .` to install.

## The software included

### Python library
The library is called `bella` (so after installing run `import bella` in Python) and includes the following modules:
 * [cayley.py](bella/cayley.py) -- methods for computing with general matrix groups via their Cayley graph (e.g. reducing words, computing limit sets)
 * [farey.py](bella/farey.py) -- methods for working with Farey words and polynomials
 * [riley.py](bella/riley.py) -- methods for working with individual Riley groups
 * [moduli.py](bella/moduli.py) -- methods for working globally with a Riley slice
 * [chistyakov.py](bella/chistyakov.py) -- methods for embedding elements of $` \mathbb{Q}_p `$ into $` \mathbb{C} `$ [[C96](#C96)]


### Examples
Install the python packages `holoview`, `bokeh`, `panel`, `pandas`, `mpmath` to try the examples in the `examples` directory.

 - `panel serve limits.py` - dynamically show limit sets for elliptic Riley groups.
 - `panel serve isometric_circles.py` - dynamically show isometric circles for elliptic Riley groups.
 - `panel serve peripherals.py` - dynamically show peripheral subgroups for the parabolic Riley groups.
 - `python padictest.py` - plot the limit set of a $`p`$-adic group.
 - `python test.py` - run profiler for both `cayley.GroupCache.free_cayley_graph_mc` and `cayley.GroupCache.cayley_graph_mc`.
 - `panel serve plotslice.py` - plot the Riley slice both with Riley polynomials and Farey polynomials.
 - `python profileslice.py`  - run the profiler on `moduli.approximate_riley_slice` to check that `try_fast = True` is much faster than `try_fast = False`.
 - `python animate_slices.py` - in `animation/` produce many frames animating the conjectured holomorphic motion of the Riley slices. Use a
    command like `ffmpeg -framerate 30 -pattern_type glob -i 'animation/*.png' -c:v libx264 -pix_fmt yuv420p riley_slice.mp4` to produce a video from these files.
 - `python guessradial.py` - test whether we can guess the radial coordinate using `riley.RileyGroup.guess_radial_coordinate()`.

## References
<a id="B88">[B83]</a>
Alan F. Beardon. *The geometry of discrete groups*. Graduate Texts in Mathematics 91. Springer-Verlag, 1983.

<a id="C96">[C96]</a>
D.V. Chistyakov, “Fractal geometry for images of continuous embeddings of p-adic numbers and solenoids into Euclidean spaces”. In: *Theoretical and Mathematical Physics* (109 1996), pp.1495–1507.

<a id="Elz22">[Elz22]</a>
Alex Elzenaar. “Deformation spaces of Kleinian groups”. MSc thesis. The University of Auckland, 2022.

<a id="EMS21">[EMS21]</a>
Alex Elzenaar, Gaven Martin, and Jeroen Schillewaert. “Approximations of the Riley slice”. November 2021. [arXiv:2111.03230](https://arxiv.org/abs/2111.03230) [math.GT].

<a id="EMS22a">[EMS22a]</a>
Alex Elzenaar, Gaven Martin, and Jeroen Schillewaert. “The combinatorics of Farey words and their traces”. April 2022. [arXiv:2204.08076](https://arxiv.org/abs/2204.08076) [math.GT]. A version with minor corrections is [on my website](https://aelzenaar.github.io/farey/farey.pdf).

<a id="EMS22b">[EMS22b]</a>
Alex Elzenaar, Gaven Martin, and Jeroen Schillewaert. “Concrete one complex dimensional moduli spaces of hyperbolic manifolds and orbifolds”. In: <i>2021-22 MATRIX annals</i>. Ed. by David R. Wood, Jan de Gier, Cheryl E. Prager, and Terrence Tao. MATRIX Book Series 5. Springer, to appear.

<a id="KS94">[KS94]</a>
Linda Keen and Caroline Series. “The Riley slice of Schottky space”. In: *Proceedings of the London Mathematics Society* 3.1 (69 1994), pp. 72–90.

<a id="KS98">[KS98]</a>
Yohei Komori and Caroline Series. “The Riley slice revisited”. In: *The Epstein birthday schrift*. Vol. 1. Geometry and Topology Monographs. 1998, pp. 303–316.

<a id="M87">[M87]</a>
Bernard Maskit. *Kleinian groups*. Grundlehren der mathematischen Wissenshaften 287. Springer-Verlag, 1987.

<a id="MSW02">[MSW02]</a>
David Mumford, Caroline Series, and David Wright. *Indra’s pearls: The vision of Felix Klein*. Cambridge University Press, 2002.
