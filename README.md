# Simplex-Algorithm-in-python

Simplex method is largely used to solve LP problems. This is a simplex implementation in python to solve a LP of the form:

max c.T x

subject to Ax ≤ b

x ≥0

To execute it:

```
python3 main.py
```

And the following LP parameters must be typed:

n m

c1 c2 . . . cm

a1,1 a1,2 . . . a1,m b1

a2,1 a2,2 . . . a2,m b2

... ... . . . ... ...

an,1 an,2 . . . an,m bn

where:

* n is the number of restrictions
* m is the number of variables
* ai are the elements of A matrix
* bi are the elements of b vector
* ci are the elements of c vector
