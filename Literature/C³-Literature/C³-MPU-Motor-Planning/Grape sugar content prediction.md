# Grape sugar content prediction

**Year:** D:20

---

Grape sugar content prediction
with multispectral alignment and
improved residual network
Yiming Chen1, Jizhou Deng1, Zhijie Liu1, Junchao Chen2, Wang Wei1, Yuanping Xiang1, Xinghui Zhu1 & Changyun Li1
Sugar content is a crucial indicator of grape ripeness and grading, and developing non-contact and non-
destructive sugar content detection devices is essential for grape-picking robots and sorting platforms. Spectroscopy, which can detect the chemical composition of grapes, has become a key technology
for developing non-destructive testing devices. In this paper, we collected 2,880 randomly labeled
multispectral images of Sunshine Rose grapes with a Changguang Yuchen MS600 PRO multispectral
camera and measured the sugar content (in Brix values) of the labeled grapes with a handheld
refractometer, using data exclusively from this grape variety. To address noise and misalignment
issues in the multispectral images, we proposed preprocessing methods including Gaussian denoising
and ECC (Enhanced Correlation Coefficient) algorithm registration. Based on a ResNet-50 residual
network, we constructed a grape sugar content prediction regression model Improved-Res with SE
(Squeeze-and-Excitation) attention modules, DSC (Depthwise Separable Convolutions), and Inception
modules. The model’s performance was evaluated by MSE (Mean Squared Error), MAE (Mean Absolute
Error), and R2 (R-Square) metrics. We compared the performance of four feature extraction methods
combined with four traditional machine learning models, as well as seven deep learning models. The
results showed that among traditional machine learning methods, the combination of color histogram
feature extraction and the XGBoost regression achieved the best performance, with MSE, MAE, and
R2 of 1.35, 0.90 Brix, and 0.78, respectively. Among deep learning methods, the ResNet-50 model
demonstrated the best performance, with MSE, MAE, and R2 of 0.95, 0.96 Brix, and 0.84, respectively. Effective improvements of SE attention module, depthwise separable convolutions, and Inception
module in the ResNet-50 model was confirmed through ablation experiments: the proposed Improved-
Res model achieved MSE, MAE, and R2 of 0.49, 0.55 Brix, and 0.92, respectively, which significantly
outperformed traditional machine learning methods and classical deep learning models. Keywords  Grape sugar content, Multispectral imaging, Deep learning, Nondestructive testing
Grapes are renowned as the foremost of the world’s four major fruits, prized for their vibrant color, pleasant
aroma, delicious taste, and rich nutrition. Not only grapes are edible and can produce wine, but also their fruit,
roots, and leaves have high medicinal values. Sugar content is a critical indicator of grape ripeness and is the
primary grape grading criterion, so it serves as a key factor in determining the timing of grape harvest and doing
grape classification1. In the early years, the assessment of grape ripeness was mainly replied on sight, touch, and taste: by observing
color changes, touching to evaluate fruit softness, and tasting the sweetness and acidity of the fruit. This process,
supplemented by accumulated experience, climatic conditions, and varietal characteristics, was used to estimate
the optimal harvest time. However, these methods are subjective, can not provide quantitative measurements
of sugar content, and also bring damage to the grapes, affecting their marketability2. With the advancement
of chemical analysis techniques, sugar content measurements such as refractometers and hydrometers
(measure the sugar content of grape juice in Brix values) have become standard methods for evaluating grape
ripeness. Although these methods provide quantitative sugar content values, they are also destructive and
time-consuming3. As people’s living standards are improving, the demand for grapes is increasing, leading to
expanding cultivation areas. However, labor has become increasingly scarce and expensive. To reduce costs and
enhance competitiveness, efforts have been made to develop grape inspection robots and harvest robots, which
are capable of assessing grape sugar content without contact and without causing damage, thus determining
1Hunan Agricultural University, Changsha 410000, China. 2Tencent Music Entertainment, Shenzhen 518000, China.
email: chenym@hunau.edu.cn
OPEN
Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports

grape yield, harvest time, and grading4. Non-contact sensing devices such as color high-definition cameras and
spectrometers, along with machine learning and other artificial intelligence technologies, have been extensively
explored and applied in this field5,6. Xinguang Wei et al. worked with the Drunk Incense, Muscat Hamburg, and Xiang Yue grape varieties in solar
greenhouses, applying grape skin color values (R, G, B, H, S, I) to a backpropagation neural network (BPNN)
to predict grape ripeness7. Xiaohong Wan et al. worked with the Red Grape variety in a natural environment,
using a Faster R-CNN convolutional neural network for grape identification, followed by the KNN algorithm
for fruit segmentation, and performed grape ripeness classification based on the H value in the HSV color
space8. These methods use color features as indicators of grape ripeness; however, color features may not fully
represent ripeness, especially in cases of minor color changes or fruit surface contamination, leading to potential
misclassification risks. Clarissa Murru et al. worked with the Alabarín blanco, Mencía, Verdejo negro, Albarín negro, and Carrasquín
grape varieties in a natural environment, collected near-infrared spectral image data, and used fast Fourier
transform processing to construct an artificial neural network (ANN) for ripeness classification9. Shi Xing et al.
developed a spectral image acquisition platform for red grapes. In a natural environment, they collected grapes
and then captured RGB images and near-infrared spectral images under natural light in the laboratory. Based
on machine learning, they established various models using linear discriminant analysis, ensemble learning
algorithms, and support vector machines to classify red grape clusters by their compactness and ripeness; based
on deep learning, they developed MobileNetV3_large and YOLO V5m models to achieve classification and
grading of red grape clusters by their compactness and ripeness10. Leon Amadeus Varga et al. collected spectral
images of avocados and kiwis under natural light in the laboratory and conducted biochemical experiments on
soluble solids, proposing a lightweight small neural network for feature extraction and modeling of their spectral
images to achieve ripeness classification11. These methods extract features from the collected spectral images and
use deep learning to build fruit ripeness classification models, rather than obtaining specific sugar content values. Furthermore, in fruit ripeness classification tasks, the boundaries of ripeness are often ambiguous, making it
difficult for classification models to accurately distinguish similar classes, thereby reducing the precision of
classification. Sheng Gao et al. did feature extraction and fusion of preprocessed hyperspectral images and RGB images of
Red Globe grapes, and built a partial least squares regression (PLSR) model based on the integrated information12. Shenghui Yang et al. used drones equipped with multispectral cameras to collect spectral images of Cabernet
Sauvignon grapes in the field, analyzed and extracted red (R), green (G), and near-infrared (NIR) components
to build linear regression and logarithmic regression models for “total sugar content-local R component"13. This
approach is also applied in the field of food inspection14,15. These methods employ traditional machine learning
models, which require significant computational resources and time when integrating multisource data and
processing large-scale data, making them unsuitable for real-time applications. Moreover, traditional machine
learning methods require more manual intervention and feature engineering, making it difficult to handle
complex nonlinear data relationships effectively. Nikolaos L. Tsakiridis et al. proposed deep autoencoder (DAE) and deep convolutional autoencoder (DCAE)
architectures to transform the raw collected grape spectra into standardized reflectance spectra for sugar content
prediction without considering illumination conditions, using the Chardonnay, Malagouzia, Sauvignon-
Blanc, and Syrah grape varieties16. Wenzheng Liu et al. collected spectral images of Giant Rose grapes with
the wavelength range of 400–1029 nm and compared six data preprocessing methods including first derivative
and multiplicative scatter correction. They conducted regression predictions on total phenols in grape skins
and seeds using partial least squares regression, support vector machine, and convolutional neural network
modeling approaches, the convolutional neural network performs the best17. These methods primarily employed
deep learning approaches, with a limited comparison to a small number of traditional machine learning models. The selection of models was relatively narrow and might have been influenced by the researchers’ experience
and preferences. This suggests a certain degree of subjectivity, and there may be other models better suited for
spectral data processing and prediction tasks. Machine learning is a core technology of artificial intelligence and has been widely applied in many fields18. As a frontier technology in machine learning, deep learning has undergone rapid development, from early
simple neural networks to today’s deep neural networks and convolutional neural networks, demonstrating
powerful data processing and feature learning capabilities. Compared to traditional methods, deep learning can
not only automatically extract complex features from vast amounts of data, exhibiting strong adaptability and
generalization capabilities, but also achieve efficient model training and reasoning through large-scale parallel
computing. These advantages have enabled deep learning to achieve remarkable results in image recognition,
natural language processing, and other fields, driving the advancement of technology towards intelligence and
automation19. In this paper, to deal with the issue of non-contact, non-destructive detection of grape sugar content, we
used multispectral imaging devices and handheld portable refractometers to acquire grape multispectral images
and corresponding sugar content values. After preprocessing such as denoising and alignment, we constructed
a dataset for training the sugar content inversion model. Based on ResNet-50, we improved the Bottleneck
module, enhanced the model’s feature extraction capabilities while reduced parameters, significantly improving
the model’s sugar content prediction accuracy. The main contributions of this paper are threefold:
(1)	 We constructed a dataset for training the grape sugar content inversion model. Each set of data comprises
preprocessed six-band grape multispectral images and corresponding sugar content labels, totaling 480 sets
of data. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

(2)	 We proposed a preprocessing scheme for grape multispectral images combining Gaussian denoising and
ECC algorithm registration.
(3)	 Based on the ResNet-50 residual network, we introduced an SE attention module into the Bottleneck, re­
placed the subsampling convolution layer and the feature extraction convolution layer with Depthwise Sep­
arable Convolutions and Inception module, respectively, and proposed the grape sugar content prediction
regression model Improved-Res. Dataset acquisition
Grape samples
The grape samples, specifically the Sunshine Rose variety, were collected from the Jin Jingfeng Modern Grape
Industry Park in Shaoshan, Hunan Province, China. The geographical coordinates of this vineyard are 27.88°N
and 112.63°E, and it has a subtropical humid climate. As shown in Fig. 1, the upper image depicts the internal
environment of the Jin Jingfeng Modern Grape Industry Park, while the lower image provides a close-up view
of the Sunshine Rose grape fruits. The growth cycle of grapes can be divided into six phenological stages: sap flow period, bud break and shoot
growth period, flowering and fruit set period, berry growth period, berry ripening period, and new shoot
maturation and leaf fall period. The selected grape variety matures from late July to late August. Consequently,
data collection was conducted on July 21, July 28, August 4, and August 11 of 2023. During each collection
session, 120 grape clusters were randomly selected, labeled, and processed to obtain their spectral images and
sugar content values. Data acquisition equipment
The multispectral images of the grapes required for the experiment were all captured by the MS600 PRO
multispectral camera from Changguang Yuchen, as shown in Fig. 2. The multispectral camera primarily comprises a multispectral gimbal camera, a downwelling light sensor, and
data transmission cables. The camera is equipped with six spectral channels, “dual red-edge” vegetation-sensitive
bands, 12-bit quantization, and ambient light synchronization correction functions, allowing for the precise
acquisition of the grapes’ spectral reflectance data. Table 1 presents some of the key performance parameters of
the multispectral camera. Table 2 lists the central wavelengths, bandwidths, and spectral ranges of the six bands. More detailed information can be found on the manufacturer’s official website (​h​t​t​p​s​:​/​/​w​w​w​.​y​u​s​e​n​s​e​.​c​o​m​.​c​n​/​z​h​
i​c​h​i​.​p​h​p​?​%​2​0​c​i​d​=​6​2​&​a​m​p​=​4​5​2​t​i​t​l​e​=.). The sugar content data of the grapes required for the experiment were measured by a Japanese Atago PAL-1
handheld portable refractometer, as shown in Fig. 3. The device consists of a sample chamber, a prism, a start button, a zero-setting button, and a digital display
screen for measurement values, allowing for simple and convenient measurement of grape sugar content. Table 3
Fig. 1. The internal environment of the Jin Jingfeng Modern Grape Industry Park and a close-up view of the
Sunshine Rose grape fruits. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

Fig. 3. Atago PAL-1 handheld portable refractometer. Bands
Central Wavelengths/nm
Bandwidths/nm
Spectral Ranges/nm
Band1

435–465
Band2

541.5–568.5
Band3

649–671
Band4

715–725
Band5

745–755
Band6

825–855
Table 2. Central wavelengths, bandwidths, and spectral ranges of six bands. Indicator Name
Indicator Parameters
Spectral Range/nm
400–1000
Number of Spectral Bands

Spatial Resolution
8.65 cm@h = 120 m
Effective Pixels/px
1.2 million
Quantization Bit Number/bit

Image Format
16-bit original TIFF & 8-bit reflectivity JPEG
Table 1. Some performance parameters of Changguang Yuchen MS600 PRO multispectral camera. Fig. 2. Changguang Yuchen MS600 PRO multispectral camera. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

presents some of the key performance parameters of the refractometer. More detailed information can be found
on the manufacturer’s official website (https://atag​o.net/japane​se/new/produ​cts-pal-top​.php). Data acquisition methods
The multispectral camera has an aperture value of f/2.2, a maximum aperture of 2.25, an exposure time of 1/251
seconds, and a focal length of 5 millimeters. A gray calibration card was used for lens calibration. The gray
calibration card was placed flat on a horizontal surface. Using the preview screen of the multispectral camera,
the handheld camera was aligned so that its optical axis pointed directly at the gray card, ensuring the card was
centered in the preview screen for each channel. The distance between the camera lens and the gray card was
maintained at approximately 80 cm. The camera automatically recognized the gray card and captured the image
until the message “Gray card captured” was displayed, as shown in Fig. 4. Studies have shown that the sweetness and acidity of grapes exhibit distinct absorption characteristics in the
visible to near-infrared wavelengths (400–970 nm), while color changes are primarily concentrated in the visible
light range (400–700 nm). This difference arises from the molecular properties of sugars, acids, and pigments. Sugars and organic acids strongly absorb in the near-infrared range (700–970 nm) due to molecular vibrations
(C-H, O-H bonds), whereas pigments like anthocyanins and chlorophyll primarily absorb visible light, driving
color changes. Consequently, spectral analysis in the visible range is effective for monitoring color development,
while near-infrared spectroscopy is better suited for assessing sugar and acid content in grapes20,21. Therefore, the
spectral bands chosen for this study are 450 nm, 555 nm, 660 nm, 720 nm, 750 nm, and 840 nm, covering both
visible and near-infrared wavelengths, which is helpful to analyze and extract features of the grapevines. During
the experiment, we selected sunny days and visited the vineyard on four occasions, and, under ambient light
conditions, used the multispectral camera to capture images of grape clusters randomly labeled at the pedicel. The camera was positioned about 40 cm away from the grape clusters to capture a single image, simulating
the scenario of a grape-picking robot conducting random image captures during its inspection process. For
Fig. 4. Multispectral camera calibrating with a gray card. Indicator Name
Indicator Parameters
Measurement Accuracy/Brix
0.0–53.0%
Measure Temperature/°C
10–100
Temperature Compensation/°C
10–75
Sampling Volume/ml
0.3 or more
Resolution
0.001
Table 3. Some performance parameters of Atago PAL-1 handheld portable refractometer. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

each grape cluster, six spectral images corresponding to the selected bands were generated during each capture
session, as illustrated in Fig. 5. In total, 480 sets (120 clusters × 4 field visits) of grape spectral images were
collected, amounting to 2,880 images. This extensive dataset provides a solid foundation for subsequent spectral
analysis and model construction. The pedicel, as the connecting part between the grape cluster and the vine, is responsible for transporting
nutrients, hormones, and water to the fruit. Grapes at the top of the cluster are closer to the pedicel and thus
receive these substances more easily, while those at the bottom face a longer transport path, resulting in slower
ripening. Therefore, the grapes at the bottom of the cluster are more representative of the overall ripeness of the
entire cluster, and the cluster is only suitable for harvesting when the grapes at the bottom reach a certain level
of maturity. For the collection of grape sugar content data, a handheld refractometer was used. First, the refractometer
was calibrated. Then, a single grape was randomly selected from the base of a labeled grape cluster, crushed, and
stirred to obtain a uniform grape juice sample. A dropper was used to drop the grape juice on the refractometer,
and the sugar content value displayed by the device was recorded. The refractometer was then rinsed with
distilled water to reduce the error of the next measurement. This method provided accurate grape sugar content
data, forming a reliable basis for the subsequent construction of the sugar content regression model. We analyzed
and summarized the grape sugar content data from four sampling sessions, including the maximum, minimum,
average, standard deviation(Sd), first quartile (Q1), median (Q2), and third quartile (Q3) values, as shown in
Table 4, with a line graph presented in Fig. 6. Dataset construction
The preprocessed grape multispectral images were annotated using the open-source tool LabelMe, ensuring that
the same region was consistently marked (for a detailed description of grape multispectral image preprocessing,
see Section “Grape multispectral image preprocessing.”). Noisy or significantly misaligned data were removed to
maintain data integrity. Finally, relevant information such as image dimensions, annotation coordinates, image
content, and sugar content values were obtained. Based on the annotation coordinates, the images were cropped
to highlight the areas of interest within the grape multispectral images of the six spectral bands, as shown in
Fig. 7. These cropped images, with a resolution of 224 × 224, combined with the sugar content values stored in
the label file, constitute a complete data sample. As time progresses, the ripeness of grapes increases, leading to higher sugar content values and an uneven
distribution of these values. To address this, the annotated 480 sets of spectral images were first randomly
shuffled and then divided into five subsets, each containing 96 sets of data. This provided an effective data
Time
Max/Brix
Min/Brix
Mean/Brix
Sd/Brix
Q1/Brix
Q2/Brix
Q3/Brix
2023.07.21
18.0
8.4
13.9
1.9
12.9
14.0
15.1
2023.07.28
19.4
8.3
14.3
2.2
13.1
14.4
15.8
2023.08.04
20.4
11.4
16.4
1.8
15.7
16.5
17.7
2023.08.11
23.8
10.0
17.4
2.1
16.2
17.7
18.6
Table 4. Grape sugar content summary across four sampling sessions. Fig. 5. Spectral images of grapes in six bands. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

foundation for performing five-fold cross-validation in subsequent traditional machine learning methods and
deep learning models. Proposed methods
Grape multispectral image preprocessing
During the acquisition of multispectral images, limitations of the equipment itself and variations in lighting
conditions introduced noise interference into the collected spectral data. Additionally, there were positional
discrepancies among the images of the six spectral bands. Therefore, data registration and preprocessing are
necessary to deal with these issues. For the denoising of multispectral images, Gaussian filtering was employed in this study. Gaussian filtering
is a widely used image processing technique primarily applied for noise reduction and image smoothing. By
Fig. 7. A data sample: cropped multispectral images of a grape cluster with labeled sugar content. Fig. 6. Line graph of grape sugar content trends across four sampling sessions. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

convolving the image with a Gaussian function, it effectively smooths the image and reduces noise and fine
details22. The Gaussian filter derives its name from the Gaussian function it utilizes, which plays a crucial role
in the image processing workflow. The calculation formula for the Gaussian function is shown in Eq. (1) below: G (x, y) =

2π σ 2 e−x2+y2
2σ 2

(1)
In this formula, x and y represent pixel coordinates, and σ is the standard deviation, which determines the
width and blurring effect of the filter. The core of the Gaussian filter is the Gaussian kernel, a matrix containing
the filter weights. When the Gaussian filter is applied to each multispectral image, its Gaussian kernel convolves
with the image, applying the filter’s weights to each pixel and its neighboring pixels, and the image is smoothed
through weighted averaging23. In this study, a 5 × 5 Gaussian kernel was chosen. This kernel size is sufficient
to effectively remove noise without excessively blurring the image, and it offers a moderate computational cost
that suits the task’s requirements. The standard deviation was initially set to zero, and it was then automatically
calculated based on the size of the Gaussian kernel to ensure optimal smoothing. This approach allows for
significant noise reduction while preserving image details, thereby enhancing the quality of the multispectral
images. The multispectral camera we used has six lenses, each corresponding to a different spectral band. Due to the
physical spacing between these lenses, the spectral images of grape samples captured in the six bands exhibit
positional deviations. Therefore, it is necessary to register the spectral images within each group of collected
grape images. This study employs the ECC algorithm for multispectral image registration. The correlation
coefficient is a commonly used statistical measure in the field of image registration, which quantifies the linear
relationship between two variables. The ECC algorithm enhances the robustness of the traditional correlation
coefficient, making it more sensitive to changes in image gray values. Typically, the gradient descent method
is used to optimize the iterative process24. By computing the partial derivatives of the affine transformation
matrix with respect to the enhanced correlation coefficient, the gradient descent method continuously adjusts
the transformation parameters to maximize the enhanced correlation coefficient. The calculation formula for the
enhanced correlation coefficient is given as Eq. (2):
ρ =
∑
x,y
(
I(x,y)−
−
I
)(
J
(
W (x,y)−
−
J
))
√∑
x,y
(
I(x,y)−
−
I
)2∑
x,y
(
J(W (x,y))−
−
J
)2

(2)
In this formula, I(x, y) and J(x, y) represent the pixel values of images I and J, respectively.
−
I and
−
J denote
the mean values of images I and J. During the registration process, the goal is to find an affine transformation
matrix W such that the correlation coefficient between the transformed image J (W (x, y)) and the original
image I (x, y) is maximized. The matrix W is then used to perform a geometric transformation on the image,
achieving the desired registration effect. The affine transformation can be represented by Eq. (3) as follows:
[ x,
y,
]
=
[ a11
a12
tx
a21
a22
ty
] [
x
y

]

(3)
In this formula, (x, y) represents the pixel coordinates in the original image, while (x,, y,) represents the
coordinates in the transformed image. The parameters a11、a12、a21 and a22 are elements of the affine
transformation matrix, and tx and ty are the translation components. The gradient descent Eq. (4) is as follows: W (k+1) = W k + α ∂ρ

## ∂W 

(4)
In this formula, W k is the affine transformation matrix at the kth iteration. α is the learning rate. ρ is the
enhanced correlation coefficient.
∂ρ
∂W is the partial derivative of the enhanced correlation coefficient with
respect to the affine transformation matrix W. This formula shows how the affine transformation matrix W is
updated by calculating the gradient of the enhanced correlation coefficient ρ with respect to W, and adjusting
the transformation parameters iteratively to maximize ρ. Since the internal parameters of the multispectral camera and the physical spacing between its lenses are
fixed, we first captured a set of calibration gray board spectral images, and the ECC algorithm was employed
to register this set of gray board images. Through iterative learning, we obtained the affine transformation
matrix for this set of gray board images. This learned transformation matrix was then applied to the subsequent
multispectral images of grapes, achieving precise alignment of the grape multispectral images. This method
facilitates the subsequent image annotation process by reducing registration errors at each shot, ensuring image
alignment across all spectral channels, and enhancing the reliability and consistency of the data. Improved-Res sugar content prediction model
ResNet-50 residual network
ResNet is a type of deep convolutional neural network model proposed by the team led by Kaiming He. Its design
introduces a residual learning mechanism to address the issues of vanishing and exploding gradients in deep
neural networks. ResNet can be subdivided into various variants such as ResNet-18, ResNet-34, and ResNet-50,
where the number following “ResNet” represents the depth of the network. This depth is determined by the
Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

number of layers in the input layer, the convolutional layers in the residual blocks, and the output layer. The
deeper the network, the greater the computational and parameter requirements, making each variant suitable
for different tasks. Therefore, it is crucial to select the appropriate model based on the specific task at hand25. In this study, we utilize the ResNet-50 model as the backbone network. The input channels have been modified
to six channels because six bands were selected in the collected grape multi-spectral images; the final output
section has been adjusted to output the sugar content of the grapes through a fully connected layer. The network
architecture is illustrated in Fig. 8, The green section represents Bottleneck1, and the blue section represents
Bottleneck2. ResNet employs residual blocks, where each block introduces a shortcut connection or skip connection that
directly passes the input to the output. This design ensures that the function space that can be fitted by the layer N
neural network will always include the function space that can be fitted by the layer N-1 neural network, thereby
ensuring effective gradient propagation26. Starting from ResNet-50, the residual blocks used have been replaced
from basic residual blocks to bottleneck residual blocks. This change effectively reduces the computational and
parameter load while maintains strong feature extraction capabilities27. In the two types of bottleneck layers, the input is represented as (C, W, W), where C is the number of input
channels, and (W, W) denotes the input height and width. These two types of bottleneck layers handle the input
differently. Bottleneck1 first reduces the dimensionality using a 1 × 1 convolutional kernel, then performs feature
extraction using a 3 × 3 convolutional kernel, and finally increases the dimensionality back by expanding the
number of output channels to four times the original, as determined by the ResNet network’s preset parameter,
“expansion”. The image size is reduced to half of its original size, which is dictated by the stride of the first 1 × 1
convolutional kernel. On the other hand, in Bottleneck2 there is no expansion in the number of channels, and
all convolutional kernels have a stride of 1, thus maintaining the number and size of input channel. Compared to
the basic residual block, the bottleneck layers offer higher efficiency and stronger feature extraction capabilities,
which can better adapt to the training of deep neural networks28. As a result, ResNet-50 and its subsequent
variants adopt the bottleneck architecture as the fundamental module. Overall, the whole network is divided into six stages. In the first stage, the input image undergoes a 7 × 7
convolution with max pooling. From the second to the fifth stage, convolution operations of 3, 4, 6 and 3 residual
blocks, respectively, are carried out on the feature maps output in the previous stage. Finally, in the output stage,
a global average pooling is applied, followed by flattening to perform either regression or classification tasks. Fig. 8. ResNet-50 network architecture diagram. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

Bottleneck module improvements
The Bottleneck module, serving as the core component of the ResNet-50 residual network, although it excels in
reducing the number of parameters and computational load, has certain limitations when dealing with complex
feature extraction. Therefore, this paper proposes the following improvements to the Bottleneck module.
(1)	 Add SE attention module. Adding SE Attention Module to Each Bottleneck’s Output Layer. The SE attention mechanism is a method used to enhance the performance of deep neural networks,
especially in image tasks. The core idea of the SE module is to learn to weight the input feature maps adaptively,
thus adjusting the importance of different feature channels29. This allows the model to better focus on the most
relevant features, thereby improving the model’s generalization ability. The process is illustrated in Fig. 9. In the Squeeze phase, a global average pooling operation is applied to compress the feature map of each
channel into a single scalar value30. This scalar can be considered the channel’s importance factor, indicating
its contribution to a specific task; it can encapsulate the global information of the channel. The computation
formula is shown in Eq. (5): Zc = Fsq (uc) =

## W × H

∑W
i=1
∑H
j=1uc (i, j) 
(5)
In this formula, Zc represents the mean value of the feature map of the cth channel, uc denotes the feature map
of the cth channel, which has a size of W × H, and (i, j) indicates the value at that position on the feature
map. In the excitation part, a small fully connected network models the importance of each channel. This network
takes the scalar values from the Squeeze phase as input and outputs a weight vectors31. This weight vector is used
to weight each channel of the original feature map, and then generate the final feature representation, thereby
enabling the model to focus more on important features. The calculation Eq. (6) is as follows:
s = Fex (z, W) = σ (g (z, W)) = σ (W2δ (W1z)) 
(6)

## W1 ∈R

r

## C × C

## W2 ∈RC× C

r
In this formula, s represents the gating unit, which is the weighted 1 × 1 × C feature vector. σ denotes
the sigmoid activation function, which constrains the weights between 0 and 1, and δ represents the ReLU
activation function. W1 and W2 are the weight matrices of the two fully connected layers, respectively32,33. The first fully connected layer reduces the dimensionality, resulting in a C/r dimensional vector, where r is
the dimensionality reduction factor; the second fully connected layer restores the dimensionality back to C,
ensuring that the feature vector has the same dimensionality as the input. In summary, the SE attention mechanism enhances model transparency regarding the importance of different
feature channels through explicit channel weighting. This mechanism effectively captures and emphasizes
important features while suppresses irrelevant ones, thereby improving the model’s generalization ability.
(2)	 Replace the subsampling convolutional layer. Replacing the subsampling convolutional layers in the Bottleneck with Depthwise Separable Convolutions. Depthwise Separable Convolution is an efficient convolutional operation widely used in deep learning,
especially in convolutional neural networks. By separating channel-wise convolutional calculations from spatial
convolutional calculations, Depthwise Separable Convolutions significantly reduce the number of parameters. This reduced parameter quantity not only lowers the model’s complexity, thereby reducing the risk of overfitting,
which is particularly important for small datasets, but also enables the large-scale processing of spectral data34. Depthwise Separable Convolutions consist of two steps: Depthwise Convolution and Pointwise Convolution. Depthwise Convolution performs convolutional operations independently on each spectral band, effectively
extracting feature information from each band, which helps in capturing high-dimensional features from
spectral data. Pointwise Convolution, using a 1 × 1convolutional kernel, linearly combines the features across
channels, integrating the features extracted by Depthwise Convolution and facilitating the interaction and fusion
Fig. 9. SE attention module architecture diagram. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

of information across different spectral bands. This enhances the comprehensive expression ability of features,
helping the model understand the data better35–37. The comparison between Depthwise Separable Convolution
and traditional convolution is shown in Fig. 10. In traditional convolution operations, the convolutional kernel not only slides on the spatial dimensions
(width and height) but also performs mixed calculations across channels. The convolution process is illustrated
in Fig. 10(a). Depthwise convolution differs in that it performs convolution operations on each channel independently,
with each convolutional kernel operating on only one channel of the input feature map. This results in the number
of output feature maps being equal to the number of input channels, i.e., the number of input channels = the
number of convolutional kernels=the number of output feature maps. The convolution process is depicted in
Fig. 10(b). Pointwise convolution uses a 1 × 1 convolutional kernel to linearly combine all the channels at each position
of the depthwise convolution output, thereby increasing inter-channel interactions. The convolution process is
shown in Fig. 10(c). Compared to traditional convolutions, depthwise separable convolutions reduce computational cost and
parameter quantity while maintain high accuracy and performance. In traditional convolution, the parameter
quantity and computational cost are described by Eq. (7): Parameter quantity = Dk × Dk × M × N 
(7)
Calculation Amount = Dk × Dk × M × N × Df × Df
In the depthwise separable convolution, the parameter quantity and computational cost are described by Eq. (8): Parameter quantity = Dk × Dk × M + M × N 
(8)
Calculation Amount = Dk × Dk × M × Df × Df + M × N × Df × Df
In the formula, Dk represents the size of the convolution kernel, M is the number of input channels, N is the
number of output channels, and Df is the size of the output feature map. The comparison of parameter quantity
and computational cost between depthwise separable convolution and traditional convolution is illustrated in
Eq. (9): Parameter quantity = depthwise separable convolution
traditional convolution
= Dk× Dk× M+M× N
Dk× Dk× M× N
=

## N +

Dk2

(9)
Calculation Amount: depthwise separable convolution
traditional convolution
= Dk × Dk × M × Df × Df + M × N × Df × Df
Dk × Dk × M × N × Df × Df
= 1

## N +

Dk2
Overall, depthwise separable convolution offers significant advantages in feature extraction of spectral data. By
independently extracting features from each spectral band (depthwise convolution) and then integrating these
features across all bands (pointwise convolution), it effectively reduces both computational load and the number
of parameters, thus lowering model complexity. In models deployed on grape-picking robots, it is essential
to focus on lightweight architecture and efficient inference to ensure real-time responsiveness and effective
processing. This approach not only minimizes redundant information and enhances feature representation
but also improves the model’s noise resistance and robustness, leading to increased precision and efficiency in
spectral data analysis. Additionally, depthwise separable convolution provides greater flexibility and scalability
for models handling high-dimensional spectral data, making it particularly suitable for deployment in resource-
constrained environments38,39. Fig. 10. Comparison of depthwise separable convolution and traditional convolution. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

(3)	 Replace the feature extraction convolution layer. Replace the feature extraction convolution layers in the Bottleneck with the Inception module. The Inception module, proposed by Christian Szegedy’s team at Google, aims to capture features at different
scales by performing multiple convolution operations of varying sizes and pooling operations within a single
module, and then concatenating the outputs at the output layer40,41. The architecture of the Inception V1 module
used in this paper is shown in Fig. 11: The 1 × 1 convolutions are used to reduce the number of input channels, thereby decreasing the computational
load and the number of parameters for subsequent convolutions. They can also incorporate non-linear activation
functions to enhance the network’s non-linear expressive power. The 3 × 3 and 5 × 5 convolutions are used to
capture spatial features of different sizes from the input feature map, obtaining more contextual information. The 3 × 3 max-pooling layer can reduce the spatial size of the input feature map, capture the features with the
highest activation values, and increase the model’s spatial invariance. The concatenate layer merges the outputs
from different paths along the channel dimension, which integrates features extracted by different convolution
kernels and pooling operations, thereby enriching the final output feature representation42. In summary, each convolution and pooling operation in the Inception module has a specific role and
purpose, including feature extraction, dimensionality reduction, computational load and parameter quantity
reduction, and feature fusion. These operations effectively expand the depth and width of the model, enhance its
generalization ability, and improve accuracy while prevent overfitting.
(4)	 Improved bottleneck. The Improved-Res model primarily improves the two types of Bottleneck residual blocks in the ResNet-50
model. The subsampling convolution layer in the Bottleneck block is replaced with a depthwise separable
convolution to reduce the model’s computational load and parameter quantity, thereby increasing computation
speed while maintaining excellent performance. The feature extraction convolution layer in the Bottleneck block
is replaced with an Inception module to capture features of the input feature map at different scales, enabling
feature fusion and improving the model’s feature representation capabilities. Finally, an SE attention module is
added before the output layer of each Bottleneck block to weight the features extracted by the Inception module,
emphasizing important features while suppressing irrelevant ones. This improves the model’s generalization
ability and reduces the risk of overfitting. The architecture of the improved Bottleneck module (the orange
section represents the improved parts) is shown in Fig. 12, and its overall architecture can be compared with
Fig. 8 for reference. Experiment and verification
Experimental setup
The experiments were conducted with an Intel Core I9 12900HX processor, an NVIDIA GeForce RTX 4060
GPU with 8GB VRAM, and 16GB RAM. The deep learning framework was PyTorch 2.1.0 GPU version, and
the programming language was Python 3.10. The experimental method employs five-fold cross-validation,
where 480 data samples are shuffled and randomly divided into five subsets, each containing 96 samples. In each
iteration, one subset is selected as the test set, while the remaining four subsets are used as the training set. The
training set is augmented to expand from 384 samples to 1,536 samples, after which the model is trained. This
process is repeated five times, ensuring each subset is used as the test set once. The average performance metrics,
including MSE, MAE, and R², are calculated across the five experiments to assess the overall performance of the
model43. Finally, the average inference time per sample and the number of samples processed per second (SPS)
are recorded as evaluation standards for inference efficiency. The calculation formulas for MSE, MAE, and R2 are
shown as Eqs. (10), (11), and (12) respectively: Fig. 11. Inception V1 module architecture diagram. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

## MSE = 1

n
n
i=1(yi −yi)2 
(10)

## MAE = 1

n
n
i=1 |yi −yi| 
(11)

## R2 = 1 −

n
i=1
yi−
yi

n
i=1

yi−
−
y
2

(12)
In the formula, yi is the true value, yi is the predicted value,
−y is the mean of the true values, and n is the sample
size. Grape multispectral image registration
The collected multispectral images of grapes were processed by Gaussian filtering for denoising, and the denoised
multispectral images of grapes are shown in Fig. 13. Then, the learned affine transformation matrix was used to align the images based on the spectral image of
the 720 nm band using the ECC algorithm. The results were evaluated by MSE, a simple and effective method to
measure the similarity between two images by calculating the average of the squared differences between each
pixel in two images. A smaller MSE indicates greater similarity between the images44. The calculation formula
is shown in Eq. (13):

## MSE =

mn
∑m
i=1
∑n
j=1[I1 (i, j) −I2 (i, j)]2 
(13)
In this formula, I1 (i, j) and I2 (i, j) are the pixel values at position (i, j) in the two images, and m and
n are the width and height of the images, respectively. The MSE results are shown in Table 5. The registered
multispectral images of the grapes are shown in Fig. 14. Traditional machine learning methods
In the field of traditional machine learning, the performance of four feature extraction methods, which are
direct flattening, mean, variance, and color histogram, combined with four regression models, which are support
vector machine regression, gradient boosting regression, random forest regression and XGboost regression45,46,
was compared. For these models, hyperparameter tuning and optimization were performed using grid search47. For support vector machine regression, the radial basis function (RBF) kernel was chosen, and the best values
for the regularization parameter (C) and gamma were found to be 1.0 and 0.1, respectively. For gradient boosting
regression, the grid search optimized the number of estimators (100), learning rate (0.05), and maximum depth
Fig. 12. Improved Bottleneck module architecture diagram. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

(3). For random forest regression, the grid search selected the optimal values: the number of trees was set to 200,
maximum depth to 10, and minimum samples per leaf to 2. For XGBoost regression, the grid search selected the
optimal hyperparameters: 200 trees were used (n_estimators = 200), with a learning rate of 0.05 and a maximum
tree depth of 3. To control overfitting, the minimum child weight was set to 1, while subsample and column
sampling per tree were both set to 0.8, ensuring a balanced trade-off between bias and variance. The MSE, MAE,
and R² results are shown in Figs. 15 and 16, and Fig. 17, as well as Table 6. Based on the results, among the traditional machine learning methods, the color histogram feature extraction
combined with the XGBoost regression model achieved the highest accuracy, with MSE value of 1.35, MAE
Fig. 14. Spectral images of grapes in six bands after ECC algorithm registration. Processing Method
450 nm
550 nm
660 nm
750 nm
840 nm
Average
Original Image(No processing)
0.1473
0.0945
0.1250
0.2113
0.3255
0.1807
ECC Registration
0.1202
0.0651
0.0913
0.1926
0.3033
0.1545
Gaussian Denoising་ECC Registration
0.0802
0.0437
0.0667
0.1636
0.2832
0.1274
Table 5. MSE values between five spectral bands and the 720 nm band for three processing methods. Fig. 13. Spectral image of grapes in six bands after Gaussian denoising. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

value of 0.90 Brix and R2 value of 0.78. However, overall, these traditional machine learning methods did
not achieve the precision required for practical production. The direct flattening feature extraction method,
although simple and straightforward, concatenates all features into a single feature vector, leading to excessively
high dimensionality. This increases the computational complexity of model training and prediction, makes the
model prone to overfitting, and loses the relative positional information between pixels. Both mean and variance
feature extraction methods suffer from information loss, failing to capture the complex structure of the data. The color histogram method, on the other hand, generates features by counting the number of pixels of different
colors, reflecting the color distribution of the image but ignoring the spatial relationship between pixels. Deep learning methods
In the field of deep learning, the proposed Improved-Res model was compared with seven classic deep learning
models, including LeNet, AlexNet, VGG-16, GoogleNet, DenseNet-121, EfficientNet-b0, and ResNet-50. Fig. 16. Histogram of MAE results of traditional machine learning methods. Fig. 15. Histogram of MSE results of traditional machine learning methods. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

The initial training configuration was set with a batch size of 32, a learning rate (lr) of 0.0001, a total of
300 epochs, the Adam optimizer, and the Mean Squared Error (MSE) as the loss function. Hyperparameter
optimization was conducted through grid search, evaluating learning rates of 0.0001, 0.001, and 0.01, as well as
batch sizes of 8, 16, and 32. The optimal combination was determined to be a learning rate of 0.001 and a batch
size of 8 based on validation loss performance. To ensure effective training, both early stopping and a learning rate scheduler were implemented. Early
stopping monitored the validation loss, with training halting if no significant improvement was observed for
50 consecutive epochs, thereby preventing overfitting and saving computational resources. Simultaneously, a
learning rate scheduler reduced the learning rate by a factor of 0.5 if the validation loss did not improve after
30 epochs. This adjustment allowed the model to refine its parameters and converge more effectively during
prolonged training. By coordinating these mechanisms, the training process leveraged both adaptive learning rates and controlled
stopping to achieve a balance between model performance and computational efficiency. The MSE, MAE and R2
results are shown in Figs. 18 and 19; Table 7. The five-fold cross-validation results of the Improved-Res model
are shown in Fig. 20; Table 8. The scatterplot of the Improved-Res model predictions on the test set is shown in
Fig. 21. Based on the results, the proposed Improved-Res model performed the best in the evaluation, with MSE value
of 0.49, MAE values of 0.55 Brix and R2 values of 0.92. This indicates that the model has the highest accuracy in
the task of predicting grape sugar content, making it the most superior among all evaluated models. ResNet-50
and EfficientNet-b0 also exhibited high accuracy, with MSE values of 0.95 and 0.97, MAE values of 0.96 Brix and
Traditional Machine Learning Methods
Metric
Flatten
Mean
Variance
Color Histogram
SVR
MSE
5.17
5.31
5.49
5.35
MAE/Brix
1.67
1.69
1.79
1.73
R2
0.14
0.11
0.09
0.09
GradientBoosting
MSE
5.89
5.53
7.41
6.51
MAE/Brix
1.78
1.76
2.17
1.92
R2
0.05
0.08
−0.46
−0.28
RandomForest
MSE
5.54
4.72
6.36
6.18
MAE/Brix
1.75
1.61
1.91
1.85
R2
0.08
0.20
−0.25
−0.22
XGBoost
MSE
4.17
4.02
4.24
1.35
MAR/Brix
1.56
1.55
1.59
0.90
R2
0.32
0.35
0.31
0.78
Table 6. The MSE, MAE, and R² results of traditional machine learning methods. Fig. 17. Histogram of R2 results of traditional machine learning methods. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

0.98 Brix, and R2 values of 0.84 and 0.83 respectively, second only to the Improved-Res model in performance. GoogleNet showed slight overfitting and achieved moderate overall performance. In contrast, LeNet, AlexNet,
and VGG-16 performed relatively poorly, with significant oscillations and suboptimal convergence. Ablation experiment
To validate the effectiveness of the proposed improvements to the ResNet-50 model, a series of ablation
experiments were conducted. These experiments involved incrementally adding different improvement modules
to the ResNet-50 model and observing their impact on the model’s performance. The experiments covered the
individual application of the SE attention module, depthwise separable convolution, and Inception module,
as well as their various combinations. By analyzing the results of these experiments, we can gain a clearer
understanding of the roles these improvement methods play within the ResNet-50 model, and gain valuable
insights and guidance for future model enhancements. The experimental environment, parameters, and evaluation methods remained consistent with those used in
the deep learning experiments mentioned earlier. Fig. 19. Histogram of R2 results of deep learning methods. Fig. 18. Histogram of MSE and MAE results of deep learning methods. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

The impact of Depthwise Separable Convolution (DSC) on inference time is shown in Table 9. The impact of
the SE attention module (SE), Depthwise Separable Convolution (DSC), and Inception module (Inception) on
MSE, MAE and R2 is shown in Figs. 22 and 23; Table 10. Based on the results, replacing the subsampling convolutional layer with DSC led to a decrease in the average
inference time per sample by 0.00178 s, while SPS (Samples Per Second) increased by 50.52. Models that added
the SE attention module alone, replaced the subsampling convolutional layer with DSC alone, and replaced the
feature extraction convolutional layer with the Inception module alone all performed better than the original
ResNet-50 model. Among these, the SE attention module showed the most significant improvement, reducing
MSE and MAE to 0.65 and 0.75 Brix, respectively, and increasing R² to 0.89, followed by the Inception module
and DSC. In combination improvements, the model incorporating both the SE attention module and the
Inception module showed further enhancement, with MSE and MAE reduced to 0.53 and 0.57 Brix, respectively,
and R² increased to 0.91. The best performance was achieved when combining the SE attention module, DSC, Fold
MSE
MAE/Brix
R2
Fold1
0.33
0.43
0.94
Fold2
0.54
0.55
0.91
Fold3
0.63
0.65
0.89
Fold4
0.55
0.59
0.91
Fold5
0.42
0.51
0.93
Mean
0.49
0.55
0.92
Standard Deviation (Std Dev)
0.1184
0.0829
0.0195
Table 8. Five-fold cross-validation results of the Improved-Res. Fig. 20. Five-fold cross-validation results of the Improved-Res. Deep Learning Methods
MSE
MAE/Brix
R2
LeNet
3.82
2.01
0.40
AlexNet
3.72
1.86
0.42
VGG-16
3.98
1.99
0.35
GoogleNet
1.83
1.88
0.70
DenseNet-121
1.00
1.11
0.82
EfficientNet-b0
0.97
0.98
0.83
Resnet-50
0.95
0.96
0.84
Improved-Res
0.49
0.55
0.92
Table 7. MSE, MAE and R2 results of deep learning methods. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

Fig. 22. The impact of SE, DSC, and Inception on MSE and MAE. With DSC
No DSC
Average Inference Time for a Single Set of Samples
0.02573
0.02751
SPS (Samples Per Second)
266.66
216.14
Table 9. The impact of depthwise separable Convolution on inference time. Fig. 21. The scatterplot of the Improved-Res model predictions on the test set. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

and the Inception module into the ResNet-50 model, resulting in MSE and MAE values of 0.49 and 0.55 Brix,
respectively, and R² increased to 0.92. Discussion
This study develops a high-precision, non-destructive sugar content detection method for Sunshine Rose grapes
using multispectral imaging and deep learning, providing key support for automated grape-picking and sorting. The proposed Improved-Res model demonstrated excellent accuracy in estimating grape maturity, achieving an
MSE of 0.49, an MAE of 0.55, and an R2 of 0.92, making taste differences nearly imperceptible. By integrating
spectral technology with an improved ResNet-50 model, the approach significantly outperforms traditional
machine learning and classical deep learning models. This innovation optimizes harvest timing, improves
market competitiveness, and advances smart agriculture, contributing to the modernization and automation of
the grape industry. While the results are promising, there is still room for improvement in feature extraction to
further enhance both precision and inference speed. The current experiments were conducted on Sunshine Rose grapes under natural conditions, but the dataset
lacks diversity in grape varieties and environmental scenarios. Expanding the dataset to include a wider range of
grape species and varying environmental conditions will be essential to improve the model’s generalizability and
robustness for real-world applications. For autonomous grape-picking robots, real-time decision-making and image processing are crucial for
adaptability and effective operation in dynamic environments. Currently, image acquisition under natural
conditions, specifically in clear weather with favorable ambient lighting, requires preprocessing configurations
to ensure reliable input for the models. To integrate these systems into picking robots, further experiments and
development are necessary to address existing limitations.
we also plan to develop a handheld device for non-destructive grape sugar content detection, enabling real-
time operation on resource-constrained hardware. Achieving this requires a balance between model accuracy
and computational efficiency, which can be addressed through optimization techniques such as compression and
MSE
MAE/Brix
R2
ResNet50
0.95
0.96
0.84
ResNet50 + SE
0.65
0.75
0.89
ResNet50 + DSC
0.76
0.81
0.88
ResNet50 + Inception
0.73
0.74
0.88
ResNet50 + SE + DSC
0.55
0.59
0.90
ResNet50 + SE + Inception
0.53
0.57
0.91
ResNet50 + DSC + Inception
0.60
0.63
0.89
ResNet50 + SE + DSC + Inception(Ours)
0.49
0.55
0.92
Table 10. Results table of the impact of SE, DSC, and inception on MSE, MAE and R2. Fig. 23. The impact of SE, DSC, and Inception on R2. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

quantization. Furthermore, deployment on mobile devices is feasible if they are equipped with a multispectral
camera. Finally, while deep learning has driven significant advancements in various fields, its lack of interpretability
remains a major challenge and an area of active research. Despite their impressive performance, developing
interpretable mechanisms for these models is vital. Such mechanisms could provide deeper insights into the
decision-making process, fostering trust and enabling further optimization for complex, real-world scenarios. Conclusion
This paper preprocessed self-collected grape multispectral images through denoising and alignment, combined
with corresponding sugar content data, to construct a dataset for training a sugar content prediction model. Based on the ResNet-50 residual network, a grape sugar content prediction regression model Improved-Res
is proposed, replacing the subsampling convolutional layer in the Bottleneck residual block with Depthwise
Separable Convolution, replacing the feature extraction convolutional layer with the Inception module, and
adding the SE attention module. Compared to traditional machine learning methods including support vector
machine regression, gradient boosting regression, random forest regression and XGboost regression, as well
as classic deep learning models such as LeNet, AlexNet, VGG-16, GoogleNet, DenseNet-121, EfficientNet-b0,
and ResNet-50, the proposed model demonstrated significantly improved accuracy. Finally, through ablation
experiments, the effectiveness of the enhancement modules was validated, further confirming the superior
performance of the model. Data availability
Data will be made available on request. For data requests, please contact the corresponding author, Yunchang Li,
at [chenym@hunau.edu.cn](mailto: chenym@hunau.edu.cn). Received: 24 December 2024; Accepted: 17 September 2025
References

### 1. Coombe, B. G. Research on development and ripening of the grape berry. Am. J. Enol. Viticult. 43, 101–110 (1992).

### 2. Jing-tao, S. et al. Research progress on Non-Destructive detection technology for grape quality. Spectrosc. Spectr. Anal. 40, 2713–

2720 (2020).

### 3. Jing, W., Wen, M. & Gang, J. Research progress on the application of machine vision technology for non-destructive testing of

grape quality. Journal Agricultural Sciences, 1–14, ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​9​0​7​/​j​.​c​n​k​i​.​n​y​k​x​y​j​.​2​0​2​5​0​2​2​5​.​0​0​1

### 4. Jing, Z. et al. Recent advances in application of Near-Infrared spectroscopy for quality detections of grapes and grape products. Spectrosc. Spectr. Anal. 41, 3653–3659 (2021).

### 5. Jing, W., Ang, Z., Wen, M. & Gang, J. & Guo-qian, X. Research progress on the application of hyperspectral technology for non-

destructive testing of grape quality. Food Science. 45, 1–18 (2024).

### 6. Wei, X., Xie, F., Wang, K., Song, J. & Bai, Y. A study on Shine-Muscat grape detection at maturity based on deep learning. Sci. Rep.

13, 4587 (2023).

### 7. Xinguang, W., Linlin, W., Dong, G., Mingze, Y. & Yikui, B. Prediction of the Maturity of Greenhouse Grapes Based on Imaging

Technology. Plant Phenomics 9753427–9753427 (2022). (2022).

### 8. Xiao-hong, W. & Rui-jie, H. Application of fruit maturity based on image recognition technology. J. Agricultural Mechanization

Res. 46, 207–211. https://doi.org/10.13427/j.cnki.njyi.2024.01.023 (2024).

### 9. Murru, C., Chimeno-Trinchet, C., Díaz-García, M. E., Badía-Laíño, R. & Fernández-González, A. Artificial neural network and

attenuated total Reflectance-Fourier transform infrared spectroscopy to identify the chemical variables related to ripeness and
variety classification of grapes for Protected. Designation of origin wine production. Comput. Electron. Agric. 164, 104922 (2019).

### 10. Xing, S. Non-Destructive Detection and Grading of The Ouality of Red Grape Strings Based on Visualtechnology, (2021).

### 11. Varga, L. A., Makowski, J. & Zell, A. in 2021 International Joint Conference on Neural Networks (IJCNN). 1–8 (IEEE).

### 12. Sheng, G. & Jian-hua, X. Hyperspectral image information fusion-based detection of soluble solids content in red Globe grapes. Computers and Electronics in Agriculture. 196, 106822(2022).

### 13. Sheng-xian, Y. et al. Cabernet Gernischt maturity determination based on Near-Ground multispectral figures by using UAVs. Spectrosc. Spectr. Anal. 41, 3220–3226 (2021).

### 14. Lanjewar, M. G., Panchbhai, K. G. & Patle, L. B. Sugar detection in adulterated honey using hyper-spectral imaging with stacking

generalization method. Food Chem. 450, 139322 (2024).

### 15. Lanjewar, M. G., Asolkar, S., Parab, J. S. & Morajkar, P. P. Detecting starch-adulterated turmeric using Vis-NIR spectroscopy and

multispectral imaging with machine learning. J. Food Compos. Anal. 136, 106700 (2024).

### 16. Tsakiridis N L. et al. In situ grape ripeness Estimation via hyperspectral imaging and deep autoencoders. Computers and Electronics

in Agriculture. 212, 108098(2023).

### 17. Wen-zheng, L. et al. Detection of key indicators of ripening quality in table grapes based on Visible-near-infrared spectroscopy. Trans. Chin. Soc. Agricultural Mach. 55, 372–383 (2024).

### 18. Panchbhai, K. G. & Lanjewar, M. G. Portable system for cocoa bean quality assessment using Multi-Output learning and

augmentation. Food Control. 174, 111234 (2025).

### 19. Xiao-bin, T. & Tong, S. Review of Development of Deep Learning Framework. The World of Survey and Research, 83–88, (2023). ​h​

t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​7​7​8​/​j​.​c​n​k​i​.​1​1​-​3​7​0​5​/​c​.​2​0​2​3​.​0​4​.​0​0​9

### 20. Ribera-Fonseca, A., Noferini, M., Jorquera-Fontena, E. & Rombolà, A. D. Assessment of technological maturity parameters and

anthocyanins in berries of cv. Sangiovese (Vitis vinifera L.) by a portable vis/NIR device. Sci. Hort. 209, 229–235 (2016).

### 21. Yi-lei, H., Hong-zhe, J., Hong-ping, Z. & Ying, W. Research progress on nondestructive detection of fruit maturity by near infrared

spectroscopy and hyperspectral imaging. Sci. Technol. Food Ind. 42, 377–383. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​3​8​6​/​j​.​i​s​s​n​1​0​0​2​-​0​3​0​6​.​2​0​2​0​0​7​0​0​7​
4 (2021).

### 22. Zhi, H., Jun, S. & Yang, X. Bai-yi, L. Application of various filters in image denoising preprocessing. Practical Electron. 32, 74–77. ​

h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​6​5​8​9​/​j​.​c​n​k​i​.​c​n​1​1​-​3​5​7​1​/​t​n​.​2​0​2​4​.​0​8​.​0​3​3 (2024).

### 23. Dong-yang, S., Jun-lin, Z. & Tian-guang, L. Zheng-ping, W. Research on image defogging algorithm based on tolerance mechanism

and Gaussian filtering. Chongqing Univ. Sci. Technology(Natural Sci. Edition). 25, 56–62. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​9​4​0​6​/​j​.​c​n​k​i​.​c​q​k​j​x​y​x​b​z​
k​b​.​2​0​2​3​.​0​5​.​0​0​6 (2023).

### 24. D, E. G. & Z, P. E. Parametric image alignment using enhanced correlation coefficient maximization. IEEE Trans. Pattern Anal. Mach. Intell. 30, 1858–1865 (2008). Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

### 25. He, K., Zhang, X., Ren, S. & Sun, J. in Proceedings of the IEEE conference on computer vision and pattern recognition. 770–778.

### 26. Jun-peng, T. et al. Bearing fault diagnosis based on adaptive Denoise residual network with image features ofvibration signals. Noise Vib. Control. 44, 109–116 (2024).

### 27. Yong, W., Zi-yin, L., Xiao-dong, W., Fei, Y. & Jun, J. Classification algorithm of class imbalance cocoon images based on improved

ResNet-50. Acta Sericologica Sinica. 50, 1–14 (2024).

### 28. Muhammad, S. & Zhaoquan, G. Deep residual learning for image recognition: A survey. Appl. Sci. 12, 8972–8972 (2022).

### 29. Jie, H., Li, S., Samuel, A., Gang, S. & Enhua, W. Squeeze-and-Excitation networks. IEEE Trans. Pattern Anal. Mach. Intell. 42, 1–1

(2019).

### 30. Guo-shuai, W. et al. Classification of wheat Stripe rust based on improved S-ResNet34 model. Journal Nanjing Agricultural

University. 48, 1–13 (2024).

### 31. Chao-ran, S., Da-long, Z., Yong, H. & An, D. RF fingerprint recognition based on SE attention Multi-Source domain adversarial

network. Computer Science. 52, 1–13 (2024).

### 32. Peng-cheng, X. et al. Research on scrap classification and rating method based on SE attention mechanism. Chin. J. Eng. 45,

1342–1352. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​3​7​4​/​j​.​i​s​s​n​2​0​9​5​-​9​3​8​9​.​2​0​2​2​.​0​6​.​1​0​.​0​0​2 (2023).

### 33. Yuan-hao, J., Jin-pu, X. & Bei-bei, Y. Jun-long, X. A method for detecting quality and defects in Raw coffee beans based on

improved ResNet50 model. J. Chin. Agricultural Mechanization. 45, 237–243. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​7​3​3​/​j​.​j​c​a​m​.​i​s​s​n​.​2​0​9​5​-​5​5​5​3​.​2​0​2​4​.​0​4​.​0​3​4 (2024).

### 34. Szegedy, C. et al. Going Deeper with Convolutions. CoRR abs/1409.4842 (2014).

### 35. Chollet, F. & Xception Deep Learning with Depthwise Separable Convolutions. CoRR abs/1610.02357 (2016).

### 36. Howard, A. G. et al. Mobilenets: Efficient convolutional neural networks for mobile vision applications. arXiv preprint

arXiv:1704.04861 (2017).

### 37. Ioffe, S. & Szegedy, C. Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift. CoRR

abs/1502.03167 (2015).

### 38. Li, S. et al. Deep learning for hyperspectral image classification: an overview. IEEE Trans. Geosci. Remote Sens. 57, 6690–6709

(2019).

### 39. Yang, X. et al. Hyperspectral image classification with deep learning models. IEEE Trans. Geosci. Remote Sens. 56, 5408–5423

(2018).

### 40. Szegedy, C., Vanhoucke, V., Ioffe, S., Shlens, J. & Wojna, Z. Rethinking the Inception Architecture for Computer Vision. CoRR

abs/1512.00567 (2015).

### 41. Szegedy, C., Ioffe, S. & Vanhoucke, V. Inception-v4, Inception-ResNet and the Impact of Residual Connections on Learning. CoRR

abs/1602.07261 (2016).

### 42. Bo, Z. et al. Fault Diagnosis of Proton Exchange Membrane Fuel Cell Integrated System Based on GoogleNet and Transfer

Learning. Proceedings ofthe CSEE, 1–12, (2024). https://doi.org/10.13334/j.0258-8013.pcsee.230210

### 43. Panchbhai, K. G. & Lanjewar, M. G. Detection of amylose content in rice samples with spectral augmentation and advanced

machine learning. Journal of Food Composition and Analysis. 142, 107455 (2025).

### 44. Fa-qiang, W., Hong-zhi, Z., Peng, W. & Hong, D. Da-peng, Z. Research progress on the similarity learning methods in computer

vision. Intell. Comput. Appl. 9, 149–152 (2019).

### 45. Jiang-tao, W., Yuan-kun, B., Jian-yun, Z. & Wei-zhong, L. Ming-jie, W. Application of geographic weighted machine learning

models in Above-ground carbon stock Estimation on individual trees. J. Northeast Forestry Univ. 52, 98–105. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​3​
7​5​9​/​j​.​c​n​k​i​.​d​l​x​b​.​2​0​2​4​.​0​6​.​0​1​4​ (2024).

### 46. Yi-ming, L., Jun-han, Y., Zhong-li, Z. & Pei-qi, X. Nian-xiong, L. A comparative study of machine learning algorithm models for

predicting carbon emissions of residential buildings in cold zone. Tsinghua Univ. (Sci Technol). 1–12. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​6​5​1​1​/​j​.​c​n​
k​i​.​q​h​d​x​x​b​.​2​0​2​4​.​2​2​.​0​3​1​ (2024).

### 47. Liashchynskyi, P. & Liashchynskyi, P. Grid search, random search, genetic algorithm: a big comparison for NAS. arXiv preprint

arXiv::1912.06059. (2019). Author contributions
Y. M. C. Conceptualization, Data curation, Formal analysis, Funding acquisition, Project administration, Re­
sources, Supervision, Writing – review and editing. J. Z. D. Conceptualization, Data curation, Formal analysis, Investigation, Methodology, Software, Validation, Visualization, Writing – original draft. Z. J. L. Data curation. J. C. C. Writing – review and editing. W. W. Data curation. Y. P. X. Project administration, Supervision. X. H. Z. Re­
sources, Supervision. C. Y. L. Funding acquisition, Project administration, Resources, Supervision. Funding
This study was funded by the Key Research and Development Project of the Science and Technology Plan of
Hunan Province, China (No. 2020NK2033) and the Natural Science Foundation Project of Changsha City, Hunan Province, China (No. kq2402123). Declarations
Competing interests
The authors declare no competing interests. Ethical approval
This article does not contain any studies with human participants or animals by any of the authors. Additional information
Correspondence and requests for materials should be addressed to C. L. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations. Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/

Open Access  This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives
4.0 International License, which permits any non-commercial use, sharing, distribution and reproduction in
any medium or format, as long as you give appropriate credit to the original author(s) and the source, provide
a link to the Creative Commons licence, and indicate if you modified the licensed material. You do not have
permission under this licence to share adapted material derived from this article or parts of it. The images or
other third party material in this article are included in the article’s Creative Commons licence, unless indicated
otherwise in a credit line to the material. If material is not included in the article’s Creative Commons licence
and your intended use is not permitted by statutory regulation or exceeds the permitted use, you will need to
obtain permission directly from the copyright holder. To view a copy of this licence, visit ​h​t​t​p​:​/​/​c​r​e​a​t​i​v​e​c​o​m​m​o​
n​s​.​o​r​g​/​l​i​c​e​n​s​e​s​/​b​y​-​n​c​-​n​d​/​4​.​0​/​.​
© The Author(s) 2025
Scientific Reports | (2025) 15:36927

| https://doi.org/10.1038/s41598-025-20848-3
www.nature.com/scientificreports/
