
import jax.numpy as jnp


def posemb_sincos_2d(h, w, width, temperature=10_000., dtype=jnp.float32):
  """Follows the MoCo v3 logic."""
  y, x = jnp.mgrid[:h, :w]

  assert width % 4 == 0, "Width must be mult of 4 for sincos posemb"
  omega = jnp.arange(width // 4) / (width // 4 - 1)
  omega = 1. / (temperature**omega)

  y = jnp.einsum("m,d->md", y.flatten(), omega)
  x = jnp.einsum("m,d->md", x.flatten(), omega)

  pe = jnp.concatenate([jnp.sin(x), jnp.cos(x), jnp.sin(y), jnp.cos(y)], axis=1)

  return jnp.asarray(pe, dtype)[None, :, :]


def posemb_mean_sincos_2d(input_size, patch_size, width, scales, temperature=10_000., dtype=jnp.float32):
  h = w = input_size // patch_size
  base_emb = posemb_sincos_2d(h, w, width, temperature, dtype) # (196, 768)
  emb_2d = jnp.reshape(base_emb, [h, w, -1]) # (14, 14, 768)

  # fill the embeddings into an image sized matrix
  f = lambda i, j, k: emb_2d[i // patch_size, j // patch_size, k]
  img = jnp.vectorize(f)(*jnp.indices((input_size, input_size, width))) # (224, 224, 768)

  # calculate weighted embedding for each scale
  mean_embs = []
  for scale in scales:
    h = scale // patch_size # [1, 2, 4, 8]
    f = lambda x: jnp.asarray(jnp.split(x, h, axis=1))
    emb_at_scale = f(f(img))
    mean_embs.append(emb_at_scale.mean(axis=(2, 3))) # [(1, 1, 768), ..., (8, 8, 768)]

  return jnp.concatenate([jnp.reshape(x, (-1, width)) for x in mean_embs + [base_emb]])


emb = posemb_mean_sincos_2d(224, 16, 768, [16, 32, 64, 128])
print(emb, emb.shape)
