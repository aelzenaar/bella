# bella/examples

## Basic examples
Run these with plain vanilla `python [filename]`. The utility bash script `generate_zoo.sh` will run all of the examples that just produce PNG files.
 - [cayley_graph_speed.py](cayley_graph_speed.py) -- demonstrate that walking the Cayley group of a non-free group incurs a massive speed overhead.
 - [parabolic_slice_hidef.py](parabolic_slice_hidef.py) -- draw a PNG file containing a high-res picture of the parabolic Riley slice.
 - [parabolic_slice_pleating_rays.py](parabolic_slice_pleating_rays.py) -- plot rational pleating rays around the parabolic Riley slice.
 - [apollonian_gasket.py](apollonian_gasket.py) -- draw a PNG file containing a picture of the Apollonian Gasket.
 - [padic.py](padic.py) -- demonstrate that it is possible to use other number types (e.g. $` p `$-adic numbers) as long as you are sufficiently masochistic.
 - [farey.py](farey.py) -- produce TeX tables of Farey and Riley words and polynomials.
 - [jorgensen_marden.py](jorgensen_marden.py) -- plot the limit sets of the Jørgensen--Marden groups which are not quasiconformally conjugate but which uniformise homeomorphic 3-manifolds.
 - [geometrically_infinite.py](geometrically_infinite.py) -- plot the limit set of a geometrically infinite group with non-empty domain of discontinuity.
 - [modular_group.py](modular_group.py) -- plot the isometric circles of $` \mathrm{PSL}(2,\mathbb{Z}) `$.
 - [connected_component_bound.py](connected_component_bound.py) -- a Schottky-type group on $` N `$ parabolic generators with $` 2(N-1) `$ components.
 - [apanasov.py](apanasov.py) -- a quasi-Fuchsian group with four components.
 - [web.py](web.py) -- a group which is not quasi-Fuchsian, but has quasi-Fuchsian component stabilisers.
 - [elementary.py](elementary.py) -- an elementary group obtained as the orientation-preserving half of the group of reflections of a parallelogram.
 - [beads.py](beads.py) -- draw limit sets of bead groups along arbitrary polygonal paths.
 - [atom.py](atom.py) -- draw the limit set of an approximation of Accola's atom group (an infinitely generated group).
 - [zarrow.py](zarrow.py) -- draw the limit set of Zarrow's non-classical Schottky group (this group is not Fuchsian but does preserve $\mathbb{R}$).
 - [accidental_parabolic.py](accidental_parabolic.py) -- draw the limit set of a B-group with an accidental parabolic.
 - [riley_slice_cusps.py](riley_slice_cusps.py) -- produce cusp points on the Riley slice corresponding to various irrational numbers.
 - [cusp_groups.py](cusp_groups.py) -- plot the limit sets of some cusp groups.

## Interactive panel scripts
Run these with `panel serve [filename]`. You need the optional `panel` dependency.
 - [parabolic_slices.py](parabolic_slices.py) -- draw a lot of different level sets of the Farey polynomials, and the zero set of the Riley polynomials.
 - [isometric_circles.py](isometric_circles.py) -- dynamically draw isometric circles of Riley groups.
 - [elliptic_parabolic_slice.py](elliptic_parabolic_slice.py) -- draw a particular elliptic slice, showing that non-primitive words give subsets of the slice exterior.
 - [riley_limits.py](riley_limits.py) -- dynamically draw limit sets and fixed points of Riley groups in a very interactive way (this is the replacement for the older `graphical_limits.py`).
 - [peripheral_subgroups.py](peripheral_subgroups.py) -- modification of `limits.py` to highlight peripheral subgroups.
 - [indras_necklace.py](indras_necklace.py) -- draw limit sets of the Indra's Necklace groups, Chapter 6 of _Indra's pearls_.
 - [theta_schottky.py](theta_schottky.py) -- draw limit sets of θ-Schottky groups, Project 4.2 of _Indra's pearls_.
 - [grandma.py](grandma.py) -- draw limit sets of Grandma's Recipe groups, Chapter 8 of _Indra's pearls_.
 - [maskit.py](maskit.py) -- draw limit sets of Maskit groups, Chapter 9 of _Indra's pearls_.
 - [schottky.py](schottky,py) -- draw limit sets of Schottky groups.
 - [lackenby_purcell.py](lackenby_purcell.py) -- draw limit sets of groups with one rank 2 cusp and an additional loxodromic.

## Animation examples
Each of these examples produces the frames for an animation in the subdirectory named the same as the example but without the `.py` suffix. Then
you can run something like

    ffmpeg -framerate 30 -pattern_type glob -i 'animate_slices/*.png' -c:v libx264 -pix_fmt yuv420p animate_slices.mp4

to generate a video file from those frames.

 - [animate_limits_as_slices_vary.py](animate_limits_as_slices_vary.py) -- compute the limit sets of the (θ=0, η=tπ, μ=2i) Riley group as t runs from 0 to 2.
 - [animate_slices.py](animate_slices.py) -- animate primitive Riley slices.
