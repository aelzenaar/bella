from bella import slices

depth = 20
p = 3
q = 6
elliptic_slice = slices.elliptic_exterior(p, q, depth)

print(elliptic_slice['x'])
