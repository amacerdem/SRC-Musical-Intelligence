# neural-synchrony-arxiv

1
Multi-Label Sentiment Analysis on 100 Languages
with Dynamic Weighting for Label Imbalance
Selim F. Yilmaz, E. Batuhan Kaynak, Aykut Koc ¸,Senior Member, IEEE,
Hamdi Dibeklio ˘glu, Member, IEEE and Suleyman S. Kozat, Senior Member, IEEE
Abstract—We investigate cross-lingual sentiment analysis,
which has attracted signiﬁcant attention due to its applications
in various areas including market research, politics and social
sciences. In particular, we introduce a sentiment analysis frame-
work in multi-label setting as it obeys Plutchik wheel of emotions.
We introduce a novel dynamic weighting method that balances
the contribution from each class during training, unlike previous
static weighting methods that assign non-changing weights based
on their class frequency. Moreover, we adapt the focal loss that
favors harder instances from single-label object recognition liter-
ature to our multi-label setting. Furthermore, we derive a method
to choose optimal class-speciﬁc thresholds that maximize the
macro-f1 score in linear time complexity. Through an extensive
set of experiments, we show that our method obtains the state-
of-the-art performance in 7 of 9 metrics in 3 different languages
using a single model compared to the common baselines and
the best-performing methods in the SemEval competition. We
publicly share our code for our model, which can perform
sentiment analysis in 100 languages, to facilitate further research.
Index Terms —Sentiment analysis, cross-lingual, label imbal-
ance, multi-label, macro-f1 maximization, social media, natural
language processing.
I. I NTRODUCTION
A. Preliminaries
W
E study sentiment analysis problem in multi-label
setting, which has been widely studied in the litera-
ture due to its signiﬁcance in various applications including
market research, politics, public health and disaster manage-
ment [1]–[3]. In particular, we introduce a method for cross-
lingual sentiment analysis, which is a harder problem than
the standard sentiment analysis problem since one needs to
make predictions for various languages including even unseen
ones. Cross-lingual sentiment analysis aims to leverage high-
quality and abundant resources in English for classiﬁcation
to improve the classiﬁcation performance of resource-scarce
languages [4]. Moreover, we employ data of three languages
to obtain the best score in 7 of 9 metrics of Arabic, English and
Spanish languages in the SemEval emotion classiﬁcation [1].
This work is supported in part by Outstanding Researcher Programme
Turkish Academy of Sciences.
S. F. Yilmaz, A. Koc ¸ and S. S. Kozat are with the Department of Electrical
and Electronics Engineering, Bilkent University, 06800 Ankara, Turkey (e-
mail:{syilmaz,kozat}@ee.bilkent.edu.tr, aykut.koc@bilkent.edu.tr).
A Koc ¸ is also with the National Magnetic Resonance Center UMRAM,
06800 Ankara, Turkey.
S. S. Kozat is also with the DataBoss A.S., Bilkent Cyberpark, 06800
Ankara, Turkey (e-mail: serdar.kozat@data-boss.com.tr).
B. Kaynak and H. Dibeklio ˘glu are with the Department of Com-
puter Engineering, Bilkent University, 06800 Ankara, Turkey (e-mail:
batuhan.kaynak@bilkent.edu.tr, dibeklioglu@cs.bilkent.edu.tr).
disapprovalremorse
contempt awe
submission
loveoptimism
aggressiveness
pensiveness
annoyance anger rage
ecstasy
joy
serenity
terror fear apprehension
admiration
trust
acceptance
vigilance
anticipation
interest
boredom
disgust
loathing amazement
surprise
distractionsadness
grief
Fig. 1: Plutchik’s [5] wheel of emotions.
Plutchik [5], in 1980, has created the wheel of emotions
in his psychoevolutionary theory of emotion to illustrate his
idea of emotion, which is shown in Fig. 1. He suggests
eight bipolar primary emotions that appear on the opposite
sides of the wheel: joy versus sadness, anger versus fear,
disgust versus trust, surprise versus anticipation. The primary
emotions are expressed at different intensities and the inter-
mediate emotions occur as a mix of these primary emotions.
Moreover, the emotions are non-exclusive in Plutchik’s model
as their combinations derive other emotions, and there exist
correlations between the emotions, e.g., joy and sadness are
represented as the opposite emotions. Following the Plutchiks
theory [5], we formulate the sentiment analysis as the multi-
label classiﬁcation task, in which more than one label can be
assigned to a text simultaneously. Yet, the class imbalance is
an inherent issue in multi-label classiﬁcation [6]. Although the
class imbalance has been extensively studied for the binary
classiﬁcation setting, it remains a challenge in multi-label
classiﬁcation [6]. Furthermore, the tail labels, i.e., the labels
with a low number of instances, impact the performance
signiﬁcantly less compared to the common labels when the
classes are equally weighted in the multi-label setting due
to the rarity of relevant examples and result in suboptimal
arXiv:2008.11573v1  [cs.LG]  26 Aug 2020
2
performance [7]. Thus, we introduce a dynamic weighting
method to dynamically adjust the class weights during training
to remedy the class imbalance.
In this article, we introduce a multilingual sentiment anal-
ysis framework in multi-label setting on 100 different lan-
guages. Our method uses focal loss to enhance the importance
of hard examples. We introduce a dynamic weighting method
to cope with the label imbalance. We also derive a macro-
f1 maximization method within linear time complexity. Our
method achieves the best result for 7 out of 9 metrics for
the SemEval competition for Arabic, English and Spanish
languages [1]. We also demonstrate the performance of our
method on cross-lingual combinations of the datasets and
assess the performance gains obtained by the components in
our method.
B. Prior Art and Comparisons
Deep learning based methods have been shown to be
successful in various classiﬁcation tasks [8]. Transfer learning
approaches have been popular in the sentiment analysis and
shown to be successful especially in datasets with small num-
ber of instances [9]. Through transfer learning, an extensive
amount of unlabeled data in the social media have been in-
corporated to increase the performance of the target sentiment
analysis task, e.g., [9] employs 1.7 billion tweets with emojis
to pretrain the network. However, [10] demonstrates that the
transfer learning approach does not improve the performance
on the SemEval emotion classiﬁcation competition datasets,
which is our target due to the richness of its labels, which
has signiﬁcantly more number of instances compared to the
number of instances used in [9]. [11] emulates a multi-
label classiﬁer through a binary classiﬁer for each of the
four opposite emotions that are on the opposite sides of the
Plutchik’s wheel of emotions as shown in Fig. 1 such as joy
and sadness. However, their approach does not include the
correlations to the rest of the labels since they train each of the
four classiﬁers with the objective of binary classiﬁcation of the
opposite sides. To remedy those issues, we introduce a multi-
label deep learning model for the emoji prediction task that
directly predicts the active set of labels simultaneously, i.e., in
the multi-task setting. Moreover, the multi-label classiﬁcation
is a generalization of binary and multi-class classiﬁcation tasks
as we describe through remarks, thus, our method is also
applicable to these tasks. The multi-label classiﬁcation also
requires a prediction method that converts scores into the
predictions, for which we derive a class speciﬁc thresholding
by macro-f1 maximization in linear time complexity.
Multi-label classiﬁcation has an inherent issue of data
imbalance [6]. Although signiﬁcant research has been per-
formed in the literature, the class imbalance problem remains
a challenge for multi-label classiﬁcation [6]. Consider the
multi-label classiﬁcation task with 16 distinct labels. There
are 216 possible combinations in the superset of the labels.
Accordingly, it is not feasible to obtain balanced data for
each combination of the labels. Many studies in multi-output
classiﬁcation either try to balance the data by resampling
or ignore the imbalance [6]. Yet, the over-sampling and
under-sampling methods are not designed for the multi-label
classiﬁcation, thus, their adaptation to the multi-label setting
is not straightforward [6]. One heuristic that is widely adapted
is using inverse class frequency per class as a weighting
factor [12]. However, this heuristic results in suboptimal
performance as shown by [13] and in Section IV-E. [13]
replaces the inverse number of instances with the expected
volume of instances and a controlling hyperparameter. [14]
proposes to use class prior probabilities as weights for the
cross-entropy loss. Commonly, these methods propose static
weights for each class. To remedy the label imbalance in the
multi-label setting, we introduce a novel dynamic weighting
method, which equalizes the contribution of each class to the
loss. We use focal loss [15] to incorporate the hardness of the
instances and our dynamic weighting method can readily be
adapted to other losses as we show through a remark.
Recent language models such as BERT [16] have been
dominating the areas in the NLP literature, however, they con-
tain an excessive amount of parameters. Accordingly, training
or ﬁne-tuning these models require an excessive amount of
resources [16]. We employ RoBERTa-XLM [17], which is a
robustly trained BERT on 100 languages, as feature extractor
to beneﬁt from BERT as well as reducing the amount of
required resources.
SemEval emotion classiﬁcation competition [1] has paved
the way for many multi-label sentiment analysis models.
EMA, PARTNA are among the models that opt for the more
traditional support vector machine approaches and still achieve
the best results in the Arabic language [18]. On the other hand,
more recent long short-term memory (LSTM), convolutional
neural network (CNNs) and attention models are also adopted
to obtain the highest ranked results in English and Span-
ish [19], [20]. It is important to note that most of these models
are language speciﬁc, and use special embeddings such as
AraVec [21] or special lexicons paired with language speciﬁc
preprocessing steps. Tw-StAR attempts to create a generic
model to apply multiple languages, yet, is ranked behind the
language-speciﬁc models [22]. We introduce a framework that
uses bidirectional LSTM with attention and multi-label focal
loss, which achieves the best score only using a single model
on 7 of the 9 metrics on three different languages of the
SemEval emotion classiﬁcation competition [1].
C. Contributions
Our contributions are as follows:
1) First time in the literature to the best of our knowledge,
we introduce a multi-label emotion classiﬁcation method
that is capable of producing uniformly high classiﬁcation
performance on 100 different languages using a single
model. Our method can readily be adapted to the cross-
lingual platforms such as Amazon without using any
language detection component. We make our model pub-
licly available 1 to facilitate reproducibility and further
research.
2) We introduce a dynamic weighting method to remedy
the class imbalance that is an inherent problem in
1https://github.com/selimﬁrat/multilingual-sentiment-analysis
3
multi-label classiﬁcation with adaptive loss weights as
training progress, unlike the previous static weighting
methods [13], [14]. We demonstrate the signiﬁcant per-
formance gains compared to the previous weighting
methods and our method performs no worse than the
uniform weighting, i.e., no weighting, for none of the
hyperparameter choices. Our dynamic weighting method
can be readily extended to other losses as we show
through a remark.
3) We derive a method to maximize macro-f1 with class
speciﬁc threshold choices, which reduces the time com-
plexity from exponential to linear.
4) Our method can readily be adapted to pretrained models
that will be available in future, non-supported languages
and different models, which we show through remarks.
5) We adapt focal loss to our multi-label emotion classiﬁ-
cation framework from the single-label object recogni-
tion literature and we show performance improvements
obtained via the focal loss [15].
6) Through an extensive set of experiments, we show that
our model achieves the best scores in 7 out of 9 metrics
in the SemEval emotion classiﬁcation competition for
Arabic, English and Spanish via a single model [1].
7) We analyze the cross-lingual performance of our method
including the different training and test language pairs.
8) We perform an ablation study to analyze the effect of the
recurrent network and perform hyperparameter analysis
for our dynamic weighting method.
D. Organization of this Paper
The rest of the paper is organized as follows. In Section II,
we describe the multi-label sentiment analysis task and show
that it is the generalization of the binary and multi-class
classiﬁcation tasks. In Section III, we introduce our deep
metric learning based framework and the components to cope
with the label imbalance. In Section IV, we demonstrate the
performance improvements obtained by our proposed model
compared to the state-of-the-art methods in the literature and
the SemEval [1] emotion classiﬁcation competition winners.
In Section V, we conclude by providing remarks.
II. P ROBLEM DESCRIPTION
In this article, all vectors are column vectors and deﬁned by
boldfaced lowercase letters. All matrices and tensors are rep-
resented by boldfaced uppercase letters. |·| denotes cardinality,
i.e., the number of elements, of set ·.
We aim to predict the labels of the given text in multi-label
framework through our network F. We receive training data
P = {(si,ci)}n
i , where si is the text of ith training instance,
n is the number of training instances, ci = [ci,1ci,2..., ci,w]T
is the label vector of the ith training instance,w is the number
of classes and ci,a, a ∈ {1, 2,...w }, is deﬁned by
ci,a =
{
1, if class a is inferred
0, otherwise.
BiLSTM BiLSTM BiLSTM…
BiLSTM BiLSTM BiLSTM…BiLSTM Layer 2
BiLSTM Layer 1
In Bilkent
…
… happens
Token
Representations
(XLM-RoBERTa)
Attention
Scores
Prediction ˆci
<latexit sha1_base64="GNN/jUxMQX8DlxCoJfAtZ+WXJv8=">AAAB+HicbVDLSsNAFJ3UV62PRt0IbgaL0FVJ6kJ3Fty4rGAf0IQwmU7aoTOZMDMRasiXuHGhqFs/wU9w5xf4FYLTx0JbD1w4nHMv994TJowq7TifVmFldW19o7hZ2tre2S3be/ttJVKJSQsLJmQ3RIowGpOWppqRbiIJ4iEjnXB0OfE7t0QqKuIbPU6Iz9EgphHFSBspsMveEOks88II4jwPaGBXnJozBVwm7pxULr7fxdfhC28G9ofXFzjlJNaYIaV6rpNoP0NSU8xIXvJSRRKER2hAeobGiBPlZ9PDc3hilD6MhDQVazhVf09kiCs15qHp5EgP1aI3Ef/zeqmOzv2MxkmqSYxni6KUQS3gJAXYp5JgzcaGICypuRXiIZIIa5NVyYTgLr68TNr1mntaq1+7lUYVzFAER+AYVIELzkADXIEmaAEMUnAPHsGTdWc9WM/W66y1YM1nDsAfWG8/7R2XoQ==</latexit>
ˆci
<latexit sha1_base64="GNN/jUxMQX8DlxCoJfAtZ+WXJv8=">AAAB+HicbVDLSsNAFJ3UV62PRt0IbgaL0FVJ6kJ3Fty4rGAf0IQwmU7aoTOZMDMRasiXuHGhqFs/wU9w5xf4FYLTx0JbD1w4nHMv994TJowq7TifVmFldW19o7hZ2tre2S3be/ttJVKJSQsLJmQ3RIowGpOWppqRbiIJ4iEjnXB0OfE7t0QqKuIbPU6Iz9EgphHFSBspsMveEOks88II4jwPaGBXnJozBVwm7pxULr7fxdfhC28G9ofXFzjlJNaYIaV6rpNoP0NSU8xIXvJSRRKER2hAeobGiBPlZ9PDc3hilD6MhDQVazhVf09kiCs15qHp5EgP1aI3Ef/zeqmOzv2MxkmqSYxni6KUQS3gJAXYp5JgzcaGICypuRXiIZIIa5NVyYTgLr68TNr1mntaq1+7lUYVzFAER+AYVIELzkADXIEmaAEMUnAPHsGTdWc9WM/W66y1YM1nDsAfWG8/7R2XoQ==</latexit>
sigmoid(W¯h)
<latexit sha1_base64="gGU0qy22RaBOFESTDv4Z74aVu3M=">AAACD3icbZC7TsMwFIadcmvLLcDIYlGBylIlZYCxgoWxCHqRmqhyXKe1aieR7SCVKG/AwquwMIAQK2JjQOJtcNIO0PJLlj795xz5nN+LGJXKsr6NwtLyyupasVRe39jc2jZ3dtsyjAUmLRyyUHQ9JAmjAWkpqhjpRoIg7jHS8cYXWb1zS4SkYXCjJhFxORoG1KcYKW31zSOHIzUSPJF0yEM6SKuJ4/mwkzrnSCQ5j9L0uG9WrJqVCy6CPYNKo3j39XHdLDX75qczCHHMSaAwQ1L2bCtSboKEopiRtOzEkkQIj9GQ9DQGiBPpJvk9KTzUzgD6odAvUDB3f08kiEs54Z7uzLaX87XM/K/Wi5V/5iY0iGJFAjz9yI8ZVCHMwoEDKghWbKIBYUH1rhCPkEBY6QjLOgR7/uRFaNdr9kmtfmVXGlUwVRHsgwNQBTY4BQ1wCZqgBTC4B4/gGbwYD8aT8Wq8TVsLxmxmD/yR8f4DiKWf1w==</latexit>
sigmoid(W¯h)
<latexit sha1_base64="gGU0qy22RaBOFESTDv4Z74aVu3M=">AAACD3icbZC7TsMwFIadcmvLLcDIYlGBylIlZYCxgoWxCHqRmqhyXKe1aieR7SCVKG/AwquwMIAQK2JjQOJtcNIO0PJLlj795xz5nN+LGJXKsr6NwtLyyupasVRe39jc2jZ3dtsyjAUmLRyyUHQ9JAmjAWkpqhjpRoIg7jHS8cYXWb1zS4SkYXCjJhFxORoG1KcYKW31zSOHIzUSPJF0yEM6SKuJ4/mwkzrnSCQ5j9L0uG9WrJqVCy6CPYNKo3j39XHdLDX75qczCHHMSaAwQ1L2bCtSboKEopiRtOzEkkQIj9GQ9DQGiBPpJvk9KTzUzgD6odAvUDB3f08kiEs54Z7uzLaX87XM/K/Wi5V/5iY0iGJFAjz9yI8ZVCHMwoEDKghWbKIBYUH1rhCPkEBY6QjLOgR7/uRFaNdr9kmtfmVXGlUwVRHsgwNQBTY4BQ1wCZqgBTC4B4/gGbwYD8aT8Wq8TVsLxmxmD/yR8f4DiKWf1w==</latexit>
¯h
<latexit sha1_base64="AZ29dCAw4aQO1Q0emQuFVhCb80E=">AAAB9HicbVC7SgNBFL3rM8ZX1FKQwSCkCrux0M6gjWUC5gHJEmYns8mQ2dl1ZjYQli39BhsLRWxT5zvs/AZ/wsmj0MQDFw7n3Mu993gRZ0rb9pe1tr6xubWd2cnu7u0fHOaOjusqjCWhNRLyUDY9rChngtY005w2I0lx4HHa8AZ3U78xpFKxUDzoUUTdAPcE8xnB2khu+xbLJGl7PuqnaSeXt4v2DGiVOAuSvxlPqt9PZ5NKJ/fZ7oYkDqjQhGOlWo4daTfBUjPCaZptx4pGmAxwj7YMFTigyk1mR6fowihd5IfSlNBopv6eSHCg1CjwTGeAdV8te1PxP68Va//aTZiIYk0FmS/yY450iKYJoC6TlGg+MgQTycytiPSxxESbnLImBGf55VVSLxWdy2Kp6uTLBZgjA6dwDgVw4ArKcA8VqAGBR3iGV3izhtaL9W59zFvXrMXMCfyBNf4BXKqWLA==</latexit>
¯h
<latexit sha1_base64="AZ29dCAw4aQO1Q0emQuFVhCb80E=">AAAB9HicbVC7SgNBFL3rM8ZX1FKQwSCkCrux0M6gjWUC5gHJEmYns8mQ2dl1ZjYQli39BhsLRWxT5zvs/AZ/wsmj0MQDFw7n3Mu993gRZ0rb9pe1tr6xubWd2cnu7u0fHOaOjusqjCWhNRLyUDY9rChngtY005w2I0lx4HHa8AZ3U78xpFKxUDzoUUTdAPcE8xnB2khu+xbLJGl7PuqnaSeXt4v2DGiVOAuSvxlPqt9PZ5NKJ/fZ7oYkDqjQhGOlWo4daTfBUjPCaZptx4pGmAxwj7YMFTigyk1mR6fowihd5IfSlNBopv6eSHCg1CjwTGeAdV8te1PxP68Va//aTZiIYk0FmS/yY450iKYJoC6TlGg+MgQTycytiPSxxESbnLImBGf55VVSLxWdy2Kp6uTLBZgjA6dwDgVw4ArKcA8VqAGBR3iGV3izhtaL9W59zFvXrMXMCfyBNf4BXKqWLA==</latexit>
h(2)
1
<latexit sha1_base64="r3ZSePNc65cA6miH75o8vEhU8pw=">AAAB+HicbVDJSgNBEK1xjeOScbl5aQxCvISZeNBjQBCPEcwCyTj0dHqSJj0L3T1CHObgd3jxoIhXP8WLCH6MneWgiQ8KHu9VUVXPTziTyra/jKXlldW19cKGubm1vVO0dveaMk4FoQ0S81i0fSwpZxFtKKY4bSeC4tDntOUPL8Z+644KyeLoRo0S6oa4H7GAEay05FnFrOsHaJB7zm1Wrp7knlWyK/YEaJE4M1KqmQeX8uHzu+5ZH91eTNKQRopwLGXHsRPlZlgoRjjNzW4qaYLJEPdpR9MIh1S62eTwHB1rpYeCWOiKFJqovycyHEo5Cn3dGWI1kPPeWPzP66QqOHczFiWpohGZLgpSjlSMximgHhOUKD7SBBPB9K2IDLDAROmsTB2CM//yImlWK85ppXrtlGplmKIAh3AEZXDgDGpwBXVoAIEUHuEZXox748l4Nd6mrUvGbGYf/sB4/wHdlZWA</latexit>
h(2)
1
<latexit sha1_base64="r3ZSePNc65cA6miH75o8vEhU8pw=">AAAB+HicbVDJSgNBEK1xjeOScbl5aQxCvISZeNBjQBCPEcwCyTj0dHqSJj0L3T1CHObgd3jxoIhXP8WLCH6MneWgiQ8KHu9VUVXPTziTyra/jKXlldW19cKGubm1vVO0dveaMk4FoQ0S81i0fSwpZxFtKKY4bSeC4tDntOUPL8Z+644KyeLoRo0S6oa4H7GAEay05FnFrOsHaJB7zm1Wrp7knlWyK/YEaJE4M1KqmQeX8uHzu+5ZH91eTNKQRopwLGXHsRPlZlgoRjjNzW4qaYLJEPdpR9MIh1S62eTwHB1rpYeCWOiKFJqovycyHEo5Cn3dGWI1kPPeWPzP66QqOHczFiWpohGZLgpSjlSMximgHhOUKD7SBBPB9K2IDLDAROmsTB2CM//yImlWK85ppXrtlGplmKIAh3AEZXDgDGpwBXVoAIEUHuEZXox748l4Nd6mrUvGbGYf/sB4/wHdlZWA</latexit>
h(2)
2
<latexit sha1_base64="DHcG8+yuGOE3WhC4dggNHjalgzQ=">AAAB+HicbVDJSgNBEK1xjeOScbl5aQxCvISZ8aDHgCAeI5gFkjj0dHqSJj0L3T1CHObgd3jxoIhXP8WLCH6MneWgiQ8KHu9VUVXPTziTyra/jKXlldW19cKGubm1vVO0dvcaMk4FoXUS81i0fCwpZxGtK6Y4bSWC4tDntOkPL8Z+844KyeLoRo0S2g1xP2IBI1hpybOKWccP0CD33Nus7J7knlWyK/YEaJE4M1KqmgeX8uHzu+ZZH51eTNKQRopwLGXbsRPVzbBQjHCam51U0gSTIe7TtqYRDqnsZpPDc3SslR4KYqErUmii/p7IcCjlKPR1Z4jVQM57Y/E/r52q4LybsShJFY3IdFGQcqRiNE4B9ZigRPGRJpgIpm9FZIAFJkpnZeoQnPmXF0nDrTinFffaKVXLMEUBDuEIyuDAGVThCmpQBwIpPMIzvBj3xpPxarxNW5eM2cw+/IHx/gPfH5WB</latexit>
h(2)
2
<latexit sha1_base64="DHcG8+yuGOE3WhC4dggNHjalgzQ=">AAAB+HicbVDJSgNBEK1xjeOScbl5aQxCvISZ8aDHgCAeI5gFkjj0dHqSJj0L3T1CHObgd3jxoIhXP8WLCH6MneWgiQ8KHu9VUVXPTziTyra/jKXlldW19cKGubm1vVO0dvcaMk4FoXUS81i0fCwpZxGtK6Y4bSWC4tDntOkPL8Z+844KyeLoRo0S2g1xP2IBI1hpybOKWccP0CD33Nus7J7knlWyK/YEaJE4M1KqmgeX8uHzu+ZZH51eTNKQRopwLGXbsRPVzbBQjHCam51U0gSTIe7TtqYRDqnsZpPDc3SslR4KYqErUmii/p7IcCjlKPR1Z4jVQM57Y/E/r52q4LybsShJFY3IdFGQcqRiNE4B9ZigRPGRJpgIpm9FZIAFJkpnZeoQnPmXF0nDrTinFffaKVXLMEUBDuEIyuDAGVThCmpQBwIpPMIzvBj3xpPxarxNW5eM2cw+/IHx/gPfH5WB</latexit>
h(2)
p
<latexit sha1_base64="2geKlPwDGObWOcAvJc9jnhWzJUQ=">AAAB+HicbVC7SgNBFL3rM8ZH1ljaDAYhNmE3FloGbCwjmAcm6zI7mU2GzD6YmRXisqXgP9gIKmJr7Vdo5d84eRSaeODC4Zx7ufceL+ZMKsv6NpaWV1bX1nMb+c2t7Z2CuVtsyigRhDZIxCPR9rCknIW0oZjitB0LigOP05Y3PBv7rRsqJIvCSzWKqRPgfsh8RrDSkmsW0q7no0HmxtdpuXqUuWbJqlgToEViz0ipVnz6+Lq6u6+75me3F5EkoKEiHEvZsa1YOSkWihFOs3w3kTTGZIj7tKNpiAMqnXRyeIYOtdJDfiR0hQpN1N8TKQ6kHAWe7gywGsh5byz+53US5Z86KQvjRNGQTBf5CUcqQuMUUI8JShQfaYKJYPpWRAZYYKJ0Vnkdgj3/8iJpViv2caV6YZdqZZgiB/twAGWw4QRqcA51aACBBB7gGV6MW+PReDXepq1LxmxmD/7AeP8BGRyWXw==</latexit>
h(2)
p
<latexit sha1_base64="2geKlPwDGObWOcAvJc9jnhWzJUQ=">AAAB+HicbVC7SgNBFL3rM8ZH1ljaDAYhNmE3FloGbCwjmAcm6zI7mU2GzD6YmRXisqXgP9gIKmJr7Vdo5d84eRSaeODC4Zx7ufceL+ZMKsv6NpaWV1bX1nMb+c2t7Z2CuVtsyigRhDZIxCPR9rCknIW0oZjitB0LigOP05Y3PBv7rRsqJIvCSzWKqRPgfsh8RrDSkmsW0q7no0HmxtdpuXqUuWbJqlgToEViz0ipVnz6+Lq6u6+75me3F5EkoKEiHEvZsa1YOSkWihFOs3w3kTTGZIj7tKNpiAMqnXRyeIYOtdJDfiR0hQpN1N8TKQ6kHAWe7gywGsh5byz+53US5Z86KQvjRNGQTBf5CUcqQuMUUI8JShQfaYKJYPpWRAZYYKJ0Vnkdgj3/8iJpViv2caV6YZdqZZgiB/twAGWw4QRqcA51aACBBB7gGV6MW+PReDXepq1LxmxmD/7AeP8BGRyWXw==</latexit>
⌧
<latexit sha1_base64="0NFRh4mpdWzAoAsxLM9IG8axbqY=">AAAB8XicbZC7SgNBFIbPeo3xFrUUZDAIVmE3FtoZsLFMwFwwCWF2MpsMmZ1dZs4KYUnpG9hYKGIrWOc57HwGX8LJpdDoDwMf/38Oc87xYykMuu6ns7S8srq2ntnIbm5t7+zm9vZrJko041UWyUg3fGq4FIpXUaDkjVhzGvqS1/3B1SSv33FtRKRucBjzdkh7SgSCUbTWbdryA9JCmow6ubxbcKcif8GbQ/7yfVz5uj8alzu5j1Y3YknIFTJJjWl6boztlGoUTPJRtpUYHlM2oD3etKhoyE07nU48IifW6ZIg0vYpJFP3Z0dKQ2OGoW8rQ4p9s5hNzP+yZoLBRTsVKk6QKzb7KEgkwYhM1iddoTlDObRAmRZ2VsL6VFOG9khZewRvceW/UCsWvLNCseLlS6cwUwYO4RhOwYNzKME1lKEKDBQ8wBM8O8Z5dF6c11npkjPvOYBfct6+ARvilOM=</latexit>
⌧
<latexit sha1_base64="0NFRh4mpdWzAoAsxLM9IG8axbqY=">AAAB8XicbZC7SgNBFIbPeo3xFrUUZDAIVmE3FtoZsLFMwFwwCWF2MpsMmZ1dZs4KYUnpG9hYKGIrWOc57HwGX8LJpdDoDwMf/38Oc87xYykMuu6ns7S8srq2ntnIbm5t7+zm9vZrJko041UWyUg3fGq4FIpXUaDkjVhzGvqS1/3B1SSv33FtRKRucBjzdkh7SgSCUbTWbdryA9JCmow6ubxbcKcif8GbQ/7yfVz5uj8alzu5j1Y3YknIFTJJjWl6boztlGoUTPJRtpUYHlM2oD3etKhoyE07nU48IifW6ZIg0vYpJFP3Z0dKQ2OGoW8rQ4p9s5hNzP+yZoLBRTsVKk6QKzb7KEgkwYhM1iddoTlDObRAmRZ2VsL6VFOG9khZewRvceW/UCsWvLNCseLlS6cwUwYO4RhOwYNzKME1lKEKDBQ8wBM8O8Z5dF6c11npkjPvOYBfct6+ARvilOM=</latexit>
Multi-Label Focal Loss
With Dynamic Weighting
Optimal Class-Speciﬁc 
Thresholds 
L
<latexit sha1_base64="kTfGAAqxbAHQuIUZ5sswvmG0MXw=">AAAB8nicbVC7SgNBFL3rM8ZX1FKQxSCkCrux0M6AjYVFAuYBmyXMTmaTIbMzy8ysEJaUfoKNhSK2Yp3vsPMb/AlnkxSaeODC4Zx7uefeIGZUacf5slZW19Y3NnNb+e2d3b39wsFhU4lEYtLAggnZDpAijHLS0FQz0o4lQVHASCsYXmd+655IRQW/06OY+BHqcxpSjLSRvE6E9AAjlt6Ou4WiU3amsJeJOyfFq49J/fvhZFLrFj47PYGTiHCNGVLKc51Y+ymSmmJGxvlOokiM8BD1iWcoRxFRfjqNPLbPjNKzQyFNcW1P1d8TKYqUGkWB6cwiqkUvE//zvESHl35KeZxowvFsUZgwWws7u9/uUUmwZiNDEJbUZLXxAEmEtflS3jzBXTx5mTQrZfe8XKm7xWoJZsjBMZxCCVy4gCrcQA0agEHAIzzDi6WtJ+vVepu1rljzmSP4A+v9ByxplYU=</latexit>
L
<latexit sha1_base64="kTfGAAqxbAHQuIUZ5sswvmG0MXw=">AAAB8nicbVC7SgNBFL3rM8ZX1FKQxSCkCrux0M6AjYVFAuYBmyXMTmaTIbMzy8ysEJaUfoKNhSK2Yp3vsPMb/AlnkxSaeODC4Zx7uefeIGZUacf5slZW19Y3NnNb+e2d3b39wsFhU4lEYtLAggnZDpAijHLS0FQz0o4lQVHASCsYXmd+655IRQW/06OY+BHqcxpSjLSRvE6E9AAjlt6Ou4WiU3amsJeJOyfFq49J/fvhZFLrFj47PYGTiHCNGVLKc51Y+ymSmmJGxvlOokiM8BD1iWcoRxFRfjqNPLbPjNKzQyFNcW1P1d8TKYqUGkWB6cwiqkUvE//zvESHl35KeZxowvFsUZgwWws7u9/uUUmwZiNDEJbUZLXxAEmEtflS3jzBXTx5mTQrZfe8XKm7xWoJZsjBMZxCCVy4gCrcQA0agEHAIzzDi6WtJ+vVepu1rljzmSP4A+v9ByxplYU=</latexit>
Subwords of si
<latexit sha1_base64="zsAJ4NuU3nr4k1heujfcqNgfko4=">AAAB+nicbVBNT8JAEJ36ifhV9OhlI5hwIi0e9EjixSNG+UigabbLFjZsu83uVkIqP8WLB43x6i/x5r9xgR4UfMkkL+/NZGZekHCmtON8WxubW9s7u4W94v7B4dGxXTppK5FKQltEcCG7AVaUs5i2NNOcdhNJcRRw2gnGN3O/80ilYiJ+0NOEehEexixkBGsj+XbpPg0mQg4UEiGqKJ9VfLvs1JwF0Dpxc1KGHE3f/uoPBEkjGmvCsVI910m0l2GpGeF0VuyniiaYjPGQ9gyNcUSVly1On6ELowxQKKSpWKOF+nsiw5FS0ygwnRHWI7XqzcX/vF6qw2svY3GSahqT5aIw5UgLNM8BDZikRPOpIZhIZm5FZIQlJtqkVTQhuKsvr5N2veZe1up39XKjmsdRgDM4hyq4cAUNuIUmtIDABJ7hFd6sJ+vFerc+lq0bVj5zCn9gff4AJeyTLg==</latexit>
Subwords of si
<latexit sha1_base64="zsAJ4NuU3nr4k1heujfcqNgfko4=">AAAB+nicbVBNT8JAEJ36ifhV9OhlI5hwIi0e9EjixSNG+UigabbLFjZsu83uVkIqP8WLB43x6i/x5r9xgR4UfMkkL+/NZGZekHCmtON8WxubW9s7u4W94v7B4dGxXTppK5FKQltEcCG7AVaUs5i2NNOcdhNJcRRw2gnGN3O/80ilYiJ+0NOEehEexixkBGsj+XbpPg0mQg4UEiGqKJ9VfLvs1JwF0Dpxc1KGHE3f/uoPBEkjGmvCsVI910m0l2GpGeF0VuyniiaYjPGQ9gyNcUSVly1On6ELowxQKKSpWKOF+nsiw5FS0ygwnRHWI7XqzcX/vF6qw2svY3GSahqT5aIw5UgLNM8BDZikRPOpIZhIZm5FZIQlJtqkVTQhuKsvr5N2veZe1up39XKjmsdRgDM4hyq4cAUNuIUmtIDABJ7hFd6sJ+vFerc+lq0bVj5zCn9gff4AJeyTLg==</latexit>
Fig. 2: The overall structure of our model.
To satisfy this decision function, we predict score ˆci,a for the
target sentence si via our network F as:
ˆci,a = F(si) =p(ci,a = 1 |si). (1)
Remark 1. Multi-class classiﬁcation is a generalization of
multi-class and binary classiﬁcation tasks. For both, we have
only one active label, i.e., ∑w
a=1ci,a = 1, ∀i ∈ { 1, 2,...,n }.
The number of classes w = 2 and w > 2 for binary
and multi-label classiﬁcation, respectively. Since we formulate
the problem as a multi-label classiﬁcation, our framework is
applicable to binary classiﬁcation, multi-class classiﬁcation
and multi-label classiﬁcation settings.
III. M ETHODOLOGY
In this section, we ﬁrst describe the language modeling
and recurrent modeling with attention for the multi-label
classiﬁcation. We then introduce our multi-label adaptation
of focal loss and our dynamic weighting method. Lastly, we
derive a method to select thresholds by maximizing macro-
f1 within linear time complexity. Fig. 2 illustrates the overall
structure of our methodology.
A. Deep Multilingual Language Modeling
Here, we describe our language modeling approach using
XLM-RoBERTa [17].
Traditional approaches such as well known Bag-of-Words
fail to generalize to the unseen data due to the sparsity of the
language [23]. Early word embedding-based methods, such as
the well-known word2vec [24], based approaches have been
used to cope with this problem via learning a vector for
each word in a large vocabulary exploiting semantic relations
between words [23]. However, these methods assign a single
4
vector to each word regardless of the context of the target sen-
tence. Recently, language models such as BERT have achieved
outstanding results on various tasks [16]. These language
models assign context-dependent vectors to each token in the
target space instead of assigning a ﬁxed vector. These models
are trained using large corpora in an unsupervised setting.
However, these models contain millions of parameters and it
is not reasonable to ﬁnetune them on a small corpus. Thus,
we use feature-vectors extracted from the pretrained model for
each text instead of directly ﬁnetuning the pretrained model.
As shown in Fig. 2, we use XLM-RoBERTa pretrained
tokenizer and pretrained model [17]. XLM-RoBERTa is pre-
trained on CommonCrawl corpora of 100 different languages.
We ﬁrst tokenize the input sentence si into subword units
via byte-pair encoding using Sentencepiece Tokenizer [25].
We convert the sentence si to X(i) ∈ Rm×di by using the
hidden state vectors of the pretrained language model, where
m is the embedding vector length and di is the number of
tokens in the sentence si. We obtain an embedding vector for
each token in the sentence, i.e., X(i) = [x1...,xdi], where
xj ∈ Rm, ∀j ∈ {1, 2,...,d i}.
Remark 2. Our model can be adapted to other languages since
we tokenize via byte-pair encoding and convert to features
without applying any language-dependent preprocessing. For
the languages that XLM-RoBERTa does not support, one can
directly use any other pretrained model that supports the
target language. We show the cross-lingual performance of
our method in Section IV-D.
B. Temporal Modeling of Sentence via Recurrent Networks
Here, we describe our recurrent modeling for the multi-
label emotion classiﬁcation using the frozen features via the
language modeling network.
We are given a sequence of token embeddings X(i) ∈di ×
m for the sentence si, where di is the number of tokens in the
sentence si and m is the embedding size. xk ∈ Rm indicates
the embedding of the kth token.
As shown in Fig. 2, we use bidirectional RNNs to incor-
porate both the forward and the backward information of the
sequence. Through the RNN we process the variable length
sequences. We employ deep networks, where the number of
layers is u. For timestep t and kth layer, we utilize − →h (k)
t
and ← −h (k)
t notations to deﬁne forward and backward RNNs,
respectively. We deﬁne kth layer of the forward RNN that
uses Elman’s formulation [26] as:
− →h (k)
t = tanh(W (k)
hh
− →h (k)
t−1 +W (k)
hx
− →h (k−1)
t +b(k)),
where − →h (0)
t = xt for t ∈ { 1, 2,...,d i} − →h (k)
0 ∼ N (0, 0.01),
b(k) is the bias term to be learned and W (k)
hh , W (k)
hx are the
weights to be learned. We also deﬁne the backward RNN’s
hidden state ← −h (k)
t for kth layer by feeding the reversed input
to the RNN, i.e.,
← −h (k)
t = tanh(V (k)
hh
← −h (k)
t+1 +V (k)
hx
← −h (k−1)
t +c(k)),
where ← −h (0)
t =xdi−t+1, ← −h (k)
di
∼ N (0, 0.01),c(k) is the bias
term to be learned and V (k)
hh , V (k)
hx are the weights to be
learned.
Remark 3. We extend our framework to the LSTM [27] due to
its success in capturing complex temporal relations. We feed
the input sentence embedding X(i) to the LSTM instead of
the RNN as:
z(k)
t = tanh(W (k)
z
− →h (k−1)
t +V (k)
z
− →h (k)
t−1 +b(k)
z )
s(k)
t = sigmoid(W (k)
s
− →h (k−1)
t +V (k)
s
− →h (k)
t−1 +b(k)
s )
f(k)
t = sigmoid(W (k)
f
− →h (k−1)
t +V (k)
f
− →h (k)
t−1 +b(k)
f )
c(k)
t =s(k)
t ⊙z(k)
t +f(k)
t ⊙c(k)
t−1
o(k)
t = sigmoid(W (k)
o
− →h (k−1)
t +R(k)
o
− →h (k)
t−1 +b(k)
o )
− →h (k)
t =o(k)
t ⊙ tanh(c(k)
t ),
where − →h (0)
t = xt, − →h (k)
0 ∼ N (0, 0.01), c(k)
t ∈ Rm is the
cell state vector, h(k)
t ∈ Rw is the hidden state vector, for the
tth LSTM unit. s(k)
t , f(k)
t and o(k)
t are the input, forget and
output gates, respectively. ⊙ is the operation for elementwise
multiplication.W ,V , and b with the subscripts z, s, f, and
o are the parameters of the LSTM unit to be learned. We also
deﬁne the backward LSTM via ← −h (k)
t by reversing the input
order for each layer of the LSTM, as in RNNs.
We concatenate the hidden states of the backward and the
forward RNN of kth layer at time t as:
h(k)
t =
[− →h (k)
t← −h (k)
t
]
.
We then apply attention to the hidden states by weighing each
timestep’s hidden state with a single parameter as [28]:
¯h =
p∑
t=1
βth(u)
t ,
where p is the sequence length and βt =
exp(hts)∑p
i=1 exp(his) for
the timestep t ∈ { 1, 2,...,p }. Lastly, we use linear layer and
sigmoid activation to convert our predictions to the labels as:
r = sigmoid(W ¯h), (2)
wherer ∈ Rs and s is the number of the target labels of the
task.
Remark 4. We use sigmoid activation at the ﬁnal layer instead
of softmax since the softmax assumes independence between
labels, whereas in our case the labels are non-independent due
to Plutchik’s theory [5] as we describe in Section I-A.
C. Multi-Label Focal Loss
In this section, we adapt the focal loss for our multi-
label framework from the single-label object recognition lit-
erature [15]. We deﬁne pi,a for notational convenience as the
5
following:
pi,a =
{
ri,a, ifci,a = 1
1 −ri,a, otherwise,
where ri,a is the sigmoid output for class a and the instance
i, which is obtained via (2). Then, the standard cross entropy
loss for instance i and class a becomes − logpi,a.
Focal loss has been proposed to overcome the class imbal-
ance problem in object recognition, which extends the cross
entropy loss [15]. The focal loss focuses training of the hard
instances instead of the well-classiﬁed ones as:
li,a = −(1 −pi,a)γ logpi,a,
where γ ∈ R is a tunable parameter and γ ≥ 0. Notice that
the focal loss extends the cross entropy loss by multiplying
with (1 −pi,a)γ. The concept of focusing on hard samples
is similar to the mining of the hard instances in deep metric
learning [29].
We convert the loss into a scalar by taking weighted sum
w.r.t. the classes and averaging w.r.t. the instances in the batch
as:
L = 1
b
b∑
i=1
w∑
a=1
αt,ali,a, (3)
such that ∑w
a=1αt,a = 1 , t is the index of the mini-batch
iteration,b is the batch size and αt,a is the weight of the class
a at the mini-batch iteration t. We can assign equal weights
to by setting αt,a = 1
w for each class a and for all mini-
batch iterationt. In the following section, we introduce a novel
method for choosing αt,a to remedy the class imbalance.
D. Novel Dynamic Weighting Method for Label Imbalance
Here, we introduce our dynamic weighting method to im-
prove the imbalanced multi-label classiﬁcation, which can also
be applied to the single-label problems and other loss functions
as we show through remarks.
Although focal loss improves the imbalanced classiﬁcation
performance, there is still plenty of room for improvement. For
instances, [15] uses alpha balanced variant of the focal loss
in practice, where they choose inverse frequency of the class
as in the imbalanced classiﬁcation. [13] also extends focal
loss by class volume based formulation and introduces another
hyperparameter. We introduce a method to equalize the losses
from all classes in the problem. Our goal is to deﬁne weights
in a way that each class has equal contribution to the loss, i.e.,
|P|∑
i=1
αt,1li,1 =
|P|∑
i=1
αt,2li,2 =... =
|P|∑
i=1
αt,wli,w,
where P is the training data.
Finding the exact value for αt,a is intractable since model
parameters change after each mini-batch and we train in mini-
batch setting. Thus, we track the losses by exponentially
smoothed approximation ωt,a at mini-batch iteration t and
class a, which is given by
ωt,a =
b∑
i=1
κli,a + (1 −κ)ωt,a−1,
where κ is the smoothing hyperparameter to be tuned and
ω1,a = 1
w, ∀a ∈ {1, 2,...,w }. We invert ωt,a and introduce a
very small ϵ term if there appears no loss for any class for
numerical stability of our method since we may get 0 loss for
some classes, as the following:
φt,a = 1
ϵ +ωt,a
,
where we set ϵ = 1 × 10−5. Using φt,a, we deﬁneαt,a in (3)
as:
αt,a = φt,a∑w
u=1φt,u
. (4)
Through (4), we gurantee that the weights sum up to 1 for
any mini-batch iteration. We set the gradient w.r.t. the network
parameters Θ to zero, i.e., ∇Θαt,a = 0, ∀t ∈ { 1, 2,... },a ∈
{1, 2,...,w }. We balance the loss contribution from the classes
by using αt,a in (3).
Remark 5. Notice that the weights of our dynamic weighting
method change over time w.r.t. the hardness of the instances
among classes, unlike the previous methods in the litera-
ture [13], [14].
Remark 6. Dynamic weighting is loss-agnostic, thus, can
readily be adapted to the other alternative losses. For exam-
ple, we can adapt it into the cross entropy loss by setting
li,a = − logpi,a and directly use (3).
Remark 7. Dynamic weighting method can also be applied to
the single label problems without any change since the multi-
label problem is a generalization of the single-label variant.
E. Class Speciﬁc Thresholding via Macro-F1 Maximization
We derive a macro-f1 maximization method by choosing the
optimal class speciﬁc threshold within linear time complexity.
We have the model output ˆci = ri, which is our score
vector, that is to be thresholded to make a prediction. We have
a class speciﬁc scoreˆci,a for classa. We expect high scores for
the inferred classes and low scores for the non-inferred classes.
We split a part of the validation set as the thresholding set and
then use it to choose the optimal threshold hat maximizes the
macro-f1 score. We concatenate the scores of all instances in
the thresholding set T into ˆca ∈ R|T| as:
ˆca =
[ˆc1,a ˆc2,a ... ˆc|T|,a
]T
.
Our aim is to ﬁnd a threshold vector τ ∈ Rw given by
τ =
[τ1 τ2 ... τ w
]T
.
We select the optimal threshold for each class that maximizes
the macro-f1 score, which is the F1 score calculated for each
class and averaged among the classes. F1 is the harmonic mean
of the precision and recall for a class a, i.e.,
F1(ca, ˆca) = 2 × precision × recall
precision + recall
6
s.t.
precision(ca, ˆca) = TP
TP + FP
recall(ca, ˆca) = TP
TP + FN,
where TP, FP and FN are the number of true positives, false
positives and false negatives, respectively.
Deﬁnition 1. The arg maxρ · function returns the minimum
value of the ρ that maximizes the proceeding function ·.
As shown in Fig. 2, we select the threshold vector τ
to threshold the model scores by maximizing the MacroF1
function on the validation set as:
τ = arg max
τ
MacroF1(δ( ˆca ≥τa),ca), (5)
where δ(·) function returns the same sized vector with its in-
put, which outputs 1 for the dimensions that satisfy inequality
and 0 for the rest. Directly optimizing (5) via grid search
becomes infeasible as the number of classes increases and it
may not be possible to ﬁnd the optimal value since the time
complexity is in Θ(Tw),2 whereT is the number of elements
to be tried and w is the number of classes. Thus, we introduce
the following lemma:
Lemma 1. τ is equivalent to
[τ1 τ2 ... τ w
]T
such that
τa = arg max
τa
F1(δ( ˆca ≥τa),ca), (6)
for all a ∈ {1, 2,...,w }.
Proof of Lemma 1: We prove the lemma by deriving (6)
from (5). Initially, we have
τ = arg max
τ
MacroF1(δ( ˆca ≥τa),ca)
= arg max
τ
1
w
w∑
a=1
F1(δ( ˆca ≥τa),ca).
Since the class speciﬁc thresholds in τ are independent, we
separate the thresholds into different arg max functions as:
τa = arg max
τa
F1(δ( ˆca ≥τa),ca).
This concludes the proof of Lemma 1.
Using Lemma 1, the time complexity becomes linear w.r.t.
the number of classes, i.e., Θ(Tw ). Thus, we calculate the
threshold vector τ using (6).
Remark 8. Notice that it is not reasonable to choose threshold
using the training set since the model already memorizes it and
unavoidably performs biased scoring for the training data. This
is why we use the unseen thresholding set.
IV. E XPERIMENTS
In this section, we ﬁrst describe the datasets, the evaluation
methodology and the implementation details. We then compare
2Θ(w(n)) denotes the set of all r(n), where a1w(n)≤ r(n)≤ a2w(n),
∀n > n 0 for n∈ Z+ such that there exist positive integers a1, a2, and n0.
our method with the ﬁrst ranking methods in the SemEval
emotion classiﬁcation competition [1] and the state-of-the-art
methods. We then analyze the performance of our method via
cross-lingual experiments. Later, we demonstrate performance
gains obtained via our dynamic weighting method and analyze
its hyperparameter. Finally, we present the individual class
performances of our method and demonstrate the performance
gains obtained by the components of our method via an
ablation study.
A. Datasets
2 4 6 8 10
Label Rank
0
500
1000
1500
2000
2500Label Frequency
Disgust Anger
Joy
Sadness
Optimism
Fear
Anticipation
Pessimism
Love
Surprise Trust
Anger
Sadness
Joy
Love
Optimism
Pessimism
Disgust Fear
Anticipation
Trust Surprise
Anger
Joy
Sadness
Pessimism
Disgust
Anticipation
Optimism Fear Love Trust Surprise
English
Arabic
Spanish
Fig. 3: Number of label occurrences vs. rank plot of the labels
in datasets that demonstrate the class imbalance.
We use datasets in three different languages from the
SemEval competition [1]: SemEval-Arabic, SemEval-English
and SemEval-Spanish. For simplicity, we refer SemEval-
Arabic, SemEval-English and SemEval-Spanish datasets as
Arabic, English and Spanish, respectively. Since the datasets
are in multi-label setting, the instances contain zero or more
labels among the 11 labels in the dataset. Fig. 3 demonstrates
the class imbalance via the number of occurrence vs. rank plot
of the labels in the datasets. We use the splits of the SemEval
emotion classiﬁcation competition [1]. Arabic dataset has a
total of 4,381 instances consisting of 160,206 tokens and split
into 3,561 training, 679 validation and 2,854 test instances.
The English dataset has 10,983 instances consisting of 338,763
tokens and split into 6,838 training, 886 validation and 3,259
test instances. The Spanish dataset has 7,094 instances con-
sisting of 176,650 tokens and split into 2,278 training, 585
validation and 1,518 test instances.
B. Evaluation Methodology and Implementation Details
We use macro averaged F1 (macro-f1), micro averaged F1
(micro-f1) and jaccard index, which are the metrics used in
the SemEval competition [1]. For fairness, we optimize our
network and the Deepmoji [9] baseline by using Tree Parzen
Estimator of the Optuna library [34] and choose the model
with the largest validation macro-f1 score among 100 trials.
For the FastText [30] baseline, we use its own hyperparameter
optimization module with 130 different trials for each of
7
Arabic English Spanish
Method Macro-F1 Micro-F1 Jaccard Macro-F1 Micro-F1 Jaccard Macro-F1 Micro-F1 Jaccard
Ours 55.0 66.1 53.4 58.4 69.6 57.6 53.0 60.6 48.6
Ours-SL 51.3 57.5 44.3 56.4 68.7 56.5 50.5 56.6 45.3
Tw-StAR [22] 44.6 59.7 46.5 45.2 60.7 48.1 39.2 52.0 43.8
FastText [30] 35.3 40.2 25.5 35.0 39.9 25.5 27.0 31.9 20.6
CA-GRU [31] 49.5 64.8 53.2 - - - - - -
HEF-DF [32] 50.2 63.1 51.2 - - - - - -
EMA [18] 46.1 61.8 48.9 - - - - - -
PARTNA 47.5 60.8 48.4 - - - - - -
NTUA-SLP [19] - - - 52.8 70.1 58.8 - - -
psyML [20] - - - 57.4 69.7 57.4 - - -
NVIDIA [10] - - - 56.1 69.0 57.7 - - -
DeepMoji [9] - - - 55.9 65.7 52.8 - - -
ELiRF-UPV [33] - - - - - - 44.0 53.5 45.8
MILAB SNU - - - - - - 40.7 55.8 46.9
TABLE I: Comparison of our method with the state-of-the-art methods in the literature and the winners in SemEval-2018
emotion classiﬁcation competition [1] with the introduced method. The previously reported state-of-the-art results are underlined.
The current state-of-the-art results are boldfaced.
the languages, i.e., 30 more trials than our optimization for
our model and the Deepmoji baseline. The methods in the
SemEval emotion classiﬁcation competition have also fol-
lowed similar approaches, e.g., EMA [18] performs a grid
search, NVIDIA [10] and NTUA-SLP [19] employ Bayesian
optimization in dimensional space of all the possible values.
We train our model via the Adam [35] optimizer. We
use ekphrasis 3 preprocessing library to perform language-
independent preprocessing of social cues such as username
normalization. We use weight decay and early stopping. We
stop the training until 10 epochs are exceeded without any
validation F1-Macro improvements.
C. Comparison with the State-of-the-Art
Here, we compare our model with the state-of-the-art meth-
ods and the best models in SemEval-2018 competition in
Arabic, English and Spanish languages.
To create our best model, we combine the Arabic, English
and Spanish data by combining their training and validation
sets. We then train our model on the combined data using the
methodology described in Section IV-B.
We use 12 different baselines to compare our method and
demonstrate its effectiveness, most of which are the highest
performing contenders in SemEval-2018 emotion classiﬁcation
competition. NTUA-SLP [19] ranked 1st on jaccard and micro-
f1 metrics for English by using a pretrained Bi-LSTM with
a multi-layer self-attention mechanism. They use word2vec
embeddings that are trained on 550 million tweets. The best
micro-f1 score for English is achieved by psyML [20], which
uses a very similar Bi-LSTM with self-attention model to
NTUA-SLP, except they utilize hierarchical clustering to group
correlated emotions together and train the same model incre-
mentally for emotions within the same cluster. NVIDIA [10]
3https://github.com/cbaziotis/ekphrasis/tree/master/ekphrasis
trains an attention-based transformer network on large scale
data and ﬁnetune this model on the training set for SemEval-
English before testing it, obtaining results on par with those
in the competition ranking. DeepMoji is a distant supervision
based LSTM architecture and it obtains the state-of-the-art
performance on many sentiment related tasks [9]. They convert
multi-label instances into seperate binary tasks. We report the
results of their chain-thaw approach on the English dataset.
For Arabic, EMA [18] (1st place in jaccard and micro-f1,
2nd place in macro-f1) and PARTNA (1st place in macro-
f1, 2nd place in jaccard and micro-f1) achieves the highest
two ranks. EMA employs AraVec embeddings [21] as features
into a support vector classiﬁer (SVC) with L1 regularization.
PARTNA uses a similar support vector based model except
using an additional Arabic stemmer designed for handling
tweets [1]. There are also studies that perform well but are
not in SemEval rankings. Among these, CA-GRU [31] uses
context information, the topic of the text in this case, as a
feature by ﬁrst feeding the text to a topic-detection model to
obtain a vector of probability distributions over topics. HEF-
DF [32] is a simple neural network hybrid model obtained
from concatenating human engineered (i.e. handpicking fea-
tures that represent syntactical and semantical signiﬁcance)
and deep features (i.e. using combinations of embeddings).
As with Arabic, two models exist for the 1st place in a
metric for Spanish: MILAB SNU (1st place in jaccard and
micro-f1, 2nd place in macro-f1) and ELiRF-UPV, which uses
manually and automatically generated lexicon sand combines
1D CNNs with an LSTM to obtain the 1st place in macro-
f1 metric [33] (2nd place in jaccard and micro-f1). We also
include Tw-StAR [22] as a baseline to compare our method’s
multilingual performance with a standard model. Tw-StAR
uses binary relevance transformation strategy to extract term
frequency-inverse document frequency (tf-idf) features for a
linear support vector machine. They also experiment with
8
combinations of 5 different preprocessing methods and reach
the 3rd rank for both Arabic and Spanish datasets. FastText is
a framework that can convert text into feature vectors by using
a skipgram model, where each word is represented as a bag of
n-grams [30]. FastText contains readily extracted vectors for
157 languages. We ﬁnetune these vectors for English, Arabic
and Spanish and use these vectors on their respective SemEval
datasets.
Table I presents the results of our model compared to
the state-of-the-art models and the competition-winners. The
models that target only a single language perform signiﬁ-
cantly better compared to the multilingual models. The only
exception is our model that is trained on three different
language’s training data combined, which obtains signiﬁcantly
better results compared to our single language ( Ours-SL)
model with the same methodology and trained on each of
these languages separately. Our method achieves the best
score on all of the metrics in Arabic and Spanish languages.
Our method achieves the best score in macro-f1 metric of
the English language. In Arabic, our method achieves 4.8%
(absolute) macro-f1 improvement compared to the previous
best model on macro-f1 score, which is HEF-DF [32]. Our
method obtains 2.3% (absolute) micro-f1 and 0.2% (absolute)
jaccard score improvement compared to the previous best
model CA-GRU [31]. In English, our method achieves 1%
(absolute) macro-f1 improvement compared to the previous
competition winner psyML [20]. Our method performs 0.5%
(absolute) micro-f1 and 1.2% (absolute) jaccard score com-
pared to the competition winner NTUA-SLP [19]. Note that
although NTUA-SLP achieves the best score on micro-f1 and
jaccard metrics, it performs 5.6% (absolute) macro-f1 less than
our method. In Spanish, our method achieves 9.0% (absolute)
macro-f1 improvement compared to the previous best model
ELiRF-UPV [33]. Our method also achieves 4.8% (absolute)
micro-f1 and 1.7% (absolute) jaccard score improvement com-
pared to the previous best model MILAB SNU.
D. Cross-Lingual Experiments
In this section, we demonstrate the cross-lingual capability
of our method using training and test data combinations of
different languages.
Table II presents the results when a model is trained on
combinations of the datasets of different languages from the
SemEval competition [1]. For each row, we train the model
using the combined training data of the languages in the ﬁrst
column and validate using the combined validation data. We
then experiment on the test sets of the English (EN), Spanish
(SP) and Arabic (AR) languages, separately. Note that the
threshold and the best model is selected using the validation
set of the combined data using the procedure we describe in
Section IV-B. Recall that we use only a single model, which
is the model shown at the last row (AR + EN + SP) in the
comparisons with the state-of-the-art in Section IV-C.
The models trained on a single language perform the best
on the training data’s language, as expected. For instance, the
model trained on English performs the best for the English
test data. This is due to the semantic differences and the
Validation Data
Training Data Arabic English Spanish
Arabic (SP) 52.7 39.6 30.7
English (EN) 37.9 60.1 36.2
Spanish (SP) 35.2 46.4 52.3
AR + EN 52.5 61.1 39.6
AR + SP 57.9 47.5 52.7
EN + SP 44.9 60.5 53.9
EN + AR + SP 55.3 61.7 52.6
TABLE II: Experiment results when the model is trained on
the combinations of the SemEval datasets and tested on the
individual validation sets. The best results are boldfaced.
implicit biases in each dataset. The results clearly indicate
that training with data from different languages signiﬁcantly
improves the performance of our model. For English test data,
including Arabic to the English training data improves the
model more than including Spanish. For Arabic test data,
including Spanish to the Arabic training data improves the
model more than including English. For Arabic test data,
using Arabic and Spanish training data combined performs
the best. For English test data, using data from all of the
three languages performs the best. For Spanish, including
English data to Spanish training data improves the model more
than including Arabic. For Spanish test data, using English
and Spanish training data combined performs the best and
including Arabic to this data lowers the performance.
Our cross-lingual experimental results are consistent for the
models that are trained on single language datasets with the
semantic similarity atlas of the languages [36]. For example,
English and Spanish are signiﬁcantly more similar to each
other than to the Arabic language. Among the models that
are trained on a single language, English and Spanish training
datasets score the best for each other’s test data compared
to the Arabic. For English test data, Spanish training data
scores 7.0% (absolute) macro-f1 more than the Arabic. For
Spanish test data, the model trained on the English training
data scores 5.5% (absolute) macro-f1 more than the Arabic.
For Arabic, which is closer to English than the Spanish in
the similarity atlas [36], training with English data results in
2.7% (absolute) macro-f1 gain compared to training with the
Spanish. Notice that the models perform promising even for
the unseen languages, e.g., the model that is trained on English
and Spanish data and tested on the unseen Arabic validation
data perform with 3% to 11% (absolute) less macro-f1 score
compared to the baselines and our best model trained on all
of the three languages. For the model tested on the English
data, which trained on the rest of the languages, perform 2%
(absolute) macro-f1 better than the Tw-StAR baseline and
10.9% (absolute) macro-f1 worse compared to the best English
model trained on all of three languages. For the model tested
on the Spanish validation data, which trained on the rest of
the languages, the model performs 0.4% (absolute) macro-f1
better than the Tw-StAR baseline and 13.4% (absolute) macro-
f1 worse than our best model that is trained on all of the three
9
0.0 0.2 0.4 0.6 0.8 1.0
Smoothing Coeﬃcient κ
56
58
60
62
64Validation Macro-F1 Score
Dynamic
Uniform
Inverse
Cost-Sensitive
Class-Balanced
(a) Only English data
0.0 0.2 0.4 0.6 0.8 1.0
Smoothing Coeﬃcient κ
56
58
60
62
64Validation Macro-F1 Score
Dynamic
Uniform
Inverse
Cost-Sensitive
Class-Balanced (b) Combined Arabic, English and Spanish data
Fig. 4: Comparison of the weighting methods for imbalanced classiﬁcation on the data from the SemEval emotion classiﬁcation
competition [1]. Figure is best viewed in color.
languages. Note that these cross-lingual scores are obtained on
the unseen validation sets of the datasets to prevent the test
leak, unlike the baselines, where they are tested on the test
set.
E. Inﬂuence of Dynamic Weighting
Here, we analyze the hyperparameter selection of our dy-
namic weighting method and compare it with the existing
weighting methods that are proposed to remedy the class
imbalance.
Fig. 4 illustrates the comparison of different weighting
methods in the literature and our dynamic weighting method.
We use the parameters of the best model except κ, which
is the smoothing hyperparameter for dynamic weighting. For
dynamic weighting method, we experiment with different κ ∈
[0, 1] with 0.1 spacing. For class-balanced focal loss term, we
additionally experimented with the β ∈ {0.99, 0.999, 0.9999}
values as in [13]. Note that β is deﬁned for[0, 1), thus, we did
not experiment for β = 1. We show the β term of the class-
balanced focal loss via the x-axis of Fig. 4, too, which controls
the growth rate of the weight with respect to the number of
instances belonging to each class. We experiment with uniform
weighting that assign equal importance to the losses from each
class, i.e., αt,a = 1
w, ∀t ∈ { 1, 2,... },a ∈ { 1, 2,...w }. We
also compare with the inverse loss, which is the inverse of
the number of instances belonging to each class. Lastly, we
compare with the cost-sensitive loss [14].
Our dynamic weighting method demonstrates signiﬁcant
performance improvement, i.e., ≈2.5% (absolute) macro-f1
improvement compared to the uniform weighting and more
improvements compared to the other methods on the only En-
glish data. The only exception is the class balanced weighting,
for which our method achieves ≈1.2% (absolute) macro-f1 im-
provement compared to the best of the class-balanced weigth-
ing when β = 0.999. On the combined data, the dynamic
weighting achieves 1.3% macro-f1 improvement whenκ = 0.4
compared to the uniform weighting and more improvements
compared to the other methods. The only exception is the
class balanced weighting, for which our method achieves 0.6%
(absolute) macro-f1 improvement when β = 0.99.
Although there exist ﬂuctuations w.r.t. κ hyperparameter,
it performs no worse than the default uniform weighting for
any of the κ values for both only English and combined
Arabic, English and Spanish data. Notice that when κ = 0 ,
the dynamic weighting method is equivalent to the uniform
weighting since the φ parameter is never updated. Our method
achieves its best value at κ = 0.4 for both datasets.
F . Individual Class Performances
In this section, we analyze the performance of our method
for individual classes.
anger
anticipation
disgust
fear joy love
optimismpessimism
sadnesssurprise
trust
Class
20
30
40
50
60
70
80
90
100Validation F1 Score
Fig. 5: Per-class F1 scores of the validation set of the combined
Arabic, English and Spanish data. Figure is best viewed in
color.
Fig. 5 illustrates the validation F1 score for all classes on
the combined data using the best model on combined data
10
obtained in Section IV-C. The model performs the best for
the joy class with 80.9% macro-f1 and performs the worst
for the trust class with 25.0% macro-f1. The surprise and
the trust classes perform the worst among all as expected
since their number of instances is the least. Discrimination
of the optimism is signiﬁcantly better than the pessimism as
the number of instances in the optimism class is signiﬁcantly
higher than the number of instances in the pessimism class.
Interestingly, the anticipation class is the third worst per-
forming class although it is not the third in terms of rarity,
which is consistent with the results of the NVIDIA study [10].
Our model performs around 70% for the rest of the classes,
i.e., anger, disgust, fear, joy, love, optimism and sadness.
In the following section, we demonstrate the performance
improvements obtained by the components in our method.
G. Ablation Study
Here, we perform an ablation study to assess the perfor-
mance gains obtained by the components in our method.
We experiment with recurrent neural networks (RNN), gated
recurrent unit (GRU), standard cross entropy loss and the
XML-CNN model that is proposed for the extreme multi-label
classiﬁcation tasks with more than thousand labels.
Network Validation Macro-F1
Bidirectional LSTM 59.4
Bidirectional LSTM \w CE 57.1
Unidirectional LSTM 57.1
Bidirectional RNN 56.4
Bidirectional GRU 57.7
XML-CNN [37] 47.8
TABLE III: Ablation study of different network architectures
and losses on the validation set of the combined Arabic,
English and Spanish data. ” \w CE” stands for ”with cross
entropy loss”.
Table III presents the results on the validation set of the
combined Arabic, English and Spanish data when the recurrent
component is changed with other models and the loss changed
with the standard cross entropy loss. For each row, we only
change loss or model. We keep all other hyperparameters as is.
Among all, the bidirectional LSTM with focal loss performs
signiﬁcantly better compared to others. Focal loss improves
the model by 2.3% (absolute) macro-f1 on the validation set.
Unidirectional LSTM, which runs on the sentences only in
the forward direction, performs 2.3% worse compared to its
bidirectional variant. Although the GRU works better than the
RNN, it performs 1.7% worse compared to the bidirectional
LSTM. XML-CNN, which is a CNN based model, performs
signiﬁcantly worse compared to the other variants.
V. C ONCLUSION
We have investigated the cross-lingual sentiment analysis in
multi-label setting. We have introduced a system that performs
sentiment analysis in 100 different languages. To cope with the
inherent class imbalance problem of multi-label classiﬁcation,
we have introduced a dynamic weighting method to remedy
the inherent class imbalance problem of multi-label classiﬁ-
cation, which balances the loss contribution of the classes as
the training progresses, unlike the static weighting methods
that assign non-changing weights to the classes. We have
adapted the focal loss to the multi-label setting from the single-
label object recognition literature. Moreover, we have derived
a macro-f1 maximization method in linear time complexity
for choosing class-speciﬁc thresholds to produce predictions.
Our system has achieved the state-of-the-art performance in
7 out of 9 metrics in 3 different languages on the SemEval
emotion classiﬁcation competition [1]. We have demonstrated
the performance gains compared to the ﬁrst ranking methods
in the SemEval emotion classiﬁcation competition [1] and the
common baselines. We have also evaluated our method in the
cross-lingual setting. We have demonstrated the performance
gains obtained by the dynamic weighting and analyzed the
effects of the components of our method through an ablation
study.
REFERENCES
[1] S. M. Mohammad, F. Bravo-Marquez, M. Salameh, and S. Kiritchenko,
“Semeval-2018 task 1: Affect in tweets,” in Proceedings of International
Workshop on Semantic Evaluation (Semeval-2018) , New Orleans, LA,
USA, 2018.
[2] L. Zhu, W. Li, Y . Shi, and K. Guo, “Sentivec: Learning sentiment-
context vector via kernel optimization function for sentiment analysis,”
IEEE Transactions on Neural Networks and Learning Systems , 2020.
[3] B. Liu, “Sentiment analysis and opinion mining,” Synthesis Lectures on
Human Language Technologies, vol. 5, no. 1, 2012.
[4] D. Wang, B. Jing, C. Lu, J. Wu, G. Liu, C. Du, and F. Zhuang, “Coarse
alignment of topic and sentiment: A uniﬁed model for cross-lingual
sentiment classiﬁcation,” IEEE Transactions on Neural Networks and
Learning Systems, 2020.
[5] R. Plutchik, “A general psychoevolutionary theory of emotion,” in
Theories of Emotion . Elsevier, 1980.
[6] D. Xu, Y . Shi, I. W. Tsang, Y .-S. Ong, C. Gong, and X. Shen, “Survey
on multi-output learning,” IEEE Transactions on Neural Networks and
Learning Systems, 2019.
[7] T. Wei and Y .-F. Li, “Does tail label help for large-scale multi-
label learning?” IEEE Transactions on Neural Networks and Learning
Systems, 2019.
[8] Y . LeCun, Y . Bengio, and G. Hinton, “Deep learning,” Nature, vol. 521,
no. 7553, 2015.
[9] B. Felbo, A. Mislove, A. Søgaard, I. Rahwan, and S. Lehmann, “Using
millions of emoji occurrences to learn any-domain representations for
detecting sentiment, emotion and sarcasm,” in Conference on Empirical
Methods in Natural Language Processing (EMNLP) , 2017.
[10] N. Kant, R. Puri, N. Yakovenko, and B. Catanzaro, “Practical text
classiﬁcation with large pre-trained language models,” arXiv preprint
arXiv:1812.01207, 2018.
[11] J. Suttles and N. Ide, “Distant supervision for emotion classiﬁcation with
discrete binary values,” in International Conference on Intelligent Text
Processing and Computational Linguistics . Springer, 2013.
[12] C. Huang, Y . Li, C. Change Loy, and X. Tang, “Learning deep rep-
resentation for imbalanced classiﬁcation,” in Proceedings of the IEEE
Conference on Computer Vision and Pattern Recognition , 2016.
[13] Y . Cui, M. Jia, T.-Y . Lin, Y . Song, and S. Belongie, “Class-balanced
loss based on effective number of samples,” in Proceedings of the IEEE
Conference on Computer Vision and Pattern Recognition , 2019.
[14] Y . S. Aurelio, G. M. de Almeida, C. L. de Castro, and A. P. Braga,
“Learning from imbalanced data sets with weighted cross-entropy func-
tion,” Neural Processing Letters , vol. 50, no. 2, 2019.
[15] T.-Y . Lin, P. Goyal, R. Girshick, K. He, and P. Doll ´ar, “Focal loss
for dense object detection,” in Proceedings of the IEEE International
Conference on Computer Vision , 2017.
[16] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “Bert: Pre-training
of deep bidirectional transformers for language understanding,” arXiv
preprint arXiv:1810.04805, 2018.
11
[17] A. Conneau, K. Khandelwal, N. Goyal, V . Chaudhary, G. Wenzek,
F. Guzm´an, E. Grave, M. Ott, L. Zettlemoyer, and V . Stoyanov, “Unsu-
pervised cross-lingual representation learning at scale,” arXiv preprint
arXiv:1911.02116, 2019.
[18] G. Badaro, O. El Jundi, A. Khaddaj, A. Maarouf, R. Kain, H. Hajj,
and W. El-Hajj, “Ema at semeval-2018 task 1: Emotion mining for
arabic,” in Proceedings of The 12th International Workshop on Semantic
Evaluation, 2018.
[19] C. Baziotis, N. Athanasiou, A. Chronopoulou, A. Kolovou,
G. Paraskevopoulos, N. Ellinas, S. Narayanan, and A. Potamianos,
“Ntua-slp at semeval-2018 task 1: Predicting affective content in
tweets with deep attentive rnns and transfer learning,” arXiv preprint
arXiv:1804.06658, 2018.
[20] G. Gee and E. Wang, “Psyml at semeval-2018 task 1: Transfer learn-
ing for sentiment and emotion analysis,” in Proceedings of The 12th
International Workshop on Semantic Evaluation , 2018.
[21] A. B. Mohammad, K. Eissa, and S. El-Beltagy, “Aravec: A set of arabic
word embedding models for use in arabic nlp,” Procedia Computer
Science, vol. 117, Nov 2017.
[22] H. Mulki, C. B. Ali, H. Haddad, and I. Babao ˘glu, “Tw-star at semeval-
2018 task 1: Preprocessing impact on multi-label emotion classiﬁcation,”
in Proceedings of the 12th International Workshop on Semantic Evalu-
ation, 2018.
[23] R. Collobert, J. Weston, L. Bottou, M. Karlen, K. Kavukcuoglu, and
P. Kuksa, “Natural language processing (almost) from scratch,” Journal
of Machine Learning Research , vol. 12, Aug 2011.
[24] T. Mikolov, I. Sutskever, K. Chen, G. S. Corrado, and J. Dean,
“Nistributed representations of words and phrases and their composi-
tionality,” in Advances in Neural Information Processing Systems , 2013.
[25] T. Kudo and J. Richardson, “Sentencepiece: A simple and language inde-
pendent subword tokenizer and detokenizer for neural text processing,”
arXiv preprint arXiv:1808.06226 , 2018.
[26] J. L. Elman, “Finding structure in time,” Cognitive Science , vol. 14,
no. 2, 1990.
[27] S. Hochreiter and J. Schmidhuber, “Long short-term memory,” Neural
Computation, vol. 9, no. 8, 1997.
[28] Z. Yang, D. Yang, C. Dyer, X. He, A. Smola, and E. Hovy, “Hierarchical
attention networks for document classiﬁcation,” in Proceedings of the
2016 Conference of the North American Chapter of the Association for
Computational Linguistics: Human Language Technologies , 2016.
[29] B. Harwood, V . Kumar BG, G. Carneiro, I. Reid, and T. Drummond,
“Smart mining for deep metric learning,” in Proceedings of the IEEE
International Conference on Computer Vision , 2017.
[30] P. Bojanowski, E. Grave, A. Joulin, and T. Mikolov, “Enriching word
vectors with subword information,” arXiv preprint arXiv:1607.04606 ,
2016.
[31] A. E. Samy, S. R. El-Beltagy, and E. Hassanien, “A context integrated
model for multi-label emotion detection,” Procedia Computer Science ,
vol. 142, 2018.
[32] N. Alswaidan and M. E. B. Menai, “Hybrid feature model for emotion
recognition in arabic text,” IEEE Access, vol. 8, 2020.
[33] J.- ´A. Gonz ´alez, L.-F. Hurtado, and F. Pla, “Elirf-upv at irosva: Trans-
former encoders for spanish irony detection,” in IberLEF@ SEPLN ,
2019.
[34] T. Akiba, S. Sano, T. Yanase, T. Ohta, and M. Koyama, “Optuna: A next-
generation hyperparameter optimization framework,” in Proceedings
of the 25th ACM SIGKDD International Conference on Knowledge
Discovery & Data Mining , 2019.
[35] D. P. Kingma and J. Ba, “Adam: A method for stochastic optimization,”
arXiv preprint arXiv:1412.6980 , 2014.
[36] L. K. Senel, ˙I. Utlu, V . Y ¨ucesoy, A. Koc, and T. Cukur, “Generating
semantic similarity atlas for natural languages,” in 2018 IEEE Spoken
Language Technology Workshop (SLT) . IEEE, 2018.
[37] J. Liu, W.-C. Chang, Y . Wu, and Y . Yang, “Deep learning for extreme
multi-label text classiﬁcation,” in Proceedings of the 40th International
ACM SIGIR Conference on Research and Development in Information
Retrieval, 2017.
