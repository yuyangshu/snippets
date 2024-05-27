# https://coderzcolumn.com/tutorials/artificial-intelligence/flax-cnn

import jax
import jax.numpy as jnp
import flax.linen as nn

from tensorflow import keras




(X_train, Y_train), (X_test, Y_test) = keras.datasets.fashion_mnist.load_data()

X_train, X_test, Y_train, Y_test = jnp.array(X_train, dtype=jnp.float32),\
                                   jnp.array(X_test, dtype=jnp.float32),\
                                   jnp.array(Y_train, dtype=jnp.float32),\
                                   jnp.array(Y_test, dtype=jnp.float32)

X_train, X_test = X_train.reshape(-1,28,28,1), X_test.reshape(-1,28,28,1)

X_train, X_test = X_train/255.0, X_test/255.0

classes =  jnp.unique(Y_train)

X_train.shape, X_test.shape, Y_train.shape, Y_test.shape


class CNN(nn.Module):
    def setup(self):
        self.conv = nn.Conv(features=64, kernel_size=(3,3), strides=(3,3), padding="VALID", name="CONV1")
        self.linear = nn.Dense(len(classes), name="DENSE")

    def __call__(self, inputs):
        x = nn.relu(self.conv(inputs))

        print("Conv output shape:", x.shape)

        x = x.reshape((x.shape[0], -1))
        x = self.linear(x)

        return nn.softmax(x)

seed = jax.random.PRNGKey(0)

model = CNN()
params = model.init(seed, X_train[:5])



for layer_params in params["params"].items():
    print("Layer Name : {}".format(layer_params[0]))
    weights, biases = layer_params[1]["kernel"], layer_params[1]["bias"]
    print("\tLayer Weights : {}, Biases : {}".format(weights.shape, biases.shape))

preds = model.apply(params, X_train[:5])

preds


# Layer Name : CONV1
# 	Layer Weights : (3, 3, 1, 64), Biases : (64,)
# Layer Name : DENSE
# 	Layer Weights : (5184, 10), Biases : (10,)
# Conv output shape: (5, 9, 9, 64)
