#!/bin/sh

image_scripts="parabolic_slice_hidef.py parabolic_slice_pleating_rays.py apollonian_gasket.py padic.py jorgensen_marden.py geometrically_infinite.py modular_group.py connected_component_bound.py apanasov.py web.py elementary.py beads.py zarrow.py accidental_parabolic.py atom.py riley_slice_cusps.py cusp_groups.py maskit_slice.py fig8lattice.py"

echo "generate_zoo.sh: generating all basic examples that just produce images."
for i in $image_scripts
do
    echo "generate_zoo.sh: running $i"
    python $i
done

