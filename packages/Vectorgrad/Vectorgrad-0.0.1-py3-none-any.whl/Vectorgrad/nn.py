import numpy as np
from .engine import Vector

class Module:
    def zero_grad(self):
        for p in self.parameters():
            p.grad = np.zeros_like(p.grad)

    def parameters(self):
        return []

class Layer(Module):
    def __init__(self, nin, nout, act_fn):
        self.w = Vector(np.random.randn(nout, nin))
        self.b = Vector(np.random.randn(nout))
        self.fn = act_fn

    def __call__(self, inp):
        #assert inp.shape[0] == self.w.data.shape[1], f"Weight matrix columns{self.w.data.shape[1]} not equal to input rows{inp.shape[0]}"
        lin_combo = self.w.matmul(inp) + self.b
        act = self.fn(lin_combo) if self.fn else lin_combo
        return act

    def parameters(self):
        return [self.w, self.b]

    def __repr__(self):
        return f"{str(self.fn.__name__) if self.fn else 'Linear'} Layer(number of Neurons = {self.b.data.shape[0]})"

class MLP(Module):
    def __init__(self,nin, nouts, act_fns):
        sz = [nin] + nouts
        self.layers = [Layer(sz[i], sz[i+1], act_fns[i]) for i in range(len(nouts))]

    def __call__(self,inp):
        for lay in self.layers:
            inp = lay(inp)
        return inp

    def parameters(self):
        return [p for layer in self.layers for p in layer.parameters()]

    def __repr__(self):
        return f"MLP of [{', '.join(str(layer) for layer in self.layers)}]"


        