## VectorGrad

Welcome to VectorGrad, a spin-off of the original [micrograd](https://github.com/karpathy/micrograd).

This is an automatic differentiation library that supports tensor operations and calculus. Here's why I built it:
1) It's much more lightweight and readable compared to bigger libraries such as TensorFlow so users can get a better idea
of how everything works

2) Its orders of magnitude more computationally efficient than its predecessor as it leverages numpy statically typed arrays
and operations to bundle parameters and leverage parallelism and SIMD calculations

3) It includes a dynamic and customizable neural network library that can build neural networks of arbitrary size and complexity,
and also allows users to choose the activation function at each layer to allow for more robust model architecture
