# Contrastive-Inspired Semi-Supervised Learning

This repo is intended to to serve as a framework for comparing loss functions in a semi-supervised learning context. 

### Interesting related papers
- [MixMatch: A Holistic Approach to Semi-Supervised Learning](https://arxiv.org/abs/1905.02249)







## Current Supported Datasets
  - Projection Dataset
  
  - TODO: MNIST
  - TODO: CIFAR-10
 
 ### Projection Dataset:
 Inputs of size 1x2n.
 
 --------------------------------------------------------------------------------
 
 The first n components are a one-hot vector in R<sup>n</sup>. The remaining values are ~ N(0,1)
 
 It is expected that we will learn a matrix [I 0] where I is the R<sup>nxn</sup> identity and 0 the zero matrix in R<sup>nxn</sup>
 
 This dataset is intented to be a simple toy dataset that is easy and quick to train and has a known solution. 
 
 ### MNIST (TODO)
 Inputs of size 28x28x1
 
  --------------------------------------------------------------------------------
 
 The classic [MNIST](http://yann.lecun.com/exdb/mnist/) dataset of handwritten decimal digits. 
 
 This dataset is intented to be the first 'real' dataset for proof of concept training. 

### CIFAR-10
Inputs of size 32x32x3

 --------------------------------------------------------------------------------

The [CIFAR-10](https://www.cs.toronto.edu/~kriz/cifar.html) dataset of color images in 10 categories. 

The next step from MNIST with the same number of categories but much harder to classify.
