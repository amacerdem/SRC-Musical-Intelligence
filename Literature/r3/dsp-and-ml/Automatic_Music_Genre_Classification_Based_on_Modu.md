# untitled

**Author:** Unknown  
**Subject:** N/A  
**Total Pages:** 13  
**Source File:** `Automatic_Music_Genre_Classification_Based_on_Modu.pdf`

---

## Page 1

670 IEEE TRANSACTIONS ON MULTIMEDIA, VOL. 11, NO. 4, JUNE 2009
Automatic Music Genre Classiﬁcation Based
on Modulation Spectral Analysis of Spectral
and Cepstral Features
Chang-Hsing Lee, Jau-Ling Shih, Kun-Ming Yu, and Hwai-San Lin
Abstract— In this paper, we will propose an automatic music
genre classiﬁcation approach based on long-term modulationspectral analysis of spectral (OSC and MPEG-7 NASE) as well ascepstral (MFCC) features. Modulation spectral analysis of everyfeature value will generate a corresponding modulation spectrumand all the modulation spectra can be collected to form a modu-lation spectrogram which exhibits the time-varying or rhythmicinformation of music signals. Each modulation spectrum is thendecomposed into several logarithmically-spaced modulation sub-bands. The modulation spectral contrast (MSC) and modulation
spectral valley (MSV) are then computed from each modulation
subband. Effective and compact features are generated fromstatistical aggregations of the MSCs and MSVs of all modulationsubbands. An information fusion approach which integrates bothfeature level fusion method and decision level combination methodis employed to improve the classiﬁcation accuracy. Experimentsconducted on two different music datasets have shown that ourproposed approach can achieve higher classiﬁcation accuracythan other approaches with the same experimental setup.
Index Terms— Mel-frequency cepstral coefﬁcients, modulation
spectral analysis, music genre classiﬁcation, normalized audiospectrum envelope, octave-based spectral contrast.
I. I NTRODUCTION
WITH the development of computer networks, it becomes
more and more popular to purchase and download dig-
ital music from the Internet. Since a typical music database often
contains millions of music tracks, it is very difﬁcult to manage
such a large music database. It will be helpful in managing a
vast amount of music tracks when they are properly categorized.The retail or online music stores often organize their collections
of music tracks by categories such as genre, artist, and album.
Music genre labels are often attached to an artist or an album
and do not reﬂect the characteristic of a particular music track.
The category information is often manually labeled by expe-rienced managers or by the consumers (for example, CDDB,
1
MusicBrainz,2etc.). Perrot and Gjerdingen reported a human
Manuscript received June 30, 2008; revised January 23, 2009. First pub-
lished April 28, 2009; current version published May 15, 2009. This work was
supported in part by the National Science Council of R.O.C. under contract
NSC-96-2221-E-216-043. The associate editor coordinating the review of thismanuscript and approving it for publication was Prof. Gerald Schuller.
The authors are with the Department of Computer Science and Information
Engineering, Chung Hua University, Hsinchu 300, Taiwan (e-mail: chlee@chu.
edu.tw; sjl@chu.edu.tw; yu@chu.edu.tw; m09502029@chu.edu.tw).
Color versions of one or more of the ﬁgures in this paper are available online
at http://ieeexplore.ieee.org.
Digital Object Identiﬁer 10.1109/TMM.2009.2017635
1http://www.cddb.com
2http://musicbrainz.orgsubject study in which college students were tested to make
music genre classiﬁcation among a total of ten music genres
[1]. Their research found that humans with little to moderate
musical training can achieve about 70% classiﬁcation accuracy,based on only 300 ms of audio. Another study conducted the ex-
periments on music genre classiﬁcation by 27 human listeners.
Each one will listen to the central 30 s of each music track and
be asked to choose one out of six music genres. These listeners
achieved an inter-participant genre agreement rate of only 76%[2]. These results indicate that there is signiﬁcant subjectivity
in genre annotation by humans. That is, different people clas-
sify music genres differently, leading to many inconsistencies.
In addition, manual annotation is a time-consuming and labo-
rious task. Thus, a number of supervised classiﬁcation tech-niques have been developed for automatic classiﬁcation of unla-
beled music tracks [3]–[16]. In this study, we focus on the music
genre classiﬁcation problem which is deﬁned as genre labeling
of music tracks. In general, automatic music genre classiﬁcation
plays an important and preliminary role in a music organizationor music retrieval system. A new album or music track can be
assigned to a proper genre in order to place it in the appropriate
section of an online music store or music database.
To determine the genre of a music track, some discriminating
audio features have to be extracted through content-based anal-ysis of the music signal. In general, the audio features developedfor audio classiﬁcation can be roughly categorized into threeclasses: short-term features, long-term features, and semantic
features. Short-term features, typically describing the timbral
characteristics of audio signals, are usually extracted fromevery short time window (or frame) during which the audiosignal is assumed to be stationary. The timbral characteristicsgenerally exhibit the properties related to instrumentations orsound sources such as music, speech, or environment sounds.The most widely used timbral features include zero crossingrate (ZCR), spectral centroid, spectral bandwidth, spectralﬂux, spectral rolloff, Mel-frequency cepstral coefﬁcients(MFCC), discrete wavelet transform coefﬁcients [4], [13],
[17], octave-based spectral contrast (OSC) [5], [6], MPEG-7
normalized audio spectrum envelope (NASE) [18], [19], etc.
Generally, music genres not only correspond to the timbre of
the music but also to the temporal structure of the music. Thatis, the time evolution of music signals will provide some usefulinformation for music genre discrimination. To characterize thetemporal evolution of a music track, long-term features can begenerated by aggregating the short-term features extracted fromseveral consecutive frames within a time window. The methods
developed for aggregating temporal features include statistical
1520-9210/$25.00 © 2009 IEEE
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 2

LEE et al. : AUTOMATIC MUSIC GENRE CLASSIFICATION 671
moments [3], [8], [12], [20], entropy or correlation [20], [21],
nonlinear time series analysis [20], autoregressive (AR) modelsor multivariate autoregressive (MAR) models [11], modulationspectral analysis [8], [12], [16], [20], [22], etc.
Semantic features give meanings to audio signals in
human-recognizable terms which generally reveal the human
interpretation or perception of certain audio properties suchas mood, emotion, tempo, genre, etc. The most widely
known semantic descriptors include tempo (measured in
beats-per-minute, BPM), rhythmic information, melody, pitch
distribution, and so on. Rhythmic features can provide the main
beat(s) and the corresponding strength of a music track. Sev-eral beat-tracking algorithms have been proposed to estimate
the main beat and the corresponding strength [3], [23]. Pitch
features, mainly derived from the pitch histogram [3], [24], can
describe the harmonic contents or the pitch range of the music.
Once the features are extracted from a music track, a clas-
siﬁer will be employed to determine the genre of the given
music track. Several supervised learning approaches, such
as
-nearest neighbor (KNN) [3], [4], linear discriminant
analysis (LDA) [4], Gaussian mixture models (GMM) [3],
[4], [6], hidden Markov models (HMM) [18], Adaboost [14],
regularized least-squares framework [15], and support vector
machines (SVM) [4], [16], [25], have been employed for
audio classiﬁcation. Li et al. [4] evaluated the performance of
different classiﬁers, including SVM, KNN, GMM, and LDA.
SVM is always the best classiﬁer for music classiﬁcation in
their comparative experiments. Grimaldi et al. [13] used a set
of features based on discrete wavelet packet transform (DWPT)
to represent a music track. The classiﬁcation performance wasevaluated by four alternative classiﬁers: KNN, one-against-all,
Round-Robin, and feature-subspace based ensembles of nearest
neighbor classiﬁers. The best result is achieved by using the fea-
ture-subspace based ensembles of nearest neighbor classiﬁers.
A number of studies tried to use a speciﬁc classiﬁer to improvethe classiﬁcation performance. However, the improvement is
limited. In fact, it has been shown that employing effective
feature sets will have much more effect on the classiﬁcationaccuracy [8].
In this paper, long-term modulation spectral analysis [26],
[27] of MFCC [28], OSC [5], [6], and MPEG-7 NASE [18],
[19] features will be used to characterize the time-varying
behavior of music signals. A modulation spectrogram corre-sponding to the collection of modulation spectra of all MFCC
(OSC or NASE) features will be constructed. Discriminative
features are then extracted from each modulation spectrogram
for music genre classiﬁcation. Our contributions are as follows:
• proposal of some novel features based on long-term mod-
ulation spectral analysis of OSC and MPEG-7 NASE;
• extraction of effective and compact modulation spectral
features from statistical aggregations of the modulation
spectral contrasts (MSCs) and modulation spectral valleys
(MSVs) computed from the modulation spectrograms ofMFCC, OSC, and NASE;
• investigation of the importance of various modulation fre-
quency ranges for music genre classiﬁcation;
• development of an information fusion approach which in-
tegrates both feature level fusion and decision level fusion
in order to improve the classiﬁcation accuracy.II. P
ROPOSED MUSIC GENRE CLASSIFICATION SYSTEM
The proposed music genre classiﬁcation system consists of
two phases: the training phase and the classiﬁcation phase. Thetraining phase is composed of three main modules: feature ex-traction, linear discriminant analysis (LDA) [29], and informa-
tion fusion. The classiﬁcation phase consists of three modules:
feature extraction, LDA transformation, and classiﬁcation. Adetailed description of each module will be described below.
A. Feature Extraction
A novel feature set derived from modulation spectral analysis
of the spectral (OSC and NASE) as well as cepstral (MFCC)
feature trajectories of music signals is proposed for music genre
classiﬁcation.
1) Mel-Frequency Cepstral Coefﬁcients (MFCC): MFCC
have been widely used for speech recognition due to their
ability to represent the speech spectrum in a compact form. In
fact, MFCC have been proven to be very effective in automaticspeech recognition and in modeling the subjective frequencycontent of audio signals [9], [28].
Before computing the MFCC of a music track, an input music
signal is ﬁrst pre-emphasized in order to amplify the high-fre-quency components, using a ﬁrst-order FIR high-pass ﬁlter asfollows:
(1)
where
 is the input signal,
 is the emphasized signal, a
typical value for the constant
 is 0.95. The emphasized signal
is then divided into a number of overlapped frames. To mini-
mize the ringing effect, we multiply each frame by a Hammingwindow
given as follows:
(2)
where
 is the length of the Hamming window. FFT is then
applied on each pre-emphasized, Hamming windowed frame toobtain the corresponding spectrum. In this paper, the frame size
is 23 ms (1024 samples for sampling frequency 44.1 kHz) with
50% overlap. The spectrum is then decomposed into a numberof subbands by using a set of triangular Mel-scale band-pass ﬁl-ters. Let
,
 , denote the sum of power spectrum
coefﬁcients within the
 th subband, where
 is the total number
of ﬁlters (
 is 25 in this study). MFCC can be obtained by ap-
plying DCT on the logarithm of
 as follows:
(3)
where
 is the length of MFCC feature vector (
 is 20 in the
study). Note that the offset of “1” in the calculation of MFCCis provided to get a positive logarithmic energy for any positive
value
. As a result, the MFCC feature vector can be repre-
sented as follows:
(4)
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 3

672 IEEE TRANSACTIONS ON MULTIMEDIA, VOL. 11, NO. 4, JUNE 2009
TABLE I
FREQUENCY RANGE OF EACH OCTA VE -SCALE BAND-PASS
FILTER ( /83/97 /109 /112/108/105/110 /103 /114/97 /116/101 /61 /52/52 /58 /49/107 /72 /122 )
2) Octave-Based Spectral Contrast (OSC): OSC was devel-
oped to represent the spectral characteristics of a music signal[5], [6]. It considers the spectral peak and valley in each sub-
band independently. In general, spectral peaks correspond to
harmonic components and spectral valleys the non-harmoniccomponents or noise in music signals. Therefore, the differencebetween spectral peaks and spectral valleys will reﬂect the spec-
tral contrast distribution.
To compute the OSC features, FFT is ﬁrst employed to ob-
tain the spectrum of each audio frame. This spectrum is thendivided into a number of subbands by the set of octave scale
ﬁlters shown in Table I. Let
denote the
power spectrum within the
 th subband,
 is the number of
FFT frequency bins in the
 th subband. Without loss of gener-
ality, let the power spectrum be sorted in a decreasing order, that
is,
 . The spectral peak and spectral
valley in the
 th subband are then estimated as follows:
(5)
(6)
where
 is a neighborhood factor (
 is 0.2 in this study). The
spectral contrast is given by the difference between the spectral
peak and the spectral valley as follows:
(7)
The feature vector of an audio frame consists of the spectral
contrasts and the spectral valleys of all subbands. Thus, the OSC
feature vector of an audio frame can be represented as follows:
(8)
where
 is the number of octave scale ﬁlters.
3) Normalized Audio Spectral Envelope (NASE): NASE
was deﬁned in MPEG-7 for sound classiﬁcation [18], [19].The NASE descriptor provides a representation of the powerspectrum of each audio frame. Each component of the NASE
feature vector represents the normalized squared magnitude of
a particular frequency subband.To extract the NASE features, each audio frame is pre-em-
phasized and multiplied by a Hamming window function andanalyzed using FFT to derive its spectrum, notated
,
, where
 is the size of FFT. The power spectrum is de-
ﬁned as the normalized squared magnitude of the DFT spectrum
as follows:
(9)
where
 is the energy of the Hamming window function
of size
 :
(10)
To reduce the number of spectral features, the power spectrum is
divided into logarithmically spaced subbands spanning between62.5 Hz (“ loEdge ”) and 16 kHz (“ hiEdge ”) over a spectrum of
8 octave interval centered at a frequency of 1 kHz (see Fig. 1).
The number of logarithmic subbands within the frequency range
[loEdge ,hiEdge ] is given by
, where
 is the spectral
resolution of the frequency subbands ranging from 1/16 of anoctave to 8 octaves as follows:
(11)
In this study,
 is used for subband decomposition (i.e.,
), which provides adequate frequency decomposition
for music genre classiﬁcation in our experiments. When the res-olution
is high, in the narrower low-frequency subbands a
small frequency change will make it move from one subband to
another. A reasonable solution is to assume that a power spec-trum coefﬁcient whose distance to a subband edge is less thanhalf the FFT resolution will contribute to the audio spectral en-
velope (ASE) coefﬁcients of both neighboring subbands. In this
paper, a linear weighting method is used to compute the contri-bution of such a coefﬁcient shared by its two neighboring sub-bands. In MPEG-7, the ASE coefﬁcients consist of one coef-
ﬁcient representing power between 0 Hz and loEdge , a series
of
coefﬁcients representing power in logarithmically spaced
subbands between loEdge and hiEdge , and a coefﬁcient repre-
senting power above hiEdge . Therefore, a total number of
ASE coefﬁcients will be generated. The ASE coefﬁcient for the
th subband is deﬁned as the sum of power spectrum coefﬁcients
within this subband as follows:
(12)
where
 and
 are, respectively, the integer frequency
bins corresponding to the lower edge and higher edge of the
 th
subband. Each ASE coefﬁcient is then converted to the decibel
scale as follows:
(13)
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 4

LEE et al. : AUTOMATIC MUSIC GENRE CLASSIFICATION 673
Fig. 1. MPEG-7 NASE subband decomposition with spectral resolution /114 /61/49 /61 /50.
The NASE coefﬁcient is derived by normalizing each decibel-
scale ASE coefﬁcient with the root-mean-square (RMS) norm
gain value,
 , as follows:
(14)
where the RMS-norm gain value
 is deﬁned as follows:
(15)
In MPEG-7, the features vector of an audio frame consists of the
RMS-norm gain value
 and the NASE coefﬁcients
 ,
. Thus, the NASE feature vector of an audio frame
will be represented as follows:
(16)
In MPEG-7, the NASE feature vectors are projected onto
a lower-dimensional representation using de-correlated basis
functions such as PCA or ICA. In this study, modulation spec-
tral analysis will be used to characterize the temporal variationsof NASE along time axis.
4) Modulation Spectral Analysis of MFCC, OSC, and NASE:
MFCC, OSC, and NASE capture only short-term frame-based
features of audio signals. To characterize the variations of asound within a longer audio segment or the whole music track,long-term features must be generated from a time series of short-
term features. In this study, long-term modulation spectral anal-
ysis of MFCC, OSC, and NASE is employed to capture thetime-varying behavior of the music signals.
Modulation spectral analysis has been used for speech recog-
nition [26], [30], speaker recognition [31], speaker separation
[32], audio identiﬁcation [27], and sound classiﬁcation [8],[12], [20], [22]. Modulation spectral analysis tries to capturelong-term spectral dynamics within an acoustic signal. Typi-
cally, a modulation spectral model is a two-dimensional joint
“acoustic frequency” and “modulation frequency” represen-tation [31], [33]. Acoustic frequency means the frequencyvariable of conventional spectrogram whereas modulation
frequency captures time-varying information through temporal
modulation of the signal. It has been suggested that in speechsignals the modulation frequencies range from 2 to 8 Hz reﬂectsyllabic and phonetic temporal structure [34]. The periodicityin music signals will cause some nonzero terms in the joint fre-
quency representation. Typically, modulation spectrum in the
range of 1–2 Hz is on the order of musical beat rates, 3–15 Hz ison the order of speech syllabic rates, and higher ones contributeto perceptual roughness revealing musical dissonance [8].
The computation of the joint acoustic-modulation frequency
spectrum is generally carried out in two phases. First, the spec-trogram is computed using FFT on each pre-emphasized, Ham-ming windowed overlapping frame. The pre-emphasis function
and the Hamming window function are shown in (1) and (2),
respectively. Let
denote this time-frequency represen-
tation, where
 is the time variable (frame number) and
 is
the acoustic frequency variable (FFT bins). The second FFT
(or DCT) is then applied on the FFT amplitude envelope of
each acoustic frequency (or frequency subband) along time axisto produce the amplitude modulation spectrogram
,
where
 is the modulation frequency index. Lower
 ’s corre-
spond to slower spectral changes while higher
 ’s correspond
to faster spectral changes.
In addition to capture the spectral dynamics through modula-
tion spectral analysis of each acoustic frequency (or frequency
subband), modulation spectral analysis of cepstral quefrencies
such as MFCC was also used for speech recognition [30] oraudio classiﬁcation [8], [12], [16], [20], [22]. In this study, wewill apply modulation spectral analysis to MFCC, OSC, and
NASE in order to capture the time-varying behavior of these
different music features. To the best of our knowledge, this is anew proposal that extracts discriminative features from the mod-
ulation spectrogram of OSC or NASE for sound classiﬁcation.
Without loss of generality, let
denote the feature vector extracted from the
 th audio frame of
a music signal, where
 is the length of the feature vector. The
feature vector
 can be the MFCC, OSC, NASE feature vector,
or a combination of these feature vectors by concatenating them
together. The modulation spectrogram is obtained by applying
FFT independently on each feature value along the time trajec-tory within a texture window of length
as follows:
(17)
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 5

674 IEEE TRANSACTIONS ON MULTIMEDIA, VOL. 11, NO. 4, JUNE 2009
Fig. 2. Modulation spectra of the ﬁrst MFCC feature value, MFCC(1), of different music genres.
Fig. 3. Modulation spectra of the third valley coefﬁcient, V alley (3), of OSC feature vector of different music genres.
where
 is the modulation spectrogram for the
 th tex-
ture window,
 is the modulation frequency index. In this study,
the window length
 is 512 (about 6 s) with 50% overlap be-
tween two successive texture windows. The representative mod-ulation spectrogram of a music track is derived by time av-
eraging the magnitude modulation spectrograms of all texture
windows as follows:
(18)
where
 is the total number of texture windows in the music
track.
Figs. 2–4 show some modulation spectra of MFCC, OSC,
and NASE feature values. From these ﬁgures, it is clear thatthere exist regular large peaks for Electronic music followed
by the World music. For the modulation spectrum of the ﬁrstMFCC value (see Fig. 2), the lower modulation frequency
components of Classical music and Jazz/Blue music are larger
than those of Metal/Punk music and Rock/Pop music whose
modulation spectra are smaller and smoother than others.For the modulation spectrum of the third valley coefﬁcient
of OSC feature vector (see Fig. 3), the modulation spectra of
Jazz/Blue music , Metal/Punk music and Rock/Pop music are
similar, whereas the modulation spectrum of Classical music
has smaller magnitude values than others. For the modulation
spectrum of the second NASE coefﬁcient (see Fig. 4), the lower
modulation frequency components of Jazz/Blue music is larger
than those of Metal/Punk music and Rock/Pop music. Simi-
larly, the modulation spectrum of Classical music has smaller
magnitude values than others. From these ﬁgures, we can see
that the modulation spectra of different music genres bear somedifferent distributions. That is, each of these three types ofmodulation features can encompass different information for
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 6

LEE et al. : AUTOMATIC MUSIC GENRE CLASSIFICATION 675
Fig. 4. Modulation spectra of the second NASE coefﬁcient, NASE(2), of different music genres.
music genre classiﬁcation. Thus, in this paper an information
fusion approach which provides both feature level fusion (by
concatenating these three different types of modulation spectralfeatures) and decision level combination (by combining theclassiﬁcation results with each type of modulation spectral
feature as the input of a classiﬁer) is employed in an attempt to
improve the classiﬁcation accuracy.
Previous study on modulation frequency selectivity has sug-
gested that the human perception for modulation frequency fol-
lows a logarithmic frequency scale with resolution consistent
with a constant-
effect [35]. Based on this ﬁnding, the av-
eraged modulation spectrum of each spectral/cepstral featurevalue will be decomposed into
logarithmically spaced mod-
ulation subbands. In this study, the number of modulation sub-
bands is 8 (
 ). Table II shows the frequency interval of each
modulation subband. For each spectral/cepstral feature value,the modulation spectral peak (MSP) and modulation spectral
valley (MSV) within each modulation subband are then eval-
uated as follows:
(19)
(20)
where
 and
 are, respectively, the low modulation fre-
quency index and high modulation frequency index of the
 th
modulation subband,
 . The MSPs correspond to the
dominant rhythmic components and MSVs the non-rhythmiccomponents in the modulation subbands. Therefore, the differ-
ence between MSP and MSV will reﬂect the modulation spec-
tral contrast distribution as follows:
(21)
A music signal that returns a high modulation spectral con-
trast value will have large MSP value and a small MSV valueand is likely to represent a signal with strong rhythmic content.A music signal that returns a low modulation spectral contrastTABLE II
FREQUENCY RANGE OF EACH MODULATION SUBBAND
value will likely be a signal without any signiﬁcant rhythmic
pattern. As a result, all MSCs (or MSVs) will form a
 ma-
trix which contains the modulation spectral contrast (or mod-
ulation spectral valley) information. Each row of the MSC (or
MSV) matrix corresponds to the variant modulation frequencycomponents of identical spectral/cepstral feature value, whichreﬂects the beat interval of a music signal. Each column of the
MSC (or MSV) matrix corresponds to the same modulation sub-
band of different spectral/cepstral feature values.
To derive a compact feature vector, the mean and standard de-
viation along each row (and each column) of the MSC and MSV
matrices will be computed as the modulation feature values of
a music track. Along each row of the MSC or MSV matrix,the mean and standard deviation correspond to the average andvariation of the rhythmic strength over variant modulation sub-
bands for a speciﬁc spectral/cepstral feature value. Along each
column of the MSC or MSV matrix, the mean and standard de-viation correspond to the average and variation of the rhythmicstrength over different spectral/cepstral feature values on a spe-
ciﬁc modulation subband. In summary, the modulation spectral
feature values derived from the
th (
 ) row of the
MSC and MSV matrices can be computed as follows:
(22)
(23)
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 7

676 IEEE TRANSACTIONS ON MULTIMEDIA, VOL. 11, NO. 4, JUNE 2009
(24)
(25)
Thus, for a music track the modulation spectral feature vector
derived from the
 rows of the MSC and MSV matrices is of
size
 and can be represented as follows:
(26)
Similarly, the modulation spectral feature values derived from
the
 th (
 ) column of the MSC and MSV matrices can
be computed as follows:
(27)
(28)
(29)
(30)
Thus, the modulation spectral feature vector derived from the
columns of the MSC and MSV matrices is of size
 and can
be represented as follows:
(31)
In this paper, these two modulation spectral feature vectors
(
 and
 ) are concatenated together to yield the modula-
tion spectral feature vector of a music track, which is of size
as follows:
(32)
5) Feature Vector Normalization: Since the dispersion is not
identical for each modulation spectral feature value, a linearnormalization will be independently applied to each modula-
tion spectral feature value to make its range between 0 and 1 as
follows:
(33)where
 denotes the normalized
 th modulation spectral
feature value,
 and
 denote, respectively, the
maximum and minimum of the
 th modulation spectral fea-
ture values of all training music tracks. These reference values,
and
 , are computed during the training phase
and are stored for later reference. In the classiﬁcation phase, foractual normalization, each modulation spectral feature value ex-
tracted from the current music signal is modiﬁed using the refer-
ence maximum and minimum values to obtain its correspondingnormalized values according to (33).
B. Linear Discriminant Analysis (LDA)
Linear discriminant analysis (LDA) [29] aims at improving
the classiﬁcation accuracy at a lower dimensional featurevector space. LDA deals with the discrimination between
various classes rather than the representation of all classes. The
objective of LDA is to minimize the within-class distance whilemaximize the between-class distance. In LDA, an optimaltransformation matrix that maps an
-dimensional feature
space to an
 -dimensional space (
 ) has to be found in
order to provide higher discriminability among various musicclasses.
Let
and
 denote the within-class scatter matrix and be-
tween-class scatter matrix, respectively. The within-class scatter
matrix is deﬁned as follows:
(34)
where
 is the
 th feature vector labeled as class
 ,
is the
mean vector of class
 ,
is the total number of music classes,
and
 is the number of training vectors labeled as class
 . The
between-class scatter matrix is given by the following:
(35)
where
 is the mean vector of all training vectors. The most
widely used transformation matrix is a linear mapping that max-
imizes the so-called Fisher criterion
 deﬁned as the ratio of
between-class scatter to within-class scatter as follows:
(36)
where
 is a transformation matrix. From the above equation,
we can see that LDA tries to ﬁnd a transformation matrix that
maximizes the ratio of between-class scatter to within-classscatter in a lower-dimensional space.
In this study, a whitening procedure is integrated with LDA
transformation such that the multivariate normal distribution
of the set of training vectors becomes a spherical one [29].First, the eigenvalues and corresponding eigenvectors of
are calculated. Let
 denote the matrix whose columns are the
orthonormal eigenvectors of
 , and
 the diagonal matrix
formed by the corresponding eigenvalues. Thus,
 .
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 8

LEE et al. : AUTOMATIC MUSIC GENRE CLASSIFICATION 677
Fig. 5. Whole information fusion structure.
Each training vector
 is then whitening transformed by
as follows:
(37)
It can be shown that the whitened within-class scatter ma-
trix
 derived from all
the whitened training vectors will become an identity ma-trix
. Thus, the whitened between-class scatter matrix
contains all the discriminative
information. A transformation matrix
 can be determined by
ﬁnding the eigenvectors of
 . Assuming that the eigenvalues
are sorted in a decreasing order, the eigenvectors correspondingto the
largest eigenvalues will form the column vectors
of the transformation matrix
 . Finally, the optimal whitened
LDA transformation matrix
 is deﬁned as follows:
(38)
will be employed to transform each
 -dimensional
feature vector to be a lower
 -dimensional vector. Let
 denote
the
 -dimensional feature vector, the reduced
 -dimensional
feature vector can be computed by the following:
(39)
C. Information Fusion Phase
In this paper, an information fusion approach which integrates
both feature level fusion and decision level combination [36] isemployed to improve the performance of music genre classiﬁ-cation. At the stage of feature level fusion, a combined modu-
lation spectral feature vector is obtained by concatenating the
three different types of modulation spectral feature vectors. Atthe stage of decision level combination, each modulation spec-tral feature vector (including the concatenated modulation spec-
tral feature vector) will serve as the input of a speciﬁc classiﬁer
and the classiﬁcation results will be combined to determine theclassiﬁed music class. The whole information fusion structureis depicted in Fig. 5.Let
,
 , and
 denote the three mod-
ulation spectral feature vectors extracted from an input musictrack. At the stage of feature level fusion, a new combined fea-ture vector
is obtained by concatenating
 ,
, and
 together as follows:
(40)
In this paper, each individual modulation spectral feature vector
(
 ,
 , and
 ) as well as the concatenated
modulation spectral feature vector (
 ) will be trans-
formed using its corresponding LDA transformation matrixin order to derive the transformed feature vectors (
,
,
 , and
 ) as follows:
(41)
(42)
(43)
(44)
where
 ,
 ,
 ,
and
 are the whitened LDA transformation
matrices corresponding to the modulation spectral feature vec-
tors
 ,
 ,
 , and
 , respectively.
Note that these LDA transformation matrices are distinct forthese four different types of modulation spectral feature vectors
and are separately computed using the corresponding type of
modulation spectral feature vector alone. To evaluate the simi-larity between two music tracks, a speciﬁc classiﬁer is designedfor each type of transformed feature vector. To combine the re-
sults from the four different classiﬁers, the sum rule will be
employed to compute the overall distance between two musictracks. For the
th (
 ) music genre class, let
 ,
,
 , and
 denote its four different types
of representative feature vectors and let
 ,
 ,
, and
 denote, respectively, the distances
between each type of transformed vector of the input musictrack and the corresponding representative feature vector of the
th music genre class as follows:
(45)
(46)
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 9

678 IEEE TRANSACTIONS ON MULTIMEDIA, VOL. 11, NO. 4, JUNE 2009
(47)
(48)
where
 denotes the distance between two vectors, which
is measured by the squared Euclidean distance. The overall dis-
tance evaluated for the
 th (
 ) music genre is deﬁned
as the sum of each individual distance as follows:
(49)
D. Music Genre Classiﬁcation Phase
In the classiﬁcation phase, the four types of modulation spec-
tral feature vectors are ﬁrst extracted from each input musictrack. The same linear normalization using (33) is applied toeach feature value. Each type of normalized feature vector is
then transformed to be a lower-dimensional feature vector by
using its corresponding whitened LDA transformation matrix.Each type of classiﬁer is employed to compute the distances be-tween the transformed feature vector and the representative fea-
ture vectors of all music class. In this study, the representative
feature vector of the
th music genre is deﬁned as the mean of
all whitened LDA transformed feature vectors computed fromall training music tracks labeled as the
th music genre as fol-
lows:
(50)
where
 denotes the whitened LDA transformed feature
vector of the
 th music track labeled as the
 th music genre,
is the representative feature vector of the
 th music genre, and
is the number of training music tracks labeled as the
 th
music genre. The sum of each individual distance computedfrom each type of classiﬁer is regarded as the overall distance
for the
th music genre,
 . Thus, the subject code
 that
denotes the identiﬁed music genre is determined by ﬁnding themusic class that has the minimum overall distance as follows:
(51)
III. E XPERIMENTAL RESULTS
In this section, we ﬁrst describe the two datasets used for
performance comparison. Second, evaluation methodologies
for these two datasets are presented. Third, investigation of theimportance of various modulation frequency ranges for music
genre classiﬁcation is demonstrated. Fourth, comparison of
classiﬁcation accuracy with different classiﬁers (KNN, GMM,
and LDA) will be presented. Finally, we compare the proposed
method with other approaches in terms of classiﬁcation accu-
racy.
A. Datasets
Two different datasets widely used for music genre classi-
ﬁcation are employed for performance comparison. The ﬁrstdataset (GTZAN) consists of ten genre classes: Blues ,Clas-sical ,Country ,Disco ,HipHop ,Jazz,Metal ,Pop,Reggae , and
Rock . Each class consists of 100 recordings of music pieces of
30-s duration. This dataset was collected by Tzanetakis [3] andwas used for performance evaluation by many researchers [3],
[4], [12], [16]. These excerpts were taken from radio, compact
disks, and MP3 compressed audio ﬁles. Each item was stored
as a 22 050 Hz, 16-bit, mono audio ﬁle. The second dataset
(ISMIR2004 GENRE) was used in the ISMIR2004 Music Genre
Classiﬁcation Contest [37]. This dataset consists of 1458 music
tracks in which 729 music tracks are used for training and theother 729 tracks for testing. The audio ﬁle format is 44.1-kHz,
128-kbps, 16-bit, stereo MP3 ﬁles. In this study, each stereo
MP3 audio ﬁle was ﬁrst converted into a 44.1-kHz, 16-bit, mono
audio ﬁle before classiﬁcation. These music tracks are classiﬁed
into six classes: Classical ,Electronic ,Jazz/Blue ,Metal/Punk ,
Rock/Pop , and World . In summary, the music tracks used for
training/testing include 320/320 tracks of Classical , 115/114
tracks of Electronic , 26/26 tracks of Jazz/Blue , 45/45 tracks of
Metal/Punk , 101/102 tracks of Rock/Pop , and 122/122 tracks of
World music genre.
B. Evaluation Methodology
The classiﬁcation performance on the GTZAN dataset is eval-
uated based on a randomized ten-fold cross-validation repeated
ten times. The dataset was randomly divided into ten folds,
of which nine are used for training and the remaining one isused to test the classiﬁcation accuracy. The classiﬁcation accu-
racy is evaluated ten times on the ten different combinations of
training/testing sets. The overall classiﬁcation accuracy is cal-
culated as the average of ten independent ten-fold cross-valida-
tions.
In order to be able to compare our proposed method with the
results from the ISMIR2004 Music Genre Classiﬁcation Con-
test, our experiment on the ISMIR2004 GENRE dataset used
the same training and testing set partition as in the contest. In the
contest, the classiﬁcation performance is evaluated based on a
50:50 training and testing set partition instead of a ten-fold cross
validation. Since the music tracks per class in the ISMIR2004
GENRE dataset are not equally distributed, the overall accuracy
of correctly classiﬁed genres is evaluated as follows:
(52)
where
 is the probability of appearance of the
 th music genre,
is the classiﬁcation accuracy for the
 th music genre.
C. Investigation of the Importance of Various Modulation
Frequency Ranges
To investigate the importance of various modulation fre-
quency ranges for music genre classiﬁcation, experimental re-
sults in terms of classiﬁcation accuracy for different band-pass
ﬁlters applied in the modulation frequency domain will be
presented. In this experiment, the band-pass ﬁlter is deﬁned in
terms of subband number. That is, a pair of subband numbers
,
 , is used to deﬁne the
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 10

LEE et al. : AUTOMATIC MUSIC GENRE CLASSIFICATION 679
Fig. 6. Comparison of the importance of various modulation frequencies for music genre classiﬁcation.
lower cutoff modulation frequency (the low edge of subband
number
 ) and higher cutoff modulation frequency (the
high edge of subband number
 ). Fig. 6 shows the clas-siﬁcation results of different modulation band-pass ﬁlters
using different modulation spectral feature vectors on the
two datasets. The vertical axis shows the classiﬁcation accu-
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 11

680 IEEE TRANSACTIONS ON MULTIMEDIA, VOL. 11, NO. 4, JUNE 2009
Fig. 7. Confusion matrices for different modulation spectral feature vectors
on the ISMIR2004 GENRE dataset.
racy, whereas the other axes indicate the pair of modulation
subband numbers,
 and
 , of the band-pass ﬁlter.
From this ﬁgure, we can see that for most cases the best
classiﬁcation rate is achieved when all modulation subbands
are used, that is, set the set of cutoff modulation frequencies
. Even for some circumstances, dif-
ferent set of cutoff modulation frequencies may yield a better
classiﬁcation result, the improvement is limited. Thus, in the
following experiments all modulation subbands will be em-
ployed to compute and generate the modulation spectral feature
vectors.
D. Classiﬁcation Results
Fig. 7 shows the confusion matrices of different modulation
feature vectors on the ISMIR2004 GENRE dataset. A confusion
matrix demonstrates which tracks are correctly classiﬁed or not
depending on the class. It is read as “
 is classiﬁed as
”. For each row or column, the music genres are arranged
in the order of Classical (C) ,Electronic (E) ,Jazz/Blue (J) ,
Metal/Punk (M) ,Rock/Pop (R) , and World (W) . For instance,
the number at the ﬁrst column and last row represents the
number of Classical music tracks being classiﬁed as World
music. A perfect matrix only contains numbers in the diagonal.
In this ﬁgure, MMFCC, MOSC, and MNASE denote the ap-
proach using modulation spectral feature vector derived from
modulation spectral analysis of MFCC, OSC, and NASE, re-
spectively; MCOMB denotes the approach using the combinedfeature vector by concatenating the feature vectors of MMFCC,
MOSC, and MNASE; MMFCC+MOSC+MNASE+MCOMB
denotes the information fusion approach which integrates
both feature level fusion and decision level fusion. Comparing
Fig. 7(a)–(c), we can see that no single feature alone out-
performs others for all music genres. For example, MMFCC
performs better than MOSC and MNASE for Metal/Punk
music; MOSC performs best for Classical ,Jazz/Blue , andTABLE III
AVERAGE CLASSIFICATION ACCURACY (CA)FOR VARIOUS FEATURE
SETS AS WELL AS DIFFERENT CLASSIFIERS ON THE GTZAN D ATASET .
GMM(3) AND GMM(4) D ENOTE THE GMM C LASSIFIERS WITHTHREE AND
FOUR GAUSSIAN COMPONENTS , /107 /61/49 /48 FOR KNN C LASSIFIER
TABLE IV
CLASSIFICATION ACCURACY (CA)OFDIFFERENT FEATURE SETS AS WELL AS
DIFFERENT CLASSIFIERS ON THE ISMIR2004 GENRE D ATASET
World music; MNASE outperforms the other two for Electronic
and Rock/Pop music. Thus, we expected that a concatenation
of these three feature vectors can represent a more generalized
feature set with potentially better classiﬁcation result in a wide
range of music genres, as shown in Fig. 7(d). In addition, the
classiﬁcation accuracy can be further improved by using theproposed information fusion approach, as is shown in Fig. 7(e).
The comparisons of classiﬁcation accuracy on the GTZAN
and ISMIR2004 GENRE datasets for various feature sets
as well as different classiﬁers (KNN, GMM, and LDA) are
shown in Tables III and IV. In these two tables, AMFCC,AOSC, and ANASE are approaches with their feature vec-
tors derived from simple averaging of the MFCC, OSC,
and NASE feature vectors of all frames across the whole
music track; AMFCC+AOSC+ANASE, MMFCC+MOSC, and
MMFCC+MOSC+MNASE are approaches using only the de-
cision level fusion to determine the classiﬁed music class from
the results of different classiﬁers. It is clear that the approachesusing modulation spectral features outperform their corre-
sponding approaches using simple averaging features. For the
GTZAN dataset, the best classiﬁcation accuracy is 90.6% using
the approach MMFCC+MOSC+MNASE. For the ISMIR2004
GENRE dataset, the best classiﬁcation accuracy is 86.83%
using the approach MMFCC+MOSC+MNASE+MCOMB.
Table V compares our proposed approach with other ap-
proaches [3], [4], [12], [16] on the GTZAN dataset with the
same experimental setup. Note that the experiment results
are evaluated based on a randomized ten-fold cross-valida-
tion repeated ten times. It is clear that our proposed approach
(MMFCC+MOSC+MNASE) achieves a classiﬁcation accuracy
of 90.6%, which is better than the other approaches.
Table VI shows the comparison with the results from
the ISMIR2004 Music Genre Classiﬁcation Contest as well
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 12

LEE et al. : AUTOMATIC MUSIC GENRE CLASSIFICATION 681
TABLE V
COMPARISON WITHOTHER APPROACHES ON THE GTZAN D ATASET WITH
THE SAME EXPERIMENTAL SETUP (TEN-FOLD CROSS -VALIDATIONS )
TABLE VI
COMPARISON WITH THE RESULTS FROM THE ISMIR2004 M USIC
GENRE CLASSIFICATION CONTEST AND APPROACHES WITH THE SAME
EXPERIMENTAL SETUP (50:50 T RAINING /TESTING SETSPLIT)
as other approaches [12], [15] with the same experimental
setup. From this table, we can see that our proposed approach
(MMFCC+MOSC+MNASE+MCOMB) performs the best
and achieves higher classiﬁcation accuracy (86.83%) than the
winner of the contest with a classiﬁcation accuracy of 84.07%.
IV . C ONCLUSION
A novel feature set, derived from long-term modulation
spectral analysis of spectral (OSC and NASE) and cepstral(MFCC) features, is proposed for music genre classiﬁcation.
For each spectral/cepstral feature set, a modulation spectro-
gram is generated by collecting the modulation spectra ofall feature values. Modulation spectral contrast (MSC) andmodulation spectral valley (MSV) are then computed from
each logarithmically-spaced modulation subband. Statistical
aggregations of all MSCs and MSVs are computed to generateeffective and compact discriminating features. An informationfusion approach which integrates both feature level fusion
and decision level combination is employed to improve the
classiﬁcation accuracy. Experiments conducted on the GTZANdataset have shown that our proposed approach outperformsother approaches with the same experimental setup. In addi-
tion, experimental results on the ISMIR2004 GENRE music
dataset have also shown that our proposed approach achieveshigher classiﬁcation accuracy (86.83%) than the winner ofthe ISMIR2004 Music Genre Classiﬁcation Contest with a
classiﬁcation accuracy of 84.07%.
A
CKNOWLEDGMENT
The authors would like to thank the anonymous reviewers for
their valuable comments that improved the representation andquality of this paper. The authors would also like to thank Dr.
Tzanetakis for kindly sharing his dataset with us.
REFERENCES
[1] D. Perrot and R. Gjerdigen, “Scanning the dial: An exploration of fac-
tors in the identiﬁcation of musical style,” in Proc. Soc. for Music Per-
ception and Cognition , 1999, Abstract, p. 88.
[2] S. Lippens, J. P. Martens, M. Leman, B. Baets, H. Meyer, and G. Tzane-
takis, “A comparison of human and automatic musical genre classiﬁ-
cation,” in Proc. IEEE Int. Conf. Acoustics, Speech, Signal Processing ,
2004, vol. 4, pp. 233–236.
[3] G. Tzanetakis and P. Cook, “Musical genre classiﬁcation of audio sig-
nals,” IEEE Trans. Speech Audio Process. , vol. 10, no. 3, pp. 293–302,
Jul. 2002.
[4] T. Li and M. Ogihara, “Toward intelligent music information retrieval,”
IEEE Trans. Multimedia , vol. 8, no. 3, pp. 564–573, Jun. 2006.
[5] D. N. Jiang, L. Lu, H. J. Zhang, J. H. Tao, and L. H. Cai, “Music type
classiﬁcation by spectral contrast feature,” in Proc. IEEE Int. Conf.
Multimedia and Expo , 2002, vol. 1, pp. 113–116.
[6] K. West and S. Cox, “Features and classiﬁers for the automatic classiﬁ-
cation of musical audio signals,” in Proc. Int. Conf. Music Information
Retrieval , 2004.
[7] K. Umapathy, S. Krishnan, and S. Jimaa, “Multigroup classiﬁcation
of audio signals using time-frequency parameters,” IEEE Trans. Mul-
timedia , vol. 7, no. 2, pp. 308–315, Apr. 2005.
[8] M. F. McKinney and J. Breebaart, “Features for audio and music clas-
siﬁcation,” in Proc. Int. Conf. Music Information Retrieval , 2003, pp.
151–158.
[9] J. J. Aucouturier and F. Pachet, “Representing music genres: A state of
the art,” J. New Music Res. , vol. 32, no. 1, pp. 83–93, 2003.
[10] U. Ba ˘gci and E. Erzin, “Automatic classiﬁcation of musical genres
using inter-genre similarity,” IEEE Signal Process. Lett. , vol. 14, no.
8, pp. 512–524, Aug. 2007.
[11] A. Meng, P. Ahrendt, J. Larsen, and L. K. Hansen, “Temporal feature
integration for music genre classiﬁcation,” IEEE Trans. Audio, Speech,
Lang. Process. , vol. 15, no. 5, pp. 1654–1664, Jul. 2007.
[12] T. Lidy and A. Rauber, “Evaluation of feature extractors and psycho-
acoustic transformations for music genre classiﬁcation,” in Proc. 6th
Int. Conf. Music Information Retrieval , 2005, pp. 34–41.
[13] M. Grimaldi, P. Cunningham, and A. Kokaram, “A wavelet packet rep-
resentation of audio signals for music genre classiﬁcation using dif-
ferent ensemble and feature selection techniques,” in Proc. 5th ACM
SIGMM Int. Workshop on Multimedia Information Retrieval , 2003, pp.
102–108.
[14] J. Bergatra, N. Casagrande, D. Erhan, D. Eck, and B. Kégl, “Aggregate
features and Adaboost for music classiﬁcation,” Mach. Learn. , vol. 65,
no. 2-3, pp. 473–484, Jun. 2006.
[15] Y. Song and C. Zhang, “Content-based information fusion for semi-
supervised music genre classiﬁcation,” IEEE Trans. Multimedia , vol.
10, no. 1, pp. 145–152, Jan. 2008.
[16] I. Panagakis, E. Benetos, and C. Kotropoulos, “Music genre classiﬁca-
tion: A multilinear approach,” in Proc. ISMIR , 2008, pp. 583–588.
[17] C. C. Lin, S. H. Chen, T. K. Truong, and Y. Chang, “Audio classiﬁca-
tion and categorization based on wavelets and support vector machine,”
IEEE Trans. Speech Audio Process. , vol. 13, no. 5, pp. 644–651, Sep.
2005.
[18] H. G. Kim, N. Moreau, and T. Sikora, “Audio classiﬁcation based
on MPEG-7 spectral basis representation,” IEEE Trans. Circuits Syst.
Video Technol. , vol. 14, no. 5, pp. 716–725, May 2004.
[19] H. G. Kim, N. Moreau, and T. Sikora , MPEG-7 Audio and Beyond:
Audio Content Indexing and Retrieval . New York: Wiley, 2005.
[20] F. Mörchen, A. Ultsch, M. Thies, and I. Löhken, “Modeling timbre
distance with temporal statistics from polyphonic music,” IEEE Trans.
Audio, Speech, Lang. Process. , vol. 14, no. 1, pp. 81–90, Jan. 2006.
[21] T. Lambrou, P. Kudumakis, R. Speller, M. Sandler, and A. Linney,
“Classiﬁcation of audio signals using statistical features on time and
wavelet transform domains,” in Proc. IEEE Int. Conf. Acoustics,
Speech, Signal Processing , 1998, vol. 6, pp. 3621–3624.
[22] C. H. Lee, J. L. Shih, K. M. Yu, and J. M. Su, “Automatic music genre
classiﬁcation using modulation spectral contrast feature,” in Proc.
IEEE Int. Conf. Multimedia and Expo , 2007, pp. 204–207.
[23] W. A. Sethares, R. D. Robin, and J. C. Sethares, “Beat tracking of mu-
sical performance using low-level audio feature,” IEEE Trans. Speech
Audio Process. , vol. 13, no. 2, pp. 275–285, Mar. 2005.
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

## Page 13

682 IEEE TRANSACTIONS ON MULTIMEDIA, VOL. 11, NO. 4, JUNE 2009
[24] G. Tzanetakis, A. Ermolinskyi, and P. Cook, “Pitch histograms in audio
and symbolic music information retrieval,” in Proc. Int. Conf. Music
Information Retrieval , 2002.
[25] C. Xu, N. C. Maddage, and X. Shao, “Automatic music classiﬁcation
and summarization,” IEEE Trans. Speech Audio Process. , vol. 13, no.
3, pp. 441–450, May 2005.
[26] B. Kingsbury, N. Morgan, and S. Greenberg, “Robust speech recogni-
tion using the modulation spectrogram,” Speech Commun. , vol. 25, no.
1, pp. 117–132, 1998.
[27] S. Sukittanon, L. E. Atlas, and J. W. Pitton, “Modulation-scale analysis
for content identiﬁcation,” IEEE Trans. Signal Process. , vol. 52, no. 10,
pp. 3023–3035, Oct. 2004.
[28] L. Rabiner and B. H. Juang , Fundamentals of Speech Recognition .
Englewood Cliffs, NJ: Prentice-Hall, 1993.
[29] R. Duda, P. Hart, and D. Stork , Pattern Classiﬁcation . New York:
Wiley, 2000.
[30] V. Tyagi, I. McCowan, H. Misra, and H. Bourlard, “Mel-cepstrum
modulation spectrum (MCMS) features for robust ASR,” in Proc.
Workshop Automatic Speech Recognition and Understanding , 2003.
[31] T. Kinnunen, “Joint acoustic-modulation frequency for speaker recog-
nition,” in Proc. IEEE Int. Conf. Acoustics, Speech, Signal Processing ,
2006, vol. 1, pp. 14–19.
[32] B. Kollmeier and R. Koch, “Speech enhancement based on physiolog-
ical and psychoacoustical models of modulation perception and bin-
aural interaction,” J. Acoust. Soc. Amer. , vol. 95, pp. 1593–1602, 1994.
[33] L. Atlas and S. Shamma, “Joint acoustic and modulation frequency,”
EURASIP J. Appl. Signal Process. , vol. 7, pp. 668–675, 2003.
[34] N. Kanedera, T. Arai, H. Hermansky, and M. Pavel, “On the relative im-
portance of various components of the modulation spectrum for auto-
matic speech recognition,” Speech Commun. , vol. 28, no. 1, pp. 43–55,
May 1999.
[35] S. Ewert and T. Dau, “Characterizing frequency selectivity for enve-
lope ﬂuctuations,” J. Acoust. Soc. Amer. , vol. 108, pp. 1181–1196,
2000.
[36] J. Kittler, M. Hatef, R. Duin, and J. Matas, “On combining classiﬁers,”
IEEE Trans. Pattern Anal. Mach. Intell. , vol. 20, no. 3, pp. 226–239,
Mar. 1998.
[37] [Online]. Available: http://ismir2004.ismir.net/ISMIR_Contest.html.
Chang-Hsing Lee was born on July 24, 1968, in
Tainan, Taiwan. He received the B.S. and Ph.D.degrees in computer and information science from
National Chiao Tung University, Hsinchu, Taiwan,
in 1991 and 1995, respectively.
He is currently an Associate Professor in the
Department of Computer Science and Information
Engineering, Chung Hua University, Hsinchu. His
main research interests include audio/sound classiﬁ-
cation, multimedia information retrieval, and image
processing.
Jau-Ling Shih was born on December 13, 1969,
in Tainan, Taiwan. She received the B.S. degree in
electrical engineering from National Sun Yat-Sen
University, Kaohsiung, Taiwan, in 1992, the M.S.
degree in electrical engineering from National Cheng
Kung University, Tainan, Taiwan, in 1994, and thePh.D. degree in computer and information science
from National Chiao Tung University, Hsinchu,
Taiwan in 2002.
She is currently an Associate Professor in the De-
partment of Computer Science and Information En-
gineering, Chung Hua University, Hsinchu. Her main research interests include
image processing, image retrieval, and audio processing.
Kun-Ming Yu received the B.S. degree in chem-
ical engineering from National Taiwan University,
Taipei, Taiwan, in 1981, and the M.S. and Ph.D.
degrees in computer science from the University ofTexas at Dallas in 1988 and 1991, respectively.
He is currently the Dean of the College of Com-
puter Science and Informatics, Chung Hua Univer-
sity, Hsinchu, Taiwan. His research interests include
load balancing, distributed and parallel computing,
high-performance computing, ad hoc network, com-
puter algorithms, and audio processing.
Hwai-San Lin was born on October 18, 1980,
in Taipei, Taiwan. He received the B.S. degree in
computer science from Chinese Culture University,
Taipei, in 2005 and the M.S. degree in computerscience and information engineering from Chung
Hua University, Hsinchu, Taiwan, in 2009.
His main research interests include audio/sound
classiﬁcation and image processing.
Authorized licensed use limited to: Chung Hwa University. Downloaded on November 25, 2009 at 03:36 from IEEE Xplore.  Restrictions apply. 

