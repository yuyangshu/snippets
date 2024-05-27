import jax.numpy as jnp


# (2, 2)
A = jnp.array([[1,2], [3,4]])

def enlarge(i, j):
    return A[i // 2, j // 2]

B = jnp.vectorize(enlarge)(*jnp.indices((4, 4)))

print(B, B.shape)

# [[1 1 2 2]
#  [1 1 2 2]
#  [3 3 4 4]
#  [3 3 4 4]] (4, 4)
