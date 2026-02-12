# Author Guidelines for 8

**Author:** foobar  
**Subject:** N/A  
**Total Pages:** 4  
**Source File:** `Music_type_classification_by_spectral_contrast_fea.pdf`

---

## Page 1

MUSIC TYPE CLASSIFICATION BY SPECTRAL CONTRAST FEATURE1 
 
                                                 
1 The work was performed at Microsoft Research Asia Dan-Ning Jiang*, Lie Lu**, Hong-Jiang Z hang**, Jian-Hua Tao*, Lian-Hong Cai* 
  
*Department of Computer Science and Technology, Tsinghua University, China 
jdn00@mails.tsinghua.edu.cn, jhtao@tsinghua.edu.cn, clh-dcs@tsinghua.edu.cn  
 
**Microsoft Research, Asia  
{llu, hjzhang}@microsoft.com  
 
 
ABSTRACT 
 
Automatic music type classification is very helpful for the 
management of digital music data base. In this paper, Octave-
based Spectral Contrast feature is proposed to represent the spectral characteristics of a music clip. It represented the relative 
spectral distribution instead of average spectral envelope. 
Experiments showed that Octave-based Spectral Contrast feature performed well in music type cl assification. Another comparison 
experiment demonstrated that Octave-based Spectral Contrast 
feature has a better discrimina tion among different music types 
than Mel-Frequency Cepstral Co efficients (MFCC), which is 
often used in previous music type classification systems. 
1. INTRODUCTION 
Music is very popular in modern life, and the amount of digital 
music increases rapidly nowadays. How to manage a large digital 
music database has arisen as a crucial problem. Automatic music 
type classification could be very  helpful for the music database 
management. Although music type is  not a very clear concept, 
music still could be divided into two major categories: classical 
music and popular music. Classical  music, which is opposed to 
popular music, is intended to include  all kinds of “serious” music, 
while popular music means “music of the populace” [6].  For 
each major music category, it could be further divided into some 
small classes due to different peri ods or different music style. In 
our music type classification system, classical music is further 
classified into baroque musi c and romantic music, which 
correspond to the baroque era and romantic era in western music history respectively [6]; popular mu sic is further classified into 
three types, which include pop songs, jazz, and rock. Thus, five types are classified in our system. 
There are many music characteristics could be used to 
discriminate different music type, such as the musical structure, tempo, rhythm, melody, chord,  and so on. However, it is 
extremely difficult to extract them precisely by signal processing methods for most digital music.  Therefore, many previous 
researches turned to spectral characteristics, which are found 
useful for discriminating different music types and easy to be 
extracted. Matityaho [1] applied multi-layer neural network on 
the average amplitude of Fourier transform coefficients to separate classical and pop music. Han [2] used the nearest mean 
classifier to classify music into  classical music, jazz, and popular 
music with some simple spectral features. Soltau [3] used HMM 
and ETM-NN method to extract the temporal structure from the 
sequence of cepstral coefficients, and implemented a music type 
classification system for rock, pop, techno and classic. Pye [4] 
used Gaussian Mixture Model (GMM) and Mel-Frequency Cepstral Coefficients (MFCC) to obtain a best classification 
result in his system, which incl udes six types of blues, easy 
listening, classical, opera, dance and indie rock. However, while 
developing different models to improve the performance of 
music type recognition system, most of these work used average 
spectral envelope (such as MFCC) to represent the spectral 
characteristics of music. This kind of features averages the spectrum in each sub-band and reflects the average spectral 
characteristics, but it could not represent the relative spectral 
characteristics in each sub-band, which seem more important to 
discriminate different  types of music.  
In this paper, Octave-based Spectral Contrast feature is 
proposed to represent the rela tive spectral characteristics of 
music. Octave-based Spectral Contrast feature considers the 
strength of spectral peaks and spectral valleys in each sub-band 
separately, so that it could represent the relative spectral 
characteristics, and then roughly reflect the distribution of harmonic and non-harmonic compone nts. Experiments showed 
that Octave-based Spectral Contrast feature had good discrimination in music type cl assification and performed better 
than MFCC feature. 
The rest of this paper is or ganized as follows. Section 2 
discusses the representation of Octave-based Spectral Contrast 
feature in detail. Our classification scheme is described in Section 3. In Section 4, experi ments are performed to evaluate 
the proposed feature. 
 
2. OCTAVE-BASED SPECTRAL CONTRAST 
REPRESENTATION 
Octave-based Spectral Contrast considers the spectral peak, spectral valley and their difference in each sub-band. For most 
music, the strong spectral peaks roughly correspond with 
harmonic components; while non-harmonic components, or 

## Page 2

noises, often appear at spectral valley s. Thus, Spectral Contrast 
feature could roughly  reflect the relative distribution of the 
harmonic and non-harmonic components in the spectrum. 
Previous  features , such as MFCC, average the s pectral 
distribution in each sub-band, and thus  lose the relative s pectral 
information. Considering two spect ra that have different spectral 
distribution m ay have s imilar average s pectral characteris tics, the 
average s pectral dis tribution is  not sufficient to repres ent the 
spectral characteris tics of m usic. However, S pectral Contras t 
keeps more information and may  have a better discrimination in 
music type clas sification.    
 
Spectral 
Contrast Digital Samples 
FFT Octave-
Scale 
Filters Peak/Valley Select 
and 
Spectral Contrast Log K-L 
Digital Samples 
FFT Mel- 
Scale 
Filters Log DCT MFCC(a) 
(b) 
Sum 
 
Fig. 1 . The comparison of (a) Octave-bas ed S pectral Contras t 
and (b) MFCC  
Fig. 1 (a) illustrates the estim ation procedure of Octave-
based Spectral Contrast feature.  FFT is first performed on the 
digital sam ples to obtain the spectrum . Then, the frequency  
domain is divided into sub-bands by several Octave-scale filters. 
The s trength of s pectral peaks , valley s, and their difference are 
estimated in each s ub-band. After being trans lated into Log 
domain, the raw Spectral Contrast feature is mapped to an 
orthogonal space and elim inated the relativity  among different 
dimensions by  Karhunen-Loeve transform. 
The above procedure is to es timate Octave-based Spectral 
Contras t feature from  one fram e. For a m usic clip or a m usic 
piece, the mean vector and s tandard deviation vector of all of its  
fram es are us ed to repres ent its  spectral characteris tics.      
The estimation procedure of MFCC is also listed in Fig. 1 (b) 
to com pare with that of Octave-bas ed Spectral Contras t feature. 
There are s ome differences  between the two procedures: 
(1) The filter bank is different. Octave-based Spectral 
Contrast feature uses octave-s cale filters, while MFCC uses Mel-
scale filters.  Although Mel-scale is  suitable for general auditory  
model, octave-scale filter is more suitable for m usic processing. 
In our implementation, the freque ncy domain is divided into six 
Octave-scale sub-bands, which are 0hz~200hz, 200hz~400hz, 
400hz~ 800hz, 800hz~1600hz, 1600hz~3200hz, and 
3200hz~8000hz (the sample rate is  16khz).  Since the Spectral 
Contrast feature is based on Octa ve-scale filters, the feature is 
named as Octave-based Spectral Contrast. It will be sim plified as 
Spectral Contrast for convenience in the left of this paper.   
(2) S pectral Contras t extracts  the strength of spectral peaks , 
valley s, and their difference in each s ub-band, while MFCC sums 
the F FT amplitudes . Thus , Spectral Contras t feature repres ents 
the relative spectral characteristics, but MFCC only involves the 
average s pectral inform ation. S pectral Contras t includes  more 
spectral inform ation than MFCC.   (3) At the las t step, S pectral Contras t feature uses a K-L 
trans form while M FCC us es a DCT trans form. They  are 
equivalent from the view of elim inating relativity . It should be 
noticed that the orthogonal base vectors for K-L transform are 
got from the training data set.  
2.1. Raw Spectral Contrast Feature Estimation  
In features  extraction, the m usic piece is  first segmented into 
frames by  200ms analy sis window with 100ms overlapping.  For 
each fram e, FFT is perform ed to get the spectral com ponents and 
then it is divided into six oc tave-based sub-bands. Finally , 
Spectral Contras t is estimated from  each octave s ub-band.  
The raw S pectral Contras t feature es timates the strength of 
spectral peaks , valley s and their difference in each s ub-band. In 
our s cheme, in order to ens ure the steadines s of the feature, the 
strength of s pectral peaks  and s pectral valley s are estimated by 
the average value in the small neighborhood around maximum 
and m inimum value res pectively , instead of the exact maximum 
and minimum value themselves. Thus, neighborhood factor α is 
introduced to describe the small neighborhood. Detailed 
expres sions are as  follows :  
Suppose the FFT vector of k-th sub-band is 
. After sorting it in a descending order, the 
new vector can be repres ented as { , where   
. } ,, , {, 2, 1, Nk k k x xxL
'
,'
2,'
1, k k k x x x >>>L},,,'
,'
2,'
1, Nk k k x xxL
N
Then the s trength of s pectral peaks  and spectral valley s are 
estimated as : 
}1log{
1'
,∑
==N
iik k xNPeakα
α   (1) 
}1log{
1'
1 ,∑
=+− =N
iiNk k xNValleyα
α  (2) 
And their difference is: 
k k k Valley Peak SC −=      (3) 
where N is total num ber in k-th sub-band, .    ]6,1[∈k
Different values of α from 0.02 to 0.2 are tested in 
experiments. It s hows that vary ing α in this range does not 
influence the perform ance s ignificantly . In real im plem entation, 
α is set to be 0.02.   
{SCk , Valley k} ( ]6,1[∈k ) is used as the 12-dimension raw 
Spectral Contrast feature. Alt hough Spectral Contrast means the 
difference of strength between the spectral peaks and valley s, the 
strength of s pectral valley s are als o contained in the feature to 
keep m ore spectral inform ation.   
2.2. Karhunen-Loeve Transform 
It is obvious that there exist so me relativity  among the different 
dimensions of raw feature. To solve this problem, Karhunen-
Loeve trans form is perform ed on the raw  feature to rem ove the 
relativity . After K-L transform , the feature vector is m apped into 
an orthogonal space, and the covariance m atrix also becom es 
diagonal in the new feature space. These properties of K-L 

## Page 3

transform make the classify ing procedure easier and lead to good 
classification perform ance even w ith simple clas sifier.   
In our experiments, the matrix  that generates the orthogonal 
base vectors  is estimated from  the covariance m atrix of each 
class. It is repres ented as : 
∑
=Σ=5
1iii w P S     (4) 
where is generate m atrix, P and  are the prior probability  
and the covariance matrix of the i-th clas s respectively . In 
experiments,  is set to be 0.2, which corresponds to equal 
probability  distribution for each class; Σ is estimated from  the 
training set of the i-th music ty pe class. The orthogonal base 
vectors  are the eigenvectors  of the generate matrix S. Then the 
transformation is done as below: wSi iΣ
iP
i
w
Ux x='     ( 5) 
T
D j u u uu U ],,,,,[2 1 LL=    (6) 
where x is the raw  feature vector, x is the S pectral Contrast 
feature vector after K -L trans form, D is the dimension of the 
feature s pace, and  is the j-th orthogonal base vector.   '
ju
3. CLASSIFICATION SCHEME 
In general, human could discriminate a music ty pe in several 
seconds, such as 10 seconds. Theref ore, our classification scheme 
is first based on 10-second music clips. Then the classification 
experiments on whole music are also performed.   
Gaussian Mixture Model (GMM) with 16 components is 
applied in our approach and Expectation Maximization (EM) 
algorithm  is used to estim ate th e param eters of GMM model for 
each m usic type. 
Let x be the feature vector of a 10-second music clip, then 
the probability  density  (mixture density ) of this music clip 
belonging to class-i is defined as: 
              (7)  ∑
==16
1),,( )|(
jij ij ij i Cux w Gxp N
where is the GM M model of the i-th class; w,  and  
are the w eight, m ean vector, and covariance m atrix of the j-th 
component in G, respectively . iGij ijuijC
i
The clas sification is  easy to proceed. A s usual w ay, each clip 
in the testing set is classified into the class that has the largest 
probability  density  according to Bay esian criterion.   
The perform ance can be increas ed w hen the w hole music is 
used as classification unit instead of 10-second clip. In order to 
classify a whole piece of m usic, the m usic is first divided into 
several 10-second clips.  Final cla ssification result of the music is 
determ ined by  com bing the probabilities of every  clip. 
Suppose there are  independent 10-second clips in a whole 
piece of m usic, and the feature s et is X , then the probability  density  of the whole m usic in class- i can be 
calculated as  follow ing: 
N
},,,{2 1 Nx xxL=∏
==N
ji j i Gxp GXP
1)|( )|(    (8) 
The clas sification is  then determ ined by  the maximum 
probability  density .   
In real implementation, one 10- second music clip is extracted 
from  every  30 seconds in each piece of music in order to 
decreas e the com putation com plexity .   
4. EX PERIMENTS 
4.1. Database for Experiments 
There are about 1500 pieces of m usic in our database for 
experiments, and five music types are included: baroque music, 
romantic m usic, pop songs, jazz, and rock. Most of the baroque 
pieces in the database are literatures of Bach and H andel, w ho 
are the most important compos ers in the baroque era. The 
romantic database is com posed of literatures of Chopin, Schubert, 
Liszt, Beethoven, and other compos ers in the romantic era. Pop 
songs are those singed by  some  popular singers, which includes 
nine m en and s ixteen w omen.  Jazz and rock in the databas e also 
include literatures of m any different composers. In each music 
type database, different possi ble m usical form  and musical 
instruments are included.   
All the music data in the da tabase are 16kHz, 16 bits, mono 
wave files. About 6250 10-sec ond clips, which are randomly  
selected from  the 1500 pieces of m usic, com pose the 
classification database, where 5000 is for training and 1250 for 
testing. For each m usic ty pe, there are about 1000 clips in the 
training set, and about 250 clips in the testing set.  10-second 
clips  from  the s ame music piece w ould not appear both in the 
training set and testing set. In the classification experiments on 
whole music, the training data is the same as those for 10-
sencond music clips, while the tes ting data is composed by  the 
music piece whose clips  are pres ented in the original tes ting data 
set.   
4.2. Cl assification Resul ts 
An experiment is first perform ed on 10-second clips by  using 
Spectral Contras t. The m ean and standard deviation of Spectral 
Contrast composes a 24-dimensi on feature for a music clip. The 
classification performance is pretty  good, and the average 
accuracy  reaches  82.3%. The detailed classification results are 
listed in Table 1. 
 BaroqueRom antic Pop Jazz Rock 
Baroque 83.2% 12.8% 0.4% 3.6% 0.0% 
Romantic 12.9% 84.2% 0.8% 1.2% 0.8% 
Pop 1.6% 2.4% 78.4% 11.6% 6.0% 
Jazz 2.0% 0.4% 15.2% 78.4% 4.0% 
Rock 0.4% 0.8% 6.0% 5.6% 87.2%
Table 1. The detailed classification results on 10-second clips  

## Page 4

From Table 1, it could be seen  that the clas sification error 
rate between the baroque and roma ntic music is high, while few 
clips  of these two types are clas sified into the other three clas ses 
by mistakes. This is because that  the baroque and rom antic m usic 
both belong to classical musi c and thus their spectral 
characteris tics are s imilar. The s ame phenom ena could be seen 
from  pop songs, jazz and rock.   
We also perform ed an experim ent on classification of whole 
music piece.  The detailed res ults are s hown in Table 2. 
 Baroque Rom antic Pop Jazz Rock 
Baroque 86.7% 10.0% 0.0% 3.3% 0.0% 
Romantic 7.3% 90.9% 0.00% 1.8% 0.00%
Pop 0.0% 0.0% 92.3% 6.2% 1.5% 
Jazz 1.7% 0.0% 5.2% 91.4% 1.7% 
Rock 0.0% 0.0% 4.5% 3.0% 92.5%
Table 2.  The detailed classification results on whole music piece  
From Table 2, the average clas sification accuracy  on w hole 
music piece is up to 90.8%, w hich is  much higher than 82.3% on 
10-second clips. The classification error rate of each music class 
decreas es much.   
4.3. Compari son w ith MFCC  
Mel-Frequency  Ceps tral Coefficients  (MFCC) are w idely used in 
audio classification [5]  and music classification [3] [4].  It has 
been proven that MFCC perform s well in these tasks.  It is also 
reported that adding an energy  term with MFCC features could 
greatly  improve the perform ance of music type classification [4]. 
So, in this com parison expe riment, we will com pare the 
performance among the following th ree feature sets: Spectral 
Contrast, MFCC with Energy  term, and MFCC without Energy  
term. The comparison experiment s are only  implemented on our 
testing set of 10-second clips.   
As Spectral Contras t, 12-order M FCC features  are extracted 
from  each fram e. Then, the m ean and the standard derivation of 
the MFCC, which compose a 24-dimension feature set, are 
estimated to repres ent the m usic clip. W hen energy  term  is 
considered, the feature is 26-dimension. 
Table 3 lis ted the average classification accuracy  when using 
different feature set. 
Feature S et Classification A ccuracy
MFCC 74.1% 
MFCC + Energy  78.0% 
Spectral Contrast 82.3% 
Table 3 . The average clas sification accuracy  when us ing M FCC, 
MFCC + Energy , and Spectral Contrast 
Table 3 shows that Spectral Contrast performs better than the 
other tw o feature s ets in m usic ty pe classification. The 
classification accuracy  reaches  to 82.3% with Spectral Contras t, 
which is 8.2% and 4.3% higher than MFCC and MFCC with 
energy  term , respectively . Fig. 2 illustrates the detailed com parison results.  F rom Fig. 2, 
it can be s een that the clas sification error rate decreas es 20%-
30% for each m usic type w hen us ing S pectral Contras t instead of 
MFCC.  It proves that the new proposed Spectral Contrast feature 
can im prove the m usic clas sification perform ance s atisfactorily .  
5060708090100
BaroqueRomantic Pop Jazz Rock
Music TypeClassification AccuracySpectral Contrast
MFCC+Energy
MFCC
 
Fig. 2. The details of the com parison results of S pectral Contrast 
and M FCC features  
5. CONCLUSION 
This paper presented a set of new feature named Octave-based 
Spectral Contrast.  Spectral Contra st deals with the strength of 
spectral peaks , valley s, and their difference s eparately  in each 
sub-band, and repres ents the relative spectral characteris tics.  
Based on S pectral Contras t feature, an autom atic m usic type 
classification system is implem ented to clas sify music into five 
classes, which include  baroque music, roma ntic music, pop songs, 
jazz, and rock.  A n average accuracy  of 82.3% is  achieved for 
classification on 10-second music clips, and 90.8% is achieved 
on w hole m usic pieces .  Our com parison experim ent also showed 
that the proposed Spectral Contrast feature had a better 
perform ance than M FCC feature in m usic type clas sification.  
6. REFERENCES 
[1] B. M atityaho and M . Furst. “ Neural Network Based Model 
for Classification of Music Ty pe”, in Proc. of 18th Conv. 
Electrical and Electronic Engineers in Israel, pp. 4.3.4/1-5, 
1995. 
[2] K. P. Han, Y. S. Pank, S. G. Jeon, G.C. Lee, and Y.  H. Ha, 
“Genre Classification Sy stem of TV Sound Signals Based on 
a Spectrogram  Analysis”, IEEE Trans actions  on Cons umer 
Electronics, VOL. 55, No. 1, pp. 33-42, 1998. 
[3] H. S oltau, T. S chultz, M artin W estphal, and Alex W aibel. 
“Recognition of Music Types”.  ICASSP 1998,  Vol.  II, pp. 
1137-1140, 1998. 
[4] D. Py e. “Content-Based Me thods for the Management of 
Digital Music”.  ICASSP 2000,  Vol.  IV, pp.2437-2440,  2000.   
[5] D. Li, I. K. Sethi, N. Dimitrova, T. M cGee, “ Classification 
of General Audio Data for Cont ent-Based Retrieval”, Pattern 
Recognition Letters, VOL. 22, No. 5, pp. 533-544, 2001. 
[6] S. Sadie as Editor, “ The Cam bridge M usic G uide”, 
Cambridge University  Press, 1985. 
 

