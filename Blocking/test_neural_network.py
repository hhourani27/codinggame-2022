import numpy as np

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def relu(z):
    result = [max(0,zi) for zi in z[0]]
    return np.array(result)

class Network:
    # sizes is a list of the number of nodes in each layer
    def __init__(self, sizes, biases, weights):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = biases
        self.weights = weights

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            z = np.matmul(w, a.T) + b.T
            a = relu(z)
        return a

#%%
sizes = [169*4,200,1]
biases = [np.random.randn(y, 1) for y in sizes[1:]]
weights = [np.random.randn(y, x) for x,y in zip(sizes[:-1], sizes[1:])]
#%%
net = Network(sizes, biases, weights)
x = np.random.randint(0,2,169*4)
result = net.feedforward(x)

#%%
(400000)/(2*(169*4+1))


