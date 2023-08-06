# bella/examples

## Basic examples
Run these with plain vanilla `python [filename]`.
 - [parabolic_slice_hidef.py](parabolic_slice_hidef.py) -- draw a PNG file containing a high-res picture of the parabolic Riley slice to high definition.

TODO: give some Farey polynomial examples

## Interactive panel scripts
Run these with `panel serve [filename]`. You need the optional `panel` dependency.
 - [parabolic_slices.py](parabolic_slices.py) -- draw a lot of different level sets of the Farey polynomials, and the zero set of the Riley polynomials.
 - [isometric_circles.py](isometric_circles.py) -- dynamically draw isometric circles of Riley groups.
 - [elliptic_parabolic_slice.py](elliptic_parabolic_slice.py) -- draw a particular elliptic slice, showing that non-primitive words give subsets of the slice exterior.
 - [limits.py](limits.py) -- dynamically draw limit sets and fixed points of Riley groups.
 - [peripheral_subgroups.py](peripheral_subgroups.py) -- modification of `limits.py` to highlight peripheral subgroups.

## Animation examples
Each of these examples produces the frames for an animation in the subdirectory named the same as the example but without the `.py` suffix. Then
you can run something like

    ffmpeg -framerate 30 -pattern_type glob -i 'animate_slices/*.png' -c:v libx264 -pix_fmt yuv420p animate_slices.mp4

to generate a video file from those frames.

 - [animate_limits_as_slices_vary.py](animate_limits_as_slices_vary.py) -- compute the limit sets of the (θ=0, η=tπ, μ=2i) Riley group as t runs from 0 to 2.
 - [animate_slices.py](animate_slices.py) -- animate primitive Riley slices.
