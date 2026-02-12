# hierarchical-brain-arxiv

Intelligent Matrix Exponentiation
Thomas Fischbacher Iulia M. Comsa Krzysztof Potempa
Moritz Firsching Luca Versari Jyrki Alakuijala
Google Research
Brandschenkestrasse 110, 8002 Z¨urich, Switzerland
{tfish,iuliacomsa,dickstra,firsching,veluca,jyrki}@google.com
Abstract
We present a novel machine learning architecture that uses the exponential of a sin-
gle input-dependent matrix as its only nonlinearity. The mathematical simplicity
of this architecture allows a detailed analysis of its behaviour, providing robustness
guarantees via Lipschitz bounds. Despite its simplicity, a single matrix exponential
layer already provides universal approximation properties and can learn fundamen-
tal functions of the input, such as periodic functions or multivariate polynomials.
This architecture outperforms other general-purpose architectures on benchmark
problems, including CIFAR-10, using substantially fewer parameters.
1 Introduction
Deep neural networks (DNNs) synthesize highly complex functions by composing a
large number of neuronal units, each featuring a basic and usually 1-dimensional non-
linear activation function f : R1 → R1. While highly successful in practice, this
approach also has disadvantages. In a conventional DNN, any two activations only
ever get combined through summation. This means that such a network requires an
increasing number of parameters to express more complex functions even as simple as
multiplication. This approach of composing simple functions does not generalize well
outside the boundaries of the training data.
An alternative to the composition of many 1-dimensional functions is using a sim-
ple higher-dimensional nonlinear function f : Rm→ Rn. A single multidimensional
nonlinearity may be desirable because it could express more complex relationships
between input features with potentially fewer parameters and fewer mathematical op-
erations.
The matrix exponential stands out as a promising but overlooked candidate for
a higher-dimensional nonlinearity that may be used as a building block for machine
learning models. The matrix exponential is a smooth function governed by a relatively
simple equation that yields desirable mathematical properties. It has applications in
solving linear differential equations and plays a prominent role in the theory of Lie
1
arXiv:2008.03936v1  [cs.LG]  10 Aug 2020
groups, an algebraic structure widely used throughout many branches of mathematics
and science.
We propose a novel ML architecture for supervised learning whose core element
is a single layer (henceforth referred to as “M-layer”), that computes a single ma-
trix exponential , where the matrix to be exponentiated is an afﬁne function of the
input features. We show that the M-layer has universal approximator properties and
allows closed-form per-example bounds for robustness. We demonstrate the ability
of this architecture to learn multivariate polynomials, such as matrix determinants,
and to generalize periodic functions beyond the domain of the input without any fea-
ture engineering. Furthermore, the M-layer achieves results comparable to recently-
proposed non-specialized architectures on image recognition datasets. We provide
open-source TensorFlow code that implements the M-layer: https://github.
com/google-research/google-research/tree/master/m_layer.
2 Related Work
Neuronal units with more complex activation functions have been proposed. One such
example are sigma-pi units [RHM86], whose activation function is the weighted sum
of products of its inputs. More recently, neural arithmetic logic units have been intro-
duced [THR+18], which can combine inputs using multiple arithmetic operators and
generalize outside the domain of the training data. In contrast with these architectures,
the M-layer is not based on neuronal units with multiple inputs, but uses a single ma-
trix exponential as its nonlinear mapping function. Through the matrix exponential,
the M-layer can easily learn mathematical operations more complex than addition, but
with simpler architecture. In fact, as shown in Section 3.3, the M-layer can be regarded
as a generalized sigma-pi network with built-in architecture search, in the sense that it
learns by itself which arithmetic graph should be used for the computation.
Architectures with higher-dimensional nonlinearities are also already used. The
softmax function is an example for a widely-used such nonlinear activation function
that solves a speciﬁc problem, typically in the ﬁnal layer of classiﬁers. Like the M-
layer, it has extra mathematical structure. For example, a permutation of the softmax
inputs produces a corresponding permutation of the outputs. Maxout networks also act
on multiple units and have been successful in combination with dropout [GWFM+13].
In radial basis networks [PS91], each hidden unit computes a nonlinear function of
the distance between its own learned centroid and a single point represented by a vec-
tor of input coordinates. Capsule networks [SFH17] are another recent example of
multidimensional nonlinearities. Similarly, the M-layer uses the matrix exponential
as a single high-dimensional nonlinearity, therefore creating additional mathematical
structure that potentially allows solving problems using fewer parameters than compo-
sitional architectures.
Matrix exponentiation has a natural alternative interpretation in terms of an or-
dinary differential equation (ODE). As such, the M-layer can be compared to other
novel ODE-related architectures that have been proposed recently. In particular, neu-
ral ordinary differential equations (NODE) [CRBD18] and their augmented extensions
(ANODE) [DDT19] have recently received attention. We discuss this in Section 3.6.
2
U T
exp(·)
S
x U x T U x exp(T U x) S exp(T U x)
Figure 1: Schematic diagram of the M-layer architecture.
Existing approaches to certifying the robustness of neural networks can be split
into two different categories. Some approaches [PRGS17] mathematically analyze a
network layer by layer, providing bounds on the robustness of each layer, that then
get multiplied together. This kind of approach tends to give fairly loose bounds,
due to the inherent tightness loss from composing upper bounds. Other approaches
[SGPV18, SGPV19] use abstract interpretation on the evaluation of the network to
provide empirical robustness bounds. In contrast, using the fact that the M-layer archi-
tecture has a single layer, in Section 3.7 we obtain a direct bound on the robustness on
the whole network by analyzing the explicit formulation of the computation.
3 Architecture
We start this section by refreshing the deﬁnition of the matrix exponential. We then
deﬁne the proposed M-layer model and explain its ability to learn particular func-
tions such as polynomials and periodic functions. Finally, we provide closed-form
per-example robustness guarantees.
3.1 Matrix Exponentiation
The exponential of a square matrixM is deﬁned as:
exp(M) =
∞∑
k=0
1
k!Mk (1)
The matrix powerMk is deﬁned inductively asM 0 =I,Mk+1 =M·Mk, using
the associativity of the matrix product; it is not an element-wise matrix operation.
Note that the expansion of exp(M) in Eq. (1) is ﬁnite for nilpotent matrices. A
matrix M is called nilpotent if there exists a positive integer k such that Mk = 0 .
Strictly upper triangular matrices are a canonical example.
3
Multiple algorithms for computing the matrix exponential efﬁciently have been
proposed [MV03]. TensorFlow implements tf.linalg.expm using the scaling and
squaring method combined with the Pad´e approximation [Hig05].
3.2 M-Layer Deﬁnition
At the core of the proposed architecture is an M-layer that computes a single matrix
exponential, where the matrix to be exponentiated is an afﬁne function of all of the
input features. In other words, an M-layer replaces an entire stack of hidden layers in
a DNN.
Figure 1 shows a diagram of the proposed architecture. We exemplify the architec-
ture as applied to a standard image recognition dataset, but we note that this formulation
is applicable to any other type of problem by adapting the relevant input indices. In the
following equations, generalized Einstein summation is performed over all right-hand
side indices not seen on the left-hand side. This operation is implemented in Tensor-
Flow by tf.einsum.
Consider an example input image, encoded as a3-index arrayXyxc, wherey,x and
c are the row index, column index and color channel index, respectively. The matrixM
to be exponentiated is obtained as follows, using the trainable parameters ˜Tajk, ˜Uaxyc
and ˜Bjk:
M = ˜Bjk + ˜Tajk ˜UayxcXyxc (2)
X is ﬁrst projected linearly to a d-dimensional latent feature embedding space by
˜Uayxc. Then, the 3-index tensor ˜Tajk maps each such latent feature to ann×n matrix.
Finally, a bias matrix ˜Bjk is added to the feature-weighted sum of matrices. The result
is a matrix indexed by row and column indicesj andk.
We remark that it is possible to contract the tensors ˜T and ˜U in order to simplify
the architecture formula, but partial tensor factorization provides regularization by re-
ducing the parameter count.
An outputpm is obtained as follows, using the trainable parameters ˜Smjk and ˜Vm:
pm = ˜Vm + ˜Smjk exp(M)jk (3)
The matrix exp(M), indexed by row and column indices j andk in the same way as
M, is projected linearly by the 3-index tensor ˜Smjk, to obtain a h-dimensional output
vector. The bias-vector ˜Vm turns this linear mapping into an afﬁne mapping. The
resulting vector may be interpreted as accumulated per-class evidence and, if desired,
may then be mapped to a vector of probabilities via softmax.
Training is done conventionally, by minimizing a loss function such as theL2 norm
or the cross-entropy with softmax, using backpropagation through matrix exponentia-
tion.
The nonlinearity of the M-layer architecture is provided by the Rd→ Rh mapping
v↦→ ˜Vm + ˜Smjk exp(M)jk. The count of trainable parameters of this component is
dn2 +n2 +n2h +h. This count comes from summing the dimensions of ˜Tajk, ˜Bjk,
˜Smjk, and ˜Vm, respectively. We note that this architecture has some redundancy in
its parameters, as one can freely multiply the T andU tensors by a d×d real matrix
4
and, respectively, its inverse, while preserving the computed function. Similarly, it is
possible to multiply each of then×n parts of the tensors ˜T and ˜S, as well asB, by both
ann×n matrix and its inverse. In other words, any pair of real invertible matrices of
sizesd×d andn×n can be used to produce a new parametrization that still computes
the same function.
3.3 Feature Crosses and Universal Approximation
A key property of the M-layer is its ability to generate arbitrary exponential-polynomial
combinations of the input features. For classiﬁcation problems, M-layer architectures
are a superset of multivariate polynomial classiﬁers, where the matrix size constrains
the complexity of the polynomial while at the same time not uniformly constraining
its degree. In other words, simple multivariate polynomials of high degree compete
against complex multivariate polynomials of low degree.
We provide a universal approximator proof for the M-layer in the Supplementary
Material, which relies on its ability to express any multivariate polynomial in the input
features if a sufﬁciently large matrix size is used. We provide here an example that
illustrates how feature crosses can be generated through the matrix exponential.
Consider a dataset with the feature vector (φ0,φ 1,φ 2) given by the ˜U·x tensor
contraction, where the relevant quantities for the ﬁnal classiﬁcation of an example are
assumed to be φ0, φ1, φ2, φ0φ1, and φ1φ2
2. To learn this dataset, we look for an
exponentiated matrix that makes precisely these quantities available to be weighted by
the trainable tensor ˜S. To do this, we deﬁne three7× 7 matricesT0jk,T1jk, andT2jk
asT001 = T102 = T203 = 1,T024 = T225 = 2,T256 = 3, and 0 otherwise. We then
deﬁne the matrixM as:
M =φ0T0 +φ1T1 +φ2T2 =


0 φ0 φ1 φ2 0 0 0
0 0 0 0 0 0 0
0 0 0 0 2 φ0 2φ2 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 3 φ2
0 0 0 0 0 0 0


Note that M is nilpotent, as M 4 = 0 . Therefore, we obtain the following matrix
exponential, which contains the desired quantities in its leading row:
exp(M) =I +M + 1
2M 2 + 1
6M 3 =
=


1 φ0 φ1 φ2 φ0φ1 φ1φ2 φ1φ2
2
0 1 0 0 0 0 0
0 0 1 0 2 φ0 2φ2 3φ2
2
0 0 0 1 0 0 0
0 0 0 0 1 0 0
0 0 0 0 0 1 3 φ2
0 0 0 0 0 0 1


The same technique can be employed to encode any polynomial in the input features
using a n×n matrix, where n is one unit larger than the total number of features
plus the intermediate and ﬁnal products that need to be computed. The matrix size can
be seen as regulating the total capacity of the model for computing different feature
crosses.
5
With this intuition, one can read the matrix as a “circuit breadboard” for wiring up
arbitrary polynomials. When evaluated on features that only take values 0 and 1, any
Boolean logic function can be expressed.
3.4 Feature Periodicity
While the M-layer is able to express a wide range of functions using the exponential
of nilpotent matrices, non-nilpotent matrices can bring additional utility. One possible
application of non-nilpotent matrices is learning the periodicity of input features. This
is a problem where conventional DNNs struggle, as they cannot naturally generalize
beyond the distribution of the training data. Here we illustrate how matrix exponentials
can naturally ﬁt periodic dependency on input features, without requiring an explicit
speciﬁcation of the periodic nature of the data.
Consider the matrixMr =
(0−ω
ω 0
)
. We have exp(tMr) =
(cosωt− sinωt
sinωt cosωt
)
, which
is a 2d rotation by an angle of ωt and thus periodic in t with period 2π/ω. This
setup can ﬁt functions that have an arbitrary period. Moreover, this representation
of periodicity naturally extrapolates well when going beyond the range of the initial
numerical data.
3.5 Connection to Lie Groups
The M-layer has a natural connection to Lie groups. Lie groups can be thought of as a
model of continuous symmetries of a system such as rotations. There is a large body
of mathematical theory and tools available to study the structure and properties of Lie
groups [Gil08, Gil12], which may ultimately also help for model interpretability.
Every Lie group has associated a Lie algebra, which can be understood as the space
of the small perturbations with which it is possible to generate the elements of the Lie
group. As an example, the set of rotations of 3-dimensional space forms a Lie group;
the corresponding algebra can be understood as the set of rotation axes in3 dimensions.
Lie groups and algebras can be represented using matrices, and by computing a matrix
exponential one can map elements of the algebra to elements of the group.
In the M-layer architecture, the role of the 3-index tensor ˜T is to form a matrix
whose entries are afﬁne functions of the input features. The matrices that compose ˜T
can be thought of as generators of a Lie algebra. Building M corresponds to selecting
a Lie algebra element. Matrix exponentiation then computes the corresponding Lie
group element.
As rotations are periodic and one of the simplest forms of continuous symmetries,
this perspective is useful for understanding the ability of the M-layer to learn periodic-
ity in input features.
3.6 Dynamical Systems Interpretation
Recent work has proposed a dynamical systems interpretation of some DNN archi-
tectures. The NODE architecture [CRBD18] uses a nonlinear and not time-invariant
ODE that is provided by trainable neural units, and computes the time evolution of
6
a vector that is constructed from the input features. This section discusses a similar
interpretation of the M-layer.
Consider an M-layer with ˜T deﬁned as ˜T012 = ˜T120 = ˜T201 = +1, ˜T210 = ˜T102 =
˜T021 =−1, and 0 otherwise, with ˜U as the 3× 3 identity matrix, and with ˜B = 0 .
Given an input vectora, the corresponding matrixM is then
( 0 a2 −a1
−a2 0 a0
a1 −a0 0
)
. Plugging
M into the linear and time invariant (LTI) ODEd/dtY (t) = MY (t), we can observe
that the ODE describes a rotation around the axis deﬁned by a. Moreover, a solution
to this ODE is given by Y (t) = exp(tM)Y (0). Thus, by choosing Smjk = Y (0)k if
m = j and 0 otherwise, the above M-layer can be understood as applying a rotation
with input dependent angular velocity to some basis vector over a unit time interval.
More generally, we can consider the input features to provide afﬁne parameters
that deﬁne a time-invariant linear ODE, and the output of the M-layer to be an afﬁne
function of a vector that has evolved under the ODE over a unit time interval. In
contrast, the NODE architecture uses a non-linear ODE that is not input dependent,
which gets applied to an input-dependent feature vector.
3.7 Certiﬁed Robustness
We show that the mathematical structure of the M-layer allows a novel proof technique
to produce closed-form expressions for guaranteed robustness bounds.
For any matrix norm∥·∥, we have [RC94]:
∥exp(X +Y )− exp(X)∥≤∥ Y∥ exp(∥Y∥) exp(∥X∥)
We also make use of the fact that ∥M∥F ≤√n∥M∥2 for any n×n matrix, where
∥·∥F is the Frobenius norm and ∥·∥2 is the 2-norm of a matrix. We recall that the
Frobenius norm of a matrix is equivalent to the 2-norm of the vector formed from the
matrix entries.
LetM be the matrix to be exponentiated corresponding to a given input example
x, and let M′ be the deviation to this matrix that corresponds to an input deviation
of ˜x, i.e. M +M′ is the matrix corresponding to input example x + ˜x. Given that
the mapping between x and M is linear, there is a per-model constant δin such that
∥M′∥2≤δin∥˜x∥∞.
The 2-norm of the difference between the outputs can be bound as follows:
∥∆o∥2≤ ∥ S∥2∥exp(M +M′)− exp(M)∥F≤
≤ √n∥S∥2∥exp(M +M′)− exp(M)∥2≤
≤ √n∥S∥2∥M′∥2 exp(∥M′∥2) exp(∥M∥2)≤
≤ √n∥S∥2δin∥˜x∥∞ exp(δin∥˜x∥∞) exp(∥M∥2)
where∥S∥2 is computed by consideringS ah×n·n rectangular matrix, and the ﬁrst
inequality follows from the fact that the tensor multiplication byS can be considered a
matrix-vector multiplication between S and the result of matrix exponential seen as a
n·n vector.
This inequality allows to compute the minimal L∞ change required in the input
given the difference between the amount of accumulated evidence between the most
7
−10 −5 0 5 10
−10
−5
0
5
10
(a) ReLU
−10 −5 0 5 10
−10
−5
0
5
10
(b) tanh
−10 −5 0 5 10
−10
−5
0
5
10
(c) M-layer
Figure 2: Comparison of ReLU/tanh DNN and M-layer classiﬁcation boundaries on a
double spiral (“Swiss roll”) classiﬁcation task.
8
likely class and other classes. Moreover, considering that ∥x∥∞ is bounded from
above, for example by 1 in the case of CIFAR-10, we can obtain a Lipschitz bound
by replacing the exp(δin∥˜x∥∞) term with a exp(δin) term.
4 Results
In this section, we demonstrate the performance of the M-layer on multiple benchmark
tasks, in comparison with more traditional architectures. We ﬁrst investigate the shape
of the classiﬁcation boundaries in a classic double spiral problem. We then show that
the M-layer is able to learn determinants of matrices up to size5×5, periodic functions
in the presence of low noise, and image recognition datasets at a level competitive with
other non-specialized architectures. For CIFAR-10, we compare the training times and
robustness to those of traditional DNNs.
The following applies for all experiments below, unless otherwise stated. DNN
models are initialized using uniform Glorot initialization [GB10], while M-layer mod-
els are initialized with normally distributed values with mean 0 and σ = 0.05. To
enhance training stability and model performance, an activity regularization is per-
formed on the output of the M-layer. This is achieved by adding λ∥exp(M)∥2
F to the
loss function with a value ofλ equal to 10−4. This value is chosen because it performs
best on the CIFAR-10 dataset from a choice of 10−3, 5· 10−3, 10−4, 5· 10−4, and
5· 10−5.
4.1 Learning Double Spirals
To compare the classiﬁcation boundaries generated by the M-layer with those of more
traditional architectures, we train DNNs with ReLU and tanh activation functions, as
well as M-layers, using a double spiral (“Swiss roll”) classiﬁcation task as a toy prob-
lem.
The data consist of 2000 randomly generated points along two spirals, with coor-
dinates in the [−10, 10] range. Uniform random noise in the [−0.5, 0.5] range is added
to each input coordinate. As we are only interested in the classiﬁcation boundaries, no
test or validation set is used.
The M-layer has a representation sized = 10 and a matrix sizen = 1. Each DNN
has two hidden layers of size 20.
A RMSprop optimizer is used to minimize the cross-entropy with softmax. The
M-layer is trained for 100 epochs using a learning rate of 0.001. The ReLU DNN is
trained for 1000 epochs using a learning rate of 0.001. The tanh DNN is trained for
1000 epochs using a learning rate of 0.01. These values are chosen in such a way that
all networks achieved a perfect ﬁt.
The resulting boundaries for the three models are shown in Figure 2. They illus-
trate the distinctive ability of the M-layer to extrapolate functions beyond the training
domain.
9
0 1 2 3 4 5 6
−50
−40
−30
−20
−10
0
10
training extrapolating
input
output
DNN
M-layer
(a) 1.42 cos(6πx + 0.84) + 6.29 cos(8πx + 0.76)
0 1 2 3 4 5 6
−40
−30
−20
−10
0
10
training extrapolating
input
output
DNN
M-layer
(b) 1.55 cos(8πx + 0.26) + 5.07 cos(14πx + 0.81)
0 1 2 3 4 5 6
−40
−30
−20
−10
0
10
training extrapolating
input
output
DNN
M-layer
(c) 1.60 cos(12πx + 0.59) + 6.92 cos(16πx + 0.44)
Figure 3: Learning periodic functions with a DNN and an M-layer. Each plot shows
outputs from three separate models of each type.
10
4.2 Learning Periodic Functions
To assess the capacity of the M-layer architecture to learn and extrapolate feature peri-
odicity, we compare the performance of an M-layer and a DNN on periodic functions
obtained as the sum of two cosines.
The data is generated as follows. The frequencies of the cosines are chosen as small
integer multiples of 2π (from 3 to 9); the amplitudes are randomly generated from the
intervals [1, 2] and [5, 10] respectively, and the phases are randomly generated in the
[0,π/ 3] range. Each model is trained on the[0, 2] range and tested it on the[2, 6] range,
with a point spacing of 10−5. Gaussian random noise with σ = 10−4 is added to the
target value of each training sample. No activity regularization is used.
The M-layer uses a representation size d = 1 and a matrix size n = 6, resulting
in a trainable parameter count of 115. Each cosine can be represented by using a 2-
dimensional subspace; a matrix size of 4 would thus be sufﬁcient, but6 was chosen to
show that an M-layer can learn periodicity even when overparameterized.
In this experiment, the initialization of the bias and of T0ij is performed by gener-
ating normally distributed numbers with σ = 0.01 and mean−10 for elements of the
diagonal, and 0 for all other elements. The coefﬁcients of the mapping from input val-
ues to the embedding space are initialized with normally distributed values with mean
0.1 andσ = 0.05. This initialization is chosen in order to make it more likely for the
initial matrix M to be exponentiated to have negative eigenvalues and therefore keep
outputs small.
The ReLU DNN is composed of two hidden layers with 50 neurons each, followed
by one hidden layer with 10 neurons, resulting in a trainable parameter count of 3221.
The DNN was initialized using uniform Glorot initialization [GB10]. As the objective
of this experiment is to demonstrate the ability to learn the periodicity of the input with-
out additional engineering, we do not consider DNNs with special activation functions
such as sin(x).
A RMSprop optimizer is used to minimize the following modiﬁedL2 loss function:
if f is the function computed by the network, x the input of the sample and y the
corresponding output, then the loss is given by (f(x)−y)2 + max(0,|f(2x + 6)|−
100)2. In other words, very large values in the [6, 10] time range are punished.
M-layers are trained for300 epochs with learning rate5·10−3, decay rate 10−5 and
batch size 128. DNNs are trained for 300 epochs with learning rate 10−3, decay rate
10−6 and batch size 64. The hyperparameters are chosen by running multiple training
steps with various choices of learning rate (10−2, 10−3, 10−4), decay rate (10−3, 10−4,
10−5, 10−6), batch size (64 and 128) and number of epochs ( 50, 100, 300). For each
model, the set of parameters that provided the bestL2 loss on the training set is chosen.
Examples of functions learned by the M-layer and the DNN are shown in Figure 3,
which illustrates that, in contrast to the DNN, the M-layer is able to extrapolate such
functions.
4.3 Learning Determinants
To demonstrate the ability of the M-layer to learn polynomials, we train an M-layer
and a DNN to predict the determinant of3× 3 and 5× 5 matrices. We do not explicitly
11
encode any special property of the determinant, but rather employ it as an example
multivariate polynomial that can be learnt by the M-layer. We conﬁrm that we observe
equivalent behavior for the matrix permanent.
Learning the determinant of a matrix with a small network is a challenging problem
due to the size of its search space. A 5× 5 determinant is a polynomial with 120
monomials of degree 5 in 25 variables. The generic inhomogeneous polynomial of this
degree has
(25+5
5
)
= 142506 monomials.
From Section 3.3, we know that it is possible to express this multivariate polyno-
mial perfectly with a single M-layer. In fact, a strictly upper triangular and therefore
nilpotent matrix can achieve this. We can use this fact to accelerate the learning of the
determinant by masking out the lower triangular part of the matrix, but we do not pur-
sue this idea here, as we want to demonstrate that an unconstrained M-layer is capable
of learning polynomials as well.
The data consist of n×n matrices with entries sampled uniformly between −1
and 1. With this sampling, the expected value of the square of the determinant is n!
3n .
So, we expect the square of the determinant to be 2
9 for a 3× 3 matrix, and 40
81 for a
5× 5 matrix. This means that an estimator constantly guessing 0 would have a mean
square error (MSE) of≈ 0.2222 and≈ 0.4938 for the two matrix sizes, respectively.
This provides a baseline for the results, as a model that approximates the determinant
function should yield a smaller error.
The size of the training set consists of between 210 and 217 examples for the 3× 3
matrices, and 220 for the 5× 5 matrices. The validation set is 25% of the training set
size, in addition to it. Test sets consist of 106 matrices.
The M-layer has d = 9 and n between 6 and 12 for 3× 3 determinants, and
n = 24 for 5× 5 determinants. The DNNs has 2 to 4 equally-sized hidden layers, each
consisting of 5, 10, 15, 20, 25 or 30 neurons, for the 3×3 matrices, and 5 hidden layers
of size 100 for the 5× 5 matrices.
An RMSprop optimizer is used to minimize the MSE with an initial learning rate
of 10−3, decay 10−6, and batch size 32. These values are chosen to be in line with
those chosen in Section 4.4. The learning rate is reduced by 80% following 10 epochs
without validation accuracy improvement. Training is carried for a maximum of 256
epochs, with early stopping after 30 epochs without validation accuracy improvement.
Figure 4 shows the results of learning the determinant of 3× 3 matrices. The M-
layer architecture is able to learn from fewer examples compared to the DNN. The best
M-layer model learning on 217 examples achieves a mean squared error of≈ 2· 10−4
with 811 parameters, while the best DNN has a mean squared error of ≈ 0.003 with
3121 parameters.
Figure 5 shows the results of learning the determinant of 5× 5 matrices. An M-
layer with 14977 parameters outperformed a DNN with 43101 parameters, achieving a
MSE of 0.279 compared to 0.0012.
4.4 Learning Image Datasets
We assess the performance of the M-layer on three image classiﬁcation tasks: MNIST
[LBBH98], CIFAR10 [Kri09], and SVHN [NWC+11].
12
103 104 105
10−4
10−3
10−2
10−1
training set size
mean squared error
M-layer 81 params
DNN 3121 params
Figure 4: Learning the determinant of a 3× 3 matrix with M-layers and DNNs with
various parameter counts and training set sizes.
The following procedure is used for all M-layer experiments in this section. The
training set is randomly shufﬂed and 10% of the shufﬂed data is set aside as a validation
set. The M-layer dimensions are d = 35 andn = 30, which are chosen by a random
search in the interval [1, 100]. An SGD optimizer is used with initial learning rate
of 10−3, momentum 0.9, and batch size 32. The learning rate is chosen as the largest
value that gave a stable performance, momentum is ﬁxed, and the batch size is chosen
as the best-performing in (32, 64). The learning rate is reduced by 80% following 5
epochs without validation accuracy improvement. Training is carried for a maximum
of 150 epochs, with early stopping after 15 epochs without validation accuracy im-
provement. The model that performs best on the validation set is tested. Accuracy
values are averaged over at least 30 runs.
We compare the performance of the M-layer with three recently-studied general-
purpose architectures. As the M-layer is a novel architecture and no additional en-
gineering is performed to obtain the results in addition to the regularization process
described above, we only compare it to other generic architectures that also use no
architectural modiﬁcations to improve their performance.
The results are shown in Table 1. The M-layer outperforms multiple fully-connected
architectures (with sigmoid, parametric ReLU, and maxout activations), while employ-
ing signiﬁcantly fewer parameters. The M-layer also outperforms the NODE network,
which is based on a convolutional architecture. The networks that outperform the M-
layer are the ReLU fully-connected network, which has signiﬁcantly more parameters,
and the ANODE network, which is an improved version of NODE and is also based on
a convolutional architecture.
Computing a matrix exponential may seem computationally demanding. To inves-
tigate this, we compare the training time of an M-layer with that of a DNN with similar
13
Table 1: Comparison of classiﬁcation performance on image recognition datasets. We
compare the M-layer to three general-purpose types of architectures: fully-connected
(f.c.) networks with different activation functions [LMK15], NODE [CRBD18], and
ANODE [DDT19]. The sources are listed as [D] [DDT19] and [L] [LMK15].
ARCHITECTURE CONVOLUTIONAL ? P ROBLEM ACCURACY % (MEAN± S.D.) P ARAMETERS SOURCE
M-LAYER NO MNIST 97.99± 0.12 68 885
NODE YES MNIST 96.40± 0.50 84 000 [D]
ANODE YES MNIST 98.20± 0.10 84 000 [D]
M-LAYER NO CIFAR-10 54.17± 0.36 148 965
SIGMOID ( F.C.) NO CIFAR-10 46.63 8 049 010 [L]
RELU ( F.C.) NO CIFAR-10 56.29 8 049 010 [L]
PRELU ( F.C.) NO CIFAR-10 51.94 8 049 010 [L]
MAXOUT (F.C.) NO CIFAR-10 52.80 8 049 010 [L]
NODE YES CIFAR-10 53.70± 0.20 172 000 [D]
ANODE YES CIFAR-10 60.60± 0.40 172 000 [D]
M-LAYER NO SVHN 81.19± 0.23 148 965
NODE YES SVHN 81.00± 0.60 172 000 [D]
ANODE YES SVHN 83.50± 0.50 172 000 [D]
number of parameters. Table 2 shows that the M-layer only takes approximately twice
as much time to train.
We also compute the robustness bounds of the M-layer trained on CIFAR-10, as
described in Section 3.7. We train n = 20 models with δin≈ 200,∥S∥2≈ 3, and
∥M∥2 typically a value between 3 and 4. The maximum L2 variation of the vector of
accumulated evidences is≈ 1. This results in a typical L∞ bound for robustness of
≈ 10−5 on the whole set of correctly classiﬁed CIFAR-10 test samples. In comparison,
an analytical approach to robustness similar to ours [PRGS17], which uses a layer-by-
layer analysis of a traditional DNN, achieves L2 bounds of≈ 10−9. Figure 6 shows
the distribution ofL∞ bounds obtained for the M-layer.
Table 2: Comparison of training time per epoch for CIFAR-10 on a Nvidia V100 GPU.
The M-layer dimensions are d = 35 and n = 30 . The DNN has 4 layers of size
43− 100− 100− 10.
ARCHITECTURE PARAMETERS TRAINING TIME
M-L AYER 148965 8 .67s± 0.56
RELU DNN 147649 4 .12s± 0.26
Early experiments show promising results on the same datasets when applying ad-
vanced machine learning techniques to the M-layer, such as combining the M-layer
with convolutional layers and using dropout for regularization. As the scope of this
14
true determinant
learnt determinant
-1
-1
-.5
-.5
0
0
.5
.5
1
1
(a) DNN
true determinant
learnt determinant
-1
-1
-.5
-.5
0
0
.5
.5
1
1 (b) M-layer
Figure 5: Learning the 5× 5 determinant. Each scatter plot shows 5000 points, each
corresponding to a pair (true determinant, learnt determinant).
10−9 10−8 10−7 10−6 10−5 10−4
0
200
400
600
max L∞perturbation
number of examples
Figure 6: MaximumL∞ perturbation on the correctly classiﬁed CIFAR-10 test samples
that is guaranteed not to produce a misclassiﬁcation.
paper is to introduce the basics of this architecture, we defer this study to future work.
5 Conclusion
This paper introduces a novel model for supervised machine learning based on a single
matrix exponential, where the matrix to be exponentiated depends linearly on the input.
The M-layer is a powerful yet mathematically simple architecture that has universal
approximator properties and that can be used to learn and extrapolate several problems
that traditional DNNs have difﬁculty with.
An essential property of the M-layer architecture is its natural ability to learn in-
put feature crosses, multivariate polynomials and periodic functions. This allows it to
extrapolate learning to domains outside the training data. This can also be achieved in
traditional networks by using specialized units that perform custom operations, such as
multiplication or trigonometric functions. However, the M-layer can achieve this with
no additional engineering.
In addition to several mathematical benchmarks, we have shown that the M-layer
performs competitively on standard image recognition datasets when compared to non-
15
specialized architectures, sometimes employing substantially fewer parameters. In ex-
change for the beneﬁts it provides, the M-layer only takes around twice as much time
as a DNN with the same number of parameters to train, while also considerably sim-
plifying hyperparameter search.
Finally, another desirable property of the M-layer is that it allows closed-form ro-
bustness bounds, thanks to its powerful but relatively simple mathematical structure.
We provide source code in TensorFlow that can be used to train and further explore
the capabilities of the M-layer. Future work will focus on adapting the M-layer for
specialized tasks, such as hybrid architectures for image recognition, and advanced
regularization methods inspired by the connection between the M-layer and Lie groups.
A Appendix
A.1 Universal Approximation Theorem
We show that a single M-layer model that uses sufﬁciently large matrix size is able
to express any polynomial in the input features. This is true even when we restrict the
matrix to be exponentiated to be nilpotent or, more speciﬁcally, strictly upper triangular.
So, for classiﬁcation problems, M-layer architectures are a superset of multivariate
polynomial classiﬁers, where matrix size constrains the complexity of the polynomial.
Theorem 1 (Expressibility of polynomials) . Given a polynomial p(x1,...,x n) inn
variables, we can choose weight tensors for the M-layer such that it computesp exactly.
Proof. The tensor contraction applied to the result of matrix exponentiation can form
arbitrary linear combinations, and is therefore able to compute any polynomial given a
matrix that contains the constituent monomials up to constant factors. Thus, it sufﬁces
to prove that we can produce arbitrary monomials in the exponentiated matrix.
Given a monomialm of degreed− 1, we consider thed×d matrixU, that has the
d− 1 (possibly repeated) factors of the monomial on the ﬁrst upper diagonal and zeros
elsewhere. Let us consider powers of U. It can be shown that all elements of Ui are
equal to 0, except for thei-th upper diagonal, and that the value in the (d− 1)-th upper
diagonal ofUd−1, which contains only one element, is the product of the entries of the
ﬁrst upper diagonal ofU. This is precisely the monomial m we started with. By the
deﬁnition of the exponential of the matrix, exp(U) then contains m
(d−1)!, which is the
monomial up a constant factor.
Given a polynomial p constiting of t monomials, for each 1≤ i≤ t, we form
matrices Ui for the corresponding monomial mi of p, as described above. Then we
build the diagonal block matrix U = diag(U1,...,U t). It is clear that exp(U) =
diag(exp(U1),..., exp(Uk)), so we can ﬁnd all monomials ofp in exp(U).
16
To illustrate the proof, we look at a monomialm =abcd.
U =


0 a 0 0 0
0 0 b 0 0
0 0 0 c 0
0 0 0 0 d
0 0 0 0 0


exp(U) =


1 a 1
2ab 1
6abc 1
24abcd
0 1 b 1
2bc 1
6bcd
0 0 1 c 1
2cd
0 0 0 1 d
0 0 0 0 1


The M-layers constructed here only make use of nilpotent matrices. When using
this property as a constraint, the size of the M-layer can be effectively halved in the
implementation.
The construction from Theorem 1 can be adapted to express not only a multivariate
polynomial, i.e. a function to R1, but also functions to Rk, which restrict to a poly-
nomial in each coordinate. This, together with the Stone-Weierstrass theorem [Sto48],
implies the following:
Corollary 2. For any continuous function f : [a,b ]n→ Rm and any ϵ > 0, there
exists an M-layer model that computes a function g such that|f(x0,...,x n−1)j−
g(x0,...,x n−1)j|<ϵ for all 0≤j≤m.
A.1.1 Optimality of construction
While our proof is constructive, we make no claim that the size of the matrix used
in the proof is optimal and cannot be decreased. Given a multivariate polynomial of
degreed with t monomials, the size of the matrix we construct would be t(d + 1)2.
In fact, by slightly adapting the construction, we can obtain a size of matrix that is
td2 + 1. Given that the total number of monomials in polynomials of n variables up
to degree d is
(n+d
d
)
, it seems likely possible to construct much smaller M-layers for
many polynomials. Thus, one wonders what is, for a given polynomial, the minimum
matrix size to represent it with an M-layer.
As an example, we look at the determinant of a 3× 3-Matrix. If the matrix is


a b c
d e f
g h i

,
then the determinant is the polynomial aei−afh−bdi +bfg +cdh−ceg. From
Theorem 1, we know that it is possible to express this polynomial perfectly with a
17
single M-layer. However, already an M-layer of size 8 is sufﬁcient to represent the
determinant of a 3× 3 matrix: If
M =


0 0 i f 0 0 0 0
0 0 h e 0 0 0 0
0 0 0 0 2 d −2f 0 0
0 0 0 0 −2g 2i 0 0
0 0 0 0 0 0 3 c −3b
0 0 0 0 0 0 3 a 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0


(4)
then exp(M) is


1 0 i f−fg +di 0 −cfg +cdi bfg −bdi
0 1 h e−eg+dh−fh +ei−ceg+aei+cdh−afh beg−bdh
0 0 1 0 2 d −2f 3cd−3af −3bd
0 0 0 1 −2g 2i −3cg+3ai 3bg
0 0 0 0 1 0 3 c −3b
0 0 0 0 0 1 3 a 0
0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 1

,
the sum of exp(M)0,7 and exp(M)1,6 is exactly this determinant. The permanent of a
3× 3 matrix can be computed with an almost identical matrix, by removing all minus
signs.
18
References
[CRBD18] Tian Qi Chen, Yulia Rubanova, Jesse Bettencourt, and David K Duve-
naud. Neural Ordinary Differential Equations. In S Bengio, H Wallach,
H Larochelle, K Grauman, N Cesa-Bianchi, and R Garnett, editors, Ad-
vances in Neural Information Processing Systems 31, pages 6571–6583.
Curran Associates, Inc., 2018. NeurIPS.
[DDT19] Emilien Dupont, Arnaud Doucet, and Yee Whye Teh. Augmented neu-
ral odes. In H. Wallach, H. Larochelle, A. Beygelzimer, F. d’Alch´e Buc,
E. Fox, and R. Garnett, editors, Advances in Neural Information Pro-
cessing Systems 32, pages 3134–3144. Curran Associates, Inc., 2019.
[GB10] Xavier Glorot and Yoshua Bengio. Understanding the difﬁculty of train-
ing deep feedforward neural networks. In Proceedings of the thirteenth
international conference on artiﬁcial intelligence and statistics , pages
249–256, 2010.
[Gil08] Robert Gilmore. Lie groups, physics, and geometry: an introduction for
physicists, engineers and chemists. Cambridge University Press, 2008.
[Gil12] Robert Gilmore. Lie groups, Lie algebras, and some of their applica-
tions. Courier Corporation, 2012.
[GWFM+13] Ian J. Goodfellow, David Warde-Farley, Mehdi Mirza, Aaron Courville,
and Yoshua Bengio. Maxout networks. In 30th International Confer-
ence on Machine Learning, ICML 2013, number PART 3, pages 2356–
2364, 2013.
[Hig05] Nicholas J. Higham. The Scaling and Squaring Method for the Matrix
Exponential Revisited. SIAM Journal on Matrix Analysis and Applica-
tions, 26(4):1179–1193, 2005.
[Kri09] Alex Krizhevsky. Learning Multiple Layers of Features from Tiny Im-
ages. Technical report, 2009.
[LBBH98] Y . Lecun, L. Bottou, Y . Bengio, and P. Haffner. Gradient-based
learning applied to document recognition. Proceedings of the IEEE ,
86(11):2278–2324, 1998.
[LMK15] Zhouhan Lin, Roland Memisevic, and Kishore Konda. How far can we
go without convolution: Improving fully-connected networks. pages
1–10, 2015.
[MV03] Cleve Moler and Charles Van Loan. Nineteen Dubious Ways to Com-
pute the Exponential of a Matrix, Twenty-Five Years Later. SIAM Re-
view, 45(1):3–49, 2003.
19
[NWC+11] Yuval Netzer, Tao Wang, Adam Coates, Alessandro Bissacco, Bo Wu,
and Andrew Y Ng. Reading Digits in Natural Images with Unsupervised
Feature Learning. In NIPS Workshop on Deep Learning and Unsuper-
vised Feature Learning 2011, 2011.
[PRGS17] Jonathan Peck, Joris Roels, Bart Goossens, and Yvan Saeys. Lower
bounds on the robustness to adversarial perturbations. In Advances in
Neural Information Processing Systems, pages 804–813, 2017.
[PS91] J. Park and I. W. Sandberg. Universal Approximation Using Radial-
Basis-Function Networks. Neural Computation, 3(2):246–257, 1991.
[RC94] Horn Roger and R Johnson Charles. Topics in matrix analysis. Cam-
bridge University Press, 1994.
[RHM86] D. E. Rumelhart, G. E. Hinton, and James L Mcclelland. A general
framework for parallel distributed processing. In Parallel distributed
processing: explorations in the microstructure of cognition , chapter 2.
1986.
[SFH17] Sara Sabour, Nicholas Frosst, and Geoffrey E Hinton. Dynamic Routing
Between Capsules. Advances in Neural Information Processing Systems
30, pages 3856–3866, 2017.
[SGPV18] Gagandeep Singh, Timon Gehr, Markus P ¨uschel, and Martin Vechev.
Boosting robustness certiﬁcation of neural networks. 2018.
[SGPV19] Gagandeep Singh, Timon Gehr, Markus P ¨uschel, and Martin Vechev.
An abstract domain for certifying neural networks. Proceedings of the
ACM on Programming Languages, 3(POPL):1–30, 2019.
[Sto48] Marshall H Stone. The generalized Weierstrass approximation theorem.
Mathematics Magazine, 21(5):237–254, 1948.
[THR+18] Andrew Trask, Felix Hill, Scott Reed, Jack Rae, Chris Dyer, and Phil
Blunsom. Neural Arithmetic Logic Units. Advances in Neural Informa-
tion Processing Systems, 2018-Decem:8035–8044, 2018.
20
