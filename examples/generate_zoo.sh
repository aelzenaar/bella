#!/bin/sh

image_scripts="parabolic_slice_hidef.py apollonian_gasket.py padic.py jorgensen_marden.py geometrically_infinite.py modular_group.py connected_component_bound.py apanasov.py web.py elementary.py beads.py"

echo "generate_zoo.sh: generating all basic examples that just produce images."
for i in $image_scripts
do
    echo "generate_zoo.sh: running $i"
    python $i
done

