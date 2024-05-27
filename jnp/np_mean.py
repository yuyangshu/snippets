import jax
import jax.numpy as jnp
import jax.lax as lax


# (2, 2, 3)
A = jnp.array([[[1, 2, 3], [2, 4, 6]],
                [[3, 6, 9], [4, 8, 12]]])

# mean
mean = A.mean(axis=(0, 1))
print("mean", mean)

# sum
sum = A.sum(axis=(0, 1))
print("sum", sum)

# sum of sub matrix
def f(i, j, k):
    return A[i // 2, j // 2, k]

# enlarge matrix
# (4, 4, 3)
B = jnp.vectorize(f)(*jnp.indices((4, 4, 3)))
print("B", B, B.shape)

# dynamic slice
C = lax.dynamic_slice(B, (0, 0, 0), (2, 2, 3))
print("C", C)

# split
D = jnp.asarray(jnp.split(B, 2, axis=1))
print("D", D)
E = jnp.asarray(jnp.split(D, 2, axis=1))
print("E", E, E.shape)
print("E[0, 1]", E[0, 1], E[0, 1].shape)

# apply twice
f = lambda X: jnp.asarray(jnp.split(X, 2, axis=1))
F = f(f(B))
print("F", F, F.shape)

# vmap?
f_v = jax.vmap(f, ((0, 1)))
G = f_v(B)
print("G", G, G.shape)


# mean [2.5 5.  7.5]
# sum [10 20 30]
# B [[[ 1  2  3]
#   [ 1  2  3]
#   [ 2  4  6]
#   [ 2  4  6]]

#  [[ 1  2  3]
#   [ 1  2  3]
#   [ 2  4  6]
#   [ 2  4  6]]

#  [[ 3  6  9]
#   [ 3  6  9]
#   [ 4  8 12]
#   [ 4  8 12]]

#  [[ 3  6  9]
#   [ 3  6  9]
#   [ 4  8 12]
#   [ 4  8 12]]] (4, 4, 3)
# C [[[1 2 3]
#   [1 2 3]]

#  [[1 2 3]
#   [1 2 3]]]
# D [[[[ 1  2  3]
#    [ 1  2  3]]

#   [[ 1  2  3]
#    [ 1  2  3]]

#   [[ 3  6  9]
#    [ 3  6  9]]

#   [[ 3  6  9]
#    [ 3  6  9]]]


#  [[[ 2  4  6]
#    [ 2  4  6]]

#   [[ 2  4  6]
#    [ 2  4  6]]

#   [[ 4  8 12]
#    [ 4  8 12]]

#   [[ 4  8 12]
#    [ 4  8 12]]]]
# E [[[[[ 1  2  3]
#     [ 1  2  3]]

#    [[ 1  2  3]
#     [ 1  2  3]]]


#   [[[ 2  4  6]
#     [ 2  4  6]]

#    [[ 2  4  6]
#     [ 2  4  6]]]]



#  [[[[ 3  6  9]
#     [ 3  6  9]]

#    [[ 3  6  9]
#     [ 3  6  9]]]


#   [[[ 4  8 12]
#     [ 4  8 12]]

#    [[ 4  8 12]
#     [ 4  8 12]]]]] (2, 2, 2, 2, 3)
# E[0, 1] [[[2 4 6]
#   [2 4 6]]

#  [[2 4 6]
#   [2 4 6]]] (2, 2, 3)
# F [[[[[ 1  2  3]
#     [ 1  2  3]]

#    [[ 1  2  3]
#     [ 1  2  3]]]


#   [[[ 2  4  6]
#     [ 2  4  6]]

#    [[ 2  4  6]
#     [ 2  4  6]]]]



#  [[[[ 3  6  9]
#     [ 3  6  9]]

#    [[ 3  6  9]
#     [ 3  6  9]]]


#   [[[ 4  8 12]
#     [ 4  8 12]]

#    [[ 4  8 12]
#     [ 4  8 12]]]]] (2, 2, 2, 2, 3)