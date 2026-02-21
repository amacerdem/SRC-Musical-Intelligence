# predictive-coding-and-stochastic-resonance-as-fund

Predictive coding and stochastic resonance 
as fundamental principles of auditory 
phantom perception
Achim Schilling,
1 , 2
William Sedley,
3
Richard Gerum,
2 , 4
Claus Metzner,
1
Konstantin Tziridis,
1
Andreas Maier,
5
Holger Schulze,
1
Fan-Gang Zeng,
6
Karl J. Friston
7
and Patrick Krauss
1 , 2 , 5
Mechanistic insight is achieved only when experiments are employed to test formal or computational models. 
Furthermore, in analogy to lesion studies, phantom perception may serve as a vehicle to understand the fundamental 
processing principles underlying healthy auditory perception. With a special focus on tinnitus—as the prime 
example of auditory phantom perception—we review recent work at the intersection of artificial intelligence, 
psychology and neuroscience. In particular, we discuss why everyone with tinnitus suffers from (at least hidden) 
hearing loss, but not everyone with hearing loss suffers from tinnitus.
We argue that intrinsic neural noise is generated and amplified along the auditory pathway as a compensatory mech -
anism to restore normal hearing based on adaptive stochastic resonance. The neural noise increase can then be mis -
interpreted as auditory input and perceived as tinnitus. This mechanism can be formalized in the Bayesian brain 
framework, where the percept (posterior) assimilates a prior prediction (brain’s expectations) and likelihood (bot -
tom-up neural signal). A higher mean and lower variance (i.e. enhanced precision) of the likelihood shifts the poster -
ior, evincing a misinterpretation of sensory evidence, which may be further confounded by plastic changes in the 
brain that underwrite prior predictions. Hence, two fundamental processing principles provide the most explanatory 
power for the emergence of auditory phantom perceptions: predictive coding as a top-down and adaptive stochastic 
resonance as a complementary bottom-up mechanism.
We conclude that both principles also play a crucial role in healthy auditory perception. Finally, in the context of 
neuroscience-inspired artificial intelligence, both processing principles may serve to improve contemporary ma -
chine learning techniques.
1 Neuroscience Lab, University Hospital Erlangen, 91054 Erlangen, Germany
2 Cognitive Computational Neuroscience Group, University Erlangen-Nürnberg, 91058 Erlangen, Germany
3 Translational and Clinical Research Institute, Newcastle University Medical School, Newcastle upon Tyne NE2 
4HH, UK
4 Department of Physics and Astronomy and Center for Vision Research, York University, Toronto, ON M3J 1P3, 
Canada
5 Pattern Recognition Lab, University Erlangen-Nürnberg, 91058 Erlangen, Germany
6 Center for Hearing Research, Departments of Anatomy and Neurobiology, Biomedical Engineering, Cognitive 
Sciences, Otolaryngology–Head and Neck Surgery, University of California Irvine, Irvine, CA 92697, USA
7 Wellcome Centre for Human Neuroimaging, Institute of Neurology, University College London, London WC1N 
3AR, UK
Received October 26, 2022. Revised June 27, 2023. Accepted July 15, 2023. Advance access publication July 28, 2023
© The Author(s) 2023. Published by Oxford University Press on behalf of the Guarantors of Brain. 
This is an Open Access article distributed under the terms of the Creative Commons Attribution-NonCommercial License ( https://creativecommons.org/licenses/by- 
nc/4.0/ ), which permits non-commercial re-use, distribution, and reproduction in any medium, provided the original work is properly cited. For commercial re-use, 
please contact journals.permissions@oup.com
https://doi.org/10.1093/brain/awad255 BRAIN 2023: 146; 4809–4825 | 4809
Correspondence to: Achim Schilling  
ENT Clinic, Head and Neck Surgery, University Hospital Erlangen  
Waldstrasse 1, 91054 Erlangen, Germany  
E-mail: achim.schilling@fau.de
Keywords: artificial intelligence; Bayesian brain; phantom perception; predictive coding; stochastic resonance; 
tinnitus
Introduction
The ultimate goal of neuroscience is to gain a mechanistic under -
standing of how information is processed in the brain. Since the 
early beginnings of the scientific study of the brain, lesions or 
more broadly anatomical damages and their physiological effects 
have provided pivotal insights into brain function. Analogously, 
phantom perception may serve as a vehicle to understand the fun -
damental processing principles underlying normal perception. The 
prime example of an auditory phantom perception is tinnitus, 
which is believed to be caused by anatomical damage along the 
auditory pathway. Here we provide a mechanistic explanation of 
how tinnitus emerges in the brain: namely, how the neural and 
mental processes underlying perception, cognition and behaviour 
contribute to and are affected by the development of tinnitus. 
These insights may not only point to strategies how tinnitus may 
be reversed or at least mitigated, but also how auditory perception 
is implemented in the brain in general.
While there is broad agreement in the auditory neuroscience 
community on these goals, there is far less agreement on the way 
to achieve them. There is still a popular belief among neuroscienti -
fic and psychological tinnitus researchers that we are largely data- 
driven. In other words, generating large, multi-modal and complex 
datasets—analysed with advanced data science methods—are be -
lieved to lead to fundamental insights into how tinnitus emerges. 
Indeed, in the last decades we have assembled a broad database, 
which has inspired models that make quantitative predictions. 
These predictions scaffold new experimental paradigms that aim 
to unravel the mechanisms of tinnitus perception. In the following, 
we summarize some of the main findings in tinnitus research, over 
the last decades, and then turn to strategic questions about how to 
leverage these advances, from the perspective of formal modelling.
Some universal correlations between hearing loss, tinnitus and 
neural hyperactivity in the auditory system have been found in 
both animal and human studies. These reproducible findings can 
be considered as the common denominator of tinnitus research 
and could offer the minimal starting point for theoretical consid -
erations. Tinnitus is a phenomenon arising somewhere along the 
auditory pathway, but not in the inner ear.
1
Thus, it can be shown 
that the spontaneous activity of neurons along the auditory path -
way is increased after hearing loss,
2–4
whereas the damaged coch -
lea transmits less information to the higher auditory nuclei.
5 , 6
However, it has been argued that not all alterations in neural activ -
ity in animal models, which were caused by an acoustic trauma, are 
necessarily related to tinnitus.
1 , 7
Although there exist some behav -
ioural tests to check for the putative presence of a tinnitus percept 
based on conditioning
8 , 9
or startle responses,
10–12
the reliability of 
these paradigms remains controversial.
7 , 13
Thus, studies on human 
subjects complement these findings. In several recent studies, it 
was shown that the tinnitus pitch lies within the frequency range 
of the hearing loss and thus it is an obvious assumption 
that tinnitus can be regarded as a within frequency channel phe -
nomenon.
14–17
Potentially, it is sufficient to assume that the me -
chanisms causing tinnitus occur in each impaired frequency 
channel individually and that crosstalk between the different fre -
quency channels along the tonotopic map is not crucial to explain 
the basic principles behind tinnitus development.
18
This assumption is supported by recent findings e.g. by Dalligna 
and coworkers,
14
who report that the tinnitus is directly centred at 
the frequency of the largest hearing loss. For the sake of complete -
ness, it should be mentioned that other studies on tinnitus and its 
relation to hearing loss found a special emphasis of the edges of the 
impaired frequency range on the tinnitus pitch.
19-21
However, re -
cently, Keppler and coworkers
15
contradicted these findings and 
stated that there is no correlation between tinnitus frequency 
and the edges of the impaired frequency ranges.
Indeed, the above neural correlates of tinnitus and hearing loss 
are just a small distillation of all studies that aspire to unravel me -
chanisms that underpin tinnitus, but these findings are robust and 
constitute the basis of most theoretical and computational models 
of tinnitus. In the 1990s the first computational models of tinnitus 
emerged. These models considered decreased lateral inhibition— 
due to deficient auditory input (i.e. cochlear damage)—as the 
main cause of tinnitus. Gerken
22
created a feed-forward brainstem 
model and suggested the inferior colliculus to be the crucial struc -
ture for tinnitus development. Kral and Majernik,
23
as well as 
Langner and Wallhäuser-Franke
24
pursued computational models, 
based on decreased lateral inhibition. Bruce and coworkers
25
devel -
oped these models further and implemented lateral inhibition in a 
spiking recurrent neural network. In a subsequent step, the princi -
ples were implemented in a model of the auditory cortex based on 
spiking neurons.
26
Besides lateral inhibition, homeostatic plasticity
27
and central 
gain changes are hypothesized to be the cause for tinnitus emer -
gence and manifestation. These hypotheses are based on the idea 
that incoming neuronal signals are amplified, in order to compen -
sate the decreased input from the damaged cochlea. Thus, Parra 
and Pearlmutter
28
implemented that principle in an ‘abstract’ mod -
el, where they simply defined several frequency channels with a 
certain input. The output was scaled with the average, which 
means that a decreased input leads to a higher scaling or amplifica -
tion factor, respectively. However, they did not consider a plausible 
neural implementation of their mathematical model. Schaette and 
Kempter
29-31
further developed several computational models, in -
vestigating the effects of central gain increase on tinnitus emer -
gence. Finally, Chrostowski and coworkers
32
developed a cortex 
model to investigate central gain changes in the cortex (for detailed 
review on computational tinnitus models see Schaette and 
Kempter
1
).
In 2013, Zeng
33
introduced a model that argues that tinnitus is 
not caused by increased central gain, which means a multiplicative 
amplification of the signal, but by increased central noise, which 
means an additive neural noise, that is intrinsically generated. 
The idea of an additional intrinsic or extrinsic noise as an explan -
ation for tinnitus has gained some popularity in recent years e.g. 
Koops and Eggermont.
34
However, Zeng raised the question why 
the brain should increase central noise levels. This question was 
4810 | BRAIN 2023: 146; 4809–4825                                                                                                                         A. Schilling et al.
addressed in 2016 by Krauss and coworkers,
18
who showed that in -
ternally generated neural noise could partially restore hearing abil -
ity after hearing loss through the effect of stochastic resonance.
35-37
Stochastic resonance is a phenomenon in which the addition of 
noise to a non-linear system can improve its sensitivity to weak sig -
nals. It occurs when a system—which is normally unable to detect 
weak signals—features an optimal level of noise that lifts the weak 
signals above the detection threshold. This is because the noise 
serves to ‘jiggle’ the system, making it easier for weak signals to 
cross a response threshold. However, the effect only works in a nar -
row range, as the noise amplitude has to be tuned to an optimal le -
vel. Noise amplitudes that are too low would not lift the 
subthreshold signal above the detection threshold. Conversely, 
noise amplitudes that are too high would significantly worsen the 
signal-to-noise ratio up to a level at which the signal disappears 
completely in the noise. Stochastic resonance has been observed 
in a variety of physical, biological and neural systems, (for overview 
cf. Koops and Eggermont
34
and Krauss et al.
35
).
The idea behind the stochastic resonance model of auditory 
phantom perception (Erlangen model of tinnitus development) is 
that a subthreshold signal—from an impaired cochlea—is lifted 
stochastically above the detection threshold by adding uncorre -
lated neural noise. In earlier studies it has been shown that human 
hearing may be enhanced beyond the absolute threshold of hearing 
by adding acoustic white noise to a subthreshold acoustic stimu -
lus.
38
The Erlangen model hypothesizes that this mechanism is 
also implemented in the dorsal cochlear nucleus (DCN) and that 
—instead of acoustic white noise—internally generated neural 
noise is added to the cochlea output, to lift it above the detection 
threshold.
37
Recently, several studies have provided evidence that 
cross-modal stochastic resonance is a universal principle for en -
hancing sensory perception.
36 , 39 , 40
This stochastic resonance hypothesis is further supported by 
the finding that, on average, hearing thresholds are better in pa -
tients suffering from hearing loss with tinnitus compared to a con -
trol group of patients suffering from hearing loss but without 
tinnitus.
19 , 41 , 42
Along the same line, the stochastic resonance effect 
as add-on to the central noise model may explain the Zwicker tone 
illusion,
43-45
i.e. the perception of a phantom sound, which occurs 
after stimulation with notched noise, and why auditory sensitivity 
for frequencies adjacent to the Zwicker tone are improved beyond 
the absolute threshold of hearing during Zwicker tone perception.
46
Furthermore, recently, a crucial prediction of the stochastic reson -
ance model of tinnitus development was confirmed experimentally 
by using brainstem audiometry
47
and assessing behavioural signs 
of tinnitus
10
in an animal model: simulated transient hearing loss 
improves auditory thresholds and leads, as a side effect, to the per -
ception of tinnitus.
48
Both the model from Zeng and the model from 
Krauss et al.,
35
are not based on a particular or specified neural net -
work architecture. However, in 2020, Schilling and coworkers de -
veloped a hybrid model based on a biophysically realistic model 
of the cochlea and the DCN combined with a deep neural network 
representing all further processing stages along the auditory path -
way. In this model, intrinsically generated noise could indeed sig -
nificantly increase speech perception via SR.
49
Recently, a similar 
hybrid neural network model has led to further insights into the 
mechanisms of impaired speech recognition caused by hearing 
loss.
50
In parallel to the intrinsic neural noise models from Zeng and 
Krauss and colleagues, Sedley and coworkers developed a concep -
tual model, which describes tinnitus as arising from a prediction er -
ror of the brain.
51 , 52
This model is based on the idea that the brain is 
a Bayesian prediction machine, trying to minimize prediction er -
rors or free energy,
53 , 54
a principle also known as predictive coding. 
According to the theoretical framework of predictive coding, the 
brain’s main function is to generate and test predictions about in -
coming sensory information. In particular, the brain is constantly 
generating hypotheses or predictions about what is happening in 
the environment, based on past experiences, and then comparing 
these predictions with incoming sensory data. The ensuing predic -
tion error is then thought to drive representations about states of 
affairs generating sensations towards better predictions; thereby 
resolving prediction errors.
This predictive coding model of tinnitus addresses the issue of 
whether or not an individual perceives tinnitus as an interplay be -
tween existing auditory predictions (which, by default, do not fea -
ture tinnitus) and spontaneous activity (i.e. noise) in the central 
auditory pathway (considered a ‘tinnitus precursor’). Whether the 
posterior (i.e. percept) crosses the threshold for perception depends 
on both of these factors, including their mean values (e.g. firing 
rate) and their precision. More recently, by using a hierarchical 
Gaussian filter, a computational instantiation of this model has 
been able to explain phenomenology in individual tinnitus subjects 
and predict their residual inhibition characteristics.
55
Despite the 
fact that in recent years tinnitus research converged to the three 
main models described above (central noise, central gain, predict -
ive coding), it has to be stated that there exist several further com -
putational simulations and approaches trying to explain and 
characterize tinnitus development based e.g. on information theor -
etical considerations (see Dotan and Shriki
56
and Gault et al.
57
).
Besides the computational models that rest upon a mathemat -
ical formulation, there exist several phenomenological models, 
such as the thalamo-cortical dysrhythmia model,
58 , 59
the thalamic 
low-threshold calcium spike model,
60
the fronto-striatal gating hy -
pothesis
61 , 62
and the overlapping subnetwork theory.
63 , 64
Finally, 
there exists another Bayesian brain/predictive coding model of tin -
nitus, which is somewhat the polar opposite to what Sedley and 
Friston were arguing for. There, tinnitus is not believed to arise 
from spontaneous noise increase, which higher predictions go on 
to accept, but on the contrary that tinnitus arises from reduced in -
put to the auditory cortex, leading it to ‘make up’ or ‘fill in’ an audi -
tory percept from auditory memory.
65
However, this assumption 
contradicts the findings that spontaneous neural activity is in -
creased along the entire auditory pathway starting from the DCN 
after hearing loss.
2-4
As there exist various models of tinnitus development, which 
are far too numerous to be treated in detail in this study, criteria 
are needed to define which models are apt to understand tinnitus 
development. In their review paper, Schaette and Kempter
1
define 
three major criteria for the quality of a model: first—and in line with 
Popper’s ideas
66
—a model should be falsifiable, which means there 
should be experimental paradigms, which could be used to test a 
certain candidate model. Second, a model should make quantita -
tive predictions, as opposed to purely qualitative, often vague, pre -
dictions, cf. also Lazebnik.
67
Third, a model should be as simple as 
possible, i.e. contain the smallest number of parameters and as -
sumptions as possible, a principle called Ockham’s razor.
68
Hence, if two models explain experimental data equally well, the 
simpler one has to be considered the better one.
With the huge progress of artificial intelligence (AI) during the 
last decade, which is mainly due to increased computing power, a 
new discipline has been founded, called Cognitive Computational 
Neuroscience (CCN) as an integrative endeavour at the intersection 
of AI, cognitive science and neuroscience.
69 , 70
Models of auditory phantom perception                                                                                BRAIN 2023: 146; 4809–4825 | 4811
Here, we first discuss the opportunities and limitations of this 
new research agenda. In particular, we present key thought experi -
ments that highlight the major challenges on the road towards a 
CCN of tinnitus. In the light of these considerations, we subse -
quently review current models of tinnitus and assess their explana -
tory power. Finally, we present an integration of those models that 
we consider most promising and point towards a unified theory of 
tinnitus development.
Three challenges ahead
The challenge of developing a common formal 
language
In 2002, Yuri Lazebnik compared the biologists’ endeavour—of try -
ing to understand the building blocks and processes of living cells— 
with the problems that engineers typically deal with. In his opinion 
paper ‘Can a biologist fix a radio?—Or, what I learned while studying 
apoptosis’, Lazebnik argued that many fields of biomedical research 
at some point reach 
‘a stage at which models, that seemed so complete, fall apart, predictions 
that were considered so obvious are found to be wrong, and attempts to 
develop wonder drugs largely fail. This stage is characterized by a sense 
of frustration at the complexity of the process’.
67
Subsequently, Lazebnik
67
discussed a number of intriguing ana -
logies between the physical and life sciences. In particular, he iden -
tified formal language as the most important difference between 
the two. Lazebnik argues that biologists and engineers use quite 
different languages for describing phenomena. On the one hand, 
biologists draw box-and-arrow diagrams, which are—even if 
a certain diagram makes overall sense—difficult to translate 
into quantitative assumptions, and hence limits its predictive or 
investigative value.
Indeed, these thoughts fit to the criterion for a ‘good model’ as 
pointed out by Schaette and Kempter,
1
i.e. that a model should 
make quantitative predictions. However, on the other hand a mod -
el should be as simple as possible and understandable, which 
means that it is important to find a compromise between too 
fine-grained and too coarse-grained descriptions of the system to 
be explained (see Marr’s levels of analysis in Fig. 1A , based on 
Marr and Poggio
71
).
Lazebnik also remarks that scientific assumptions and conver -
sations are often ‘vague’ and ‘avoid clear, quantifiable predictions’. 
A freely adapted example drawn from Lazebnik’s paper
67
would be 
a statement like 
‘an imbalance of excitatory and inhibitory neural activity after 
hearing-loss appears to cause an overall neural hyperactivity, which in 
turn seems to be correlated with the perception of tinnitus
’.
Descriptions of electrophysiological findings are an important 
starting point for hypothesis generation, but they are no more 
than a first step. Description needs to be complemented with ex -
planation and prediction (compare also the four main goals of 
psychology as described in Holt et al.
72
). Furthermore, Lazebnik 
urges a more formal common language for biological sciences, in 
particular a language that has the precision and expressivity found 
in engineering, physics or computer science. Any engineer trained 
in electronics for instance, is able to unambiguously understand a 
diagram describing a radio or any other electronic device. Thus, en -
gineers can discuss a radio using terms that are common ground in 
the community. Furthermore, this commonality enables engineers 
to identify familiar functional architectures or motifs; even in a dia -
gram of a completely novel device. Finally, due to the mathematical 
underpinnings of the language used in engineering, it is perfectly 
suited for quantitative analyses and computational modelling. 
For instance, a description of a certain radio includes all key para -
meters of each component like the capacity of a capacitor, but 
not irrelevant parameters—that do not ‘matter’—like its colour, 
shape or size.
We emphasize that this does not mean that anatomical descrip -
tions are useless in order to understand brain function, especially 
since there is a close correlation between structure and function 
in the brain. However, also in neurobiology there exist both kinds 
of detail: those that are crucial for understanding neural process -
ing, and those that are not relevant variables.
Lazebnik concludes that ‘the absence of such language is the 
flaw of biological research that causes David’s paradox’, i.e. the 
paradoxical phenomenon frequently observed in biology and 
neuroscience that ‘the more facts we learn the less we understand 
the process we study’.
67
Some conclusions for tinnitus research can be drawn from 
Lazebniks’ thoughts on a more formal approach in biological 
sciences. The ‘central gain’ and ‘homeostatic plasticity’ theory on 
tinnitus emergence is a good example how the communication 
on tinnitus research can be improved. For example, Roberts stated 
in 2018 that the increase of central gain is ‘increase of input output 
functions by forms of homeostatic plasticity’, which means that 
homeostatic plasticity is necessarily connected to central gain 
adaptations.
73
In contrast to that, Schaette and Kempter
1
state 
that central gain changes can occur within seconds and thus are 
not necessarily caused by homeostatic plasticity. Only on longer 
timescales, both effects can be regarded as ‘functionally equiva -
lent’.
1
Indeed, tinnitus research would profit from a unified termin -
ology for the different concepts, in the best case, a mathematical 
formulation.
The challenge of developing a unified mechanistic 
theory
In 2014, Joshua Brown built on Lazebnik’s ideas and published the 
opinion article ‘The tale of the neuroscientists and the computer: 
why mechanistic theory matters’.
74
In this thought experiment, a 
group of neuroscientists finds an alien computer and tries to figure 
out its function.
First, the MEG/EEG researcher tried to investigate the computer. 
She found that every time ‘when the hard disk was assessed, the 
disk controller showed higher voltages on average, and especially 
more power in the higher frequency bands’.
74
Subsequently, the cognitive neuroscientist, i.e. the functional 
MRI researcher argued that MEG/EEG has insufficient spatial reso -
lution to see what is going on inside the computer. He carried out 
a large number of experiments, the results of which can be sum -
marized with the realization that during certain tasks, certain re -
gions seem to be more activated and that none of these 
components could be understood properly in isolation. Thus, the 
researcher analysed the interactions of these components, show -
ing that there is a vast variety of different task-specific networks 
in the computer.
Finally, the electrophysiologist noted, critically, that his collea -
gues may have found coarse-grained patterns of activity, but it is 
still unclear what the individual circuits are doing. He starts to im -
plant microelectrode arrays into the computer and probes 
4812 | BRAIN 2023: 146; 4809–4825                                                                                                                         A. Schilling et al.
individual circuit points by measuring voltage fluctuations. With 
careful observation, the electrophysiologist identifies units re -
sponding stochastically when certain inputs are presented, and 
that nearby units seem to process similar inputs. Furthermore, 
each unit seems to have characteristic tuning properties.
Brown’s tale ends with the conclusion that even though they 
performed a multitude of different empirical investigations, yield -
ing a broad range of interesting results, it is still highly questionable 
whether ‘the neuroscientists really understood how the computer 
works’. 
74
This provocative thought experiment speaks to some ideas that 
are relevant for tinnitus research.
In 2021, four leading scientists in tinnitus research discussed 
different tinnitus models at the Annual-Mid-Winter Meeting of 
the Association for Otolaryngology and diagnosed a ‘lack of consist-
ency of concepts about the neural correlate of tinnitus’. 75Thus, a 
clearly defined theoretical framework is needed, which helps em -
pirical groups to develop experimental paradigms suited to confirm 
or falsify different candidate models. To achieve that, inter- 
disciplinary teams or at least an inter-disciplinary approach is 
needed.
76
The challenge of developing appropriate analysis 
methods
In 2017 Jonas and Kording implemented the thought experiment of 
Brown in an experimental study. In their study ‘Could a neuroscien -
tist understand a microprocessor?’ 77the authors address this ques -
tion by emulating a classical microprocessor, the MOS 6502, which 
was implemented as the central processing unit (CPU) in the Apple 
I, the Commodore 64, and the Atari Video Game System, in the 
1970s and 1980s. In contrast to contemporary CPUs, like Intel’s 
i9-9900K, that consist of more than three billion transistors, the 
MOS 6502 only consisted of 3510 transistors. It served as a ‘model 
organism’ in the mentioned study, and performed three different 
‘behaviors’, i.e. three classical video games (
Donkey Kong, Space 
Invaders and Pitfall).
The idea behind this approach is that the microprocessor, as an 
artificial information processing system, has three decisive advan -
tages compared to natural nervous systems. First, it is fully under -
stood at all levels of description and complexity, from its gross 
architecture and the overall data flow, through logical gate primi -
tives, to the dynamics of single transistors. Second, its internal 
state is fully accessible without any restrictions to temporal or spa-
tial resolution. And third, it offers the ability to perform arbitrary in-
vasive experiments on it, which are impossible in living systems 
due to ethical or technical reasons. Using this framework, the 
authors applied a wide range of popular data analysis methods 
from neuroscience to investigate the structural and dynamical 
properties of the microprocessor. The methods used included— 
but were not restricted to—Granger causality for analysing task- 
specific functional connectivity, time-frequency analysis as a hall
-
mark of MEG/EEG research, spike pattern statistics, dimensionality 
reduction, lesioning and tuning curve analysis.
The authors concluded that although each of the applied meth -
ods yielded results strikingly similar to what is known from neuros -
cientific or psychological studies, none of them could actually 
elucidate how the microprocessor works, or more broadly speak
-
ing, was appropriate to gain a mechanistic understanding of the in -
vestigated system.
Of course, there are potential criticisms of this study; for ex -
ample, the brain is no computer and thus the drawn parallels are 
insufficient. Nevertheless, the idea to use a known model system 
to check for the validity of the evaluation procedures and common 
methods is a seminal principle. In 2009 Bennett and coworkers
78
performed an even stranger experiment, when they used standard 
functional MRI and statistics techniques to analyse the brain activ -
ity of a dead salmon, and indeed found a blood oxygenation level- 
Figure 1 Marr’s levels of analysis. (A) The scheme illustrates how measurement methods (such as MEG, EEG etc.), neuroscientific disciplines, as well as 
theoretical models can be structured in three different levels of analysis (according to Marr and Poggio 71). (B) Tinnitus models in the light of the three 
levels of analysis. The grey bars illustrate how the different models cover the different levels of analysis (implementational, algorithmic, computation-
al). The central noise model and the stochastic resonance model can be unified (1). The stochastic resonance model is at the algorithmic level as there 
exists a neural network model, 38 which could reproduce the stochastic resonance effect in tinnitus context. The exact molecular mechanism, such as 
the specific neurotransmitter, are unknown and therefore it is not at the implementational level. The mathematical formulation of the predictive cod -
ing model cannot be fully translated to a neural network model and therefore it is at the computational model. A neural network implementation of the 
predictive coding model would be algorithmic. Homeostatic plasticity is a collection of the molecular and thus implementational mechanisms behind 
the central gain model (2).
Models of auditory phantom perception                                                                                BRAIN 2023: 146; 4809–4825 | 4813
dependent (BOLD) signal due to stimulation. At first glance, this ex -
periment seemed to be at least useless if not even funny, but it was 
a wake-up call and indeed changed the way functional MRI data are 
evaluated. Nowadays there exist strict rules how to correct for mul -
tiple testing in functional MRI research, to prevent pseudo-effects 
being a result of wrong statistical testing.
78 , 79
In computational 
neuroscience and AI research, newly developed methods are al -
ways applied to standard datasets such as the MNIST (Modified 
National Institute of Standards and Technology) database consist -
ing of 60 000 images of hand-written digits
80 , 81
or artificially gener -
ated datasets with known properties, e.g. Schilling et al.,
47 , 82
Zenke 
and Vogels
83
and Krauss et al.
84
The principle of using fully known— 
even trivial systems—to test the validity of tools, methods or even 
theories could be an important approach in tinnitus research. Even 
in computational modelling, simply implementing a system in all 
details without an underlying theory, which serves as a solid 
base, will not lead to a real understanding. Indeed, theory needs 
computational modelling, but the statement is also true the other 
way around.
85
Therefore, it is crucial that computational models 
meet a basic standard—they should be capable of accurately ex -
plaining well established and simple phenomena. This serves as a 
basis to verify their validity before drawing more complex 
conclusions.
Towards a cognitive computational 
neuroscience of tinnitus
What does it mean to understand a system?
If popular analysis methods fail to deliver mechanistic understand -
ing, what are the alternative approaches? Most obviously, narrative 
hypotheses about the structure and function of the system under 
investigation will help. Instead of simply describing data features 
with correlations, coherence, Granger causality etc.—in the hope 
of learning something about the functioning of the system under 
investigation—it would be much more effective to have a concrete 
hypothesis about the structure or function architecture of the sys -
tem and then search for empirical evidence for that and alternative 
hypotheses.
Note that this does not exclude explorative analysis of existing 
data, in order to generate new hypotheses. However, as we pointed 
out in a previous publication,
86
to avoid statistical errors due to 
‘HARKing’ (‘hypothesizing after results are known’ is defined as 
generating scientific statements exclusively based on the analysis 
of huge datasets without previous hypotheses
87 , 88
and to guarantee 
consistency of the results, it is necessary to apply e.g. resampling 
techniques such as subsampling.
47
Alternatively, the well estab -
lished machine learning practice of cross-validation: i.e. splitting 
the dataset into multiple parts before the beginning of the evalu -
ation can be used. There, one data part is used for generating new 
hypotheses and another part for subsequently statistically testing 
these hypotheses. Accumulation of such data-driven knowledge 
may finally lead to a new theory.
Ideally, the verbally defined (narrative) hypotheses to be experi -
mentally tested would be derived from such an underlying theory. 
As Kurt Lewin, the father of modern experimental psychology, 
pointed out: ‘There is nothing so practical as a good theory’.
89
If 
we had theorized that the microprocessor from the thought experi -
ment above performs arithmetic calculations, we could have, e.g. 
derived the hypothesis that there must be something like 1-bit ad -
ders, and could have searched for them specifically.
Conversely, Allan Newell, one of the fathers of artificial intelli -
gence, stated that ‘You can‘t play 20 questions with nature and 
win’.
90
This suggests that testing one narrative hypothesis after an -
other will never lead to a mechanistic understanding. Therefore, 
this raises the fundamental question of what it actually means to 
‘understand’ a system.
Yuri Lazebnik argued that understanding of a system is 
achieved when one could fix a broken implementation: 
‘Understanding of a particular region or part of a system would occur 
when one could describe so accurately the inputs, the transformation, 
and the outputs that one brain region could be replaced with an entirely 
synthetic component’.
67
In engineering terms, this understanding can be simply de -
scribed as y = f (x), where x is the input, y is the output and f is the 
transformation.
According to David Marr, one can seek to understand a system 
at (at least) three complementary levels of analysis.
71
He distin -
guished the computational, the algorithmic and the implementa -
tional level of analysis ( Fig. 1A ). The computational level is the 
most coarse-grained level of analysis. It asks what computational 
problem is the system seeking to solve, that results in the observed 
phenomena; in our context, phantom perceptions like tinnitus. 
This level of analysis is addressed by the fields of psychology and 
cognitive neuroscience. In contrast, the implementational level re -
presents the most fine-grained description of a system. Here, the 
system’s concrete physical layout is analysed. In computer science 
and engineering, this corresponds to the exact hardware architec -
ture and the individual software realization, with a particular pro -
gramming language. In the brain, where there exists no clear 
distinction between software and hardware (or wetware), this level 
of description corresponds to the structural design of ion channels, 
synapses, neurons, local circuits and larger systems, and the 
physiological processes these components are subject to. This level 
of analysis can be considered as the hallmark of physiology and 
neurobiology. Finally, the algorithmic level takes an intermediate 
position between the previously described levels. It is about which 
algorithms—that are physically realized at the implementational 
level—the system employs to manipulate its internal representa -
tions, in order to solve the tasks and problems identified at the com -
putational level. In computer science, the algorithmic level would 
be described independently of a specific programming language 
by abstract pseudocode.
Indeed, there are ways of moving between the different levels of 
description, afforded by ‘cognitive computational models’
91
and 
‘cognitive computational neuroscience’.
92
Thus, in both fields, cog -
nitive processes are simulated or recapitulated in silico, however, 
cognitive computational neuroscience uses—in contrast to ‘cogni -
tive computational models’—neural networks as basis of the simu -
lations. Therefore, cognitive computational neuroscience gives us 
an idea how processing might work algorithmically in the brain. 
Note that the similar terms (cognitive computational neuroscience 
and cognitive computational models) reflect the long—and not al -
ways straight-forward—history of science of mind. Indeed, very re -
cently the term cognitive computational neuroscience is more and 
more replaced by the term neuroAI.
93 , 94
We argue that analysis at the algorithmic level is most crucial to 
understand auditory phantom perceptions like tinnitus or Zwicker 
tone. Only by knowing the algorithms that underlie normal audi -
tory perception, we will gain a detailed understanding of what 
exactly happens under certain pathological conditions such as 
4814 | BRAIN 2023: 146; 4809–4825                                                                                                                         A. Schilling et al.
hearing loss, and which processes eventually cause the develop -
ment of tinnitus, so that we can mitigate or reverse these processes.
Which discipline addresses this level of analysis in tinnitus re -
search? Computational neuroscience comes to mind immediately. 
However, in ‘good old-fashioned’ computational neuroscience, 
great efforts have been made to model the physiological and bio -
physical processes at the level of single neurons, dendrites, axons, 
synapses or even ion channels, leading to increasingly complex 
computational models. These models, mostly based on systems 
of coupled differential equations, can mimic experimental data in 
great detail. Perhaps the most popular among these models is the 
famous Hodgkin-Huxley model,
95
which reproduces the temporal 
course of the membrane potential of a single neuron with impres -
sive accuracy. These types of models are of great importance to 
deepen our understanding of fundamental physiological processes. 
However, in our opinion, they also must be considered as belonging 
to the implementational level of analysis, since they merely de -
scribe the physical realization of the algorithms, rather than the al -
gorithms themselves.
In the following section, we will discuss emerging research di -
rections that speak to the algorithmic level of analysis in the con -
text of tinnitus research.
The integration of artificial intelligence in tinnitus 
research
As we argued above, hypothesis testing alone does not lead to a 
mechanistic understanding. Instead, it needs to be complemented 
by the construction of task-pointing computational models, since 
only synthesis in a computer simulation can reveal the interaction 
of proposed components entailed by a mechanistic explanation, i.e. 
which algorithms are realized, and whether they can account for 
the perceptual, cognitive or behavioural function in question. As 
Nobel laureate and theoretical physicist Richard Feynman pointed 
out: ‘What I cannot create, I do not understand’.
Along these lines, one may consider extending the four goals of 
psychology, i.e. to describe, explain, predict and change cognition 
and behaviour,
72
by adding a fifth one: to build synthetic cognition 
and behaviour. This is in the tradition of ‘Walter’s tortoises’,
96-99
one major attempt to build synthetic cognition and behaviour using 
analogue electronics. This approach could be revisited in the 21st 
century, using artificial deep neural networks.
As pointed out in previous publications,
69 , 100-103
these computa -
tional models can be based on constructs from AI, for example deep 
learning.
104 , 105
A related development in AI rests upon the explicit 
use of generative models, leading to formulations of action and per -
ception, in terms of predictive coding and active inference. 
Examples of their application to auditory processing and hallucina -
tions range from examining the role of certain oscillatory frequen -
cies in message passing, through to simulations of active listening 
and speech perception.
106-112
Artificial deep neural networks are designed to solve problems 
clearly defined at the computational level of analysis, in our case 
auditory perception tasks like, e.g. speech recognition. These mod -
els are precisely defined at an algorithmic level, which is complete -
ly independent from any individual programming language or 
specific software library, i.e. the implementational level of analysis. 
Hence, these algorithms could, at least in principle, also be realized 
in the brain as biological neural networks. Once we have built such 
models and algorithms in computer simulations, we can subse -
quently compare their dynamics and internal representations 
with brain—and behavioural—data in order to reject or adjust 
putative models, thereby successively increasing biological fidel -
ity.
69
Vice versa, the ensuing models may also serve to generate 
new testable hypotheses about cognitive and neural processing in 
auditory neuroscience.
As mentioned above, this research approach—combining AI, 
cognitive science and neuroscience—has been coined as CCN.
69
Furthermore, besides the advantages discussed above, this ap -
proach furnishes the opportunity for in silico testing of new, puta -
tive treatment interventions for conditions like tinnitus, prior to 
in vivo experiments. In this way, CCN may even serve to reduce 
the number of animal experiments.
However, we note that CCN of auditory perception is not only 
beneficial for neuroscience. As noted in Hassabis et al.,
113
under -
standing biological brains could play a vital role in building intelli -
gent machines, and that current advances in AI have been inspired 
by the study of neural computation in humans and animals. Thus, 
CCN of auditory perception may contribute to the development of 
neuroscience-inspired AI systems in the domain of natural lan -
guage processing.
114
Finally, neuroscience may even serve to inves -
tigate machine behaviour,
115
i.e. illuminate the black box of deep 
learning.
116 , 117
However, so far, most AI research does not even at -
tempt to mimic or understand the brain or biology in general.
In other neuroscientific strands, such as research on spatial 
navigation, the fusion of classical neuroscience and AI has already 
led to major breakthroughs and still promises further advances in 
the future.
118
For example, Stachenfeld and colleagues developed 
a mathematical framework for the function of place and grid cells 
in the entorhinal-hippocampal system based on predictive cod -
ing.
119 , 120
On the other hand, researchers from Google DeepMind 
developed artificial agents based on Long-Short-Term-Memory 
(LSTM)
121 , 122
neurons, in which place and grid cells emerged auto -
matically.
123
In another AI model, Gerum and coworkers
124
showed 
that spatial navigation in a maze could be achieved by very small 
neural networks, which are trained with an evolutionary algorithm 
and are evolutionary pruned.
Towards a unified model of tinnitus 
development
The hierarchy of the different tinnitus models
In the following section, we describe a path towards a CCN of tin -
nitus research. Thus, in a first step we have to go back to 
Labzebnik
67
and find a way to communicate efficiently and formal -
ly about various tinnitus models. Extant tinnitus models can be 
sorted by the different levels of analysis according to Marr and 
Poggio.
71
This means that each model can be assigned to one or 
more of the three categories ( Fig. 1B ): implementational level (mo -
lecular mechanisms, synapses etc.), algorithmic level (how neural 
signals are translated to information processing) and computation -
al level (what are the basic mathematical imperatives for process -
ing; see also ‘What does it mean to understand a system?’).
The three levels of analysis can be easily illustrated with the 
Lateral Inhibition Model of tinnitus, which describes tinnitus as a 
result of decreased lateral inhibition
23 , 125
due to decreased cochlear 
input; e.g. caused by a noised-induced cochlear synaptopathy.
6
Thus, the lateral inhibition model explains tinnitus on all different 
levels of description. The implementational level (see Marr’s level 
of analysis in Fig. 1A ), which corresponds to the molecular mechan -
isms of lateral inhibition, is nearly fully understood. For example, in 
the DCN cartwheel cells release glycine to inhibit fusiform cells, 
Models of auditory phantom perception                                                                                BRAIN 2023: 146; 4809–4825 | 4815
which are excitatory.
126-128
The computational role of inhibition is 
to narrow the input range of the fusiform cells.
128
To provide 
such contrast enhancement via lateral inhibition, neurons sur -
rounding a certain excitatory neuron, which receives auditory in -
put, are inhibited. This wiring scheme ‘sharpens’ the tuning 
curves of neurons along the auditory pathway. The wiring scheme 
corresponds to the algorithmic level of analysis. The computational 
level of description is the mathematical description of decreased 
lateral inhibition. Thus, hearing loss leads to decreased input 
from the cochlea, which causes a decreased firing rate of the inhibi -
tory neurons and thus to disinhibition of subsequent excitatory 
neurons. These properties can be easily written down in simple 
mathematical formulas. This means that the underlying mechan -
isms of the lateral inhibition model of tinnitus are fully understood 
from specific neurotransmitter processes to an abstract mathemat -
ical formulation. This is the goal of cognitive computational neuro -
science. However, the fact that the model explains tinnitus 
manifestation on all scales does not say anything about the correct -
ness of the model’s predictions. Indeed, a good model should be 
understood on all scales (implementational to computational), 
but it must also fit experimental observations, which is not the 
case in the Lateral Inhibition Model. Other models trying to explain 
tinnitus do not provide full explanatory power.
The thalamic bursting theory—which proposes that bursting 
neurons in the thalamus cause tinnitus—has a valid explanation 
for the origin of the spike bursts (low threshold calcium spikes, 
for details see Jeanmonod et al.
60
). However, it remains elusive, in 
terms of how these bursts cause tinnitus. Other top-down models 
—such as the predictive coding model,
52
based on the Bayesian 
Brain theory—provide a valid mathematical description of the pro -
posed mechanisms, but do not provide a full explanation of how the 
Bayesian statistics can be implemented in a neural network and 
thus in the brain.
129
However, there exist some first approaches to -
ward neural networks for Bayesian inference which will ultimately 
prove possible, but are still not fully developed.
130-132
Other tinnitus 
models describe macro-phenomena such as the thalamo-cortical 
dysrhythmia,
59
or describe tinnitus as a result of overlapping neur -
al circuits.
63
Those models are phenomenological, but do not pro -
vide a mathematical description and thus are difficult to falsify or 
test in silico.
A critical role of stochastic resonance and central 
noise
In the following paragraph we provide an in-depth discussion of 
central noise and central gain, as possible causes for tinnitus, and 
consider how to adjudicate between—or combine—these two the -
ories. To discuss these two models and their relationship, it is ne -
cessary to introduce a proper nomenclature. Thus, in the 
following we refer to the mathematical description of Zeng, who 
describes central gain as a linear amplification factor g, which in -
creases the input signal I (s = subjectively perceived loudness re -
spectively evoked neural activity; cf. Chrostowski et al.
32
). Central 
noise N is a further additive term
33 , 133
( Eq. 1 ).
s = g · I + N (1) 
Central gain increase is a collective term summarizing all me -
chanisms that lead to an increased amplification of the input sig -
nal (I ) along the auditory pathway (for an extensive review, see 
Auerbach et al.
134
). Therefore, the term central gain increase can 
refer to a decrease in inhibitory synaptic responses, an increase 
in excitatory synaptic responses, as well as enhanced intrinsic 
neuronal excitability.
134
All of these mechanisms cause a multi -
plicative amplification of the input signal (amplification 
factor: g). To sharpen the scientific language, it is necessary to 
distinguish between the observable effect (central gain increase) 
and the underlying neuronal principles (e.g. homeostatic plasti -
city
27 , 134
). Central gain increase could be caused by homeostatic 
plasticity, which means that the average spike rate of affected 
neurons—after a decrease of neuronal input due to a hearing 
loss—is kept constant by plastic changes of the system (e.g. en -
hanced intrinsic excitability, synaptic scaling, meta-plasticity
134
). 
Central gain and homeostatic plasticity are often used as syno -
nyms in the context of tinnitus models, although they describe 
the problem on different levels.
The central noise model—in contrast to the central gain model 
—describes tinnitus as a consequence of increased spontaneous 
activity, which is added to the input signal (additive term, N ).
33
In 
analogy to the relation of central gain and homeostatic plasticity, 
the underlying principle of the central noise model is stochastic 
resonance.
135-137
The original central noise model of Zeng from 
2013 was exclusively based on psychophysical considerations and 
measurements, which means that the term s in Eq. 1 was meant 
to be the subjectively perceived loudness.
33
Furthermore, the ori -
ginal model makes no statements on the nature of the central 
noise, or on higher brain functions such as thalamic gating or pre -
dictive coding etc., and thus provides no explanation what the 
neuronal signal looks like and why an addition of noise causes an 
ongoing conscious percept.
The novelty of the stochastic resonance model is based on the 
idea that the abstract concept of an additive central noise can be in -
terpreted as real intrinsically generated neural noise, which in -
creases hearing ability by exploiting the stochastic resonance 
effect. Thus, the term s in Eq. 1 is re-interpreted as actual neural 
activity.
We categorized the stochastic resonance model
18 , 35 , 37
as an al -
gorithmic level model on Marr’s scale ( Fig. 1 ), which means that 
the calculations ( Eq. 1 and the calculation of the autocorrelation 
function, cf. below) necessary to leverage the stochastic resonance 
effect should be linked to the neural substrate of the auditory path -
way. This corresponds to the implementational level according to 
Marr. The stochastic resonance model ( Fig. 2 ) is based on the idea 
that the auditory system continuously optimizes sensitivity via a 
feedback loop, which adapts the amplitude of the additive noise 
(central noise) to maximize information transmission. The infor -
mation transmission is quantified via the autocorrelation of the sig -
nal.
18 , 35
Thus, one might call the inverse autocorrelation function 
the cost-function to be minimized. However, to calculate the auto -
correlation of the signal, so-called neuronal delay lines are needed, 
which are prominent in two brain regions the cerebellum and the 
DCN.
138
The mechanism behind the auto-correlation calculation 
based on delay lines is based on the fact that the signal transmis -
sion is slowed down by the delay line through inter-neurons or un -
myelinated nerve fibres.
42
Thus, the delayed signal is then 
compared to the same signal at a later time point, which was not 
delayed. The delay serves the purpose to generate a time shift (in 
mathematical formulation of auto-correlation function commonly 
termed as lag-time τ), which allows us to compare one signal 
stream at several time points with itself.
139 , 140
Another strong argument for the validity of the stochastic res -
onance model is the fact that otherwise there is no plausible ex -
planation for the cross-modal input from the somatosensory 
system to the DCN,
141 , 142
except the notion that the somatosensory 
4816 | BRAIN 2023: 146; 4809–4825                                                                                                                         A. Schilling et al.
system serves as the noise-generator of the stochastic resonance 
feedback loop. 18 It is common knowledge that—for the stochastic 
resonance effect—the exact spectral composition of noise is irrele -
vant.92,143This suggests spontaneously firing neurons in the som -
atosensory system are sufficient to trigger the stochastic 
resonance effect. In summary, the theoretical construct of an infor -
mation transmission maximizing feedback can be mapped onto 
certain neuronal structures, with an architecture that is sufficient 
to perform the requisite calculations.
The whole stochastic resonance model is an intra-frequency 
channel model, which means that cross-talk between different 
frequency channels is not necessary to explain the emergence of 
tinnitus. As already described above, tinnitus is highly related to 
frequency channels, which are impaired by e.g. synaptopathy in 
the cochlea and a resulting (hidden) hearing loss.
14 Frequencies 
are represented tonotopical along the whole auditory pathway 
up to the auditory cortex.
144 Thus, it seems plausible that the 
amplitude of the neural noise added to each frequency channel 
of the DCN is tuned individually. Such a channel-wise optimiza
-
tion of the noise amplitude is the simplest explanation according 
to Occam’s razor and provides a plausible explanation for the fact 
that the tinnitus pitch is highly correlated to impaired frequency 
channels.
37
Tinnitus as a result of multiplicative central gain or 
additive central noise?
Central gain increase and central noise increase cannot be fully de -
coupled, for example, an increased excitability of neurons along the 
auditory pathway caused by homeostatic plasticity automatically 
leads to an amplification of neural noise. The fact that the additive 
neural noise (central noise) is amplified (central gain) along the 
auditory pathway is a direct consequence of the neuroanatomy of 
the auditory system. As the neural noise is already added in the 
DCN
18 being the first processing stage of the auditory pathway, 
multiplicative amplification (central gain) has necessarily an effect 
on the noise.
145
Thus, Eq. 1could be altered so that the amplification factor also 
has an effect on the central noise:
s= g · (I+ N) (2) 
As described above, the homeostatic plasticity mechanisms medi -
ating central gain increase have been implicated in tinnitus gener -
ation,146 however, these mechanisms are simply too slow to 
explain acute tinnitus phenomena after a noise trauma caused by 
a sudden loud stimulus.
147
In contrast, neural circuits operating on faster time scales can 
explain acute tinnitus: namely, tinnitus is caused by a subcortical 
feedback loop adapting neural noise input into the auditory sys -
tem. 35 As described above and illustrated in Fig. 2we suggest that 
stochastic resonance plays a critical role in not only generating tin-
nitus but also restoring hearing to a certain degree.18,34,36
To illustrate this role, we interpret Eq. 2in a classical signal de-
tection task, in which the neural signal(s) has to reach a threshold 
for the input signal I to be detected.
In cases of hearing loss, the input I is effectively reduced. 
Therefore, to reach the same neural threshold, one could increase 
either the central noise N
, or the central gain g, or both. Because in-
creasing gain results in a squared increase in variance,133 which in -
creases the difficulty of signal detection, it is not the most 
economical means of compensating for hearing loss in cognitive 
neural computation (e.g. Occam’s razor). Instead, it makes sense 
to add internal neural noise to lift weak input signals above the sen
-
sory threshold by means of stochastic resonance. 135-137In trad -
itional stochastic resonance, a non-linear device such as hard 
thresholding and periodic signals, are needed.
136 Recently, it has 
been shown that autocorrelation can serve as an estimator for the 
information content of the signal, even if it is non-periodic.
35
The critical role of stochastic resonance is supported by broad 
empirical evidence: first, additional intrinsic neural noise18,41 as 
well as external acoustic noise 38 can improve pure-tone hearing 
thresholds by ∼5 dB. However, this 5 dB threshold decrease (i.e. im-
provement) does not explain why this mechanism is evolutionary 
Figure 2 Stochastic resonance model of tinnitus induction. In the healthy auditory system, the input signal (A) can pass the detection threshold result-
ing in a supra-threshold signal as output (B). In case of hearing loss, the input signal remains below the threshold (C), resulting in zero output. However, 
if the optimum amount neural noise (D) is added to the weak signal, then signal plus noise can pass the threshold again (E), making a previously un-
detectable signal, detectable again (F). The optimum amount of noise depends on the momentary statistics of the input signal and is continuously ad-
justed via a feedback loop. This processing principle is called adaptive stochastic resonance.
Models of auditory phantom perception                                                                                BRAIN 2023: 146; 4809–4825 | 4817
advantageous, as the cost of a potentially annoying and morbid tin -
nitus perception may be high. In a computational model, it has 
been shown that frequency-specific intrinsic neural noise has the 
potential to significantly improve speech recognition by a far larger 
amount (up to a factor of 2).
49
This improvement in speech compre -
hension and the perception of complex sounds—which could also 
be important for orienting animals as warning sounds—could be 
an explanation for the emergence of this mechanism in our audi -
tory system during evolution. Furthermore, a significantly im -
proved speech perception could have major positive effects and 
might contribute to a decreased cognitive decline in elderly 
people.
148 , 149
In recent studies, the fact that different modalities exploit sto -
chastic resonance to improve the signal has been proven.
40 , 150
It 
seems that stochastic resonance and especially cross-modal sto -
chastic resonance is a universal principle of sensory processing.
36
Second, central noise is needed to stabilize a biological system. 
Zeng showed that ‘mathematically, the loudness at threshold is 
infinite when the internal noise is zero (c = 0), and vice versa. This 
is a fundamental argument for why the brain has or needs 
internal noise because infinite loudness is clearly biologically 
unacceptable’.
151
Third, as described above, the central noise model based on the 
stochastic resonance mechanism provides a mechanistic explan -
ation for the purpose of the somatosensory projections to auditory 
nuclei such as the DCN.
142 , 152 , 153
In fact, very recently, Koops and 
Eggermont argued that ‘increased and uncorrelated noise, poten -
tially the result from a noise source outside of the auditory 
pathway’
34
might play a major role in tinnitus development. 
Potentially, this somatosensory input is nothing else than intrinsic -
ally generated neural noise, which is modulated in the DCN to le -
verage stochastic resonance in the auditory system. This theory 
accords with the finding that tinnitus can be modulated by somato -
sensory input like, e.g. jaw movement.
154-156
Furthermore, tinnitus 
development can be prevented
157-160
or suppressed
158-160
by the 
presentation of external acoustic noise, which works best when 
the noise spectrum covers the impaired frequencies and the tin -
nitus pitch.
158-160
In a recent study, a novel approach was devel -
oped combining somatosensory stimulation with auditory 
stimulation, to modulate the tinnitus loudness.
161
Finally, it has 
been demonstrated that electrotactile stimulation of the fingertips 
enhances cochlear implant speech recognition in noise,
162
Mandarin tone recognition
163
and melody recognition.
164
While 
the authors did not make any mention of stochastic resonance or 
internal noise, it is a reasonable assertion that the observed effect 
might have acted via cross-modal stochastic resonance.
36
These arguments suggest that tinnitus is indeed caused by addi -
tive neural noise (central noise) instead of a multiplicative gain. 
Central gain induced tinnitus would be characterized by increased 
evoked activity along the auditory pathway in tinnitus patients. 
Thus, auditory brainstem responses should have higher ampli -
tudes in tinnitus patients compared to control patients. However, 
an increased evoked activity in tinnitus was refuted in several re -
cent human patient as well as in animal studies.
165-168
Increased 
evoked neural activity is related to hypersensitivity against mild 
sounds, the so-called hyperacusis. Thus, increased central gain is 
potentially a better fit to explain hyperacusis rather than 
tinnitus.
167 , 168
Hyperacusis could be one missing key to disentangle central 
noise and central gain adaptations of the auditory system.
As described above, central gain and central noise cannot be 
fully disambiguated ( Eq. 2 ) as both auditory input and added neural 
noise is amplified via homeostatic plasticity along the auditory 
pathway. Therefore, tinnitus severity should correlate with ampli -
fication along the auditory pathway, which means that tinnitus se -
verity should be highly correlated with the hyperacusis severity. 
This correlation was found in 2020 by Cederroth and coworkers.
169
In summary, the three findings that first tinnitus patients without 
hyperacusis show no increase in evoked activity,
165 , 167
second hy -
peracusis patients show increased evoked activity
167
and third tin -
nitus severity correlates with hyperacusis,
169
are a strong 
indication for the theory described above. To put the theory in a 
nutshell: central noise increase causes tinnitus, central gain in -
crease causes hyperacusis, and central gain increase does not just 
cause hyperacusis but also amplifies the neural noise perceived 
as tinnitus.
Tinnitus and the Bayesian brain
The combined central gain and the central noise model provides a 
sophisticated and mathematically well developed explanation for 
the tinnitus-related neural hyperactivity in the brainstem. 
However, these theories do not explain why this hyperactivity is 
transmitted through the thalamus and induces a conscious experi -
ence. Indeed, there exist several mechanisms in the brain that are 
supposed to prevent ongoing neural activity to be transmitted to 
the cortex
170
and becoming a conscious and disturbing auditory 
percept. Up to now it is unclear why these mechanisms fail to 
do so. Furthermore, the stochastic resonance model does not 
make predictions on tinnitus heterogeneity. In particular, tin -
nitus is probably always caused by hearing loss, but hearing 
loss does not necessarily lead to tinnitus.
171
Additionally, the sto -
chastic resonance model predicts that hearing aids should at 
least milden tinnitus, due to a downregulation of added neural 
noise in the DCN control circuit. However, while this is true for 
some patients, hearing aids do not milden tinnitus in all pa -
tients,
172
and this heterogeneity is not covered by the stochastic 
resonance model.
In the following, we provide an explanation of how and why the 
added central noise bypasses the filter mechanism of the brain and 
how this might also deliver solution approaches to the problem of 
tinnitus heterogeneity.
The only model with a solid mathematical background dealing 
with these issues is the sensory precision model from 
Sedley et al.,
52
which is based on the algorithmic formulation of 
predictive coding within the computational ‘Bayesian brain’ hy -
pothesis.
53 , 65 , 129 , 173-175
Bayesian formulations of predictive process -
ing are based on the Bayes theorem ( Eq. 3 )
176 , 177
that describes, 
mathematically, how to update beliefs in the light of new incoming 
information. Furthermore, this account also proposes a solution to 
other paradoxical evidence from the tinnitus literature, including 
that certain types of brain activity linked to perception (gamma os -
cillations) can show both positive and negative correlations with 
perceived tinnitus loudness, depending on how tinnitus loudness 
is manipulated.
178
p(x|o) / p(o|x)p(x) (3) 
Here, o corresponds to observations (e.g. sensorineural responses) 
and x to their inferred causes (e.g. auditory loudness). In this con -
text, the brain is continuously updating its posterior belief distribu -
tion p(x|o) about actual sound intensity x, given auditory afferents or 
observations o. This update is achieved by combining the prior ex -
pectations p(x) ( Fig. 3A ), descending from the higher regions of the 
4818 | BRAIN 2023: 146; 4809–4825                                                                                                                         A. Schilling et al.
processing hierarchy, with sensory input—reporting the likelihood 
or sensory evidence—ascending from below [ p(o|x), Fig. 3B]. 
‘Likelihood’ refers to the probability that the pattern of sensory in-
put indicates a particular underlying sensory event or cause. In the 
healthy system (no hearing loss, Fig. 3A
–C) the default prediction 
(prior, Fig. 3A) would be that there is no auditory input. In silence, 
the likelihood is a broad distribution with a low mean (Fig. 3B ), as 
there is exclusively spontaneous activity. This spontaneous activity 
has been termed a ‘tinnitus precursor’, which usually has a low pre
-
cision and is therefore not interpreted as auditory input. Reducing 
sensory precision is also called sensory attenuation. However, if the 
precision of the tinnitus precursor increases (or, sensory attenu
-
ation is insufficient) then the posterior shifts to the perception of 
a sound, and tinnitus occurs.
The occurrence of an external sound (evoked response) shifts 
the likelihood to higher values and the precision of the likelihood 
rises, as neuronal activity encoding a certain loudness level 
is generated, with a high precision. Therefore, the posterior 
belief is—although the prior predicts no input—that there is an 
auditory input, as precise sensory evidence shifts the posterior 
to higher values.
Starting from this configuration, the predictive coding model of 
tinnitus development can be structured in three main steps: (i) 
hearing loss (Fig. 3D
); (ii) compensation of hearing loss through sto-
chastic resonance and central gain; and (iii) increased precision of 
this spontaneous central noise (tinnitus precursor). A fourth step 
is thought to result in tinnitus becoming chronic, which is adjust
-
ment of auditory priors (shifting away from ‘silence’ as the default, 
to expecting a tinnitus-like sound); this allows the tinnitus precur-
sor to be perceived even at relatively low precision levels, as it 
shows some concordance with auditory priors. The first step is 
hearing loss, which means that there is loss of precise input from 
the cochlea. Thus, the activity of the neurons along the auditory 
pathway is attenuated, which means that the likelihood becomes 
less precise in relation to the posterior (
Fig. 3E). Thus, the posterior 
is shifted to lower values (Fig. 3F), and things are perceived as qui-
eter or silent. This means that hearing loss and predictive coding 
alone are not sufficient to explain tinnitus. In a next step, the de -
creased input through hearing loss is compensated by adding neur -
al noise by means of stochastic resonance ( Fig. 3G). This means that 
the mean of the likelihood [p
(o|x) in Eq. 4, Fig. 3H, dark blue distribu-
tion] is increased as neural activity (
N in Eq. 2) is added to auditory 
Figure 3 Predictive coding model of tinnitus induction. The posterior (represents the percept) is the product of the likelihood (bottom-up neuronal sig-
nal) and the prior (top-down prediction of the auditory input). The predictive coding hypothesis of tinnitus development is formalized in the Bayesian 
brain framework. The brain predicts the likelihood of the occurrence of a certain auditory input loudness [p(x), x: model] in one certain frequency chan-
nel. The prior (prediction) is based on the experiences on how often certain auditory stimuli occurs and has nothing to do with the present neuronal 
signal coming from the cochlea. In the healthy case the prior distribution has a low mean (standard auditory input is zero, A). The likelihood p(o|x) (B) 
represents the bottom-up signal, respectively, the measurements of the sensor (cochlea and brainstem). The posterior is the probability that under the 
condition of one particular neuronal signal (spike rate) a certain stimulus loudness is the cause of that neural activity. In the healthy case, the low spon-
taneous activity (B) is most probably the consequence of the absence of an auditory input. The effect that low spontaneous activity (with low precision) 
is assumed to be the consequence of no auditory input is called sensory attenuation (C, left side of the dashed curve). Decreased cochlear input due to 
hearing loss (D) shifts the likelihood (E) and consequently the posterior (F) to lower values, which means that a hearing loss does not directly cause 
tinnitus. Central noise (G) increases the spontaneous activity and thus increases the mean of the likelihood (H, dark blue distribution). The product 
of p(x) and p(o|x) is shifted to higher values (I, dark blue). Potentially, the precision of the likelihood is also increased (lower variance) through the central 
noise effect (H, cyan distribution), which further shifts the posterior to higher values (I, cyan), as the mean of the product of the probabilities is weighted 
with the precision. The increased neuronal activity is interpreted as auditory input, which means that there is a tinnitus percept. This effect can be 
amplified, as the continuous change of neural activity (through central gain and central noise) leads to continuous miss predictions. The prediction 
error between prior [p(x)] and likelihood [p(o|x)] is decreased by adapting the prior (J). Therefore, tinnitus becomes the standard prediction, which fur-
ther manifests the phantom percept (L). The effect might be the correlate of chronic manifestation of tinnitus.
Models of auditory phantom perception                                                                                BRAIN 2023: 146; 4809–4825 | 4819
input through the mechanism of stochastic resonance. This effect 
is further increased by the central gain amplification along the 
auditory pathway (g in Eq. 2 , likelihood Fig. 3H , cyan distribution), 
further amplifying tinnitus loudness (posterior belief: Fig. 3I ). 
There are good reasons to assume that the precision of the neuron -
al signal is increased through subcortical phenomena: as described 
above, internal neural noise is not comparable with the pressure 
fluctuations (white uncorrelated acoustic noise) used to lift sub -
threshold auditory signal above the detection threshold, as shown 
be Zeng and coworkers.
38
Thus, noise increase might entail the 
addition of regular spike trains. Therefore, as the stochastic reson -
ance feedback loop optimizes for a certain noise amplitude with 
low variance the precision of the likelihood might be increased 
(note that stochastic resonance is not limited to any particular 
noise
92 , 143
). Nevertheless, it is not obvious that central noise in -
creases the sensory precision. The addition of regular spike trains 
or patterns to the cochlear signal might cause the system to run 
in an attractor. The number of possible neural states is limited as 
the neural noise causes a continuous activity and makes 
low-activity states very unlikely. This is in line with the therapeutic 
approaches of Tass and Popovych,
179
who tried to get out of this 
neuronal attractor by presenting acoustic stimuli. An amplification 
through central gain in contrast to an additive noise might have the 
opposite effect, as a multiplicative term would increase the number 
of possible neural activity patterns. This fact indicates that central 
noise is a better complement to the predictive coding model of tin -
nitus development. It is an upcoming challenge and important 
milestone to unravel the exact neuronal patterns that fulfil the 
properties described above.
Besides the fact that the increased spontaneous activity through 
central noise and central gain mechanisms changes the likelihood, 
it also leads to continuous prediction errors. Therefore, the final 
part of the model is an update of the prior ( Fig. 3J ). Thus, the prior 
is shifted to higher input loudness values to minimize the error be -
tween likelihood and predictions ( Fig. 3K ). Physiologically, any ac -
companying increase in the precision of these priors is usually 
associated with an increase in the postsynaptic gain or excitability 
of neuronal populations reporting prediction errors (usually super -
ficial pyramidal cells in the cortex). See Benrimoh et al.,
107
Bastos 
et al.,
173
Adams et al.,
180
Friston et al.,
181
Kanai et al.,
182
Shipp
183
and Sterzer et al.
184
for a predictive coding account of neuronal mes -
sage passing and the role of precision weighted prediction errors in 
hallucinatory phenomena.
In short, the result is that the presence of auditory input be -
comes the new default prediction and shifts the posterior to higher 
values ( Fig. 3L ). This final step could be the correlate of tinnitus and 
might explain why—in some patients—the restoration of hearing 
through, e.g. hearing aids does not cure tinnitus.
An important question is why divergent behaviour should occur 
in optimally functioning systems such as those involved in stochas -
tic resonance and predictive coding; i.e. why should similar condi -
tions, such as hearing loss, result in accepting central noise as a 
percept in some cases but not others. To address this, we must con -
sider that what is ‘optimal’ varies according to the hierarchical level 
concerned, and the situational context. With regard to hierarchical 
level, accepting central noise as a percept reduces prediction error 
at the lower hierarchical level where the noise is generated, but (at 
least initially) results in the introduction of a prediction error at 
higher hierarchical levels by introducing an unexpected percept. 
Thus, the balance of priority between hierarchical levels may 
help to explain the emergence (or non-emergence) of tinnitus in 
different instances. Regarding wider context, we consider here 
stress as one example; in certain stressful situations, one is hyper -
vigilant to a broad range of sensory inputs, particularly those which 
might indicate potential threats, which can include novel or previ -
ously unanticipated ones. Such stress can be considered a relative 
shift of precision away from sensory priors, towards sensory likeli -
hoods. This might explain the initial onset of tinnitus during stress, 
which has been reported.
185
However, once default sensory priors 
have adjusted to accept tinnitus, the conflict between hierarchical 
levels disappears, as low-level likelihood and high-level prediction 
become concordant.
Conclusion and outlook
In conclusion, the combination of the process theory of central 
noise increase and adaptive stochastic resonance—as a bottom-up 
mechanism—together with the computational model of predictive 
coding—as a complementary top-down mechanism—provides an 
integrated explanation of tinnitus emergence. Here, bottom-up re -
fers to the overall information flow, i.e. modification of signals ori -
ginating from lower brain structures, like the cochlear nucleus and 
primary auditory cortex. It is important to note that this does not 
imply that the predictive coding framework is solely top-down or 
that the stochastic resonance model is solely bottom-up.
Furthermore, the models provide a mathematical framework, 
which can be used to make quantitative predictions that can be 
tested through novel experimental paradigms, e.g. for the calcula -
tion of the autocorrelation function, specific neuronal delay-lines 
are needed. As the neuroanatomy along the auditory pathway is 
mostly known, one could calculate how long specific delay lines 
are and if they fit this hypothesis. Furthermore, one can look specif -
ically for the noise generator—most probably in the somatosensory 
system—and characterize, e.g. the spectral composition of its out -
put. Independent of these predictions, since both stochastic reson -
ance and predictive coding as universal processing mechanisms 
are ubiquitous in the brain, we speculate that the presented inte -
grative framework may extend to the perception of other sensory 
modalities and even beyond to certain aspects of cognition and be -
haviour in general.
A current challenge is a network theory of predictive coding, 
which explains how these computations are implemented in the 
brain.
129
Several studies have attempted to place predictive coding 
in the larger context of Bayesian belief updating in the 
brain.
173 , 181 , 183 , 186-188
Furthermore, to unravel the exact characteris -
tics of the neural noise necessary to significantly decrease sensory 
precision, is an important challenge that needs to be addressed in 
future studies.
Our integrated model of auditory (phantom) perception demon -
strates that the fusion of computational neuroscience, AI and ex -
perimental neuroscience leads to innovative ideas and paves the 
way for further advances in neuroscience and AI research. For in -
stance, novel evaluation techniques for neurophysiological data 
based on AI and Bayesian statistics were recently established,
189- 
192
the role of noise in neural networks and other biological infor -
mation processing systems was considered
193-196
and the benefit 
and application of noise and randomness in machine learning ap -
proaches was further investigated.
49 , 197 , 198
On the one hand, the fu -
sion of these complementary fields may evince the neural 
mechanisms of tinnitus (CCN
69
) and information processing princi -
ples that underwrite functional brain architectures. On the other 
hand, neuroscience-inspired AI
113
may accelerate research in ma -
chine learning. We hope that the four major steps towards a CCN 
4820 | BRAIN 2023: 146; 4809–4825                                                                                                                         A. Schilling et al.
of tinnitus, i.e. (i) finding an exact language; (ii) developing a mech -
anistic theory; (iii) testing the methods in fully specified test sys -
tems; and (iv) merging AI with computational and experimental 
neuroscience, will afford novel opportunities in tinnitus research.
Acknowledgement
We wish to thank Arnaud Norena for useful discussion.
Funding
This work was funded by the Deutsche Forschungsgemeinschaft 
(DFG, German Research Foundation): grant KR5148/2-1 (project 
number 436456810) to PK, grant KR5148/3-1 (project number 
510395418) to P.K., grant GRK2839 (project number 468527017) to 
P.K., grant SCHI 1482/3-1 (project number 451810794) to A.S., grant 
TZ100/2-1 (project number 510395418) to K.T. Additionally, P.K. 
was supported by the Emerging Talents Initiative (ETI) of the 
University Erlangen-Nuremberg (grant 2019/2-Phil-01), and K.F. is 
supported by funding for the Wellcome Centre for Human 
Neuroimaging (Ref: 205103/Z/16/Z) and a Canada-UK Artificial 
Intelligence Initiative (Ref: ES/T01279X/1). Furthermore, the re -
search leading to these results has received funding from the 
European Research Council (ERC) under the European Union’s 
Horizon 2020 research and innovation program (ERC Grant No. 
810316 to A.M.).
A.M.: ERC Grant No. 810316. A.S.: DFG grant SCHI 1482/3-1 
(project number 451810794). K.F.: Wellcome Centre for Human 
Neuroimaging (Ref: 205103/Z/16/Z); Canada-UK Artificial 
Intelligence Initiative (Ref: ES/T01279X/1). K.T.: DFG grant TZ100/ 
2-1 (project number 510395418). P.K.: DFG grant KR5148/2-1 (project 
number 436456810); DFG grant KR5148/3-1 (project number 
510395418); DFG grant GRK2839 (project number 468527017); 
Emerging Talents Initiative (ETI) of the University Erlangen- 
Nürnberg (grant 2019/2-Phil-01).
Competing interests
The authors report no competing interests.
References
1. Schaette R, Kempter R. Computational models of neurophysio -
logical correlates of tinnitus. Front Syst Neurosci. 2012;6:34.
2. Kaltenbach JA. The dorsal cochlear nucleus as a participant in 
the auditory, attentio naland emotional components of tin -
nitus. Hear Res. 2006;216:224-234.
3. Kaltenbach JA, Afman CE. Hyperactivity in the dorsal cochlear 
nucleus after intense sound expos ure and its resemblance to 
tone-evoked activity: A physiological model for tinnitus. Hear 
Res. 2000;140(1-2):165-172.
4. Kaltenbach JA, Rachel JD, Mathog TA, Zhang J, Falzarano PR, 
Lewandowski M. Cisplatin-induced hyperactivity in the dorsal 
cochlear nucleus and its relation to outer hair cell loss: 
Relevance to tinnitus. J Neurophysiol. 2002;88:699-714.
5. Moore BCJ. Perceptual consequences of cochlear hearing loss 
and their implications for the design of hearing aids. Ear 
Hear. 1996;17:133-161.
6. Tziridis K, Forster J, Buchheidt-Dörfler I, et al. Tinnitus develop -
ment is associated with synaptopathy of inner hair cells in 
Mongolian gerbils. Eur J Neurosci. 2021;54:4768-4780.
7. Eggermont JJ. Hearing loss, hyperacusis, or tinnitus: What is 
modeled in animal research? Hear Res. 2013;295:140-149.
8. Jastreboff PJ, Brennan JF, Coleman JK, Sasaki CT. Phantom 
auditory sensation in rats: An animal model for tinnitus. 
Behav Neurosci. 1988;102:811.
9. Lobarinas E, Sun W, Cushing R, Salvi R. A novel behavioral 
paradigm for assessing tinnitus using schedule-induced poly -
dipsia avoidance conditioning (SIP-AC). Hear Res. 2004;190(1-2): 
109-114.
10. Gerum R, Rahlfs H, Streb M, et al. Open (G) PIAS: An 
open-source solution for the construction of a high- precision 
acoustic startle response setup for tinnitus screening and 
threshold estimation in rodents. Front Behav Neurosci. 2019; 
13:140.
11. Schilling A, Krauss P, Gerum R, Metzner C, Tziridis K, Schulze 
H. A new statistical approach for the evaluation of gap- 
prepulse inhibiti on of the acoustic startle reflex (GPIAS) for 
tinnitus assessment. Front Behav Neurosci. 2017;11:198.
12. Turner JG, Brozoski TJ, Bauer CA, et al. Gap detection deficits in 
rats with tinnitus: A potential novel screening tool. Behav 
Neurosci. 2006;120:188.
13. Eggermont JJ, Roberts LE. Tinnitus: Animal models and find -
ings in humans. Cell Tissue Res. 2015;361:311-336.
14. Dalligna C, Rosito LS, Dalligna DP, et al. Is there an association 
between tinnitus pitch and hearing loss? Otolaryngol Head Neck 
Surg. 2014;151(1_suppl):P213-P213.
15. Keppler H, Degeest S, Dhooge I. The relationship between tin -
nitus pitch and parameters of audiometry and distortion prod -
uct otoacoustic emissions. J Laryngol Otol. 2017;131:1017-1025.
16. Schecklmann M, Vielsmeier V, Steffens T, Landgrebe M, 
Langguth B, Kleinjung T. Relationship between audiometric 
slope and tinnitus pitch in tinnitus patients: Insights into the 
mechanisms of tinnitus generation. PLoS One. 2012;7:e34878.
17. Yakunina N, Nam E-C. Does the tinnitus pitch correlate with 
the frequency of hearing loss? Acta Otolaryngol. 2021;141: 
163-170.
18. Krauss P, Tziridis K, Metzner C, Schilling A, Hoppe U, Schulze 
H. Stochastic resonance controlled upregulation of internal 
noise after hearing loss as a putative cause of tinnitus-related 
neuronal hyperactivity. Front Neurosci. 2016;10:597.
19. König O, Schaette R, Kempter R, Gross M. Course of hearing 
loss and occurrence of tinnitus. Hear Res. 2006;221(1-2):59-64.
20. Moore BCJ. The relationship between tinnitus pitch and the 
edge frequency of the audiogram in individuals with hearing 
impairment and tonal tinnitus. Hear Res. 2010;261(1-2):51-56.
21. Pan T, Tyler RS, Ji H, Coelho C, Gehringer AK, Gogel SA. The re -
lationship between tinnitus pitch and the audiogram. Int J 
Audiol. 2009;48:277-294.
22. Gerken GM. Central tinnitus and lateral inhibition: An auditory 
brainstem model. Hear Res. 1996;97(1-2):75-83.
23. Kral A, Majernik V. On lateral inhibition in the auditory system. 
Gen Physiol Biophys. 1996;15:109-128.
24. Langner G, Wallhäusser-Franke E. Computer simulation of a 
tinnitus model based on labelling of tinnitus activity in the 
auditory cortex. In: Proceedings of the Sixth International 
Tinnitus Seminar. Cambridge The Tinnitus; 1999:20-25.
25. Bruce IC, Bajaj HS, Ko J. Lateral-inhibitory-network models of 
tinnitus. IFAC Proc Vol. 2003;36:359-363.
26. Dominguez M, Becker S, Bruce I, Read H. A spiking neuron 
model of cortical correlates of sensorineural hearing loss: 
Spontaneous firing, synchrony, and tinnitus. Neural Comput. 
2006;18:2942-2958.
27. Turrigiano GG. Homeostatic plasticity in neuronal networks: 
The more things change, the more they stay the same. 
Trends Neurosci. 1999;22:221-227.
Models of auditory phantom perception                                                                                BRAIN 2023: 146; 4809–4825 | 4821
28. Parra LC, Pearlmutter BA. Illusory percepts from auditory 
adaptation. J Acoust Soc Am. 2007;121:1632-1641.
29. Schaette R, Kempter R. Development of tinnitus-related neur -
onal hyperactivity through homeostatic plasticity after hear -
ing loss: A computational model. Eur J Neurosci. 2006;23: 
3124-3138.
30. Schaette R, Kempter R. Development of hyperactivity after 
hearing loss in a computational mod el of the dorsal cochlear 
nucleus depends on neuron response type. Hear Res. 2008; 
240(1-2):57-72.
31. Schaette R, Kempter R. Predicting tinnitus pitch from 
patients’ audiograms with a computation al model for the 
development of neuronal hyperactivity. J Neurophysiol. 2009; 
101:3042-3052.
32. Chrostowski M, Yang L, Wilson HR, Bruce IC, Becker S. Can 
homeostatic plasticity in deafferented primary auditory cortex 
lead to travelling waves of excitation? J Comput Neurosci. 2011; 
30:279-299.
33. Zeng F-G. An active loudness model suggesting tinnitus as in -
creased central noise and hyperacusis as increased nonlinear 
gain. Hear Res. 2013;295:172-179.
34. Koops EA, Eggermont JJ. The thalamus and tinnitus: Bridging 
the gap between animal data and findings in humans. Hear 
Res. 2021;407:108280.
35. Krauss P, Metzner C, Schilling A, et al. Adaptive stochastic res -
onance for unknown and variable input signals. Sci Rep. 2017;7: 
2450.
36. Krauss P, Tziridis K, Schilling A, Schulze H. Cross-modal sto -
chastic resonance as a universal principle to enhances ensory 
processing. Front Neurosci. 2018;12:578.
37. Schilling A, Tziridis K, Schulze H, Krauss P. The stochastic res -
onance model of auditory perception: A unified explanation of 
tinnitus development, Zwicker tone illusion, and residual in -
hibition. Prog Brain Res. 2021;262:139-157.
38. Zeng F-G, Fu Q-J, Morse R. Human hearing enhanced by noise. 
Brain Res. 2000;869(1-2):251-255.
39. Voros JL, Sherman SO, Rise R, et al. Galvanic vestibular stimu -
lation produces cross-modal improvements in visual thresh -
olds. Front Neurosci. 2021;15:640984.
40. Yashima J, Kusuno M, Sugimoto E, Sasaki H. Auditory noise im -
proves balance control by cross-modal stochastic resonance. 
Heliyon. 2021;7:e08299.
41. Gollnast D, Tziridis K, Krauss P, Schilling A, Hoppe U, Schulze 
H. Analysis of audiometric differences of patients with and 
without tinnitus in a large clinical database. Front Neurol. 
2017;8:31.
42. Tziridis K, Schulze H. Is phase locking crucial to improve hear -
ing thresholds in tinnitus patients? authoreacom. 2023.
43. Zwicker E. “Negative afterimage” in hearing. J Acoust Soc Am. 
1964;36:2413-2415.
44. Schilling A, Choi B, Parameshwarappa V, Norena AJ. Offset re -
sponses in primary auditory cortex are enhanced after 
notched noise stimulation. J Neurophysiol. 2023;129:1114-1126.
45. Schilling A, Tziridis K, Schulze H, Krauss P. Behavioral assess -
ment of Zwicker tone percepts in gerbils. Neuroscience. 2023; 
520:39-45.
46. Wiegrebe L, Kössl M, Schmidt S. Auditory enhancement at the 
absolute threshold of hearing and its relationship to the 
Zwicker tone. Hear Res. 1996;100(1-2):171-180.
47. Schilling A, Gerum R, Krauss P, Metzner C, Tziridis K, Schulze 
H. Objective estimation of sensory thresholds based on neuro -
physiological parameters. Front Neurosci. 2019;13:481.
48. Krauss P, Tziridis K. Simulated transient hearing loss improves 
auditory sensitivity. Sci Rep. 2021;11:14791.
49. Schilling A, Gerum R, Metzner C, Maier A, Krauss P. Intrinsic 
noise improves speech recognition in a computational model 
of the auditory pathway. Front Neurosci. 2022;16:908330.
50. Haro S, Smalt CJ, Ciccarelli GA, Quatieri TF. Deep neural net -
work model of hearing-impaired speech-in-noise perception. 
Front Neurosci. 2020;14:588448.
51. Sedley W, Alter K, Gander PE, Berger J, Griffiths TD. Exposing 
pathological sensory predictions in tinnitus using auditory in -
tensity deviant evoked responses. J Neurosci. 2019;39: 
10096-10103.
52. Sedley W, Friston KJ, Gander PE, Kumar S, Griffiths TD. An in -
tegrative tinnitus model based on sensory precision. Trends 
Neurosci. 2016;39:799-812.
53. Friston K. The free-energy principle: A unified brain theory? 
Nat Rev Neurosci. 2010;11:127-138.
54. Friston K. Does predictive coding have a future? Nat Neurosci. 
2018;21:1019-1021.
55. Hu S, Hall DA, Zubler F, et al. Bayesian Brain in tinnitus: 
Computational modeling of three perceptual phenomena 
using a modified Hierarchical Gaussian Filter. Hear Res. 2021; 
410:108338.
56. Dotan A, Shriki O. Tinnitus-like “hallucinations” elicited by 
sensory deprivation in an entropy maximization recurrent 
neural network. PLoS Comput Biol. 2021;17:e1008664.
57. Gault R, McGinnity TM, Coleman S. Perceptual modeling of tin -
nitus pitch and loudness. IEEE Trans Cogn Dev Syst. 2020;12: 
332-343.
58. De Ridder D, Vanneste S, Langguth B, Llinas R. Thalamocortical 
dysrhythmia: A theoretical update in tinnitus. Front Neurol. 
2015;6:124.
59. Llinás RR, Ribary U, Jeanmonod D, Kronberg E, Mitra PP. 
Thalamocortical dysrhythmia: A neurological and neuro -
psychiatric syndrome characterized by magnetoencephalo -
graphy. Proc Natl Acad Sci. 1999;96:15222-15227.
60. Jeanmonod D, Magnin M, Morel A. Low–threshold calcium 
spike bursts in the human thalamus: Common physiopathol -
ogy for sensory, motor and limbic positive symptoms. Brain. 
1996;119:363-375.
61. Knipper M, Van Dijk P, Schulze H, et al. The neural bases of tin -
nitus: Lessons from deafness and cochlear implants. J Neurosci. 
2020;40:7190-7202.
62. Rauschecker JP, May ES, Maudoux A, Ploner M. Frontostriatal 
gating of tinnitus and chronic pain. Trends Cogn Sci. 2015;19: 
567-578.
63. De Ridder D, Elgoyhen AB, Romo R, Langguth B. Phantom per -
cepts: Tinnitus and pain as persisting aversive memory net -
works. Proc Natl Acad Sci. 2011;108:8075-8080.
64. Vanneste S, De Ridder D. The auditory and non-auditory brain 
areas involved in tinnitus. An emergent property of multiple par -
allel overlapping subnetworks. Front Syst Neurosci. 2012;6:31.
65. De Ridder D, Vanneste S, Freeman W. The Bayesian brain: 
Phantom percepts resolve sensory uncertainty. Neurosci 
Biobehav Rev. 2014;44:4-15.
66. Popper KR. Science as falsification. Conjectures Refutations. 
1963;1:33-39.
67. Lazebnik Y. Can a biologist fix a radio?—Or, what I learned 
while studying apoptosis. Cancer Cell. 2002;2:179-182.
68. Lazar N. Ockham’s razor. Wiley Interdiscip Rev Comput Stat. 2010; 
2:243-246.
69. Kriegeskorte N, Douglas PK. Cognitive computational neuro -
science. Nat Neurosci. 2018;21:1148-1160.
70. Naselaris T, Bassett DS, Fletcher AK, et al. Cognitive computa -
tional neuroscience: A new conference for an emerging discip -
line. Trends Cogn Sci. 2018;22:365-367.
4822 | BRAIN 2023: 146; 4809–4825                                                                                                                         A. Schilling et al.
71. Marr D, Poggio T. A computational theory of human stereo vi -
sion. Proc R Soc Lond Biol Sci. 1979;204:301-328.
72. Holt N, Bremner A, Sutherland E, Vliek M, Passer M, Smith R. 
EBOOK: Psychology: The science of mind and behaviour. 4th ed. 
McGraw Hill; 2019.
73. Roberts LE. Neural plasticity and its initiating conditions in tin -
nitus. HNO. 2018;66:172-178.
74. Brown JW. The tale of the neuroscientists and the 
computer: Why mechanistic theory matters. Front Neurosci. 
2014;8:349.
75. Knipper M, Mazurek B, Dijk P, Schulze H. Too blind to see the 
elephant? Why neuroscientists ought to be interested in tin -
nitus. J Assoc Res Otolaryngol. 2021;22:609-621.
76. Silver R, Boahen K, Grillner S, Kopell N, Olsen KL. Neurotech for 
neuroscience: Unifying concepts, organizing principles, and 
emerging tools. J Neurosci. 2007;27:11807-11819.
77. Jonas E, Kording KP. Could a neuroscientist understand a 
microprocessor? PLoS Comput Biol. 2017;13:e1005268.
78. Bennett CM, Miller MB, Wolford GL. Neural correlates of inter -
species perspective taking in the post-mortem atlantic sal -
mon: An argument for multiple comparisons correction. 
Neuroimage. 2009;47(Suppl 1):S125.
79. Bennett CM, Wolford GL, Miller MB. The principled control of 
false positives in neuroimaging. Soc Cogn Affect Neurosci. 2009; 
4:417-422.
80. Gerum RC, Schilling A. Integration of leaky-integrate-and-fire 
neurons in standard machine learning architectures to gener -
ate hybrid networks: A surrogate gradient approach. Neural 
Comput. 2021;33:2827-2852.
81. LeCun Y, Jackel LD, Bottou L, et al. Learning algorithms for clas -
sification: A comparison on handwritten digit recognition. 
Neural Netw Stat Mech Perspect. 1995;261:2.
82. Schilling A, Maier A, Gerum R, Metzner C, Krauss P. 
Quantifying the separability of data classes in neural net -
works. Neural Netw. 2021;139:278-293.
83. Zenke F, Vogels TP. The remarkable robustness of surrogate 
gradient learning for instilling complex function in spiking 
neural networks. Neural Computat. 2021;33:899-925.
84. Krauss P, Metzner C, Lange J, Lang N, Fabry B. Parameter-free 
binarization and skeletonization of fiber networks from con -
focal image stacks. PLoS One. 2012;7:e36575.
85. Gerstner W, Sprekeler H, Deco G. Theory and simulation in 
neuroscience. Science. 2012;338:60-65.
86. Schilling A, Tomasello R, Henningsen-Schomers MR, et al. 
Analysis of continuous neuronal activity evoked by natural 
speech with computational corpus linguistics methods. Lang 
Cogn Neurosci. 2021;36:167-186.
87. Kerr NL. HARKing: Hypothesizing after the results are known. 
Pers Soc Psychol Rev. 1998;2:196-217.
88. Munafò MR, Nosek BA, Bishop DVM, et al. A manifesto for re -
producible science. Nat Hum Behav. 2017;1:1-9.
89. Lewin K. Field theory in social science: Selected theoretical pa -
pers (Edited by Dorwin Cartwright.). 1951
90. Newell A. You can’t play 20 questions with nature and win: 
Projective comments on the papers of this symposium. 1973
91. Peters JM. A cognitive computational model of risk hypothesis 
generation. J Account Res. 1990;28:83-103.
92. Nozaki D, Mar DJ, Grigg P, Collins JJ. Effects of colored noise on 
stochastic resonance in sensory neurons. Phys Rev Lett. 1999; 
82:2402.
93. Wang Z, She Q, Smeaton AF, Ward TE, Healy G. Synthetic- 
Neuroscore: Using a neuro-AI interface for evaluating 
generative adversarial networks. Neurocomputing. 2020;405: 
26-36.
94. Zador A, Escola S, Richards B, et al. Catalyzing next-generation 
Artificial Intelligence through NeuroAI. Nat Commun. 2023; 
14:1597.
95. Hodgkin AL, Huxley AF. A quantitative description of mem -
brane current and its application to conduction and excitation 
in nerve. J Physiol. 1952;117:500.
96. Walter WG. An imitation of life. Sci Am. 1950;182:42-45.
97. Holland O. The first biologically inspired robots. Robotica. 2003; 
21:351-363.
98. Schlimm D. Learning from the existence of models: On psychic 
machines, tortoises, and computer simulations. Synthese. 
2009;169:521-538.
99. Braitenberg V. Vehicles: Experiments in synthetic psychology: MIT 
Press; 1986.
100. Barak O. Recurrent neural networks as versatile tools of neuro -
science research. Curr Opin Neurobiol. 2017;46:1-6.
101. Marblestone AH, Wayne G, Kording KP. Toward an integration 
of deep learning and neuroscience. Front Comput Neurosci. 2016; 
10:94.
102. Van Gerven M. Computational foundations of natural intelli -
gence. Front Comput Neurosci. 2017;11:112.
103. Van Gerven M, Bohte S. Artificial neural networks as models 
of neural information processing. Front Comput Neurosci. 2017; 
11:114.
104. LeCun Y, Bengio Y, Hinton G. Deep learning. Nature. 2015;521: 
436-444.
105. Schmidhuber J. Deep learning in neural networks: An 
overview. Neural Netw. 2015;61:85-117.
106. Arnal LH, Giraud A-L. Cortical oscillations and sensory predic -
tions. Trends Cogn Sci. 2012;16:390-398.
107. Benrimoh D, Parr T, Vincent P, Adams RA, Friston K. Active 
inference and auditory hallucinations. Comput Psychiatr. 2020; 
2:183.
108. Friston KJ, Sajid N, Quiroga-Martinez DR, Parr T, Price CJ, 
Holmes E. Active listening. Hear Res. 2021;399:107998.
109. Hovsepyan S, Olasagasti I, Giraud A-L. Combining predictive 
coding with neural oscillations optimizes on-line speech pro -
cessing. bioRxiv. 2018:477588.
110. Isomura T, Parr T, Friston K. Bayesian Filtering with multiple 
internal models: Toward a theory of social intelligence. 
Neural Comput. 2019;31:2390-2431.
111. Koelsch S, Vuust P, Friston K. Predictive processes and the pe -
culiar case of music. Trends Cogn Sci. 2019;23:63-77.
112. Powers AR, Mathys C, Corlett PR. Pavlovian conditioning–in -
duced hallucinations result from overweighting of perceptual 
priors. Science. 2017;357:596-600.
113. Hassabis D, Kumaran D, Summerfield C, Botvinick M. 
Neuroscience-inspired artificial intelligence. Neuron. 2017;95: 
245-258.
114. Cambria E, White B. Jumping NLP curves: A review of natural 
language processing research. IEEE Comput Intell Mag. 2014;9: 
48-57.
115. Rahwan I, Cebrian M, Obradovich N, et al. Machine behaviour. 
Nature. 2019;568:477-486.
116. Hutson M. Artificial intelligence faces reproducibility crisis. vol 359. 
American Association for the Advancement of Science; 2018.
117. Voosen P. The AI detectives. vol 357. American Association for 
the Advancement of Science; 2017.
118. Bermudez-Contreras E, Clark BJ, Wilber A. The neuroscience of 
spatial navigation and the relationship to artificial intelli -
gence. Front Comput Neurosci. 2020;14:63.
119. McNamee DC, Stachenfeld KL, Botvinick MM, Gershman SJ. 
Flexible modulation of sequence generation in the entorhinal– 
hippocampal system. Nat Neurosci. 2021;24:851-862.
Models of auditory phantom perception                                                                                BRAIN 2023: 146; 4809–4825 | 4823
120. Stachenfeld KL, Botvinick MM, Gershman SJ. The hippocam -
pus as a predictive map. Nat Neurosci. 2017;20:1643-1653.
121. Hochreiter S, Schmidhuber J. Long short-term memory. Neural 
Comput. 1997;9:1735-1780.
122. Hochreiter S, Schmidhuber J. LSTM Can solve hard long time 
lag problems. Adv Neural Inf Process Syst. 1997:473-479.
123. Banino A, Barry C, Uria B, et al. Vector-based navigation using 
grid-like representations in artificial agents. Nature. 2018;557: 
429-433.
124. Gerum RC, Erpenbeck A, Krauss P, Schilling A. Sparsity through 
evolutionary pruning prevents neuronal networks from over -
fitting. Neural Netw. 2020;128:305-312.
125. Eggermont JJ. Central tinnitus. Auris Nasus Larynx. 2003;30: 
7-12.
126. Caspary DM, Hughes LF, Schatteman TA, Turner JG. Age- 
related changes in the response properties of cartwheel cells 
in rat dorsal cochlear nucleus. Hear Res. 2006;216:207-215.
127. Golding NL, Oertel D. Physiological identification of the targets 
of cartwheel cells in the dorsal cochlear nucleus. J Neurophysiol. 
1997;78:248-260.
128. Roberts MT, Trussell LO. Molecular layer inhibitory interneur -
ons provide feedforward and lateral inhibition in the dorsal 
cochlear nucleus. J Neurophysiol. 2010;104:2462-2473.
129. Friston K. The history of the future of the Bayesian brain. 
NeuroImage. 2012;62:1230-1233.
130. Hawkins J, Blakeslee S. On intelligence. Times Books; 2004.
131. Kadmon J, Timcheck J, Ganguli S. Predictive coding in balanced 
neural networks with noise, chaos and delays. Adv Neural Inf 
Process Syst. 2020;33:16677-16688.
132. Choksi B, Mozafari M, Biggs O’May C, Ador B, Alamia A, 
VanRullen R. Predify: Augmenting deep neural networks 
with brain-inspired predictive coding dynamics. Adv Neural 
Inf Process Syst. 2021;34:14069-14083.
133. Zeng F-G. Tinnitus and hyperacusis: Central noise, gain and 
variance. Curr Opin Physiol. 2020;18:123-129.
134. Auerbach BD, Rodrigues PV, Salvi RJ. Central gain control in 
tinnitus and hyperacusis. Front Neurol. 2014;5:206.
135. Benzi R, Sutera A, Vulpiani A. The mechanism of stochastic 
resonance. J Phys A Math Gen. 1981;14:L453.
136. Gammaitoni L, Hänggi P, Jung P, Marchesoni F. Stochastic res -
onance. Rev Mod Phys. 1998;70:223.
137. McDonnell MD, Abbott D. What is stochastic resonance? 
Definitions, misconceptions, debates, and its relevance to biol -
ogy. PLoS Comput Biol. 2009;5:e1000348.
138. Nelken I, Young ED. Why do cats need a dorsal cochlear nu -
cleus? J Basic Clin Physiol Pharmacol. 1996;7:199-220.
139. Cariani PA. Neural timing nets. Neural Netw. 2001;14:737-753.
140. Cariani PA. Temporal codes and computations for sensory re -
presentation and scene analysis. IEEE Trans Neural Netw. 2004; 
15:1100-1111.
141. Wu C, Martel DT, Shore SE. Increased synchrony and bursting 
of dorsal cochlear nucleus fusiform cells correlate with tin -
nitus. J Neurosci. 2016;36:2068-2073.
142. Shore SE, Zhou J. Somatosensory influence on the cochlear nu -
cleus and beyond. Hear Res. 2006;216:90-99.
143. Gingl Z, Kiss L, Moss F. Non-dynamical stochastic resonance: 
Theory and experiments with white and arbitrarily coloured 
noise. Europhys Lett. 1995;29:191.
144. Kandler K, Clause A, Noh J. Tonotopic reorganization of devel -
oping auditory brainstem circuits. Nat Neurosci. 2009;12: 
711-717.
145. Vale C, Sanes DH. The effect of bilateral deafness on excitatory 
and inhibitory synaptic strength in the inferior colliculus. Eur J 
Neurosci. 2002;16:2394-2404.
146. Yang S, Weiner BD, Zhang LS, Cho S-J, Bao S. Homeostatic plas -
ticity drives tinnitus perception in an animal model. Proc Natl 
Acad Sci. 2011;108:14974-14979.
147. Axelsson A, Hamernik RP. Acute acoustic trauma. Acta 
Otolaryngol. 1987;104(3-4):225-233.
148. Schilling A, Krauss P. Tinnitus is associated with improved 
cognitive performance and speech perception–can stochastic 
resonance explain? Front Aging Neurosci. 2022;14:1073149.
149. Hamza Y, Zeng F-G. Tinnitus is associated with improved cog -
nitive performance in non-hispanic elderly with hearing loss. 
Front Neurosci. 2021;15:735950.
150. Plater EB, Seto VS, Peters RM, Bent L. Remote subthreshold 
stimulation enhances skin sensitivity in the lower extremity. 
Front Hum Neurosci. 2021;15:789271.
151. Zeng F-G. A unified theory of psychophysical laws in auditory 
intensity perception. Front Psychol. 2020;11:1459.
152. Dehmel S, Pradhan S, Koehler S, Bledsoe S, Shore S. 
Noise overexposure alters long-term somatosensory-auditory 
processing in the dorsal cochlear nucleus—Possible basis 
for tinnitus-related hyp eractivity? J Neurosci. 2012;32:1660-1671.
153. Wu C, Stefanescu RA, Martel DT, Shore SE. Tinnitus: 
Maladaptive auditory–somatosensory plasticity. Hear Res. 
2016;334:20-29.
154. Lanting CP, De Kleine E, Eppinga RN, Van Dijk P. Neural corre -
lates of human somatosensory integration in tinnitus. Hear 
Res. 2010;267(1-2):78-88.
155. Pinchoff RJ, Burkard RF, Salvi RJ, Coad ML, Lockwood AH. 
Modulation of tinnitus by voluntary jaw movements. Am J 
Otol. 1998;19:785-789.
156. Won JY, Yoo S, Lee SK, et al. Prevalence and factors associated 
with neck and jaw muscle modulation of tinnitus. Audiol 
Neurotol. 2013;18:261-273.
157. Sturm JJ, Zhang-Hooks Y-X, Roos H, Nguyen T, Kandler K. 
Noise trauma-induced behavioral gap detection deficits cor -
relate with reorganization of excitatory and inhibitory local 
circuits in the inferior colliculus and are prevented by acoustic 
enrichment. J Neurosci. 2017;37:6314-6330.
158. Schaette R, König O, Hornig D, Gross M, Kempter R. Acoustic 
stimulation treatments against tinnitus could be most effect -
ive when tinnitus pitch is within the stimulated frequency 
range. Hear Res. 2010;269(1-2):95-101.
159. Schilling A, Krauss P, Hannemann R, Schulze H, Tziridis K. 
Reduktion der Tinnituslautstärke : Pilotstudie zur Abschwächung 
von tonalem Tinnitus mit schwellennahem, individuell spek -
tral optimiertem Rauschen [Reducing tinnitus intensity: Pilot 
study to attenuate tonal tinnitus using individually spectrally 
optimized near-threshold noise]. HNO. 2021;69:891-898.
160. Tziridis K, Brunner S, Schilling A, Krauss P, Schulze H. 
Spectrally matched near-threshold noise for subjective tin -
nitus loudness attenuation based on stochastic resonance. 
Front Neurosci. 2022;16:831581.
161. Conlon B, Langguth B, Hamilton C, et al. Bimodal neuromodu -
lation combining sound and tongue stimulation reduces tin -
nitus symptoms in a large randomized clinical study. Sci 
Transl Med. 2020;12:eabb2830.
162. Huang J, Sheffield B, Lin P, Zeng F-G. Electro-tactile stimulation 
enhances cochlear implant speech recognition in noise. Sci 
Rep. 2017;7:1-5.
163. Huang J, Chang J, Zeng F-G. Electro-tactile stimulation (ETS) 
enhances cochlear-implant Mandarin t one recognition. 
World J Otorhinolaryngol Head Neck Surg. 2017;3:219-223.
164. Huang J, Lu T, Sheffield B, Zeng F-G. Electro-tactile stimulation 
enhances cochlear-implant melody recogniti on: Effects of 
rhythm and musical training. Ear Hear. 2020;41:106-113.
4824 | BRAIN 2023: 146; 4809–4825                                                                                                                         A. Schilling et al.
165. Hofmeier B, Wertz J, Refat F, et al. Functional biomarkers that 
distinguish between tinnitus with and without hyperacusis. 
Clin Transl Med. 2021;11:e378.
166. Möhrle D, Hofmeier B, Amend M, et al. Enhanced central neural 
gain compensates acoustic trauma-induced cochlear impair -
ment, but unlikely correlates with tinnitus and hyperacusis. 
Neuroscience. 2019;407:146-169.
167. Koops E. Neuroimaging correlates of hearing loss, tinnitus, and hy -
peracusis. University of Groningen; 2021.
168. Koops EA. A closer fit to hyperacusis than to tinnitus? 2023
169. Cederroth CR, Lugo A, Edvall NK, et al. Association between hy -
peracusis and tinnitus. J Clin Med. 2020;9:2412.
170. McCormick DA, Bal T. Sensory gating mechanisms of the thal -
amus. Curr Opin Neurobiol. 1994;4:550-556.
171. Tan CM, Lecluyse W, McFerran D, Meddis R. Tinnitus and pat -
terns of hearing loss. J Assoc Res Otolaryngol. 2013;14:275-282.
172. Shekhawat GS, Searchfield GD, Stinear CM. Role of hearing 
aids in tinnitus intervention: A scoping review. J Am Acad 
Audiol. 2020;24:747-762.
173. Bastos AM, Usrey WM, Adams RA, Mangun GR, Fries P, Friston 
KJ. Canonical microcircuits for predictive coding. Neuron. 2012; 
76:695-711.
174. Clark A. Whatever next? Predictive brains, situated agents, and 
the future of cognitive science. Behav Brain Sci. 2013;36:181-204.
175. Knill DC, Pouget A. The Bayesian brain: The role of uncertainty in 
neural coding and computation. Trends Neurosci. 2004;27:712-719.
176. Stigler SM. The true title of Bayes’s essay. Stat Sci. 2013;28:283-288.
177. Vilares I, Kording K. Bayesian Models: The structure of the 
world, uncertainty, behavior, and the brain. Ann N Y Acad Sci. 
2011;1224:22.
178. Sedley W, Teki S, Kumar S, Barnes GR, Bamiou D-E, Griffiths 
TD. Single-subject oscillatory gamma responses in tinnitus. 
Brain. 2012;135:3089-3100.
179. Tass PA, Popovych OV. Unlearning tinnitus-related cerebral 
synchrony with acoustic coordinated reset stimulation: 
Theoretical concept and modelling. Biol Cybern. 2012;106:27-36.
180. Adams RA, Stephan KE, Brown HR, Frith CD, Friston KJ. The com -
putational anatomy of psychosis. Front Psychiatry. 2013;4:47.
181. Friston KJ, Parr T, Vries B. The graphical brain: Belief propaga -
tion and active inference. Netw Neurosci. 2017;1:381-414.
182. Kanai R, Komura Y, Shipp S, Friston K. Cerebral hierarchies: 
Predictive processing, precision and the pulvinar. Philos Trans 
R Soc B Biol Sci. 2015;370:20140169.
183. Shipp S. Neural elements for predictive coding. Front Psychol. 
2016;7:1792.
184. Sterzer P, Adams RA, Fletcher P, et al. The predictive coding ac -
count of psychosis. Biol Psychiatry. 2018;84:634-643.
185. Mazurek B, Boecking B, Brueggemann P. Association between 
stress and tinnitus—New aspects. Otol Neurotol. 2019;40: 
e467-e473.
186. Adams RA, Shipp S, Friston KJ. Predictions not commands: 
Active inference in the motor system. Brain Struct Funct. 2013; 
218:611-643.
187. Da Costa L, Parr T, Sengupta B, Friston K. Neural dynamics un -
der active inference: Plausibility and efficiency of information 
processing. Entropy. 2021;23:454.
188. Friston K, FitzGerald T, Rigoli F, Schwartenbeck P, Pezzulo G. 
Active inference: A process theory. Neural Comput. 2017;29: 
1-49.
189. Krauss P, Metzner C, Joshi N, et al. Analysis and visualization of 
sleep stages based on deep neural networks. Neurobiol Sleep 
Circadian Rhythms. 2021;10:100064.
190. Krauss P, Metzner C, Schilling A, et al. A statistical method for 
analyzing and comparing spatiotemporal cortic al activation 
patterns. Sci Rep. 2018;8:1-9.
191. Krauss P, Schilling A, Bauer J, et al. Analysis of multichannel 
EEG patterns during human sleep: A novel approach. Front 
Hum Neurosci. 2018;12:121.
192. Metzner C, Schilling A, Traxdorf M, Schulze H, Krauss P. Sleep 
as a random walk: A super-statistical analysis of EEG data 
across sleep stages. Commun Biol. 2021;4:1-11.
193. Bönsel F, Krauss P, Metzner C, Yamakou ME. Control of noise- 
induced coherent oscillations in three-neuron motifs. Cogn 
Neurodyn. 2022;16:941-960.
194. Krauss P, Prebeck K, Schilling A, Metzner C. “Recurrence 
resonance” in three-neuron motifs. Front Comput Neurosci. 
2019;13:64.
195. Krauss P, Schulze H, Metzner C. A chemical reaction network 
to generate random, power-law-distributed time intervals. 
Artif Life. 2017;23:518-527.
196. Metzner C, Krauss P. Dynamical phases and resonance 
phenomena in information-processing recurrent neural 
networks. arXiv preprint arXiv:210802545. 2021.
197. Harikrishnan NB, Nagaraj N. When noise meets chaos: 
Stochastic resonance in neurochaos learning. Neural Netw. 
2021;143:425-435.
198. Yang Z, Schilling A, Maier A, Krauss P. Neural networks with 
fixed binary random projections improve accuracy in classify -
ing noisy data. In: Bildverarbeitung für die Medizin 2021. Springer; 
2021:211-216.
Models of auditory phantom perception                                                                                BRAIN 2023: 146; 4809–4825 | 4825
