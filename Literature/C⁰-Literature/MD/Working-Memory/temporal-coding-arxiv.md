# temporal-coding-arxiv

THE COST OF TRAINING NLP M ODELS
A CONCISE OVERVIEW
Or Sharir
AI21 Labs
ors@ai21.com
Barak Peleg
AI21 Labs
barakp@ai21.com
Y oav Shoham
AI21 Labs
yoavs@ai21.com
April 2020
ABSTRACT
We review the cost of training large-scale language models, and the drivers of these costs. The
intended audience includes engineers and scientists budgeting their model-training experiments, as
well as non-practitioners trying to make sense of the economics of modern-day Natural Language
Processing (NLP).1
1 Costs: Not for the faint hearted
The cost of ﬂoating-point operations (FLOPs), the basic Neural Network (NN) operation, has been decreasing. For
example, Google reported [1] a 38% cost decrease in ResNet-50 training costs 2. This was achieved with optimized
hardware (moving from GPUs to TPUs) coupled with framework-level optimizations, exploiting parallelism opportu-
nities. This kind of cost reduction isn’t an isolated occurrence – we’re seeing the costs of training large models fall
as hardware innovations and training techniques improve. Despite this, overall costs have increased, and can run into
the millions. We’ll explain why this is occurring and what factors play a signiﬁcant role in the costs of training 3 NLP
models.
Just how much does it cost to train a model? Two correct answers are “depends” and “a lot”. More quantitatively,
here are current ballpark list-price costs of training differently sized BERT [4] models on the Wikipedia and Book
corpora (15 GB). For each setting we report two numbers - the cost of one training run, and a typical fully-loaded cost
(see discussion of "hidden costs" below) with hyper-parameter tuning and multiple runs per setting (here we look at a
somewhat modest upper bound of two conﬁgurations and ten runs per conﬁguration).4
• $2.5k - $50k (110 million parameter model)
• $10k - $200k (340 million parameter model)
• $80k - $1.6m (1.5 billion parameter model)
These already are signiﬁcant ﬁgures, but what they imply about the cost of training the largest models of today is
even more sobering. Exact ﬁgures are proprietary information of the speciﬁc companies, but one can make educated
1We thank Barak Lenz, Shai Shalev-Shwartz and other members of AI21 Labs, as well as Jack Clark, Jeff Dean, Deep Ganguli,
Chris Re, Sebastian Ruder and Lior Wolf, who generously commented on previous drafts. Further comments on the document are
welcome, and the document will be updated as appropriate. Note: While the comments of our colleagues from other organizations
greatly improved the document, they were not representing their organizations, did not share any proprietary information, and may
not necessarily agree with everything written here.
2It also reported a dramatic 27 × decrease in training time. While training time is not our focus, it is relevant indirectly:
Compressed time makes it realistic to train larger models, which costs more.
3There is a whole other discussion to be had on the costs of NLP models at inference time. These are quite related to the training
costs, but deserve a separate discussion. In particular, the inference phase allows for post-training model optimizations, for example
via model distillation [2, 3]. This discussion is beyond the scope of this article.
4The following ﬁgures are based on internal AI21 Labs data. They can be somewhat lower due to discounts, or using preemptible
versions of the system. The ﬁgures also assume the use of cloud solutions such as GCP or AWS, and on-premise implementations
are sometimes cheaper. Still, the ﬁgures provide a general sense of the costs.
arXiv:2004.08900v1  [cs.CL]  19 Apr 2020
The Cost of Training NLP Models: A Concise Overview
guesses. For example, based on information released by Google, we estimate that, at list-price, training the 11B-
parameter variant5 of T5 [5] cost well above $1.3 million for a single run. Assuming 2-3 runs of the large model and
hundreds of the small ones, the (list-)price tag for the entire project may have been $10 million6.
Not many companies – certainly not many startups – can afford this cost. Some argue that this is not a severe issue; let
the Googles of the world pre-train and publish the large language models, and let the rest of the world ﬁne-tune them
(a much cheaper endeavor) to speciﬁc tasks. Others (e.g., Etchemendy and Li [6]) are not as sanguine.
2 Cost Drivers: Size Matters
We are not aware of a formula that tells you how many FLOPs are needed in a given NLP setting to achieve a given
performance7. However, there are several variables that impact this number, all of which have increased dramatically
in the past few years, far surpassing the once-deemed “massive” vision-focused ML models.8
Here are some of the relevant variables, which fall into three categories: (a) size of dataset, (b) model size (we use
the number of parameters as a proxy), and (c) training volume (we use as proxy the total number of tokens processed
during pre-training). The top row applies to all models, and the bottom row zooms in on transformer-based models.
Zoom-in on Transformer-speciﬁc Attributes
Layers
0
20
40
60
80
GPT
BERT-Large
GPT2-1.5B
RoBERTa
XLNet
ELECTRA-1.75M
MegatronLM
T5-11B
Turing-NLG
78
48
72
24
24
24
48
24
12
Attention Heads
0
35
70
105
140
GPT
BERT-Large
GPT2-1.5B
RoBERTa
XLNet
ELECTRA-1.75M
MegatronLM
T5-11B
Turing-NLG
28
128
32
16
16
16
12
16
12
Contextual-Embedding 
Dimension
0K
1K
3K
4K
5K
GPT
BERT-Large
GPT2-1.5B
RoBERTa
XLNet
ELECTRA-1.75M
MegatronLM
T5-11B
Turing-NLG
4256
1024
3072
1024
1024
1024
1600
1024
768
Feed-Forward Dimension
0K
18K
36K
54K
72K
GPT
BERT-Large
GPT2-1.5B
RoBERTa
XLNet
ELECTRA-1.75M
MegatronLM
T5-11B
Turing-NLG
17K
66K
12K
4K
4K
4K
6K
4K
3K
credit:
Bird’s-eye View
Data Size
(billion words)
0
10
20
30
40
WSJ
Wikipedia
OpenWebText
C4
35
8.5
2.5
0.03
Model Size
(billion parameters)
0
5
10
15
20
GPT
BERT-Large
GPT2-1.5B
RoBERTa
XLNet
ELECTRA-1.75M
MegatronLM
T5-11B
Turing-NLG
17.0
11.0
8.3
0.3
0.4
0.4
1.5
0.3
0.1
Training Volume
(trillion tokens)
0
0.6
1.2
1.8
2.4
GPT
BERT-Large
GPT2-1.5B
RoBERTa
XLNet
ELECTRA-1.75M
MegatronLM
T5-11B
Turing-NLG
0.2
1
0.2
1.8
2.1
2.1
0.5
0.1
.03
In NLP ,
Everything is Big
and Getting
Bigger
† The total number of tokens processed during pre-training. This is the product of three different attributes affecting total FLOPs cost of training (beyond the 
cost attributed to model size): input sequence length, training steps, and batch size.
†
5 With context lengths of 512 for both encoding and decoding, 128 attention heads, and 65k-dimensional feed-forward layers.
6These $ ﬁgures come with substantial error bars, but we believe they are in the right ballpark.
7 It is worth noting the work of [7], which analyzes the impact of various variables, including model size and amount of compute,
on performance, as measured by perplexity. Although the paper does not directly address the question we are after, the methodology
it offers may provide useful hints. Other relevant papers include [8, 9, 10].
8Although computer vision is not our focus here, the contrast with NLP is striking, and we discuss it brieﬂy in Appendix A.
2
The Cost of Training NLP Models: A Concise Overview
The exact ways in which these increases impact the number of FLOPs are subtle, and depend on the speciﬁc training
scheme and architecture. For example, fewer FLOPs are needed when training BERT-style models versus GPT-2 [11]
models with comparable model and data sizes, and training steps. Other training schemes can introduce additional
factors that dictate cost; for example, the adversarial training scheme of ELECTRA [12] uses an additional “generator”
model during training. This increases the relative per-step costs, but requires fewer steps, thus reducing the overall
costs. Despite these subtleties, however, it is clear that all these growing numbers correlate with an overall trend
towards a greater number of FLOPs, which determine the bottom line.
On top of the above, there are also additional hidden costs, which are often overlooked. Each model must be trained
multiple times – this is in order to minimize random effects (each run is inherently stochastic), and to search over a
combinatorially large hyper-parameter search space. This means there can be a large multiple over the cost of a single
training episode (although signiﬁcant cost savings can be had by conducting most of the experiments on the smaller
models ﬁrst, before training the large models in the optimized conﬁguration).
3 The Future
The reason the community has adopted the mega-scale, brute-force statistical approach is that it works; it has yielded
better performance than any alternative. And since NLP has substantial economic value, no cost is too high in pursuit
of good performance. We do not see an end to the use of large NN models operating on massive corpora, and one
can imagine the costs escalating further, as the community develops more elaborate architectures in pursuit of more
ambitious tasks. As you go from sentences to whole documents and beyond, you can imagine the need for more
dimensions per token, longer contexts, and potentially more layers. Adding external knowledge sources, although
potentially reducing the sole reliance on the network (see below), could also contribute to expanding the size of the
network in order to reﬂect the external knowledge in the embedding space. Indeed, there is already discussion [13] of
100B-parameter models. That said, we see several factors that may help tame this explosion and prevent things from
getting out of hand. In increasing order of importance:
• Further reduction of raw-compute prices due to increased competition. According to this (admittedly self-
interested) blog post [14], the prices on AWS were reduced over 65 times since its launch in 2006, and by as
much as 73% between 2014 and 2017. We expect the same trend for AI-oriented compute offerings.
• More efﬁcient NN architectures, driven in part by economics and partly by environmental considerations. For
example, the Reformer [15] architecture uses heuristics to reduce the complexity of the attention mechanism
of transformers from quadratic to O(n log n). Similarly, ALBERT [16] achieves better accuracy with fewer
parameters by factorizing the embedding matrix and weight sharing across layers. We expect to see more of
this.
• Ending the State-of-the-Art (SOTA) race. There is increasing recognition in the community that signiﬁcant
amount of compute is sunk into reaching the top of leaderboards of the many challenge datasets, often in-
volving many (in some reported cases, thousands) of runs, just so that one instance will luck into ﬁrst place.
Such overﬁtting is of course of little value, and we expect to see less of it.
• Maxing out on useful data. There is just that much (useful) text that has been written, or that will be. At some
point, we will have trained on Borges’ Universal Library.
• Useful as NNs are, there is a school of thought that holds that statistical ML is necessary but insufﬁcient,
and will get you just that far. Instead, the thinking goes, you need to incorporate structured knowledge and
symbolic methods into the mix, and that in turn depends on brain rather than (only) brawn. This is a view we
subscribe to at AI21 Labs (see [17] as an example).
References
[1] Google, ResNet-50 training cost comparison , https : / / cloud . google . com / images / products / tpu /
machine-learning-performance_2x.png, Accessed: 2020-04-12, 2020.
[2] V . Sanh, L. Debut, J. Chaumond, and T. Wolf, “DistilBERT, a distilled version of BERT: Smaller, faster, cheaper
and lighter,” in NeurIPS EMC2 Workshop, 2019.
[3] X. Jiao, Y . Yin, L. Shang, X. Jiang, X. Chen, L. Li, F. Wang, and Q. Liu,TinyBERT: Distilling BERT for natural
language understanding, 2019. arXiv: 1909.10351 [cs.CL].
3
The Cost of Training NLP Models: A Concise Overview
[4] J. Devlin, M.-W. Chang, K. Lee, and K. Toutanova, “BERT: Pre-training of deep bidirectional transformers
for language understanding,” in Proceedings of the 2019 Conference of the North American Chapter of the
Association for Computational Linguistics: Human Language Technologies, Volume 1 (Long and Short Pa-
pers), Minneapolis, Minnesota: Association for Computational Linguistics, Jun. 2019, pp. 4171–4186. DOI:
10.18653/v1/N19-1423. [Online]. Available: https://www.aclweb.org/anthology/N19-1423.
[5] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y . Zhou, W. Li, and P. J. Liu, “Exploring the
limits of transfer learning with a uniﬁed text-to-text transformer,” ArXiv e-prints, 2019. arXiv: 1910.10683.
[6] J. Etchemendy and F.-F. Li, National research cloud: Ensuring the continuation of american innovation, https:
/ / hai . stanford . edu / news / national - research - cloud - ensuring - continuation - american -
innovation, Accessed: 2020-04-12, 2020.
[7] J. Kaplan, S. McCandlish, T. Henighan, T. B. Brown, B. Chess, R. Child, S. Gray, A. Radford, J. Wu, and D.
Amodei, Scaling laws for neural language models, 2020. arXiv: 2001.08361 [cs.LG].
[8] J. Dodge, S. Gururangan, D. Card, R. Schwartz, and N. A. Smith, “Show your work: Improved reporting of
experimental results,” in Proceedings of the 2019 Conference on Empirical Methods in Natural Language Pro-
cessing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP), Hong
Kong, China: Association for Computational Linguistics, Nov. 2019, pp. 2185–2194.DOI: 10.18653/v1/D19-
1224. [Online]. Available: https://www.aclweb.org/anthology/D19-1224.
[9] Z. Li, E. Wallace, S. Shen, K. Lin, K. Keutzer, D. Klein, and J. E. Gonzalez, Train large, then compress:
Rethinking model size for efﬁcient training and inference of transformers, 2020. arXiv: 2002.11794 [cs.CL].
[10] J. S. Rosenfeld, A. Rosenfeld, Y . Belinkov, and N. Shavit, “A constructive prediction of the generalization error
across scales,” in International Conference on Learning Representations , 2020. [Online]. Available: https:
//openreview.net/forum?id=ryenvpEKDr.
[11] A. Radford, J. Wu, R. Child, D. Luan, D. Amodei, and I. Sutskever, Language models are unsupervised multi-
task learners, OpenAI’s Blog: https://d4mucfpksywv.cloudfront.net/better- language- models/
language_models_are_unsupervised_multitask_learners.pdf, 2019.
[12] K. Clark, M.-T. Luong, Q. V . Le, and C. D. Manning, “ELECTRA: Pre-training text encoders as discriminators
rather than generators,” in International Conference on Learning Representations , 2020. [Online]. Available:
https://openreview.net/forum?id=r1xMH1BtvB.
[13] SambaNova, A new state of the art in NLP: Beyond gpus, https://sambanova.ai/a-new-state-of-the-
art-in-nlp-beyond-gpus/ , Accessed: 2020-04-12, 2020.
[14] A. Rallo, New research from TSO Logic shows aws costs get lower every year , https : / / aws . amazon .
com/blogs/apn/new- research- from- tso- logic- shows- aws- costs- get- lower- every- year/ ,
Accessed: 2020-04-12, 2018.
[15] N. Kitaev, L. Kaiser, and A. Levskaya, “Reformer: The efﬁcient transformer,” in International Conference on
Learning Representations, 2020. [Online]. Available: https://openreview.net/forum?id=rkgNKkHtvB.
[16] Z. Lan, M. Chen, S. Goodman, K. Gimpel, P. Sharma, and R. Soricut, “ALBERT: A lite BERT for self-
supervised learning of language representations,” in International Conference on Learning Representations ,
2020. [Online]. Available: https://openreview.net/forum?id=H1eA7AEtvS.
[17] Y . Levine, B. Lenz, O. Dagan, D. Padnos, O. Sharir, S. Shalev-Shwartz, A. Shashua, and Y . Shoham, “Sense-
BERT: Driving some sense into BERT,” inProceedings of the 2010 Conference of the Association for Compu-
tational Linguistics (ACL), 2020. [Online]. Available: https://arxiv.org/pdf/1908.05646.pdf.
[18] H. Touvron, A. Vedaldi, M. Douze, and H. Jegou, “Fixing the train-test resolution discrepancy,” in Advances in
Neural Information Processing Systems 32, Curran Associates, Inc., 2019, pp. 8252–8262. [Online]. Available:
http://papers.nips.cc/paper/9035-fixing-the-train-test-resolution-discrepancy.pdf .
[19] S. Ruder, NLP’s ImageNet moment has arrived , https://thegradient.pub/nlp- imagenet/ , Accessed:
2020-04-12, 2018.
[20] D. Geman, S. Geman, N. Hallonquist, and L. Younes, “Visual Turing test for computer vision systems,” Pro-
ceedings of the National Academy of Sciences , vol. 112, no. 12, pp. 3618–3623, 2015, ISSN : 0027-8424. DOI:
10 . 1073 / pnas . 1422953112. eprint: https : / / www . pnas . org / content / 112 / 12 / 3618 . full . pdf.
[Online]. Available: https://www.pnas.org/content/112/12/3618.
4
The Cost of Training NLP Models: A Concise Overview
A NLP versus CV
With a few notable exceptions9, you do not see in computer vision (CV) the large numbers and cost escalations you
do in NLP, and it is natural to ask why. We enter this discussion with some trepidation. While some of the folks at
AI21 Labs have experience in CV , it is not our core competence as a company. Furthermore, some of the CV experts
with whom we spoke did not have ﬁrm opinions here, and the opinions they did have did not always agree with each
other. Still, since we have been asked this question we feel we should address it, but please treat the following more
as a beginning of a discussion rather than deﬁnitive answers.10
We believe that there are fundamentally two reasons why training CV models is cheaper than training NLP models:
• Images versus sentences. Images are smooth and local, in that by and large the value of a pixel depends
mostly on its close neighborhood and less so on other parts of the image, and furthermore the value does
not change drastically from one pixel to its neighbor. Moreover, images are iconic, by which we mean that
"what you see is what you get"; an image of chair and a desk represents a chair and desk. Language is very
different. Words far apart can be coupled probabilistically, and language iscompositional; the way you string
words together carries as much meaning as the semantic content of the words themselves.
• Object recognition versus – what? The canonical problem in computer vision – object recogni-
tion/classiﬁcation – is, while by no means trivial, relatively simple. It has no direct analog in NLP. One
could argue that topic- or sentiment-analysis are somewhat analogous at the document level, and word-sense
disambiguation is at the sentence level. But the analogy is weak, and neither of these plays the same central
role that object recognition does in vision. Another telling analogy is between object identity in vision (is
the person seen in this image the same as the person in this other image?) and noun-phrase co-reference in
NLP (does “the president” refer to the same entity as “Mr. Trump”?). Here the separation between vision and
language is stark; object identity is close to being a solved problem, while co-reference is still unsolved. And
this is leaving aside the issue that even once solved, co-reference on its own would not bring the same value
that object recognition does in CV .
These differences manifest themselves in several ways, including these:
• CNNs versus transformers. CV problems lend themselves to Convolutional Neural Networks (CNNs),
while the canonical NLP approach has centered around transformer models, which are inherently more ex-
pensive than CNNs. The different choice of architecture is directly related to the differences between images
and sentences; the locality property matches with the local windows of convolutional layers, and smoothness
with the sub-sampling operation in pooling layers. Since language does not enjoy these properties, we must
use a more general, but less efﬁcient, architecture such as the transformer.
• Supervised versus semi-supervised versus self-supervised learning. NLP and computer vision employ
all of these learning regimes, but the balance is different. Unlike in computer vision, most of the training
time of NLU models is devoted to self-supervised learning of language itself, and only a small portion is
devoted to (supervised) ﬁne-tuning of the model to solve a speciﬁc task. This is related to the inherent
complexity of the structure of language and the nature of NLU and NLG tasks. Much larger datasets are
needed in order to provide useful signal, and, just as bad, the tasks are inherently more ambiguous and the
data is harder for people to annotate than in image classiﬁcation; it is easier to answer the question “Is that
a person or a car” than “Does this sentence imply that sentence”. Furthermore, data augmentation is much
more successful in vision than in NLP, and semi-supervised learning aided by data augmentation has led to
many recent SOTA results in vision. In contrast, NLP has been driven toward purely self-supervised learning
(“the NLP revolution will not be supervised!”). This in turn translates into larger training datasets compared
to the supervised setting, as well as longer training cycles.
Again, important caveats apply to all of the above. Even in object recognition, the larger context of the image can
matter when determining what is depicted in a given image patch. Furthermore, object recognition is not the sole focus
of CV , and more elaborate tasks, such as scene understanding [20], certainly do not have the smooth, local properties
mentioned (to use a famous example, object recognition techniques do not tell you the interesting part about an image
depicting a piano dropping through the air and about to land on someone’s head). As another example, in the area
9There have been a few attempts to create “mega-models” for CV , e.g., FixResNet [18] has 830M parameters and was trained
on nearly a billion weakly-labeled images. However, the gains are not as great compared to the added costs, and such approaches
have not become the norm just yet.
10See also this article [19] for an interesting discussion circa 2018.
5
The Cost of Training NLP Models: A Concise Overview
of image synthesis, which often requires accommodating complex logical, real-world constraints in the synthesized
image, CNNs give way to inherently more expensive models such as GANs.
Despite these important caveats, we feel the above analysis is fair, for two reasons. First, it is the case that among CV
technologies, object recognition has brought the most commercial value to date, and CNNs have been the main driver
behind its success. And second, more ambitious tasks such as scene understanding are getting close to NLP in being
less well deﬁned and less well solved. They also call for the same commonsense reasoning as does NLP, and thus are
likely require the elaborate techniques – and costs – currently associated with NLP.
6
