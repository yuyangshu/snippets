import jax.numpy as jnp


# (2, 2)
A = jnp.array([[1,2], [3,4]])
print(A)

# (1, 2)
B = jnp.array([[3,4]])
print(B)

# (2, 2)
# each inner vector is added with B
C = A + B
print(C)
print(C.shape)


# [[1 2]
#  [3 4]]
# [[3 4]]
# [[4 6]
#  [6 8]]
# (2, 2)
