# Higher-order Sonification of the Human Brain

**Year:** D:20

---

Higher-order Sonification of the Human Brain
Francisco-Shu Kitaura
University of La Laguna
Emi-Pauline Kitaura
Institute for Astrophysics of the Canary Islands
Niels Janssen
University of La Laguna
Antonella Maselli
Institute of Cognitive Sciences and Technologies, National Research Council (CNR)
Ernesto Pereda
University of La Laguna
Aurelio Carnero-Rosell
Institute for Astrophysics of the Canary Islands
Article
Keywords: Posted Date: June 26th, 2025
DOI: https://doi.org/10.21203/rs.3.rs-6623643/v1
License:   This work is licensed under a Creative Commons Attribution 4.0 International License. Read Full License
Additional Declarations: No competing interests reported. Version of Record: A version of this preprint was published at Scientific Reports on November 27th,

### 2025. See the published version at https://doi.org/10.1038/s41598-025-26438-7. Higher-order Soniﬁcation of the Human Brain
Francisco-Shu Kitauraa,b,*, Emi-Pauline Kitauraa, Niels Janssenc,d,e, Antonella Masellif, Ernesto Peredad,e,g, and Aurelio Carnero Rosella,b
aInstituto de Astrof´ısica de Canarias, C/ V´ıa L´actea, s/n, E-38205, San Crist´obal de La Laguna, Spain
bDepartamento de Astrof´ısica, Universidad de La Laguna (ULL), E-38206, San Crist´obal de La Laguna, Spain
cFacultad de Psicolog´ıa, Universidad de la Laguna (ULL), E-38200, San Crist´obal de La Laguna, Spain
dInstituto de Tecnolog´ıas Biom´edicas (ITB), Universidad de La Laguna (ULL), E-38200, San Crist´obal de La
Laguna, Spain
eInstituto Universitario de Neurociencias (IUNE), Universidad de la Laguna (ULL), E-38200, San Crist´obal de La
Laguna, Spain
fInstitute of Cognitive Sciences and Technologies, National Research Council (CNR), Rome, Italy
gDepartmento de Ingenier´ıa Industrial, Universidad de la Laguna (ULL), E-38200, San Crist´obal de La Laguna, Spain
*fkitaura@ull.edu.es
ABSTRACT
Soniﬁcation, the process of translating data into sound, has recently gained traction as a tool for both disseminating scientiﬁc
ﬁndings and enabling visually impaired individuals to analyze data. Despite its potential, most current soniﬁcation methods
remain limited to one-dimensional data, primarily due to the absence of practical, quantitative, and robust techniques for
handling multi-dimensional datasets. We analyze structural magnetic resonance imaging (MRI) data of the human brain by integrating two- and three-point statistical
measures in Fourier space: the power spectrum and bispectrum. These quantify the spatial correlations of 3D voxel intensity
distributions, yielding reduced bispectra that capture higher-order interactions. To showcase the potential of the soniﬁcation
approach, we focus on a reduced bispectrum conﬁguration which applied to the OASIS-3 dataset (864 imaging sessions),
yields a brain age regression model with a mean absolute error (MAE) of 4.7 years. Finally, we apply soniﬁcation to the
ensemble-averaged (median) outputs of this conﬁguration across ﬁve age groups: 40–50, 50–60, 60–70, 70–80, and 80–100
years. The auditory experience clearly reveals differentiations between these age groups, an observation further supported
visually when inspecting the corresponding sheet music scores. Our results demonstrate that the information loss (e.g.,
normalized mean squared error) during the reconstruction of the original bispectra, speciﬁcally in conﬁgurations sensitive to
brain aging, from the soniﬁed signal is minimal. This approach allows us to encode multi-dimensional data into time-series-like
arrays suitable for soniﬁcation, creating new opportunities for scientiﬁc exploration and enhancing accessibility for a broader
audience. The technique of soniﬁcation has emerged as a valuable tool in various ﬁelds for its ability to transform complex data into
auditory experiences1, making it easier for researchers and the public alike to grasp intricate concepts (e.g.,2). Beyond its role
in disseminating scientiﬁc ﬁndings, soniﬁcation also serves as a crucial assistive technology for visually impaired individuals,
allowing them to analyze data through auditory means (e.g.,3,4). Soniﬁcation might even help revealing unrecognized patterns
and feedbacks in unwieldy datasets5. A wide number of soniﬁcation methods and algorithms have been developed and applied
in the context of astronomy6–17 and other ﬁelds (e.g.,18,19). Recently, Artiﬁcial Intelligence algorithms based on Neural
Networks and Deep Learning have also been implemented20,21. Enge et al.22 present an overview of the ﬁeld of soniﬁcation,
analyzing the complementarity and redundancy between soniﬁcation and visualization. Recent studies even suggest that data
soniﬁcation has emerged as a viable alternative to data visualization23. It has been shown that audiﬁcation as a tool for the spectral analysis of time-series data24 can be particularly useful in
the presence of low signal-to-noise ratios, where smaller biases are obtained with auditory than with visual stimuli25. For
long, it has been suggested to use the loudness, pitch, and duration of each instrumental tone to obtain a multi-dimensional
perceptual scaling of musical timbres26. In fact, soniﬁcation can also be used to represent additional dimensions in complex
multi-dimensional datasets27–29. Audiﬁcation and soniﬁcation of texture in images, have also been proposed30 to represent
spatial data, for example, in the context of geographical information31,32, and biomedicine33,34. However, despite its growing popularity and utility as an additional tool to visualisation35, current soniﬁcation methods
are primarily limited to one-dimensional data due to the lack of practical and robust methods for quantitatively handling
multi-dimensional data with solely auditory stimuli. This limitation signiﬁcantly restricts the range of applications and the

depth of insight that soniﬁcation can provide. To address this gap, there is a need for innovative approaches that can effectively
capture the complexity of multi-dimensional datasets and translate them into meaningful quantitative auditory representations. One discipline poised to greatly beneﬁt from soniﬁcation methods capable of handling multidimensional data is neuroimag-
ing. The primary goal of this ﬁeld is to extract meaningful information from complex 3D and 4D images that capture both the
structure (3D) and dynamics (4D, with time as the fourth dimension) of the human brain, recorded through tomographic tech-
niques such as X-ray computed tomography (CT), positron emission tomography (PET), or magnetic resonance imaging (MRI). In MRI, for instance, highly detailed 3D images of brain structures are obtained with excellent spatial resolution—typically
using cubic voxels measuring 1×1×1 mm—where voxel intensity reﬂects the type and density of tissue. While these images
are commonly used in clinical settings to detect abnormalities or injuries, advanced mathematical techniques in neuroimaging
research allow for the quantiﬁcation of these images and the identiﬁcation of subtle differences between groups (e.g., healthy
versus pathological subjects or across different age groups) or within the same individual over time. These differences are
often not visually apparent due to the complexity of the 3D data, necessitating the use of sophisticated analytical tools to
uncover them (see, e.g.,36). Soniﬁcation could offer an innovative approach to making these hidden patterns more accessible
and interpretable. In this study, as part of the CosmicBrain project, we propose a novel soniﬁcation method that leverages higher-order
statistics in Fourier space to construct one-dimensional arrays from multi-dimensional data and apply it to human brain magnetic
resonance imaging (MRI). The analysis of three-dimensional spatial distributions is a well-established approach in cosmological large-scale structure
studies, particularly for understanding the clustering properties of complex systems. In this context, we focus on using two-point
and three-point correlation functions to probe the underlying structure of the data. The two-point function captures pairwise
correlations, but the three-point function extends this to higher-order statistics. It was ﬁrst computed in conﬁguration space
in the 1970s from the three-dimensional galaxy distribution37, and later extended to Fourier space as the bispectrum38. The
three-point statistics are precious in cosmological studies for understanding structure formation39 and for investigating the bias
between galaxies and dark matter tracers40 as it is sensitive to non-Gaussianities induced by gravitational evolution. These
statistics are sensitive to the complex, multidimensional patterns in the data, capturing information beyond what two-point
statistics can reveal41. By combining two- and three-point statistics, we gain a more comprehensive understanding of the
clustering properties of structures, an approach that has been successfully applied to galaxy survey data (see42). In particular,
the three-point function measures non-Gaussian features that are key for understanding the cosmic web’s morphology39. Using three-dimensional MRI data, our study leverages these well-established statistical tools to characterize the clustering
of brain structures. This is part of the CosmicBrain project, where the same techniques used in cosmology have been adapted
to analyze the human brain, mainly to provide tools for the early diagnosis of neurodegenerative diseases (see Carnero-Rosell
et al.43). The cosmic density ﬁeld represents a multivariate statistical problem, where each voxel in the three-dimensional grid
provides statistical information about the cosmic volume44. Similarly, in the context of brain MRI, each voxel represents a
location within the brain’s anatomy, allowing us to capture intricate spatial distributions. By applying two- and three-point
statistics to brain MRI data in Fourier space, we transform this complex three-dimensional information into a more interpretable
format, such as the clustering amplitude of a triangle conﬁguration given two sides as a function of the subtended angle. This
kind of data can be trivially converted into time-series data for soniﬁcation. The combination of two- and three-point statistical
analysis allows for a robust framework that captures the essential structural characteristics of the data, opening up new avenues
for scientiﬁc inquiry and improving data accessibility. Details on the soniﬁcation method can be found in the methods section
(see Figure 1). Soniﬁcation of bispectra from magnetic resonance imaging data
Based on the OASIS-3 database (see methods section), we examine the bispectrum conﬁguration of the MRI data from healthy
subjects in different age ranges, which exhibits complex behavior by integrating information from both the two- and three-point
statistics, commonly referred to as the reduced bispectrum. For a comprehensive introduction to higher-order statistics and
reduced bispectra in particular, we refer to Carnero-Rosell et al.43 and references therein. Speciﬁcally, we focus on the reduced
bispectrum conﬁguration Q019036 with wave numbers k1 = 0.19 and k2 = 0.36 mm−1 (see ﬁgure 3). Using this particular
conﬁguration as a biomarker achieves an averaged mean absolute error (MAE) of approximately 4.7 years for predicting age
between ∼40 and 100 years. We employed a Random Forest classiﬁer45 using a leave-one-out cross-validation (LOO-CV)
technique46, ensuring that each subject’s estimate was independent of the training sample. Age-regression with neural networks
can improve the MAE to 4.2 years with the same bispectrum conﬁguration43. Importantly, exploring additional bispectrum
conﬁgurations is beneﬁcial, as it allows capturing information across multiple spatial scales (both large and small), thus enabling
a more comprehensive characterization of brain aging. We selected the conﬁguration above as a challenging example since it
spans a wide range of values yet demonstrates subtle internal variations, which are particularly difﬁcult to represent effectively
through soniﬁcation.
2/19

3D-space
multivariate
distributions
higher-order
statistics
triangle
conﬁgurations
stick lengths
soniﬁcation
Cosmic Brain
project
1D-signal
encoding 3D information

Time [beats]

Midi note numbers
θ
Figure 1. This diagram illustrates the soniﬁcation method for three-dimensional data, utilizing higher-order statistical analysis
in Fourier space. The two-point statistics are represented by sticks of varying lengths, which connect pairs of voxels (in the
conﬁguration space analog), indicating their respective intensities from the MRI scan. The three-point statistics are depicted
through different triangle conﬁgurations, where two ﬁxed side lengths are considered with varying subtended angles to connect
three voxels. A one-dimensional function is derived by combining these statistical measures, which can then be directly
soniﬁed.
3/19

frequency [kHz]
C1
D1

## E1 F1

G1
A1

## B1 C2

D2
E2
F2
G2
A2
B2
C3
D3

## E3 F3

G3
A3

## B3 C4

D4
E4
F4
G4
A4
B4
C5
D5

## E5 F5

G5
A5

## B5 C6

D6
E6
F6
G6
A6
B6
C7
D7

## E7 F7

G7
A7

## B7 C8

D8
E8
F8
G8
A8
B8
C#1
D#1
F#1
G#1
A#1
C#2
D#2
F#2
G#2
A#2
C#3
D#3
F#3
G#3
A#3
C#4
D#4
F#4
G#4
A#4
C#5
D#5
F#5
G#5
A#5
C#6
D#6
F#6
G#6
A#6
C#7
D#7
F#7
G#7
A#7
C#8
D#8
F#8
G#8
A#8
notes
C1+25
D1+25
E1+25
F1+25
G1+25
A1+25
B1+25
C2+25
D2+25
E2+25
F2+25
G2+25
A2+25
B2+25
C3+25
D3+25
E3+25
F3+25
G3+25
A3+25
B3+25
C4+25
D4+25
E4+25
F4+25
G4+25
A4+25
B4+25
C5+25
D5+25
E5+25
F5+25
G5+25
A5+25
B5+25
C6+25
D6+25
E6+25
F6+25
G6+25
A6+25
B6+25
C7+25
D7+25
E7+25
F7+25
G7+25
A7+25
B7+25
C8+25
D8+25
E8+25
F8+25
G8+25
A8+25
B8+25
Figure 2. Soniﬁcation piano: notes used in this study covering the frequency range within the sensitivity of adult humans
(20-30 yrs: ∼16, 40 yrs: ∼14, 50 yrs: ∼12, 60 yrs: ∼10, 70 yrs: ∼8 kHz). Regular notes (Ci, Di, Ei, Fi, Gi, Ai, Bi for different
octaves i ranging from 1 to 8) have been split into two columns (ﬁrst two on the left) for visualisation purposes. The same has
been done with quarter tones (indicated by +25) on the right. Semitones are indicated in the third column on the left. The
piano convention of black keys for semitones is adopted. We consider soniﬁcation cases with and without quarter tones
depending on the bispectrum conﬁguration and the desired accuracy.
4/19

40-45
45-50
50-55
55-60
60-65
65-70
70-75
75-80
80-85
85-90
90-100
Age Bins

Number of Subjects
OASIS-3

MAE
Subjects per Age Bin and MAE in Q019036

PREDICTION [yrs]
AGE [yrs]
Figure 3. On the left: age distribution for the OASIS-3 864 MRI sessions dataset reduced by Carnero-Rosell et al.43 with the
corresponding MAE at different AGE bins according to Random Forests classiﬁcation based solely on the Q019036
bispectrum conﬁguration. On the right: corresponding age regression.
−2

Bispectrum
Original Data 80 −100
Soniﬁed Data 80 −100
Reference Data 40 −50
0.75
1.00
1.25
Ratio

Angle/Time
−0.025
0.000
Diﬀerence

Diﬀ−Bispectrum
Original Data 80 −100 to 40 −50
Soniﬁed Data 80 −100 to 40 −50
0.8
1.0
1.2
Ratio

Angle/Time
−0.05
0.00
0.05
Diﬀerence
Figure 4. Soniﬁcation of bispectra from human MRI, using an age group of 80-100 years as an example. The original data
and the corresponding inverse mapping after soniﬁcation are displayed, with the bispectrum for the 40-50 age group included
as a reference. The ratios and differences between the original and the inverse-mapped soniﬁed signals are also presented.
5/19













































































































Group 80−100 with reference 40−50






























































































Group 40−50
Figure 5. Scores corresponding to (top:) the age group of 80 to 100 using as the reference the group of 40 to 50 to set the
range; and (bottom:) the age group of 40 to 50.
6/19












































































Difference between groups 80−100 and 40−50
Figure 6. Scores corresponding to the difference between the age group of 80 to 100 with the group of 40 to 50.
7/19

Our goal is to assign distinct musical notes and envelope to the signiﬁcant variations in the bispectrum signal, allowing
for a smooth auditory representation of its transitions, while ensuring the signal remains within the audible frequency range
for adult human listeners. This task becomes challenging, when realising the large bispectrum range differences between the
younger and older groups. To achieve this, we have selected a range of notes spanning eight octaves, including semitones
and, when necessary, quarter tones, covering frequencies from a few tens of Hertz up to approximately 8 kHz. While further
tone subdivisions are possible, they would likely compromise auditory distinguishability. The frequency range was chosen
to encompass both the subtle and signiﬁcant variations in the bispectrum signal, ensuring that the transitions are captured
smoothly and remain within the audible range for adult humans. For more details, see Figure 2 and methods section, where
the speciﬁc frequency mapping and note selection are discussed in depth. This setup has allowed us to accurately sonify the
bispectra across different age groups while maintaining a consistent amplitude range. Technical details of the soniﬁcation
procedure can be found in the methods section. We based the amplitude range on the group exhibiting the largest variations,
speciﬁcally the youngest cohort in our sample: 40-50 years (see left panel in Figure 4). By standardizing the amplitude in this
way, we ensure that the soniﬁcation of bispectrum variations remains comparable across age groups, providing a clear auditory
representation of the differences in the bispectrum signal across the age spectrum. To assess the accuracy of the soniﬁcation procedure, we adopt an information-theoretic approach to evaluate how well the
original signal can be recovered after undergoing soniﬁcation (see methods section). This process involves discretizing the
continuous bispectrum signal into integer values, and the challenge lies in determining how much information is lost in this
transformation. By analyzing the ﬁdelity of the recovered signal compared to the original, we can quantify the effectiveness of
the soniﬁcation process and ensure that the discretization does not signiﬁcantly degrade the essential features of the bispectrum
signal. We treat the originally measured bispectrum from MRI data and its soniﬁed version in two ways: ﬁrst, as a "ground
truth" function Y and a "modeled" function ˆY, and second, as their corresponding probability distribution functions P and Q,
respectively. The accuracy of the soniﬁcation method is then evaluated through metrics deﬁned between Y and ˆY, or between P
and Q, allowing us to measure the ﬁdelity of the soniﬁed signal compared to the original. During the reconstruction study, we found that the discretization step can introduce systematic biases, which could affect
the accuracy of the soniﬁed signal. However, applying an appropriate rounding procedure, can effectively mitigate these biases. While the differences between distant age groups are perceptible in the soniﬁcations, distinguishing between closer age groups
becomes more challenging. For instance, it is difﬁcult to differentiate between the 40-50 and 50-60 year age groups. This is due
to the more subtle variations in the bispectrum signal for these adjacent age ranges, which are less pronounced in the auditory
representation than the differences observed between more distant groups. To address this challenge, we propose sonifying the differences between different age groups’ bispectrum signals, rather
than the signals themselves (see right panel in Figure 4). This approach emphasizes the subtle variations that might otherwise
be hard to distinguish. Additionally, to further enhance the soniﬁed output, we introduce a normalization factor (less than 1)
that ampliﬁes these differences, making them more perceptible. This normalization highlights the variations and ensures that
the signal remains within a consistent and manageable auditory range. Another way to enhance the soniﬁed representation
of the bispectrum signal involves applying a nonlinear transformation that stretches or compresses the dynamic range of the
data. This technique improves the dynamic representation of the soniﬁed signal by amplifying or reducing the variations in
amplitude, making subtle differences more perceptible, without altering the overall structure or rank order of the data. Applying
this technique we have found ways to reduce the ratio deviations (see Figure 10). By applying this approach to the differences between the age groups 40-50 and 50-60, 40-50 and 70-80, as well as 40-50
and 80-100, we observe surprisingly similar signal shapes across these comparisons, although the amplitudes differ, indicating
a potential homologous brain aging. However, the amplitude variation can be effectively managed with adaptive normalization,
ensuring that the differences remain perceptible while maintaining a consistent volume range for the soniﬁed signals. Based on the results shown in Figure 4 we write the corresponding scores with tones and semitones. The scores correspond-
ing to the soniﬁed bispectrum signals for the 80–100-year and 40–50-year age groups are shown in Figure 5. The score in
Figure 6 highlights the structured patterns in the differences between these age groups, emphasizing the informational content
underlying these variations. Discussion
In this work, we investigated the use of soniﬁcation of higher-order summary statistics as a method for characterizing complex
multidimensional patterns within one-dimensional time series. In particular, we explored soniﬁcation of bispectrum signals derived from MRI data, with the goal to provide an intuitive
and effective auditory representation of complex higher-order statistics, such as the reduced bispectrum. This method holds
promise for diagnostic applications, particularly in detecting early signs of dementia and monitoring deviations from expected
bispectrum patterns for speciﬁc age groups.
8/19

We have introduced a large notes array, offering a densely distributed set of notes to capture and sonify subtle differences in
the bispectrum signal. This array spans a wide frequency range, allowing for the representation of both ﬁne details and broader
variations in the data. By ensuring a sufﬁcient number of notes across the audible spectrum, we can maintain precision in
the soniﬁcation process, making even minor deviations perceptible while preserving the overall integrity of the signal. This
approach ensures that the full range of bispectrum variations is accurately conveyed through sound. Additionally, we have demonstrated how to enhance the bispectrum signal for soniﬁcation through appropriate normalization,
ensuring that amplitude variations remain within a manageable and perceptible range. Furthermore, we have introduced
nonlinear rank-ordered transformations to reduce deviations, allowing for dynamic adjustments that stretch or compress the
signal’s range while preserving the relative structure and order of the data. These techniques collectively improve the accuracy
and clarity of the soniﬁed signal, making subtle differences more audible and enhancing the overall effectiveness of the
soniﬁcation process. The examples shown in this study also demonstrate the potential of sonifying bispectrum difference signals for acoustic
diagnostics, particularly identifying deviations from a reference bispectrum signal for a speciﬁc age group. By focusing on the
differences between bispectrum signals, subtle variations that might indicate cognitive changes can be identiﬁed, providing
a novel and potentially effective method for early detection through auditory analysis. The extension of this study to the
soniﬁcation of bispectrum signal conﬁgurations across multiple scales can signiﬁcantly enhance and deepen diagnostic analysis. While this approach shows promise, a thorough study investigating its full potential for medical diagnostics, particularly in
neurodegenerative diseases, is left for future work. One may investigate the potential relationship between the soniﬁcation of brain MRI and the process of speech production,
where the brain plausibly transforms complex, multidimensional signals (i.e., thoughts) into a linear sequence of speech sounds. The soniﬁcation technique presented here can generally be used to analyse any multi-dimensional data from any ﬁeld of
research, such as, in the ﬁeld of neuroscience: functional MRI, positron emission tomography, or even functional connectivity
maps derived from EEG and MEG, which makes it a very promising tool in the ﬁeld. References

### 1. Kramer, G. Auditory display: Soniﬁcation, audiﬁcation, and auditory interfaces (1994).

### 2. Sawe Nik, T. J., Chafe Chris. Using Data Soniﬁcation to Overcome Science Literacy, Numeracy, and Visualization Barriers

in Science Communication. Front. Commun. 5, 46, DOI: 10.3389/fcomm.2020.00046 (2020).

### 3. Arcand, K. K. et al. A Universe of Sound: Processing NASA Data into Soniﬁcations to Explore Participant Response.

arXiv e-prints arXiv:2403.18082, DOI: 10.48550/arXiv.2403.18082 (2024). 2403.18082.

### 4. Ediyanto & Kawai, N. Science Learning for Students with Visually Impaired: A Literature Review. In Journal of Physics

Conference Series, vol. 1227 of Journal of Physics Conference Series, 012035, DOI: 10.1088/1742-6596/1227/1/012035

## (IOP, 2019).

### 5. Russo, M., Gernon, T. M., Santaguida, A. & Hincks, T. K. Improving Earth science communication and accessibility with

data soniﬁcation. Nat. Rev. Earth Environ. 5, 1–3, DOI: 10.1038/s43017-023-00512-y (2024).

### 6. Droppelmann, C. A. & Mennickent, R. E. Creating Music Based on Quantitative Data from Variable Stars. JAAVSO 46,

154, DOI: 10.48550/arXiv.1811.02930 (2018). 1811.02930.

### 7. Russo, M. Soniﬁcation 101: How to convert data into music with python. Medium (2022). Accessed: 2023-10-12.

### 8. Harrison, C., Trayford, J., Harrison, L. & Bonne, N. Audio universe: tour of the solar system. Astron. Geophys. 63,

2.38–2.40, DOI: 10.1093/astrogeo/atac027 (2022). 2112.02110.

### 9. Bardelli, S., Ferretti, C., Presti, G. & Rinaldi, M. A Soniﬁcation of the zCOSMOS Galaxy Dataset. In Revista Mexicana

de Astronomia y Astroﬁsica Conference Series, vol. 54 of Revista Mexicana de Astronomia y Astroﬁsica Conference Series,
47–52, DOI: 10.22201/ia.14052059p.2022.54.10 (2022). 2202.05539.

### 10. Zanella, A. et al. Soniﬁcation and sound design for astronomy research, education and public engagement. Nat. Astron. 6,

1241–1248, DOI: 10.1038/s41550-022-01721-z (2022). 2206.13536.

### 11. Valle, A. & Korol, V. For LISA. A piano-based soniﬁcation project of gravitational waves. arXiv e-prints arXiv:2202.04621, DOI: 10.48550/arXiv.2202.04621 (2022). 2202.04621.

### 12. García-Benito, R. & Pérez-Montero, E. Painting graphs with sounds: CosMonic soniﬁcation project. In Revista Mexicana

de Astronomia y Astroﬁsica Conference Series, vol. 54 of Revista Mexicana de Astronomia y Astroﬁsica Conference Series,
28–33, DOI: 10.22201/ia.14052059p.2022.54.06 (2022). 2205.12984.
9/19

### 13. Reinsch, D. & Hermann, T. Interacting with soniﬁcations-the mesonic framework for interactive auditory data science. In

Proceedings of the 7th Interactive Soniﬁcation Workshop (ISon 2022), 65–74 (Zenodo, Delmenhorst, Germany, 2023).

### 14. Trayford, J. W. & Harrison, C. M. Introducing STRAUSS: A ﬂexible soniﬁcation Python package. arXiv e-prints

arXiv:2311.16847, DOI: 10.48550/arXiv.2311.16847 (2023). 2311.16847.

### 15. Trayford, J. W. et al. Inspecting spectra with sound: proof-of-concept and extension to datacubes. RAS Tech. Instruments

2, 387–392, DOI: 10.1093/rasti/rzad021 (2023). 2306.10126.

### 16. Ubach, H. & Espuny, J. Soniﬁcation of gravitationally lensed gravitational waves / Soniﬁcació de l’efecte de lent gravitatòria

en ones gravitacionals. arXiv e-prints arXiv:2407.09588, DOI: 10.48550/arXiv.2407.09588 (2024). 2407.09588.

### 17. Huppenkothen, D., Pampin, J., Davenport, J. R. A. & Wenlock, J. The Soniﬁed Hertzsprung-Russell Diagram. arXiv

e-prints arXiv:2401.00488, DOI: 10.48550/arXiv.2401.00488 (2023). 2401.00488.

### 18. Garcia, B., Diaz-Merced, W., Casado, J. & Cancio, A. Evolving from xSonify: a new digital platform for sonorization. In

European Physical Journal Web of Conferences, vol. 200 of European Physical Journal Web of Conferences, 01013, DOI:
10.1051/epjconf/201920001013 (2019).

### 19. Casado, J., de la Vega, G. & García, B. SonoUno development: a User-Centered Soniﬁcation software for data analysis. The J. Open Source Softw. 9, 5819, DOI: 10.21105/joss.05819 (2024).

### 20. Lyu, Z., Li, J. & Wang, B. AIive: Interactive Visualization and Soniﬁcation of Neural Networks in Virtual Reality. arXiv

e-prints arXiv:2109.15193, DOI: 10.48550/arXiv.2109.15193 (2021). 2109.15193.

### 21. García Riber, A. & Serradilla, F. Toward an auditory Virtual Observatory (preprint). arXiv e-prints arXiv:2405.11382, DOI: 10.48550/arXiv.2405.11382 (2024). 2405.11382.

### 22. Enge, K. et al. Open Your Ears and Take a Look: A State-of-the-Art Report on the Integration of Soniﬁcation and

Visualization. arXiv e-prints arXiv:2402.16558, DOI: 10.48550/arXiv.2402.16558 (2024). 2402.16558.

### 23. Bornmann, L. The sound of science. EMBO reports 25, 3743–3747, DOI: https://doi.org/10.1038/s44319-024-00230-6

(2024). https://www.embopress.org/doi/pdf/10.1038/s44319-024-00230-6.

### 24. Alexander, R. L., O’Modhrain, S., Roberts, D. A., Gilbert, J. A. & Zurbuchen, T. H. The bird’s ear view of space physics: Audiﬁcation as a tool for the spectral analysis of time series data. J. Geophys. Res. (Space Physics) 119, 5259–5271, DOI:

## 10.1002/2014JA020025 (2014).

### 25. Guiotto Nai Fovino, L., Zanella, A. & Grassi, M. Evaluation of the Effectiveness of Soniﬁcation for Time-series Data

Exploration. AJ 167, 150, DOI: 10.3847/1538-3881/ad2943 (2024). 2402.09953.

### 26. Grey, J. M. Multidimensional perceptual scaling of musical timbres. Acoust. Soc. Am. J. 61, 1270–1277, DOI: 10.1121/1.

381428 (1977).

### 27. Cooke, J., Díaz-Merced, W., Foran, G., Hannam, J. & Garcia, B. Exploring Data Soniﬁcation to Enable, Enhance,

and Accelerate the Analysis of Big, Noisy, and Multi-Dimensional Data. In Grifﬁn, R. E. (ed.) Southern Horizons in
Time-Domain Astronomy, vol. 339 of IAU Symposium, 251–256, DOI: 10.1017/S1743921318002703 (2019).

### 28. Diaz-Merced, W. L., Candey, R. M., Mannone, J. C., Fields, D. & Rodriguez, E. Soniﬁcation for the Analysis of Plasma

Bubbles at 21 MHz. Sun Geosph. 3, 42–45 (2008).

### 29. Tucker Brown, J., Harrison, C. M., Zanella, A. & Trayford, J. Evaluating the efﬁcacy of soniﬁcation for signal detection

in univariate, evenly sampled light curves using ASTRONIFY. MNRAS 516, 5674–5683, DOI: 10.1093/mnras/stac2590
(2022). 2209.04465.

### 30. Martins, A. C., Rangayyan, R. M. & Ruschioni, R. A. Audiﬁcation and soniﬁcation of texture in images. J. Electron. Imaging 10, 690–705, DOI: 10.1117/1.1382811 (2001).

### 31. Bearman, N. & Fisher, P. F. Using sound to represent spatial data in ArcGIS. Comput. Geosci. 46, 157–163, DOI:

10.1016/j.cageo.2011.12.001 (2012).

### 32. Schito, J. & Fabrikant, S. I. Exploring maps by sounds: using parameter mapping soniﬁcation to make digital elevation

models audible. Int. J. Geogr. Inf. Sci. 32, 874–906, DOI: 10.1080/13658816.2017.1420192 (2018).

### 33. Matinfar, S. et al. Soniﬁcation as a reliable alternative to conventional visual surgical navigation. Sci. Reports 13, 5930, DOI: 10.1038/s41598-023-32778-z (2023). 2206.15291.

### 34. Chiroiu, V., Munteanu, L., Ioan, R., Dragne, C. & Majercsik, L. Using the Soniﬁcation for Hardly Detectable Details in

Medical Images. Sci. Reports 9, 17711, DOI: 10.1038/s41598-019-54080-7 (2019).
10/19

### 35. Dubus, G. & Bresin, R. A Systematic Review of Mapping Strategies for the Soniﬁcation of Physical Quantities. PLoS

ONE 8, e82491, DOI: 10.1371/journal.pone.0082491 (2013).

### 36. Parizel, P. M. et al. Magnetic Resonance Imaging of the Brain, 107–195 (Springer Berlin Heidelberg, Berlin, Heidelberg,

2010).

### 37. Groth, E. J. & Peebles, P. J. E. Statistical analysis of catalogs of extragalactic objects. VII. Two- and three-point correlation

functions for the high-resolution Shane-Wirtanen catalog of galaxies. ApJ 217, 385–405, DOI: 10.1086/155588 (1977).

### 38. Baumgart, D. J. & Fry, J. N. Fourier Spectra of Three-dimensional Data. ApJ 375, 25, DOI: 10.1086/170166 (1991).

### 39. Frieman, J. A. & Gaztanaga, E. The Three-Point Function as a Probe of Models for Large-Scale Structure. ApJ 425, 392, DOI: 10.1086/173995 (1994). astro-ph/9306018.

### 40. Matarrese, S., Verde, L. & Heavens, A. F. Large-scale bias in the Universe: bispectrum method. MNRAS 290, 651–662, DOI: 10.1093/mnras/290.4.651 (1997). astro-ph/9706059.

### 41. Kitaura, F.-S. et al. Constraining the halo bispectrum in real and redshift space from perturbation theory and non-linear

stochastic bias. MNRAS 450, 1836–1845, DOI: 10.1093/mnras/stv645 (2015). 1407.1236.

### 42. Kitaura, F.-S. et al. The clustering of galaxies in the SDSS-III Baryon Oscillation Spectroscopic Survey: mock galaxy

catalogues for the BOSS Final Data Release. MNRAS 456, 4156–4173, DOI: 10.1093/mnras/stv2826 (2016). 1509.06400.

### 43. Carnero-Rosell, A. et al. Scale-dependent brain age with higher-order statistics from structural magnetic resonance imaging.

bioRxiv DOI: 10.1101/2025.03.24.644902 (2025). https://www.biorxiv.org/content/early/2025/05/08/2025.03.24.644902.
full.pdf.

### 44. Kitaura, F.-S. Non-Gaussian gravitational clustering ﬁeld statistics. MNRAS 420, 2737–2755, DOI: 10.1111/j.1365-2966.

2011.19680.x (2012). 1012.3168.

### 45. Breiman, L. Random forests. Mach. Learn. 45, 5–32, DOI: 10.1023/A:1010933404324 (2001).

### 46. Hastie, T., Tibshirani, R. & Friedman, J. The Elements of Statistical Learning: Data Mining, Inference, and Prediction. Springer series in statistics (Springer, 2001).

### 47. LaMontagne, P. J. et al. Oasis-3: Longitudinal neuroimaging, clinical, and cognitive dataset for normal aging and alzheimer

disease. medRxiv DOI: 10.1101/2019.12.13.19014902 (2019). https://www.medrxiv.org/content/early/2019/12/15/2019.12.
13.19014902.full.pdf.

### 48. Penfold, R. Practical MIDI Handbook (PC Publishing, USA, 1988).

### 49. Rothstein, J. MIDI: a comprehensive introduction (A-R Editions, Inc., USA, 1992). Acknowledgements
The research conducted in this work was primarily funded by the the Cabildo de Tenerife under IACTEC Technological
Training Program, grant TF INNOVA, in support of the Cosmic Brain project starting in 2021 (PI: FSK). EPK and FSK
thank Matt Russo for sharing the very instructive soniﬁcation instructions in python7, which have been followed as a basis for
the code developed in this article. The authors acknowledge the Spanish Ministry of Economy and Competitiveness (MINECO)
for ﬁnancing the Big Data of the Cosmic Web project: PID2020-120612GB-I00/AEI/10.13039/501100011033 (PI: FSK) and the Cosmology with Large Scale Structure Probes project funded by the IAC (PI: FSK), which
provided numerical tools and computing facilities. EPK thanks the IAC for hospitality during her internship in the summer

### 2024. FSK and EPK thank Dr María Joyanes Pérez for discussions on musical notes. Funding
Spanish Ministry of Economy and Competitiveness: PID2020-120612GB-I00/AEI/10.13039/501100011033. Author contributions statement
FSK proposed this project, directed the study, prepared the software and wrote the paper. EPK contributed to the soniﬁcation
piano, coding, soniﬁcation and metric calculations. ACR, NJ, AM and EP contributed in the development of the higher-order
statistics analysis method, to providing the input data of this work and to improve the manuscript.
11/19

Additional information
All the bispectrum data and software used in this work are publicly available at https://github.com/pacoshu/
sonification. The software developed for soniﬁcation relies on several specialized libraries: Streamlit for the web
application interface; music libraries including midiutil and music21 for MIDI manipulation and score generation; statistical
libraries such as sklearn.metrics, scipy.stats, and scipy.spatial.distance for analysis and metric calculations; and data processing
and visualization libraries, including pandas, numpy, matplotlib, as well as io, os, and itertools for efﬁcient data handling and
plotting. The authors declare no competing interest. Methods
Input data
The data considered in this study was prepared by Carnero-Rosell et al.43 within the Cosmic Brain project based on the
OASIS-3 database47. All MRI data was collected through the Knight Alzheimer Research Imaging Program at Washington University in St. Louis, MO, USA. Some of the MRI data was collected on a Siemens Vision 1.5T, while the majority of the scans came from
two different versions of a Siemens TIM Trio 3T (Siemens Medical Solutions USA, Inc). Participants were lying in the scanner
in a supine position, head motion was minimized by inserting foam pads between the participant’s head and antenna coil, and
for some participants a vitamin E capsule was placed over the left temple to mark lateralization. A 16 channel head coil was
used in all scans. Although a variety of different structural and functional imaging protocols are included in the OASIS dataset
such as FLAIR, DTI and ASL, here we focused on the T1w scans. The T1w images were acquired using a 3DMPRAGE
protocol TI/TR/TE: 1000/2400/3.08 ms, ﬂip angle = 8◦, resulting in 1 mm isotropic voxels. Data were provided by OASIS-3: Longitudinal Multimodal Neuroimaging: Principal Investigators: T. Benzinger, D. Marcus, J. Morris; NIH P30 AG066444, P50 AG00561, P30 NS09857781, P01 AG026276, P01 AG003991, R01 AG043434, UL1 TR000448, R01 EB009352. AV-45 doses were provided by Avid Radiopharmaceuticals, a wholly owned subsidiary of Eli
Lilly. Soniﬁcation frequency range
The ﬁrst note C1 has a frequency of 32.702 Hz, while the last regular note B8 has a frequency of 7902.13 Hz. In case we include quarter tones, we need to make additional calculations. The 12-tone equal temperament system divides
an octave into 12 equal parts, where each part corresponds to a semitone. In this system, the frequency of a note increases by a
factor of 2 when going up by an octave. Moving up by one semitone corresponds to multiplying the frequency by 21/12, since
there are 12 semitones in an octave. The cent is a unit used to measure musical intervals, speciﬁcally fractions of semitones. There are 100 cents in a semitone. To calculate the frequency change for a given number of cents, we use the formula 2n/1200, where n is the number of
cents. For a quarter tone, which is 25 cents (half of a semitone), we substitute n = 25 into the formula: ffactor = 225/1200. To
calculate the frequency of B8+25 (25 cents above B8), we have to multiply the original frequency by the quarter tone factor:
fB8+25 = 7902.13×225/1200 = 7961.09 Hz. Hence, the total frequency range we are considering when including quarter tones spans from 32.702 to 7961.09 Hz, just
below the typical upper sensitivity limit of 8 kHz for humans of about 70 yrs. This should be considered when targeting older
age groups. Methodology Overview
This methodology section describes the steps involved in converting bispectrum MRI data into soniﬁable MIDI sequences. The
soniﬁcation steps can be seen in Figure 7. Figure 8 shows the soniﬁcation procedure to present relative signals with respect to a
reference one which determines the range. We can see from the upper-left panel of Figure 8 (corresponding to the bispectra
shown in Figure 9), that the differences between the 40-50 and 50-60 years group are very tiny. In such cases it seems more
adequate to focus on the soniﬁcation of the differences. We demonstrate in Figure 10 how those differences can be enhanced
applying the method explained below.

### 1. MRI data preparation: The ﬁrst step involves obtaining the MRI brain intensity map on a mesh. This map is represented

in three dimensions, with each voxel containing an intensity value corresponding to a speciﬁc brain location. These
values provide the base data for subsequent analysis.

### 2. Statistical analysis: To capture the structural complexity of the brain, we compute two-point and three-point correlation

functions in Fourier space.
12/19

Details on these computations can be found in Carnero-Rosell et al.43 and references therein.

### 3. Bispectrum normalization: The data is normalized to ensure consistency across datasets: y′

i =
yi
cnorm, where cnorm is a
predeﬁned normalization constant. This step ensures that intensity values are comparable and prevents skewing due to
extreme values.

### 4. Bispectrum linear mapping to a positive deﬁnite range: We deﬁne the linear mapping function "map_value":

˜yi
=
map_value(y′
i,y′
min,y′
max,ymin,ymax)
=
ymin + (y′
i −y′
min)
(y′max −y′
min) ·(ymax −ymin)
The normalized data is linearly mapped to a positive ﬁnite range [ymin,ymax] to facilitate MIDI conversion:
˜yi
=
map_value(yi,ymin,ymax,ymin,ymax)

### 5. Time linear mapping to a positive deﬁnite range: The subtended angles from triangle conﬁgurations are converted to a time line:
ti = map_value(θi,θmin,θmax,0,duration_beats)
We are choosing, per default, a duration of 2 seconds, a duration_beats of 20, and a beats per minute (bpm) of 60.

### 6. Nonlinear rank-ordered transformation: To enhance perceptibility, the data is then exponentiated by a factor fexp: ymap = ˜yfexp. This process stretches (fexp > 1) or compresses (fexp < 1) the dynamic range of the data, improving the soniﬁcation’s
dynamic representation, while preserving the structure and rank order. For fexp = 1 we have ymap = ˜y.

### 7. Soniﬁcation: mapping to MIDI notes: The transformed intensity values are mapped to MIDI1 notes using the function: MIDI value = 69+12log2
 f


where f is the frequency corresponding to the intensity value. The MIDI note number 69 corresponds to the musical note A4, which is standardized at a frequency of 440 Hz (often
referred to as "concert pitch"). Quarter tones and octave shifts are adjusted accordingly. The MIDI note pitch is derived
by discretizing the intensity range into predeﬁned musical notes (see Figure 2):
indexnote = round(map_value(ymap,y′
min,y′
max,0,nnotes −1)),
where the range is adjusted, in the relative representation case (see Figure 8), to a reference signal covering the largest
range:
y′
min
=
min(ymap)×scale_factor
y′
max
=
max(ymap)×scale_factor,
and
scale_factor = max(yref)−min(yref)
max(ymap)−min(ymap). The scale factor is set to one when computing differences. With the index we obtain the MIDI notes: MIDIvalue[indexnote]. The volume (or velocity) of each note is assigned on a suitable range:
vel = round(map_value(ymap,min(ymap),max(ymap),velmin,velmax))
1MIDI (Musical Instrument Digital Interface) is a technical standard that describes a communication protocol, digital interface, and electrical connectors
that connect a wide variety of electronic musical instruments, computers, and related audio devices for playing, editing, and recording music48,49.
13/19

where the velocity lies within the range 65 ≤vel ≤110 to ensure perceptibility. The term "velocity" in MIDI was chosen
to represent the intensity of a note, but it doesn’t refer to the literal speed of a note’s sound. Instead, it refers to how
quickly the key is pressed (from a physical perspective) and how that is mapped to the loudness or dynamic quality of the
note. The reduced bispectra soniﬁcation can be seen in Figures 9 and 10. The latter shows the application of the normalization
and the nonlinear transformation. The nonlinear transformation enhances the representation of features that exhibit minimal
variations within a signal that spans a wide range of values. We can see in the lower-left panel of Figure 7, how some bispectrum
bins acquire the same value in the sonﬁcation process. This problem is not present in the lower-right panel where fexp = 0.45
was applied. As a consequence of this transformation the ratio plots in the top and bottom panels of Figure 10 display a ﬂatter
behaviour than in Figure 4. Information loss
To assess the accuracy of the soniﬁcation, the information loss is calculated by transforming the MIDI values back into the
original bispectrum space: ˜yinverse = map_value(MIDIvalue, MIDImin, MIDImax,ymin,ymax). This includes reversing the exponentiation (for fexp ̸= 1): yinverse = ˜y1/ fexp
inverse. Information loss is measured using, e.g., the normalised mean squared error (NMSE):

## NMSE =

n ∑n
i=1 (yi −yinverse,i)2

n−1 ∑n
i=1(yi −¯y)2. For a more complete metric analysis see Table 1 applied to the reduced bispectrum for both absolute and differences soniﬁcation. These metrics provide insights into the accuracy of the soniﬁcation and guide any necessary adjustments. Depending on the metric, we will treat the data as a function (Y) or as a PDF (P): Given ˆY = ground truth data set, Y = model data set,
i) Make the data positive deﬁnite:
if min(Y) < 0, then set Y = Y −min(Y),
if min(ˆY) < 0, then set ˆY = ˆY −min( ˆY),
ii) Construct probability distributions:

## P = Y

## ∑Y,

## Q =

ˆY

## ∑ˆY. The metrics in Table 1 were obtained with the inclusion of quarter tones. Results without quarter tones were worse by about
an order of magnitude in the NMSE.
14/19

Angle
−0.5
0.0
0.5
1.0
1.5
2.0
Function

Angle
−0.5
0.0
0.5
1.0
1.5
2.0
Function

Time [beats]

Midi note numbers

Time [beats]

Midi note numbers
Figure 7. Soniﬁcation procedure across four panels: The upper-left panel shows the original signal with each data point
represented by a small circle. In this example, the difference of the reduced bispectra (conﬁguration k1 = 0.19 and k2 = 0.36)
for age groups: 80-100 and 40-50 is shown. In the upper-right panel, the minimum value is subtracted from the signal. The
lower-left panel illustrates the signal discretization process, additionally applying a linear mapping to convert the signal into the
range of MIDI values that are perceptible to adult human listeners. Finally, the lower-right panel demonstrates the effect of
incorporating a nonlinear rank-ordered transformation with a power-law of exponent fexp = 0.45. The velocity (volume) of the
soniﬁed signal is represented through the size of the circles. The normalization is one.
15/19

Time [beats]

Midi note numbers

Time [beats]

Midi note numbers

Time [beats]

Midi note numbers

Time [beats]

Midi note numbers
Figure 8. Similar soniﬁcation procedure to Figure 7, but showing relative reduced bispectra relations (conﬁguration k1 = 0.19
and k2 = 0.36). The different panels show the discretized signal for the 50-60 (upper-left), 60-70 (upper-right), 70-80
(lower-left), 80-100 (lower-right) age group within the range of the reference 40-50 years group mapped to the corresponding
MIDI values. The ﬁlled circles stand for the reference bispectrum.
16/19

−2

Bispectrum
Soniﬁed Data 40 −50
Reference Data 40 −50
0.5
1.0
Ratio

Angle/Time
−0.025
0.000
0.025
Diﬀerence
−2

Bispectrum
Original Data 50 −60
Soniﬁed Data 50 −60
Reference Data 40 −50

Ratio

Angle/Time
−0.025
0.000
0.025
Diﬀerence
−2

Bispectrum
Original Data 60 −70
Soniﬁed Data 60 −70
Reference Data 40 −50
0.5
1.0
1.5
Ratio

Angle/Time
−0.025
0.000
0.025
Diﬀerence
−2

Bispectrum
Original Data 70 −80
Soniﬁed Data 70 −80
Reference Data 40 −50
0.5
1.0
Ratio

Angle/Time
−0.025
0.000
Diﬀerence
Figure 9. Soniﬁcation of reduced bispectra (conﬁguration k1 = 0.19 and k2 = 0.36) from human brain magnetic resonance
imaging for different ages. The original data and the corresponding inverse mapping after soniﬁcation are indicated for each
age range.
17/19

Diﬀ−Bispectrum
Original Data 50 −60 to 40 −50
Soniﬁed Data 50 −60 to 40 −50
0.8
1.0
1.2
Ratio

Angle/Time
−0.05
0.00
0.05
Diﬀerence

Diﬀ−Bispectrum
Original Data 60 −70 to 40 −50
Soniﬁed Data 60 −70 to 40 −50
0.8
1.0
1.2
Ratio

Angle/Time
−0.05
0.00
0.05
Diﬀerence

Diﬀ−Bispectrum
Original Data 70 −80 to 40 −50
Soniﬁed Data 70 −80 to 40 −50
0.8
1.0
1.2
Ratio

Angle/Time
−0.05
0.00
0.05
Diﬀerence

Diﬀ−Bispectrum
Original Data 80 −100 to 40 −50
Soniﬁed Data 80 −100 to 40 −50
0.8
1.0
1.2
Ratio

Angle/Time
−0.05
0.00
0.05
Diﬀerence
Figure 10. Soniﬁcation of difference between reduced bispectra (conﬁguration k1 = 0.19 and k2 = 0.36) from human brain
magnetic resonance imaging for different ages groups with respect to the youngest age group in our sample (40-50 yrs). Upper-left panel: cnorm = 0.25, fexp = 0.7; upper-right panel: cnorm = 0.5, fexp = 0.35; lower-left panel: cnorm = 0.75,
fexp = 0.35; lower-right panel: cnorm = 1, fexp = 0.45.
18/19

Statistical Measure Name (SMN)
Mathematical Formula
Age Group
Mean
¯y = 1
n ∑n
i=1 yi
40-50
50-60
60-70
70-80
80-100
Variance
Var(Y) =

n−1 ∑n
i=1(yi −¯y)2
ABS
ABS
DIFF
ABS
DIFF
ABS
DIFF
ABS
DIFF
Mean Absolute Error [→0]

## MAE(Y, ˆY) = 1

n ∑n
i=1 |yi −ˆyi|
0.0026
0.0162 0.0015 0.0003 0.0046 0.0104 0.0064 0.0078 0.0064
Mean Squared Error [→0]

## MSE(Y, ˆY) = 1

n ∑n
i=1(yi −ˆyi)2
0.0004
0.0004 0.0000 0.0169 0.0000 0.0001 0.0001 0.0001 0.0001
Root Mean Squared Error [→0]

## RMSE(Y, ˆY) =

√
MSE
0.0194
0.0192 0.0020 0.0169 0.0062 0.0127 0.0089 0.0102 0.0088
Normalized MSE [→0]

## NMSE(Y, ˆY) =

MSE
Var(Y) ×100 [%]
0.0255
0.0274 0.0571 0.0275 0.0832 0.0215 0.0587 0.0199 0.0292
Relative MSE [→0]
ReMSE(Y, ˆY) = MSE
¯y2 ×100 [%]
0.4138
0.3510 0.0132 0.2763 0.0351 0.1734 0.0303 0.1422 0.0217
Signal-to-Noise Ratio [→≫1]
SNR(Y, ˆY) = Var(Y)
MSE
3924.6
3648.1 1750.3 3642.7 1202.4 4649.4 1704.2 5017.8 3420.7
R-squared [→1]
R2(Y, ˆY) = 1−∑n
i=1(yi−ˆyi)2
∑n
i=1(yi−¯y)2
0.9997
0.9997 0.9994 0.9997 0.9993 0.9998 0.9994 0.9998 0.9997
Explained Variance [→1]
EVAR(Y, ˆY) = 1−Var(Y−ˆY)
Var(Y)
0.9998
0.9998 0.9994 0.9997 0.9992 0.9998 0.9992 0.9998 0.9997
Cosine Similarity [→1]

## CS(P, Q) =

∑n
i=1 pi·qi
√
∑n
i=1 p2
i ·√
∑n
i=1 q2
i
1.0000
1.0000 0.9999 1.0000 0.9999 1.0000 0.9999 1.0000 0.9999
Kullback-Leibler Divergence [→0]
DKL(P, Q) = ∑n
i=1 pi log pi
qi
0.0000
0.0000 0.0001 0.0000 0.0001 0.0000 0.0001 0.0000 0.0001
Cross-Entropy [→0]
H(P, Q) = −∑n
i=1 pi logqi
0.0535
0.0534 0.0533 0.0534 0.0521 0.0534 0.0516 0.0534 0.0504
Total Variation Distance [→0]

## TVD(P, Q) = 1

2 ∑n
i=1 |pi −qi|
0.0024
0.0024 0.0043 0.0026 0.0066 0.0022 0.0062 0.0021 0.0053
Hellinger Distance [→0]

## DH(P, Q) =

q
∑n
i=1(√pi−√qi)2

0.0027
0.0026 0.0042 0.0029 0.0060 0.0025 0.0055 0.0022 0.0052
Table 1. Metrics and their mathematical formulae computed for different age groups corresponding to the reduced bispectra (conﬁguration k1 = 0.19 and k2 = 0.36). The ideal case is indicated within brackets, e.g., [→0] or [→1]. "ABS" stands for soniﬁcation of absolute bispectra, and "DIFF" stands for difference between bispectra
of a group and a reference one of 40−50.
19/19
