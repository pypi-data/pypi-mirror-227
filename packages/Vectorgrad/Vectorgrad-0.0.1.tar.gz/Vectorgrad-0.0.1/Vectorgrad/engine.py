#Let's write Vector class (new version of original value)
import numpy as np

class Vector:
    #want Vector to always store data into numpy arrays of type float 32 (whether the Vector just stores a singular scalar or not)
    def __init__(self,data, _children = (), _op = '', requires_grad = True):
        self.data = (np.array(data)).astype(np.float32)
        self.grad = np.zeros_like(self.data)
        self._prev = set(_children)
        self._op = _op
        self._backward = lambda: None
        self.requires_grad = requires_grad

    #add is unique in that it allows us to add tensors as well as scalars
    def __add__(self,other):
        other = other if isinstance(other,Vector) else Vector(other, requires_grad = False)
        out = Vector(self.data + other.data, (self,other), '+')
        
        def _backward():
            self.grad += out.grad
            if other.requires_grad: other.grad += out.grad
        out._backward = _backward
        return out

    #multiply works for scalar multiplication, element-wise multiplication, and multiplying a tensor by a scalar
    def __mul__(self,other):
        other = other if isinstance(other,Vector) else Vector(other, requires_grad = False)
        out = Vector(self.data*other.data, (self,other), '*')
        def _backward():
            self.grad += other.data * out.grad
            if other.requires_grad: other.grad += self.data * out.grad
        out._backward = _backward

        return out
            

    #Next we will implement scalar/tensor exponentiation (element-wise for tensor)
    def __pow__(self,other):
        assert isinstance(other, (int, float)), "only supporting int/float powers for now"
        out = Vector(self.data**other, (self,), f'**{other}')

        def _backward():
            self.grad += (other * self.data**(other-1)) * out.grad
        out._backward = _backward
        return out

    #later we will want to test to see if we can include other.requires_grad = False here too,
    #I will avoid that for now in case it causes future bugs
    def matmul(self,other):
        other = other if isinstance(other, Vector) else Vector(other)
        out = Vector(np.dot(self.data,other.data), (self, other), 'matmul')
        def _backward():
            self.grad += np.dot(out.grad[:, np.newaxis], other.data[np.newaxis, :]) #we add in new axes so that its treated as row vector matmul col vector
            other.grad += np.dot(self.data.T, out.grad)
        out._backward = _backward
        return out

    def relu(self):
        out = Vector(np.maximum(self.data, 0), (self,), 'ReLU')

        def _backward():
            self.grad += np.where(self.data < 0, 0, 1) * out.grad
        out._backward = _backward
        return out

    def tanh(self):
        out = Vector(np.tanh(self.data), (self,), 'Tanh')

        def _backward():
            self.grad += (1 - out.data**2)*out.grad
        out._backward = _backward
        return out

    #The sum function allows us to sum all the elements in a tensor together (if no axis provided will sum up all elements together)
    #Additionally you can provide the axis argument if you want to sum along the columns (0), or along the rows (1)
    def sum(self,axis = None):
        out = Vector(np.sum(self.data,axis = axis), (self,), 'SUM')
        
        def _backward():
            output_shape = np.array(self.data.shape)
            output_shape[axis] = 1
            tile_scaling = self.data.shape // output_shape
            grad = np.reshape(out.grad, output_shape)
            self.grad += np.tile(grad, tile_scaling)
            
        out._backward = _backward

        return out

    #Takes in a tensor -> returns tensor of the same size but now its a probability distribution
    def softmax(self):
        exps = np.exp(self.data)
        out = Vector(exps/ np.sum(exps), (self,), 'softmax')

        def _backward(): #only calculates gradients for vectors, dont try this with matrices!!
            n = self.data.shape[0]
            softmax_matr = np.zeros((n,n))
            softmax_matr[np.diag_indices(n)] = out.data
            softmax_matr -= np.outer(out.data, out.data)
            self.grad += np.dot(out.grad, softmax_matr)
        out._backward = _backward

        return out

    def log(self):
        out = Vector(np.log(self.data), (self,), 'log')
        def _backward():
            self.grad += out.grad/self.data
        out._backward = _backward
        return out

    def backward(self):
        # topological order all of the children in the graph
        topo = []
        visited = set()
        def build_topo(v):
            if v not in visited:
                visited.add(v)
                for child in v._prev:
                    build_topo(child)
                topo.append(v)
        build_topo(self)
        # go one variable at a time and apply the chain rule to get its gradient
        self.grad = np.ones_like(self.data)
        for v in reversed(topo):
            v._backward()

    def __neg__(self): # -self
        return self * -1

    def __radd__(self, other): # other + self
        return self + other

    def __sub__(self, other): # self - other
        return self + (-other)

    def __rsub__(self, other): # other - self
        return other + (-self)

    def __rmul__(self, other): # other * self
        return self * other

    def __truediv__(self, other): # self / other
        return self * other**-1

    def __rtruediv__(self, other): # other / self
        return other * self**-1

    def __repr__(self):
        return f"Vector(data={self.data}, grad={self.grad if self.requires_grad else 'N/A'})"
