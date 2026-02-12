# Biol. Pharm. Bull. 48(8): 1150-1164 (2025)

**Authors:** International Academic Publishing Co. Ltd.
**Year:** D:20

---

© 2025 Author(s). This is an open access article distributed under the terms of Creative Commons Attribution-NonCommercial
4.0 License (https://creativecommons.org/licenses/by-nc/4.0/). Published by The Pharmaceutical Society of Japan. Vol. 48, No. 8
Biol. Pharm. Bull. 48, 1150–1164 (2025)
Review
Semantics of Brain-Machine Hybrids
Yuji Ikegayaa,b,c
a Graduate School of Pharmaceutical Sciences, The University of Tokyo, Tokyo 113–0033, Japan:
b Institute for AI and Beyond, The University of Tokyo, Tokyo 113–0033, Japan: and
c Center for Information and Neural Networks, National Institute of Information and
Communications Technology, Suita, Osaka 565–0871, Japan. Correspondence: yuji@ikegaya.jp
Received April 19, 2025
Brain-machine interfaces, also known as brain-computer interfaces, represent a rapidly advancing ﬁeld
at the intersection of neuroscience and technology, enabling direct communication pathways between the
brain and external devices. This review charts the historical evolution of brain-machine interfaces, from
fundamental discoveries such as electroencephalography and volitional single-neuron control to sophisticated
decoding of neural population activity for real-time control of robotics and sensory reconstruction. Clinical
breakthroughs lead to unprecedented success in restoring motor function after paralysis through brain-spine
interfaces, enabling high-speed communication through thought-to-text/speech systems, providing sensory
feedback for prosthetics, and implementing closed-loop neuromodulation for the treatment of neurological
disorders such as epilepsy and depression. Beyond therapeutic applications, brain-machine interfaces drive
innovation in neurotech art (neuroart) and entertainment (neurogames), allowing neural activity to directly
generate music, visual art, and interactive experiences. In addition, the potential for human augmentation
is expanding, with technologies that enhance physical strength, sensory perception, and cognitive abilities. These converging advances challenge fundamental concepts of human identity and suggest that brain-ma-
chine interfaces may enable humanity to transcend inherent biological limitations, potentially ushering in an
era of technologically guided evolution. Key words machine learning, computer, neuron, interface, feedback, artiﬁcial intelligence

## 1. INTRODUCTION

In “The Jameson Satellite,” a serialized story published
in the science ﬁction magazine “Amazing Stories” in 1931, American author Neil Ronald Jones introduced the Zoromes,
a ﬁctional race of cyborgs. The Zoromes are described as
mechanized beings with cubic metallic bodies, four articulated
appendages for locomotion, and six metallic tentacles extend-
ing from their upper torso. Originally biological organisms,
they achieved a form of immortality by transplanting their
brains into mechanical chassis, allowing the biological brain
to retain control of the mechanical construct. By transcending
biological limitations and achieving perpetual existence, the
Zoromes arguably represent the earliest documented concep-
tualization of a brain-machine interface (BMI) from a modern
scientiﬁc perspective. A BMI, also often called a brain-computer interface (BCI),
represents a direct communication pathway established be-
tween the central nervous system—often the brain—and an
external device, such as a computer or a prosthetic limb.1)
The fundamental goal is to translate neural signals reﬂecting
intent into actionable commands for controlling machines or
computers. The process begins with neural signal acquisition. This
can be achieved through invasive methods, where surgically
implanted electrodes, such as microelectrode arrays or elec-
trocorticography grids, directly interface with cortical tissue. These provide high-ﬁdelity signals, capturing individual neu-
ron action potentials (spikes) or local ﬁeld potentials (LFPs)
from speciﬁc brain regions, often the motor or sensory cortex. Alternatively, non-invasive methods, such as scalp electro-
encephalography (EEG) or functional near-IR spectroscopy
(fNIRS), record neural activity from outside the skull. Sophisticated computational algorithms, frequently employ-
ing machine learning (or artiﬁcial intelligence, AI), ﬁlter the
data, extract relevant neural features (e.g., ﬁring rates, oscilla-
tory patterns), and ultimately decode the user’s intention (e.g.,
desired movement direction, cognitive state). The decoded
intention is then converted into output commands that operate
an external device. Applications include controlling prosthetic
limbs, navigating computer interfaces, operating wheelchairs,
or using text generation software, oﬀering pathways for inter-
action with the environment. BMIs hold immense clinical promise for restoring motor,
sensory, and communication functions in individuals aﬀected
by severe neurological conditions like spinal cord injury,
stroke, or amyotrophic lateral sclerosis (ALS). They also serve
as powerful research tools for investigating fundamental
neuroscience questions about neural coding, motor control,
sensory processing, and brain plasticity. Furthermore, closed-
loop BMIs are being explored for neuromodulation therapies,
https://doi.org/10.1248/bpb.b25-00285
This review of the author’s work was written by the author upon receiving
the 2025 Pharmaceutical Society of Japan Award. Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
potentially treating conditions like epilepsy or Parkinson’s
disease by detecting aberrant neural states and delivering tar-
geted interventions.

## 2. THE PAST OF BMI

2.1. Prehistory of BMI Modern BMI research traces its
origins to early 20th-century neuroscience. A critical founda-
tion was the discovery of measurable electrical activity in the
brain. Julius Bernstein, a student in the laboratory of the Ger-
man physiologist Emil du Bois-Reymond, recorded the time
course of an action potential around 1865; however, at that
time, recording neural activity was signiﬁcantly hindered by
the limitations of experimental techniques. The development
of EEG recording was crucial for enabling more accessible
recording of neural activity. In 1875, Richard Caton published
a paper titled “Electric Currents of the Brain,” describing the
recording of electrical potentials from the surface of the heads
of rabbits and monkeys.2) Subsequently, in 1924, Hans Berger
reported the ﬁrst recordings of human EEGs and identiﬁed
rhythmic oscillations such as alpha waves.3) Berger acknowl-
edged that his discovery of alpha waves in the human brain
was inspired by Caton’s paper. This non-invasive method of
recording brain activity would later become an important cor-
nerstone for the development of BMI. Another important advance in the ﬁeld of BMI is the dem-
onstration that neural activity can be volitionally controlled;
note that a BMI can only function eﬀectively if the user is
able to control their neural activity voluntarily. In a land-
mark experiment in 1969, Eberhard Fetz demonstrated that
unanesthetized monkeys (Macaca fascicularis) could learn to
volitionally modulate the ﬁring rate of individual neurons in
the motor cortex.4) The central method used in this research
was operant conditioning. The monkeys received a reward
(food pellets) for increasing the ﬁring rate of a speciﬁc neuron,
while auditory or visual feedback indicating the neuron’s ﬁr-
ing rate was provided to aid the learning process. After train-
ing sessions, the monkeys were able to signiﬁcantly increase
the activity of target neurons (often by 50 to 500%) above
baseline rates. Conditioning a decrease in ﬁring rate was
also successful. This control was largely independent of the
neurons’ typical motor-related activity patterns. A later study
demonstrated more robust neural control, with monkeys learn-
ing to control nearly all tested neurons, maintain target ﬁring
rates for several seconds, and exhibit improved performance
over successive training sessions.5) These works provided the
ﬁrst direct evidence that individual cortical neurons could be
brought under volitional control. This landmark discovery
suggests that if single neurons could be volitionally modu-
lated, they could potentially serve as control signals for direct
brain-machine communication.
2.2. Early Days of BMI Several years before the terms
BMI and BCI were formally introduced, composer Alvin
Lucier created a piece titled “Music for Solo Performer” that
utilized the performer’s neural oscillations (speciﬁcally alpha
waves, 8–13 Hz) to generate sound.6) EEG electrodes (typically
three silver electrodes) positioned on the performer’s scalp
detected alpha activity. These raw signals were substantially
ampliﬁed using a diﬀerential ampliﬁer and subsequently ﬁl-
tered to isolate the alpha frequency band. The ampliﬁed sig-
nals were then transmitted to speakers placed near or above
various percussion instruments, including drums, cymbals,
pianos, and other resonant objects such as trash cans. The
low-frequency vibrations emanating from the speakers caused
the instruments to resonate, thereby producing sound. The
performer would sit still and attempt to enter a state conducive
to generating alpha waves. Lucier’s work is considered a landmark in experimental
music and an early instance of artistic soniﬁcation. This work
highlighted the potential of EEG as a signal source for con-
trolling external systems within an artistic, open-loop context. It explored the direct translation of endogenous physiological
signals into external artistic expression and resulted in per-
formances described as “theatrically exciting.” Although not
constituting a BCI in the contemporary sense of goal-oriented
control, “Music for Solo Performer” represents one of the
earliest documented examples of actuating an external device
directly via extracted brain signals. This piece translated the
abstract concept of measurable brain activity into the concrete
realm of physical sound generation and predated the formal
deﬁnition of BCI. It eﬀectively demonstrated signal extraction
and external actuation. Jacques Vidal is widely credited with introducing the term
BCI into the scientiﬁc literature through a 1973 publication.7)
He conceptualized computers as a potential “prosthetic exten-
sion of the brain” and initially employed the term extensively. His 1973 paper articulated the “BCI challenge”: controlling
external objects using EEG signals, particularly slow cortical
potentials like the contingent negative variation (CNV). Vidal followed this in 1977 with the ﬁrst published ex-
perimental demonstration of the BCI concept.8) This system
utilized non-invasive EEG recorded over the visual cortex,
speciﬁcally visual evoked potentials (VEP). VEPs are neural
responses elicited by visual stimuli. Vidal’s system detected
VEPs to determine the user’s point of visual ﬁxation. This
gaze information was subsequently converted into commands
to manipulate graphical objects, such as a cursor on a com-
puter screen, enabling the user to navigate a maze. Biography
Yuji Ikegaya earned his Ph. D. in Pharmaceutical Sciences from the University of Tokyo in 1998
and have been serving as a professor at the University of Tokyo’s Faculty of Pharmaceutical Scienc-
es since 2014. His expertise lies in neurophysiology, with a particular emphasis on neuronal plastic-
ity. Since 2018, he has been leading the ERATO Brain-AI Hybrid Project, pioneering the transplanta-
tion of AI chips to push the boundaries of intelligence. Yuji Ikegaya

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
Vidal’s contributions were highly signiﬁcant. He established
the term “BCI,” demonstrated the feasibility of non-invasive
control using VEP, and explicitly linked BCI development to
computer interaction and visual neuroscience, advancing be-
yond theoretical concepts and single-neuron studies. Although
considered to possess limited accuracy at the time, it consti-
tuted an important proof of concept. Bozinovski et al. reported the ﬁrst control of a physical ob-
ject (a mobile robot) using non-invasive EEG signals in 1988.9)
This robotic control system employed changes in the EEG
alpha rhythm (8–13 Hz)—speciﬁcally, the increase associated
with relaxation or closed eyes (termed contingent alpha varia-
tion, CαV, by the authors)—to generate start/stop commands. The EEG was recorded from the Pz scalp location and pro-
cessed using software designed to recognize the presence or
absence of predominant alpha activity. Increased alpha power
(associated with closed eyes) triggered a “start” command,
while decreased alpha power (associated with open eyes) trig-
gered a “stop” command. The robot, called Elephobot Line
Tracer, possessed autonomous line-following capabilities, with
the BCI providing high-level start/stop control. The system in-
corporated machine learning elements for calibration (learning
probability density functions for closed/open eye states) and
real-time pattern recognition. In 1990 (though some sources indicate research dating back
to 1988), the same group reported a closed-loop BCI utilizing
CNV potentials.10) The CNV is a slow negative potential that
develops in anticipation of a stimulus or response. Their sys-
tem employed the CNV, reﬂecting the brain’s state of expecta-
tion, to control a buzzer within a feedback loop. They termed
the cognitive component representing anticipatory learning the
electroexpectogram. This research also incorporated adaptive
ﬁltering techniques. The 1988 robot control experiment was signiﬁcant as the
ﬁrst demonstration of controlling the movement of a physical
mobile object using EEG, thereby directly linking EEG re-
search with robotics. It addressed the psychokinesis challenge
from an engineering perspective and introduced machine
learning methodologies into the BCI ﬁeld. Their subsequent
CNV research explored the use of anticipatory brain poten-
tials and closed-loop adaptive control. These contributions
expanded the repertoire of EEG signals and control paradigms
investigated in early BCI research.
2.3. Toward Practical Application of BMI A key
question in motor neuroscience involves understanding how
the brain achieves precise motor control, such as arm reach-
ing, given that individual motor cortex neurons exhibit broad
tuning to a particular preferred direction. Investigating this
issue, Georgopoulos and colleagues studied primate motor
cortex during reaching tasks in three dimentional (3D) space. In 1986, they discovered that the direction of movement is ac-
curately encoded not by single neurons, but by the collective
activity of a neuronal population.11)
They proposed the population vector algorithm. In this
model, each neuron’s contribution is represented as a vector
pointing in its preferred direction, which was determined ex-
perimentally, e.g., via a center-out task. The magnitude of this
vector is weighted by the neuron’s ﬁring rate (or change in
ﬁring rate) during a speciﬁc movement. The vector sum of all
these individual contributions yields the “population vector,”
the direction of which accurately predicts the actual direction
of arm movement. The magnitude of the population vector can
correlate with movement speed. This ﬁnding represented a pivotal advance in understand-
ing motor control and neural coding. It demonstrated how
precise information could emerge from the combined activity
of broadly tuned elements. This work shifted the focus from
the capabilities of single neurons, as explored by researchers
like Fetz, to the computational power inherent in population
codes, and provided a crucial conceptual and mathematical
bridge between the inherent variability of individual neuronal
activity and the brain’s capacity to generate precise, directed
motor output, showing how a population could reliably encode
information. The population vector algorithm established the
theoretical groundwork for sophisticated invasive BMIs aimed
at controlling prosthetic limbs or cursors based on decoded
population activity, providing a powerful mathematical frame-
work for decoding motor intent from neural ensembles. With the goal of “reading the neural code,” Dan and col-
leagues sought to decode visual information from neural ﬁring
patterns within the early visual system.12) Speciﬁcally, they
reconstructed visual stimuli from ensemble activity in the cat
lateral geniculate nucleus, a critical thalamic relay nucleus
for vision. Methodologically, they recorded spike trains from
ensembles of lateral geniculate nucleus neurons (up to 177
cells) while anesthetized cats viewed movies depicting natural
scenes. They employed linear decoding techniques (multi-
input, multi-output reverse correlation/reconstruction ﬁlters) to
estimate the spatiotemporal visual input likely responsible for
the observed spike patterns. These ﬁlters accounted for indi-
vidual cell properties and inter-neuronal correlations. Recon-
struction quality was assessed by comparing the reconstructed
visual information to the actual stimuli using metrics such
as correlation coeﬃcients and spectral analysis. The results
demonstrated the successful reconstruction of recognizable,
spatiotemporal natural scenes (including moving objects and
faces) from neuronal ensemble activity. Reconstruction quality
improved with the number of neurons included in the analysis,
beginning to saturate around 12–16 cells for natural scenes,
suggesting neuronal adaptation to natural stimulus statistics. Linear decoding methods proved capable of capturing sig-
niﬁcant visual information, particularly at higher temporal
frequencies, with neuronal noise identiﬁed as a major limiting
factor for ﬁdelity. This work constituted a pioneering demonstration of recon-
structing dynamic, natural sensory experiences from neural
activity. It showed that linear methods could extract substan-
tial visual information from population codes in the early
visual pathway. These ﬁndings paved the way for developing
sensory neuroprosthetics (e.g., visual prostheses) and provided
valuable insights into how sensory information is encoded and
represented by neural ensembles. This research complemented
motor decoding eﬀorts by addressing the sensory input aspect
of brain interfaces. In response to these initial attempts, Nicolelis and col-
leagues investigated whether population activity recorded
from the motor cortex could be utilized for real-time control
of external robotic devices. In a 1999 study using rats, they
trained the animals to press a lever, which controlled a robot
arm delivering a water reward. Ensembles of motor cortex
neurons were simultaneously recorded13); note that more than
25 neurons are required for successful control. Mathematical

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
transformations, including neural networks, were developed to
generate ‘neuronal population functions’ capable of predicting
lever trajectory from neuronal ﬁring rates. These functions
were then converted into command signals to directly control
the lever in real-time, establishing a ‘neurorobotic’ mode of
operation. It is worth noting that machine learning called
recurrent neural networks was used for the ﬁrst time in BMI. A subsequent study published in 2000 extended this para-
digm to owl monkeys.14) Larger electrode arrays (up to 96
electrodes) were implanted in multiple cortical areas, includ-
ing motor, premotor, and somatosensory cortex. Population
activity was recorded while the monkeys performed reaching
tasks. Computational algorithms, initially employing linear
models and other mathematical methods, were used to pre-
dict hand trajectory from neural signals in real-time. These
decoded signals subsequently enabled the monkeys to control
a multi-jointed robot arm in three-dimensional space; the
monkeys successfully controlled the robot arm using decoded
brain signals derived from distributed cortical populations. Neural signals related to trajectory were observed broadly
across the recorded cortical areas. Crucially, population-based
decoding consistently outperformed predictions based on sin-
gle neurons. The feasibility of remote control over the internet
was also demonstrated. These experiments were signiﬁcant achievements, dem-
onstrating—ﬁrst in rats and subsequently in primates—that
brain activity could be decoded in real-time to provide con-
tinuous control of complex robotic devices. This work vali-
dated the potential of invasive BMIs for restoring movement
in individuals with paralysis by enabling control over sophisti-
cated prosthetics. The ﬁndings also reinforced the principle of
distributed population coding, consistent with Georgopoulos’s
work, and highlighted the brain’s plasticity in adapting to neu-
roprosthetic control. These advancements around 1999 marked
a pivotal moment in the ﬁeld. Research progressed beyond
the theoretical possibilities outlined by Georgopoulos or the
basic control demonstrated by Vidal and Bozinovski, showcas-
ing the ability to perform complex, high-ﬁdelity decoding of
both sensory information and continuous motor commands in
real-time. This considerably advanced the benchmark for BMI
capabilities.
2.4. Recent Application of BMI Restoring movement
after paralysis has been a major focus of BMI studies. In
2023, researchers in Switzerland (EPFL/CHUV) and France
(CEA-Clinatec) reported a breakthrough “brain-spine inter-
face” for a man with chronic tetraplegia.15) Two 64-electrode
implants were placed on the surface of his motor cortex and
connected wirelessly to an implanted pulse generator on his
spinal cord. When the participant thought about walking, the
system decoded the brain signals in real time and stimulated
his leg muscles accordingly. As a result, he regained the abil-
ity to stand, walk, and even climb stairs after years of pa-
ralysis. The patient described the implant as “life-changing,”
allowing him to perform daily activities such as getting up
to paint and enjoying a drink with friends while standing. This digital bridge between the brain and spine demonstrates
how BMIs can bypass damaged nerves and restore voluntary
movement. It builds on earlier trials of epidural electrical
stimulation for spinal cord injury, but now with direct brain-
controlled movement rather than pre-programmed steps. Other BMI trials have helped paralyzed patients control
external mobility aids. For example, researchers have enabled
people with tetraplegia to drive brain-controlled wheelchairs
through thought alone in real-world environments using
noninvasive EEG-based BCIs with training.16) Such studies
report that users can safely navigate obstacle courses after
iterative learning, highlighting BMI potential for independent
mobility in the home or hospital settings. In another dramatic
demonstration funded by Defense Advanced Research Proj-
ects Agency (DARPA) in the United States, a 55-year-old
paralyzed woman was able to pilot an F-35 jet simulator using
only her mind—she had implanted electrodes originally for a
robotic arm study, which were repurposed to control a ﬂight
simulator.17) This feat, while experimental, showed that high-
dimensional motor tasks (like aircraft controls) can be mapped
from neural signals, an application of interest to the military
for remote vehicle operation and to aviation medicine. Brain-controlled prosthetic limbs have seen major im-
provements in the last few years, especially with the addition
of sensory feedback. Earlier BMI prosthetic trials allowed
paralyzed individuals to control robotic arms to perform tasks
like grasping objects, but without sensation, it was challeng-
ing to manipulate fragile or unseen items. Recent trials have
integrated bidirectional BCI systems that not only read motor
commands from the brain but also write sensory information
back to the brain (or peripheral nerves). For example, in a

### 2021 University of Pittsburgh study, a participant with tet-

raplegia (implanted with motor cortex electrodes) controlled a
robotic arm that could “feel” via electrical stimulation of his
sensory cortex.18) Whenever the robotic hand touched an ob-
ject, signals were fed back into the brain, creating an artiﬁcial
sense of touch. This tactile feedback enabled the man, Nathan
Copeland, to perform tasks like pouring water between cups
much more ﬂuidly. With vision alone, it took him about 20 s
to grasp and move an object, but with added touch feedback
he did it in 10 s. He also found that objects did not slip from
the robot hand as often, since he could feel how ﬁrmly he was
grasping them. This closed-loop BCI demonstrates how neuro-
prosthetics with sensory feedback vastly improve performance
and user conﬁdence. Restoring communication is another critical area of BMI
clinical research, especially for patients with ALS, brainstem
stroke, or other conditions that leave them “locked in.” Recent
trials have achieved unprecedented communication speeds by
decoding neural activity into text or speech. In 2021, a Stan-
ford University-led team, as part of the BrainGate consortium,
implanted microelectrode arrays in the motor cortex of a man
with high spinal cord injury and demonstrated a brain-to-text
BCI that decoded his attempted handwriting motions.19) By
imagining himself writing letters, the participant was able
to output text on a screen at about 90 characters per minute
(roughly 18 words per minute)—a record at that time for BCI
communication, comparable to average smartphone typing
speeds in able-bodied peers. This “mental handwriting” ap-
proach was more than twice as fast as previous BCI typing
methods and underscored how machine learning can extract
rapid, ﬁne-grained patterns from neural signals. Building on such advances, researchers have begun to
tackle direct speech prosthesis via BMI. In 2023, a team at
University of California, San Francisco implanted a high-den-
sity electrocorticography array in a woman who had lost the
ability to speak due to a brainstem stroke.20) Using AI-based

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
decoding, they achieved the ﬁrst instance of synthesizing both
whole words and facial expressions from brain activity. In this
trial, the participant’s attempted speech signals were convert-
ed in real time into a digital avatar speaking with her intona-
tion and even smiling or scowling appropriately. The system
could decode brain signals into text at nearly 80 words per
minute, vastly outpacing her prior assistive device. While still
experimental, the technology points toward a future oﬃcially
approved BCI. Indeed, an earlier case in 2021 had already
shown that a mute, paralyzed patient could produce dozens of
words (from a limited vocabulary) via a speech BCI at approx.
75% accuracy, using an implant in speech motor cortex. By
2023, accuracy and vocabulary had improved; one BrainGate
study reported decoding internal speech with up to 97% ac-
curacy (with autocorrect) for an ALS patient, allowing him to
communicate words he was “thinking” of saying.21)
Notably, even patients in completely locked-in states (no
eye or muscle movement) have begun to beneﬁt from BCIs. In one 2022 case, a late-stage ALS patient received an im-
planted electrode system and learned to respond to auditory
cues via modulating his brain signals.22) Over months, he was
able to slowly spell out messages (around one character per
minute) by thinking “yes” or “no” in response to an auditory
speller, thus regaining a basic communication channel. While
extremely slow, this study proved that some communication
is possible even after all muscle control is lost, using only the
brain’s electrical activity. Such cases remain rare, but they
highlight the importance of BMI for preserving the ability to
communicate in the most severe paralysis conditions. While many BMIs focus on restoring lost motor or com-
munication function, an important subset of clinical trials
involves implanted brain interfaces that treat neurological
disorders like epilepsy, tremor, or Parkinson’s disease. These
are often closed-loop systems–they sense abnormal brain ac-
tivity and deliver targeted stimulation or other interventions. A prime example is the NeuroPace Responsive Neurostimula-
tion system for epilepsy, which, although approved in 2013,
saw wider adoption and follow-up studies in the past ﬁve
years. The NeuroPace Responsive Neurostimulation is a BMI
that monitors EEG activity from electrodes on the brain and
automatically applies electrical pulses when it detects epileptic
seizure patterns, often aborting seizures before symptoms es-
calate. Long-term trial data showed signiﬁcant median seizure
frequency reductions (around 75% in many patients at 6+
years of use) and a subset of patients becoming nearly seizure-
free.23) These outcomes underscore that closed-loop BMIs can
provide lasting therapeutic beneﬁts in a real-world setting. Moreover, cognitive and mood improvements were noted in
some patients, likely because better seizure control improves
overall brain network stability. Researchers are now extending the closed-loop neuromodu-
lation concept to other conditions. Adaptive deep brain stimu-
lation (DBS) for Parkinson’s disease is a key trend. Next-gen-
eration DBS devices (e.g. Medtronic Percept PC, AlphaDBS)
can record brain signals such as local ﬁeld potentials and
adjust stimulation in real time. Clinical studies have tested
“adaptive DBS” algorithms that raise or lower the stimulation
intensity based on neural feedback, aiming to deliver therapy
only when needed. Early trials in Parkinson’s patients have
shown that adaptive DBS can maintain symptom relief (trem-
or, rigidity control) with less stimulation on time, thereby po-
tentially reducing side eﬀects. In 2021, a breakthrough case at
University of California, San Francisco applied a personalized
closed-loop DBS system for severe depression.24) Investigators
identiﬁed a speciﬁc brain activity pattern that corresponded
to the patient’s depressive symptoms; they then programmed
a neurostimulator to detect that biomarker and stimulate the
ventral striatum whenever the pattern appeared. The result
was a dramatic and sustained alleviation of depression in this
one patient. This was the ﬁrst in-human demonstration of a
closed-loop BMI for a psychiatric disorder, and it paves the
way for larger trials in depression and obsessive–compulsive
disorder using responsive brain implants. As BMI technology matures, a growing ecosystem of com-
panies and investors is pushing the ﬁeld toward commercial
products. The past decade has seen an inﬂux of startup activ-
ity, venture capital funding, and even big corporate partner-
ships in neurotechnology. At the same time, regulators like
the Food and Drug Administration (FDA) in the United States
have begun creating pathways to evaluate and approve these
novel devices. To summarize the competitive landscape, Table
1 compares a few leading BMI eﬀorts and their recent prog-
ress.
2.5. Neurotech Art and Entertainment In recent years,
artists and scientists have collaborated to transform neural ac-
tivity into visual art and interactive experiences (Table 2). One
striking example is a pair of brain-powered dresses presented
by engineer Leonhard Schreiner and designer Anouk Wippre-
cht. In the Screen Dress, the wearer’s brain engagement level
(measured via a 4-channel EEG headband) is visualized by
animated eye graphics on the dress that open and move with
the wearer’s mental state.25) In the companion Pangolin Scales
Dress, a full 1024-channel “ultra-high-density” EEG system
drives motors and light-emitting diodes on a 3D-printed exo-
skeletal dress; the dress’s scale-like ﬂaps and lights respond in
real time to the wearer’s brainwaves. For example, calm theta
waves create soft purple movements, while alert beta waves
trigger rapid white ﬂickers). These projects transform brain
signals into dynamic fashion statements, demonstrating how
neural data can directly animate physical art on the human
body. An interactive light sculpture by artist Laura Jade makes
the activity inside your head visible. The piece is a brain-
shaped Plexiglas sculpture engraved with neural patterns that
glows in real time in response to the participant’s EEG sig-
nals.26) Wearing a wireless Emotiv EEG headset, viewers see
the sculpture glow in diﬀerent colors and intensities as their
brain activity changes, essentially using their minds to “paint”
the sculpture with light. This project, created during Jade’s
art-science residency, merges lighting design with neurosci-
ence to provide a personalized visual display of one’s own
neural oscillations. Brain Painting is a P300-based BCI art tool that allows
people to create digital paintings using only their brain sig-
nals. It presents a palette and shapes on a screen and uses
EEG to detect where the user is focusing attention to select
colors or brush strokes.27) By cycling through options with
visual ﬂashes and using the brain’s response, even people with
locked-in syndrome have been able to paint pictures without
any muscle movement. This innovative art-making method
turns brain activity into brush strokes, demonstrating a non-
medical use of BCI to facilitate creative expression for those

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
who otherwise cannot physically paint. In collaboration with Steve Potter’s lab, SymbioticA, an
Australian bioart group, is bringing neural-driven art into the
animal lab. It was essentially a primitive cybernetic organ-
ism—an amalgam of wetware and hardware—that produced
evolving drawings. In this art-science installation, living brain
matter literally became the artist.28) A culture of rat corti-
cal neurons grown on a multi-electrode array served as the
“brain” to control a drawing machine. The neuron signals
were sent over the Internet to a robotic arm that drew on
paper, creating abstract art based on the neural activity. This
provocative piece demonstrated an unexpected form of artistic
creation: a hybrid animal-machine system in which the spon-
taneous activity of a non-human brain resulted in tangible art. In PluginHUMAN, an immersive art installation by
Sargeant and Dwyer, the audience’s brainwaves drive a maze
of audiovisuals.29) Visitors wear EEG headsets and walk
through a maze of hanging panels with projection-mapped vi-
suals and surround sound. A custom brain-computer interface
translates each participant’s brainwave patterns into changes
in the projected abstract imagery and ambient soundscape. The result is a mesmerizing “brain forest” environment that
changes its colors, lights, and audio in response to the minds
of its explorers, making each visitor’s experience unique to
their own neural data. We also presented a novel BCI technique that uses latent
diﬀusion models, a type of deep neural network, to gener-
ate images directly from continuous brain activity.30) Unlike
previous BCI art methods that rely on decoding speciﬁc user
intentions (e.g., via P300 signals) to control drawing tools, this
end-to-end approach bypasses conscious control. By recording
local ﬁeld potentials from the neocortex of freely moving rats,
this system continuously transformed the neural signals into
sequences of morphing images using a pre-trained Stable Dif-
fusion v1.5 model without text input. The results showed that
the generated images successfully reﬂected the statistically
dynamic nature of the underlying neural activity, showing
continuity between successive frames (Fig. 1). This method
provides a unique way to visualize brain function and opens
new possibilities for creative expression independent of con-
scious intent, with potential future applications in art. The paramusical ensemble “Activating Memory” is a
unique musical performance in which four paralyzed patients
became composers by using their EEG signals. Developed by
Eduardo Miranda’s team at the University of Plymouth, the
system allowed each participant (wearing an EEG cap) to se-
lect short musical phrases on a computer by directing their at-
tention to speciﬁc ﬂashing icons using a P300 brain-computer
interface.31) The selected passages were then played in real
time by a live string quartet, eﬀectively turning the patients’
thoughts into a collaborative composition. The resulting piece,
“Activating Memory,” was premiered at a contemporary music
festival in the United Kingdom and demonstrated a powerful
fusion of neuroscience and art: bedridden individuals creating
and performing complex music using only brain signals. The Encephalophone is also a mind-controlled musical in-
strument invented by neuroscientist/musician Thomas Deuel
and colleagues. The Encephalophone is played without any
physical movement: the performer wears an EEG cap and
generates musical notes by modulating speciﬁc brain rhythms, Table 1. Leading BMI Developers and Their Progress in 2020–2025
Organization
Approach & Device
Recent Milestones (2020–25)
Funding/Partnerships
Neuralink
(U. S. A.)
Fully implanted 1024-chan-
nel microelectrode array
(“N1”) with robotic sur-
gical insertion. Demonstrated a monkey controlling a video
game via implant (2021); won FDA ap-
proval for ﬁrst human trial (May 2023);
reportedly performed ﬁrst human im-
plants by late 2023. Approx. $363M venture funding (2016–
2022); backed by Elon Musk. Col-
laborations kept mostly in-house;
high public proﬁle. Synchron
(U. S. A./AUS)
Stentrode endovascular neu-
ral interface (16-electrode
mesh delivered via blood
vessels). First BCI implanted without open brain
surgery; completed ﬁrst human study in
AUS enabling texting and e-shopping by
thought. Gained FDA IDE and implanted

## 6 U. S.

patients
(2021–23);
preparing
larger trial toward approval. Approx. $75M Series C funding in
2022 (total approx. $145M); inves-
tors include Bezos & Gates. Partner-
ships with Mount Sinai Hospital, DARPA (funding). Blackrock Neurotech
(U. S. A.)
Utah array-based implant
(NeuroPort/MoveAgain);
developing
high-density
“Neuralace” (>10k elec-
trodes). BCI tech used in 30+ research patients via
BrainGate; MoveAgain system received
FDA Breakthrough designation (2021). Aiming to launch ﬁrst commercial BCI
for home use in paralysis in mid-2020s. Secured major investment to scale up
(2024).
$200M investment from Tether in
2024 for majority stake (valuation
approx. $350M). Long-term supplier
to academic labs; partnered with AE
Studio on software. BrainGate Consortium
(U. S. A.)
Academic multi-center trial
using surgically implant-
ed Utah arrays + custom
decoders. Ongoing trial with continuous improve-
ments: published wireless transmitter
results (2021); showcased 90%+ accu-
racy speech decoding for an ALS patient
(NEJM 2023). Demonstrated safety over
15+ years of implants. Funded by NIH, Dept. of Veterans
Aﬀairs, and others. Not a company;
collaborations with Brown, Stanford, MGH, Case Western, etc. Provides
foundational research for industry. Paradromics
(U. S. A.)
High-channel-count ECoG
implant
(thousands
of
electrodes) and data hub. Achieved high-bandwidth recording in ani-
mals; awarded FDA Breakthrough Device
status (c.2022). Building “Neuroport”
for speech BCI and planning ﬁrst human
studies (2024). Approx. $38M venture seed fund-
ing + DARPA contracts; part of
DARPA’s NESD program. Recently
raised total approx. $88M. Approaches vary between invasive and minimally invasive, and each has reached important milestones toward clinical translation. Funding has accelerated, with private
capital complementing earlier government-funded research. Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
such as alpha waves.32) These brain signals are translated into
pitches on a synthesizer in real time, allowing the user to play
melodies using only his or her thoughts. Originally developed
to enable disabled musicians to continue making music, the
Encephalophone also opened up a new musical realm in which
brain waves are the instrument. This device illustrates how
brain-machine interfaces can serve creative expression—here,
the brain becomes a musical controller, producing real-time
compositions from neural activity. In a demonstration by Elon Musk’s Neuralink, a macaque
monkey named Pager played a game of Pong using only his
brain implants.33) Researchers implanted tiny electrode ar-
rays in the monkey’s motor cortex and trained Pager to move
a cursor with a joystick. Once calibrated, the joystick was
disconnected—yet the monkey could continue to move the
on-screen paddle telepathically via neural signals. A video
released in 2021 showed Pager successfully collecting the
Pong ball using only his mind, without a physical controller. This demonstration highlighted an entertaining (and viral)
example of a brain-machine gaming interface with an animal,
underscoring that even a primate’s neural activity can directly
control a video game in real time. Going a step further, scientists have taught a collection of
living neurons in a dish to play a video game. In an experi-
ment led by Cortical Labs, about 800000 human and mouse
neurons grown on a microelectrode array were connected to a
computer running Pong.34) The system, dubbed “DishBrain,”
fed electrical signals to the neurons indicating the position of
the Pong ball; remarkably, the neural cluster learned to adjust
ﬁring patterns to move a virtual paddle and hit the ball back. Within minutes of feedback training, the dish of brain cells
demonstrated goal-directed learning and successfully played
a rudimentary game. This sci-ﬁ-like project was a research
eﬀort to study learning and intelligence, but it doubled as an
unexpected entertainment application—eﬀectively an arcade
game played by a petri dish of neurons. Table 2. Representative Neurotechnology-Driven Art and Entertainment
Project/Work
Creative Domain
Brain Source
Interface/Method
Music for Solo Performer
(1965)
Live music performance
Human (EEG alpha waves)
Analog EEG ampliﬁcation to trig-
ger percussion instruments in
real time. Brain Painting BCI
(2010s)
Visual art (digital)
Human (EEG P300 focus)
Non-invasive P300 speller inter-
face to select colors/shapes on a
virtual canvas. Paramusical Ensemble
(2015)–“Activating Memory”
Music composition/performance
Human (EEG–locked-in patients)
EEG cap with visual P300 selec-
tion; patients choose musical
phrases played by live string
quartet. Encephalophone
(2017)
Musical instrument
Human (EEG–alpha/mu)
EEG-based instrument translating
brain rhythms into synthesizer
notes in real time. Screen Dress
(2025)
Interactive fashion art
Human (EEG–4 channels)
EEG engagement level drives ani-
mated eye graphics on dress’s
embedded screens. Pangolin Scales Dress
(2025)
Interactive fashion art
Human (EEG–1024 channels)
Ultra-HD EEG controls servomo-
tor “scales” and LED lights
reﬂecting diﬀerent brainwave
frequencies. Brainlight
(2015)
Light sculpture
Human (EEG)
Wireless EEG headset controls
illumination in a brain-shaped
perspex sculpture.

## DREAM 2.2

(2018)
Immersive installation
Human (EEG–audience)
Custom EEG-driven audio-visual
system; brainwaves modulate
projected visuals and sounds in
a maze. MEART–Semi-Living Artist
(2001–04)
Robotic art installation
Rat neurons in vitro (MEA)
Cultured cortical cells on electrode
array send signals to robotic
drawing arm, creating art. Neuralink “MindPong”
(2021)
Gaming (demo)
Monkey (implant BMI)
1024-electrode wireless implant
in motor cortex; neural activity
moves cursor to play Pong. DishBrain Pong
(2022)
Gaming (experiment)
Human & mouse neurons (in vitro)
Microelectrode array with 800k
neurons;
electrophysiological
feedback enables Pong paddle
control. Mindﬂex Toy
(2009)
Game/Toy
Human (EEG–Focus)
EEG headset measures concen-
tration to control airﬂow that
levitates a foam ball through
obstacles. From brainwave-driven dresses and paintings to thought-composed music and neuron-enabled gameplay, these projects demonstrate the expanding boundaries of art and
entertainment powered by brain-machine interfaces. They illustrate how EEG signals, brain implants, and even cultured neurons can be used to generate music, control visuals,
and animate objects in real time. Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
Brainwave games and toys—Brain-computer interfaces
have also entered the playful realm of consumer products. For
example, Mindﬂex is a toy in which players guide a foam ball
through an obstacle course using only their concentration. An
EEG headband measures the player’s level of concentration
and adjusts a small fan that ﬂoats the ball—the more you con-
centrate, the higher the ball ﬂoats.35) Similarly, interactive ex-
hibits such as Mindball have pitted the relaxation levels of two
players against each other: EEG sensors detect who is calmer
and move a ball toward the more stressed opponent. Even
wearable fashion gadgets like the Necomimi (cat ears) have
become popular, with motorized cat ears that perk up or droop
down depending on the wearer’s brain state (alert or relaxed). These whimsical games and devices show how neural signals
can be harnessed for fun, allowing people to control physical
objects or avatars using their mind as a game controller.
2.6. BMI-Augmented Humans Bridging humans with
machines or computers can be used as human enhancement
technologies, which aim to augment natural human abilities
through integration with advanced devices and systems. Un-
like medical prosthetics or therapies that restore lost function,
non-medical enhancements are designed to push capabili-
ties beyond typical human limits—enabling stronger bodies,
sharper senses and faster minds. They cover a wide range of
technologies, from exoskeleton suits and BMI to AI-powered
wearables and sensory augmentation devices (Table 3). Factories and warehouses have started to equip workers
with wearable exoskeleton suits to reduce fatigue and pre-
vent injuries during physically demanding tasks, although
these are not based on BMI. For example, car manufactur-
ers such as Mazda Toyota Manufacturing in the U. S. have
integrated shoulder-supporting exoskeleton vests into their
assembly lines. After trialling the devices in 2022, the com-
pany deployed dozens of exoskeleton units to assist workers
with overhead tasks (such as installing components under car
frames), resulting in a reported 55% reduction in shoulder fa-
tigue among workers. European companies have also adopted
devices such as the German Bionic Cray X suit, a powered
exoskeleton that can help lift up to 30 kg repeatedly by sup-
porting the user’s back and legs. The Cray X even uses AI al-
gorithms and an early warning system to monitor posture and
provide feedback to the wearer—essentially anticipating strain
and reducing the risk of injury during heavy lifting. These
real-world applications illustrate how augmentative wearables
are enhancing human strength and endurance in industry. Real-world applications of augmented reality and sensor
fusion are giving people superhuman sensory awareness. One high-proﬁle example is the helmet-mounted display on
the F-35 ﬁghter jet, which gives pilots 360-degree vision and
fused sensor data. The advanced helmet uses cameras around
the aircraft to allow the pilot to literally ‘see through’ the
body of the aircraft, displaying a panoramic view on the visor. It overlays critical information and target markers onto the
pilot’s vision as an augmented reality feed. The F-35’s helmet
even integrates night vision and IR inputs, allowing the pilot
to see in the dark without separate goggles. This operational
Fig. 1. Diﬀusion Model-Based Image Generation from Rat Brain Activity
A novel BCI using a latent diﬀusion model was developed to generate images directly from continuous rat brain activity. This system bypasses conscious control, creat-
ing visuals that reﬂect raw neural dynamics. This oﬀers new paths for unconscious artistic expression and brain function visualization. (A) A photograph of an experimen-
tal setup. (B) Detailed illustration of the steps taken to generate an image from rat local ﬁeld potentials. The recorded local ﬁeld potentials were mapped onto a noisy latent
vector zT, which was then denoised to produce a denoised latent vector z. This latent representation of the denoised image was then processed by a latent-to-image decoder
to produce image X. (C) Noisy latent vector zT and the corresponding generated image obtained by the diﬀusion process and the latent-to-image decoder. This ﬁgure is
modiﬁed from a paper by Yamashiro et al.30)

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
system eﬀectively enhances human vision and situational
awareness beyond natural limits, and is in service with U. S.
and allied militaries. While invasive brain implants for augmentation are still
experimental, non-invasive BCI devices have been publicly
demonstrated. EEG headsets are being used in new ways for
entertainment and communication. At the 2018 Consumer
Electronics Show, a startup showed oﬀ a consumer BCI called
NextMind that allows users to control VR games using only
their thoughts-by focusing their attention on targets, players
could perform actions like exploding virtual objects with-
out using their hands. Similarly, academic groups have held
“drone races” in which participants control drones through
EEG headsets, eﬀectively moving an object through thought
alone. These demonstrations are early steps toward everyday
mind-machine integration. Another example is the MIT Media
Lab’s AlterEgo prototype, a wearable device that enables
silent, internal communication with a computer. The system
detects neuromuscular signals from the wearer’s jaw and
throat as they verbalize words in their head, allowing them
to ask questions of an AI assistant without speaking and hear
answers through a bone-conduction earpiece. In one demon-
stration, users were able to silently report their opponent’s
moves in a chess game and receive recommended responses
from a computer, all without making a sound. This type of
intelligence augmentation device eﬀectively acts as a private,
thought-driven “smart assistant,” pointing to future everyday
applications of BCI technology. Beyond the early implementations above, many human en-
hancement technologies are currently in the experimental or
trial phase. Scientists, companies, and military research agen-
cies across the globe are actively testing new ways to push
human abilities further. These projects provide a glimpse of
what may soon become feasible. One fascinating line of research is adding extra functional
limbs to the human body. In a recent trial at University Col-
lege London, researchers equipped volunteers with a robotic
“Third Thumb”—a 3D-printed thumb extension worn on
the hand and controlled with pressure sensors under the big
toes.36) Over ﬁve days of training, participants learned to use
the extra thumb to carry out dexterous tasks one-handed, such
as building a tower of blocks, and even multitasking (manipu-
lating objects with the extra thumb while doing mental math). Impressively, users quickly began to feel the robotic thumb
as if it were part of their body, demonstrating the brain’s
adaptability to augmentation. This experiment—conﬁrmed by
neural imaging—shows that the human brain can incorporate
a prosthetic enhancement and suggests future interfaces for
adding entirely new limbs or tools to able-bodied users. These
supernumerary limb experiments are expanding the limits of
human multi-tasking and coordination. Pushing the envelope of human communication, scientists
have conducted experiments directly linking brains of mul-
tiple people. In a notable 2019 study, an international team
created a Brain-to-Brain Interface that let three people col-
laborate using brain signals alone.37) Two “sender” participants
Table 3. Representative Technologies for Human Augmentation
Technology
Status
Purpose/capability
Origin (Country/region)
Shoulder/Back Exoskeletons
(e.g., SuitX, German Bionic)
Implemented in
industry
Augment lifting strength; reduce worker fa-
tigue/injury
U. S. A., Germany, Japan
(global adoption)
Military Exosuit
(Lockheed Martin Onyx)
Field-tested
Assist soldiers in carrying heavy gear with
AI-aided movement
U. S. A. Jetpack Rescue Suit
(Gravity Industries)
Demonstrated (2020)
Enable rapid personal ﬂight for emergency
responders
U. K. AR Helmet for Pilots

## (F-35 HMDS)

In service
360° vision and data overlay for enhanced
situational awareness
U. S. A. (used by various air forces)
AI Facial Recognition Glasses
Deployed
Real-time identiﬁcation of individuals in
crowds (augmented vision)
China
EEG Mind-Control Interface
(NextMind)
Demo/Dev Kit (2020)
Hands-free control in VR via brain signals
(attention-based BCI)
France
AlterEgo Silent Speech
Wearable
Prototype tested
Enable silent communication with AI by
reading internal vocal signals
U. S. A. Brain-to-Brain Interface
(BrainNet experiment)
Research trial
Direct brain signal sharing for group prob-
lem-solving
U. S. A./Europe collaboration
Robotic Third Thumb
(UCL)
Research trial
Extra thumb controlled by foot–enhances
one-hand dexterity
U. K. Neuralink/Synchron BCI
Implants
In trials (since 2022)
Brain implants enabling thought-based device
control (paralysis aid, future augmentation)
U. S. A./Australia (global research)
DARPA TNT Neurostimulation
Research phase
Accelerate learning in healthy individuals via
nerve stimulation
U. S. A. Future Memory Chip Implant
Theoretical/Early dev. Boost memory retention and recall beyond
normal human limits
U. S. A. (academia, DARPA)
Bionic AR Contact Lens
Prototype (early tests)
Augmented reality display in the eye; poten-
tial IR/UV vision
U. S. A. (Silicon Valley startups)
Powered Full-Body Exosuit
Early development
Drastically amplify strength/speed for sol-
diers and workers
U. S. A., China, EU (defense R&D)
Brain-Cloud Interface
Conceptual
(R&D ongoing)
Direct wireless link between brain and cloud
AI for instant information access
Global (tech visionaries)
Human enhancement technologies are rapidly moving from concept to reality around the world. Table lists a number of these technologies, their status, purpose, and origin. Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
wearing EEG caps conveyed a yes/no instruction (whether to
rotate a block in a Tetris-like game) by just thinking it, which
was then transmitted via magnetic stimulation to a third per-
son’s brain. The third participant, not seeing the game, suc-
cessfully received the instruction in their mind and completed
the task, demonstrating direct brain-to-brain communication
of information. This and similar trials (sometimes dubbed
“BrainNet”) hint at a future where teams could exchange
information telepathically or solve problems together by shar-
ing cognitive load between brains. Such capabilities, while
rudimentary now, represent a form of collective human en-
hancement—essentially creating a networked “hive mind” for
collaborative thinking. Researchers are also experimenting with technologies to
improve cognitive functions such as learning, memory, and
concentration in healthy people. DARPA has a program called
Targeted Neuroplasticity Training to accelerate learning by
stimulating the nervous system. This project is investigating
methods such as non-invasive electrical nerve stimulation to
increase brain plasticity during training, eﬀectively accelerat-
ing skill acquisition. By triggering the release of neurotrans-
mitters that strengthen neural connections, this approach
aims to improve how quickly someone can learn a foreign
language or interpret complex images, for example. Several
human trials are underway to test whether techniques such as
stimulating the vagus nerve during training can improve cog-
nitive performance without signiﬁcant side eﬀects. Similarly,
companies have marketed transcranial brain stimulation head-
sets (using mild electrical or magnetic pulses) that claim to
improve everything from athletic performance to video game
concentration. Preliminary military research has suggested
that transcranial direct current stimulation may modestly ac-
celerate learning in tasks such as target recognition or lan-
guage proﬁciency.38) These studies treat the human body as a
system that can be tuned for better performance, blurring the
line between biology and machine optimization. Another experimental frontier is the synergy of human and
artiﬁcial intelligence working as a combined unit. Military
research programs in the U. S., China, and Europe are test-
ing “cognitive co-pilot” AI systems that support humans in
complex tasks. For instance, the U. S. Air Force has tried an
AI co-pilot in a ﬁghter jet simulator that can autonomously
handle tactical maneuvers, freeing the human pilot to focus
on strategy. In one 2023 test, a live ﬂight of a training jet was
controlled for a time by an AI agent, demonstrating a form of
shared control between human and machine. Meanwhile, ex-
perimental command interfaces allow a single soldier to coor-
dinate multiple robotic drones with high-level brain signals or
simple gestures, with AI managing the low-level details. The
goal of these trials is to augment a person’s eﬀective reach and
decision-making—essentially multiplying what one human
can do through intelligent automation. Early results show
that humans can adapt to trusting an AI partner for critical
split-second tasks (e.g., air combat maneuvers) and that brain-
control of swarms is feasible on a basic level. As this ﬁeld
progresses, we could see operational scenarios where a human
operator, equipped with a BCI and AI assistance, performs the
work of an entire team—a dramatic leap in human capability
empowered by machines.

## 3. THE FUTURE OF BMI

3.1. BMI-Induced Metamorphosis of Humans Numer-
ous innovative enhancement technologies are in the theoretical
or early development stage. While not yet realized, they are
grounded in current research trends and could become feasible
in the near future. Here, I would like to predict the possible
future forms of humans by listing several possibilities. Future human augmentation will not be limited to existing
senses; it will likely involve granting humans entirely new
ways to perceive the world. Engineers are developing bionic
contact lenses that could give users continuous augmented re-
ality vision or even the ability to see parts of the electromag-
netic spectrum we normally cannot (IR, UV). Prototypes of
AR contact lenses (such as those by Mojo Vision in the U. S.)
have already been tested, foreshadowing discreet vision en-
hancements. Researchers also imagine wearable sensor suites
feeding into the nervous system to provide novel senses—for
example, a vibrotactile vest that gives a 360° proximity sense
(alerting the wearer to movements or obstacles all around
them), or an implant that vibrates to indicate cardinal direc-
tion (essentially a built-in compass). Some biohackers have
experimented with magnetic implants to feel electromagnetic
ﬁelds, hinting at how an added sense could work. Indeed, in
my laboratory, we have successfully implanted a geomagnetic
sensor into the brain of an animal and had it solve a maze re-
lying on its absolute sense of direction39) (Fig. 2). Other researchers have used sensory substitution interfaces
to give blind individuals rudimentary “vision” through touch
or sound; the same concepts could apply to sighted users
to extend their perception. A plausible future device might
let a user “feel” Wi-Fi signals or chemical traces in the air,
analogous to how some animals sense magnetic ﬁelds or
pheromones. These sensory extensions would fundamentally
expand human experience and capabilities—a person could
navigate in pitch darkness via IR sense or detect health-related
signals from their body in real time. As sensor technology and
brain interfacing improve, the boundary of human senses will
broaden dramatically. The coming years will likely see today’s exoskeletons
evolve into more powerful, agile, and widely used gear. Re-
searchers aim to create full-body powered suits that substan-
tially increase strength, speed, and endurance while remaining
practical for regular use. Advances in lightweight materials,
energy-dense batteries, and soft robotics suggest that by 2030,
a wearable exosuit could allow a person to run at Olympic
sprinter speeds or carry a few hundred pounds with ease. Military organizations are funding next-generation combat
suits that integrate ballistic protection with strength augmen-
tation—essentially an “Iron Man” style armor that gives sol-
diers both defense and ampliﬁed power. For instance, China
has publicly shown concept videos of powered armor for
soldiers, and European projects (like in Germany and France)
are exploring exoskeletons to help infantry move faster with
heavy kit. In civil applications, future exoskeletons might en-
able construction workers to handle heavy tools and materials
single-handedly, or allow a ﬁreﬁghter to carry multiple people
out of danger. As these suits become more autonomous, AI
will likely be embedded to coordinate the suit’s movement
with the wearer’s intent, providing seamless assistance. The
trajectory of development points toward a time when wearing

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
a robotic suit could be as common for certain jobs as using
a power drill—eﬀectively making superhuman strength and
endurance part of the standard human toolbox. Farther on the horizon, futurists and some researchers
envision a world where human brains interface directly with
cloud computing and AI systems. In theory, a high-bandwidth
wireless BCI could allow real-time communication between
the brain and external databases or AI “co-processors.” This
means a person could potentially access information instantly
(without typing or even formulating a query in words)—for
example, recalling speciﬁc data or images from the cloud as if
it were their own memory. Such a brain-cloud link could also
enable “software upgrades” to the human mind, like down-
loading a new language or skill set directly into neural pat-
terns (a concept popularized in sci-ﬁ, but being considered in
brain simulation research). At a simpler level, a direct brain-
AI connection might function as an ever-present cognitive as-
sistant, monitoring one’s neural activity for signs of confusion
or fatigue and injecting just-in-time knowledge or alertness
boosts. Some experimental interfaces have already achieved
one-way information transmission (e.g., sending visual data to
the brain via neural implants for artiﬁcial vision), so extending
this to bidirectional ﬂow is a matter of overcoming techni-
cal challenges of bandwidth and decoding thoughts reliably. If achieved, the result would be a profound leap in human
capabilities—eﬀectively melding human intelligence with ma-
chine intelligence. A person could think of a complex problem
and have an AI parallel-process it, returning suggestions di-
rectly into the person’s conscious train of thought. While still
speculative, research by leading institutions and companies is
steadily moving in this direction, indicating that brain-cloud
interfaces are considered a plausible evolution of both AI and
human augmentation technologies. As humanity pushes further into space and extreme Earth
environments, augmentation tech is expected to play a key
role. Concepts are being explored for astronaut augmentation
suits that might protect against radiation or muscle/bone loss
by electrically stimulating the body during long missions. Exoskeletons and augmented reality will assist astronauts in
performing complex repairs or construction in space by pro-
viding extra strength and real-time instruction overlays. Even
neural control of robotic avatars is considered—for instance,
an astronaut on Mars controlling multiple robotic rovers or
drones via brain interface to multiply their reach across a
wide area. On Earth, deep-sea divers or miners might wear
exosuits that recycle breathing air and withstand pressure,
eﬀectively enlarging the habitable zone for humans. Enhance-
ments like expanded spectral vision could allow disaster
responders to see through smoke or detect vital signs behind
walls. These future applications, while specialized, demon-
strate the broad potential of human augmentation: to adapt
our bodies and minds to environments and tasks previously
beyond our capacity.
3.2. Dreamlike Futures Driven by BMI I would like to
Fig. 2. Visual Cortical Prosthesis with a Geomagnetic Compass Restores Spatial Navigation in Blind Rats
Spatial navigation was restored in blind rats via artiﬁcial head-direction cues. Microstimulators connected to a digital compass were implanted in the rat visual cortex. The blind rats learned to use this real-time directional feedback to successfully navigate mazes, performing similarly to sighted rats, demonstrating sensory substitution’s
potential. (A) Wiring diagram of the magnetic sensor brain chip. Two brain stimulation electrodes are connected to the digital magnetic sensor. The stimulation intensity
can be changed in the range of 0–4V (volts), and it is equipped with a power switch and a rechargeable lithium battery. (B) External image of the magnetic sensor brain
chip. (C) Image of the chip attached to the head of a rat. It is 25 mm long, 10 mm wide, 9 mm thick, and weighs 2.5 g. This ﬁgure is modiﬁed from a paper by Norimoto
and Ikegaya.39)

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
predict the future neurotechnology I would like to see in 100
years. These technologies are unlikely to be realized in the
near future. But the progress of science and technology has al-
ways exceeded our expectations. Therefore, with the hope that
future progress will exceed expectations in a non-linear way, I
predict the future world.
3.2.1. Dream Theater
Projected advances in non-invasive neural interfacing and
artiﬁcial intelligence may enable the development of systems
capable of recording, analyzing, and replaying human dream
experiences. Such “dream theater” technology would likely
use sophisticated sensors, perhaps integrated into sleep en-
vironments, to capture the complex patterns of neural activ-
ity, particularly during REM sleep, along with associated
physiological markers. AI algorithms trained on large neuro-
phenomenological datasets would then translate this bio-signal
data into reconstructible multi-sensory formats, allowing users
to retroactively experience their dreams in immersive virtual
environments. Potential applications are many, ranging from
therapeutic uses where individuals could explore unconscious
content under clinical guidance, to signiﬁcant advances in
neuroscience research on consciousness and memory. In addi-
tion, the ability to archive and even share dream content (with
explicit consent) could create new avenues for artistic expres-
sion, interpersonal connection, and potentially educational
simulations based on symbolic dream structures.
3.2.2. 100% Synchronized Mobility
Personal transportation could evolve into a highly inte-
grated, autonomous system of multimodal mobility pods
capable of both ground and air travel. This “synchronized
mobility” paradigm envisions personal devices seamlessly
connected within a larger network managed by sophisticated
AI. These pods would use advanced propulsion systems to en-
able transitions between, for example, ground-level magnetic
conduits and low-altitude ﬂight paths. Crucially, the system
would operate with near-total automation, optimizing routes,
speed, and mode of travel based on real-time network traﬃc
data, environmental conditions, user destination inputs, and
potentially even the user’s physiological state as monitored by
integrated biometric sensors. The goal is to provide eﬃcient,
safe, and comfortable transportation tailored to individual
needs, eliminating traditional traﬃc congestion and minimiz-
ing travel time. Potential societal beneﬁts include dramatically
improved transportation eﬃciency, increased accessibility for
diverse populations, reduced accident rates, and the possibility
of signiﬁcant urban redevelopment by reclaiming space cur-
rently dedicated to traditional road infrastructure.
3.2.3. Delivering the Five Senses
Future communication technologies may transcend current
audio-visual limitations to incorporate the transmission and
reproduction of the full range of human senses—sight, sound,
touch, smell, and taste—over distances. This concept requires
the development of advanced sensor suites capable of captur-
ing detailed haptic information (pressure, texture, tempera-
ture), complex olfactory and gustatory data (via sophisticated
chemosensors), and high-ﬁdelity audio-visual streams. This
multi-sensory data would require high-bandwidth transmission
and sophisticated receiver interfaces, including full-body hap-
tic suits, spatial audio systems, high-resolution visual displays,
and controlled olfactory and gustatory simulators capable of
replicating speciﬁc smells and tastes based on the transmitted
chemical analyses. Such technology would enable true telep-
resence, allowing individuals to experience remote environ-
ments or share sensory experiences with others with unprec-
edented realism. Applications include remote collaboration
requiring tactile feedback (e.g., telesurgery, complex repairs),
deeply immersive education and training, highly realistic vir-
tual tourism, enhanced social interaction for geographically
separated individuals, and new opportunities for accessibility.
3.2.4. Superhuman Sports Competition
The next century could see the emergence of novel sports
competitions that are fundamentally diﬀerent from current
sports, enabled by virtual reality (VR), augmented real-
ity (AR), accessible zero-gravity environments, and human-
machine integration. These “superhuman sports” could use
fully immersive virtual arenas where physics can be altered,
or use AR overlays on physical ﬁelds to add dynamic informa-
tion or interactive elements. Dedicated facilities that provide
microgravity or zero gravity conditions would enable sports
that emphasize three-dimensional movement and unique
biomechanics. In addition, athletes could use performance-
enhancing technologies, such as sophisticated exoskeletons
for increased strength or agility, or neural interfaces for faster
reaction times, and compete in speciﬁc regulated classes. A
signiﬁcant development could be the integration of advanced
robotics and AI, leading to formats where humans work with
robotic teammates, requiring complex inter-agent strategies, or
compete against highly capable AI opponents. These competi-
tions would push the limits of human physical and cognitive
performance, oﬀer new forms of spectacular entertainment,
potentially experienced through immersive spectator inter-
faces, and serve as platforms for research in areas such as
robotics, AI strategy, and human augmentation.
3.2.5. Instantaneous Skill Acquisition
Developments in BCI technology and cognitive neuro-
science could potentially lead to methods for transferring
complex skills and knowledge directly into the human brain,
bypassing traditional learning processes. This “instantaneous
skill acquisition” would hypothetically involve BCIs capable
of precise neural stimulation, guided by AI systems that trans-
late curated skill datasets (e.g., machine operating procedures,
linguistic knowledge) into speciﬁc patterns of neural activ-
ity. The goal would be to induce or accelerate the formation
of the neural correlates associated with the desired skill or
knowledge base. If realized, this could drastically reduce the
time required to achieve proﬁciency in complex tasks, facili-
tate rapid workforce adaptation, enhance emergency response
capabilities by enabling personnel to quickly learn to use
unfamiliar equipment, and potentially democratize access to
specialized expertise.
3.2.6. Telepathy
BCIs combined with sophisticated AI could enable a form
of technologically mediated telepathy, facilitating direct brain-
to-brain communication. This system would aim to decode the
neural correlates of thoughts, intentions, and possibly emo-
tional states in an individual and transmit this information,
possibly via an intermediary AI translator that converts it into
a standardized neural code or directly stimulates the recipi-
ent’s BCI to evoke the intended meaning. Such a technology
could transcend language barriers and allow for richer, more
nuanced, and faster communication. In theory, research into
mapping the neural or analog signaling systems of non-human

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
organisms could enable rudimentary forms of interspecies
communication, allowing humans to interpret basic states or
intentions in animals, or even to analyze collective signals
from plants or microbial communities. Potential applications
include universal translation, enhanced collaboration, novel
therapeutic tools for communication disorders, and the promo-
tion of deeper ecological awareness.
3.2.7. Virtual Space-Time Warp
Leveraging mature VR and comprehensive sensory simu-
lation technologies, it may become possible to create highly
immersive and interactive reconstructions of past events,
environments, and individuals. This “Virtual Time Machine”
concept relies on powerful AI engines to process massive
data sets—historical records, archaeological ﬁndings, pale-
ontological data, climate models, potentially even digitized
personal archives—to generate high-ﬁdelity simulations. Users
equipped with advanced VR displays and full sensory feed-
back systems (haptic, olfactory, gustatory) could experience
these simulations with a strong sense of presence. Functional-
ity could include exploring historical settings such as ancient
cities, witnessing signiﬁcant events of the past, encountering
realistic simulations of extinct creatures based on scientiﬁc
data, or even interacting with AI-driven reconstructions of de-
ceased individuals modeled from their available data. Primary
applications are in education, providing embodied learning
experiences far beyond traditional methods, and potentially in
therapeutic contexts such as grief counseling (though ethically
sensitive). It could also be used for entertainment, cultural
preservation, and professional training.
3.3. Obsolescence of Man The relentless pace of scien-
tiﬁc advancement, particularly in the ﬁelds of neurotechnol-
ogy, BMI/BCI, and human augmentation, compels a perspec-
tive beyond immediate clinical or practical applications. While
detailed empirical ﬁndings are the foundation of scientiﬁc
progress, synthesizing the trajectory indicated by these con-
verging ﬁelds reveals profound implications that challenge
our most fundamental understanding of human identity and
potential. An analysis of current capabilities-restoring com-
plex motor function via neural bypasses, decoding neural
correlates of language, augmenting sensory input and physical
capacity, achieving rudimentary brain-to-brain information
transfer-points to a conclusion of startling signiﬁcance: the
biological blueprint of Homo sapiens no longer dictates the
necessary or ultimate limits of human existence. The assump-
tion that we must remain conﬁned to our current form is being
actively dismantled by our own technological ingenuity. For centuries, the study of the human condition has sought
to identify an immutable “human nature”—a core set of char-
acteristics deﬁned by our biology. For example, reason, com-
plex language, the use of tools, certain modes of conscious-
ness, and the inescapable realities of aging and mortality
might have been considered deﬁnitional constraints. Based on
these biological limitations and possibilities, complex social,
ethical, and political frameworks have been constructed. How-
ever, the data presented from BMI and augmentation research
does not merely reﬁne these frameworks; it fundamentally
destabilizes them. It empirically demonstrates that “human”
functionality is not a static property, but a remarkably adap-
tive system capable of radical expansion and modiﬁcation
when integrated with technology. Our current biological state
increasingly appears to be a contingent starting point, not a
ﬁxed destiny. Consider the strong evidence for the decoupling of intention
and cognition from their native biological substrate. When
cortical signals representing the intention to walk are suc-
cessfully decoded and used to drive spinal cord stimulators
or prosthetic limbs, bypassing damaged neural pathways, we
are witnessing more than therapeutic success. This demon-
strates the principle of functional substrate independence in
action. The cognitive process achieves its functional goal via
an artiﬁcial medium, proving that the execution of intention is
not inextricably bound to the original organic hardware. The
central nervous system turns out to be an astonishingly adapt-
able control system, capable of interfacing with and directing
non-biological components. This empirical reality forces us to
confront the core idea: there is no intrinsic biological mandate
that requires humans to remain solely within the operational
boundaries of their birth-assigned physiology. The trajectory of human augmentation reinforces this
conclusion. Exoskeletons that augment strength, augmented
reality systems that fuse digital information directly into per-
ception, BCIs that translate thought into control signals, and
even experimental integrations such as supernumerary robotic
limbs demonstrate the profound morphological and cognitive
plasticity achievable through technological mediation. These
are not merely external devices; they represent nascent forms
of human-machine integration that extend embodiment, sen-
sory range, and cognitive capabilities in ways that redeﬁne the
user’s interaction with the world. The boundary between the
biological “self” and the artiﬁcial “tool” becomes function-
ally blurred, potentially irrelevant. This leads to a necessary
reconceptualization of human potential. It is no longer just
about optimizing innate biological talents or pushing the lim-
its of unaided physiology. Instead, human potential becomes
an open-ended design and engineering challenge—a question
of what capabilities can be achieved through the synergistic
integration of biological systems with engineering technolo-
gies, limited more by ingenuity and physical laws than by
basic biology. The potential is no longer just within us; it is
constructible. This demonstrated malleability forces a radical reassess-
ment of what constitutes the meaning of human existence
from a functional and operational perspective. If core biologi-
cal limitations—physical frailty, sensory limitations, cognitive
processing speeds, even the barriers of communication—can
be systematically overcome or augmented by technology, then
the very challenges that have historically deﬁned the human
struggle lose their centrality. What deﬁnes our existence when
the timeline of mortality becomes elastic, when knowledge
acquisition bypasses laborious learning (“Instant Skill Acqui-
sition”), when communication transcends linguistic ambiguity
(“Telepathy”), or when subjective experience can be curated
and shared with unprecedented ﬁdelity (“Delivering the Five
Senses,” “Dream Theater”)? The operational deﬁnition of
being human is shifting. The “meaning” derived from navigat-
ing a speciﬁc set of biological constraints is replaced by the
meaning found in exploring a vastly expanded state space of
possible functions, experiences, and interactions enabled by
technology. As a result, the meaning and purpose of human life has
changed—or, more accurately, the parameters that deﬁne
possible meanings and purposes are undergoing a revolution-

Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
ary expansion. Historically, purpose was often framed by
biological imperatives (survival, reproduction, adaptation to
the environment) and the pursuit of knowledge or fulﬁllment
within those constraints. Technology now introduces the pos-
sibility of designed purpose. Meaning can increasingly be de-
rived from participating in technologically mediated realities,
contributing to hybrid cognitive networks (‘BrainNet’, AI co-
pilots), exploring novel sensory inputs or engineered environ-
ments (‘Virtual Space-Time Warp’), or even deliberately shap-
ing our own ongoing evolution. The narrative arc of human
life, traditionally bounded by biological milestones, is subject
to technological revision. Purpose is transformed from a found
condition to a designed goal, potentially selected from a menu
of technologically enabled possibilities that far exceeds bio-
logical precedent. What, then, will be the future operational role of entities
derived from the Homo sapiens lineage? Extrapolation of
current trends—toward deeper brain-computer interfacing,
enhanced physical and cognitive augmentation, possibly even
brain-cloud integration—suggests that biological humans may
be a transitional form. We may be precursors of successor
entities that seamlessly integrate biology and technology and
possess capabilities (augmented senses, radically enhanced
cognition, networked consciousness, indeﬁnite operational
lifespans) that make them functionally distinct from us. This
is not a dystopian prediction, but a plausible trajectory based
on observed scientiﬁc progress and capability expansion. Acknowledging this trajectory requires intellectual cour-
age that goes beyond reﬂexive fears of “losing humanity. What speciﬁc aspects of our current biologically constrained
existence do we implicitly defend as sacrosanct? Vulner-
ability to disease and decay? Cognitive biases hardwired by
evolutionary pressures? The inherent limitations of biological
computation and communication? Emerging technologies oﬀer
potential pathways beyond these limitations. A rigorous scien-
tiﬁc perspective compels us to analyze this potential without
premature ethical closure, focusing instead on the functional
and evolutionary implications. Ongoing research into brain-to-brain communication,
cognitive augmentation through AI partnership, and targeted
neuroplasticity represent more than technological develop-
ment; they are explorations into the fundamental nature of
cognition, individuality, and cooperation. They explore the
possibility that intelligence will become a networked, hybrid
phenomenon, shifting the primary unit of agency from the
individual biological organism to integrated human-machine
systems. The future role of humans may be less about indi-
vidual capabilities and more about contributing specialized
biological processing or subjective experience within a larger
cognitive architecture, tackling challenges on a scale previ-
ously unimaginable. While highly futuristic concepts such as widespread te-
lepathy or instantaneous skill downloads remain speculative,
they represent logical extensions of demonstrated principles:
increasingly precise neural decoding and stimulation, sophis-
ticated AI pattern analysis, and growing understanding of
the neural correlates of cognition and skill. To dismiss such
possibilities is to ignore the consistent historical pattern of
technological acceleration, where today’s theoretical frontier
becomes tomorrow’s technological reality. Thus, the central insight-that there is no immutable bio-
logical imperative for humans to remain as they are—is not
an abstract philosophical notion, but an emergent consequence
of scientiﬁc and technological progress. It represents a po-
tential turning point in the history of life, in which a species
develops the capacity to actively and consciously redesign its
own functional golem, transcending the limitations imposed
by its evolutionary heritage. We are potentially witnessing the
dawn of conscious, technologically mediated evolution. The
critical task now is not merely to reﬁne these technologies,
but to grapple with the profound transformation they imply
for human potential, the operational meaning of human exis-
tence, and the radically altered landscape of the meaning and
purpose of human life. Rejecting the notion of a ﬁxed human
essence allows us to confront the possibility that we are not
the endpoint of evolution, but perhaps the initiators of a new,
uncharted phase-one deﬁned not by the constraints we inherit,
but by the capabilities we choose to build. This perspective,
grounded in scientiﬁc reality while acknowledging its para-
digm-shifting implications, oﬀers a truly breakthrough view
of our potential future.

## 4. CONCLUSION

In this review, I have described the history of brain-ma-
chine fusion from its earliest days and made predictions about
the future. I have been fully aware that the realization of these
boldly drawn future scenarios—ranging from deeply personal
dream theaters and hyper-eﬃcient synchronized mobility to
the transmission of full sensory experiences, the emergence
of superhuman sports, the possibility of instantaneous skill
acquisition, technologically mediated telepathy, and immersive
virtual journeys through time—would undoubtedly trigger
a cascade of events. These technologies would undoubtedly
trigger a cascade of profound and complex ethical questions
requiring rigorous societal debate, careful governance, and the
establishment of entirely new moral frameworks. This review
article deliberately focuses primarily on articulating the sheer
technological potential and visionary scope inherent in these
concepts. In other words, the intention here is ﬁrst to map out
the frontiers of what might be possible from an innovation
standpoint, stimulating thought about future capabilities and
their transformative applications in ﬁelds as diverse as thera-
py, transportation, communication, entertainment, education,
and even basic human connectivity (I personally look forward
to the future that the Zoromes in “The Jameson Satellite” will
realize safely and beneﬁcially). Therefore, deliberately reserv-
ing the equally crucial, and necessarily nuanced analysis of
their multifaceted ethical implications—ranging from privacy
and consent to equity, autonomy, and the very deﬁnition of
human experience—for a separate, dedicated, and more appro-
priately detailed examination, rather than diluting the current
exploration of forward-looking technological trajectories. Acknowledgments This article was prepared in commem-
oration of receiving the Award of the Pharmaceutical Society
of Japan. The author wishes to express sincere gratitude to the
members of the award selection committee, all relevant par-
ties, and everyone who contributed to this research. This work
was supported by JST ERATO (JPMJER1801), the Institute
for AI and Beyond of the University of Tokyo, and AMED
Brain/MINDS 2.0 (24wm0625207s0101; 24wm0625401h0001; Biol. Pharm. Bull. Vol. 48, No. 8 (2025)
24wm0625502s0501). In preparing this manuscript, the author
partly utilized several models of generative artiﬁcial intelli-
gence, including their “deep research” functions, to search for
literature, write the draft, and proofread. Conﬂict of Interest The author declares no conﬂict of
interest. REFERENCES
1) Lebedev MA, Nicolelis MAL. Brain-machine interfaces: From basic
science to neuroprostheses and neurorehabilitation. Physiol. Rev.,
97, 767–837 (2017).
2) Caton R. The electric currents of the brain. Chicago J. Nerv. Mental
Disease, 2, 610 (1875).
3) Tudor M, Tudor L, Tudor KI. Hans Berger (1873–1941)—the history
of electroencephalography. Acta Med. Croatica, 59, 307–313 (2005).
4) Fetz EE. Operant conditioning of cortical unit activity. Science, 163,
955–958 (1969).
5) Moritz CT, Fetz EE. Volitional control of single cortical neurons in
a brain-machine interface. J. Neural Eng., 8, 025017 (2011).
6) Lucier A. Music for solo performer. Lovely Music, Lovely Com-
munications, Ltd. (1982). https://www.discogs.com/release/758828-
Alvin-Lucier-Music-For-Solo-Performer-For-Enormously-
Ampliﬁed-Brain-Waves-And-Percussion?srsltid=AfmBOorOmR6-
UsheIJkd8VCee2uIfZJQIu0kb5yW3piHtIqdwzkGgRrX
7) Vidal JJ. Toward direct brain-computer communication. Annu. Rev. Biophys. Bioeng., 2, 157–180 (1973).
8) Vidal JJ. Real-time detection of brain events in EEG. Proc. IEEE
Inst. Electr. Electron. Eng., 65, 633–641 (1977).
9) Bozinovski S, Sestakov M, Bozinovska L. Using EEG alpha rhythm
to control a mobile robot, Proceedings of the Annual International
Conference of the IEEE Engineering in Medicine and Biology Soci-
ety, New Orleans, LA, USA, on 1988/11/4-1988/11/7, 1988, IEEE.
10) Bozinovska L, Stojanov G, Sestakov M, Bozinovski S. CNV pattern
recognition: step toward a cognitive wave observation. Proc. Eur. Signal Process. Conf., 1659–1662 (1990).
11) Georgopoulos AP, Schwartz AB, Kettner RE. Neuronal population
coding of movement direction. Science, 233, 1416–1419 (1986).
12) Stanley GB, Li FF, Dan Y. Reconstruction of natural scenes from
ensemble responses in the lateral geniculate nucleus. J. Neurosci.,
19, 8036–8042 (1999).
13) Chapin JK, Moxon KA, Markowitz RS, Nicolelis MA. Real-time
control of a robot arm using simultaneously recorded neurons in the
motor cortex. Nat. Neurosci., 2, 664–670 (1999).
14) Wessberg J, Stambaugh CR, Kralik JD, Beck PD, Laubach M, Chapin JK, Kim J, Biggs SJ, Srinivasan MA, Nicolelis MA. Real-
time prediction of hand trajectory by ensembles of cortical neurons
in primates. Nature, 408, 361–365 (2000).
15) Lorach H, Galvez A, Spagnolo V, et al. Walking naturally after spi-
nal cord injury using a brain-spine interface. Nature, 618, 126–133
(2023).
16) Rebsamen B, Guan C, Zhang H, Wang C, Teo C, Ang MH Jr, Burdet E. A brain controlled wheelchair to navigate in familiar
environments. IEEE Trans. Neural Syst. Rehabil. Eng., 18, 590–598
(2010).
17) Phillip A. A paralyzed woman ﬂew an F-35 ﬁghter jet in a simula-
tor—using only her mind, 2015.
18) Flesher SN, Downey JE, Weiss JM, Hughes CL, Herrera AJ, Tyler-
Kabara EC, Boninger ML, Collinger JL, Gaunt RA. A brain-com-
puter interface that evokes tactile sensations improves robotic arm
control. Science, 372, 831–836 (2021).
19) Willett FR, Avansino DT, Hochberg LR, Henderson JM, Shenoy
KV. High-performance brain-to-text communication via handwrit-
ing. Nature, 593, 249–254 (2021).
20) Metzger SL, Littlejohn KT, Silva AB, Moses DA, Seaton MP, Wang R, Dougherty ME, Liu JR, Wu P, Berger MA, Zhuravleva I, Tu-Chan A, Ganguly K, Anumanchipalli GK, Chang EF. A high-
performance neuroprosthesis for speech decoding and avatar con-
trol. Nature, 620, 1037–1046 (2023).
21) Barrie R. Three companies to rival Neuralink in the BCI clinical
trial landscape, 2024.
22) Chaudhary U, Vlachos I, Zimmermann JB, Espinosa A, Tonin A, Jaramillo-Gonzalez A, Khalili-Ardali M, Topka H, Lehmberg J, Friehs GM, Woodtli A, Donoghue JP, Birbaumer N. Spelling inter-
face using intracortical signals in a completely locked-in patient en-
abled via auditory neurofeedback training. Nat. Commun., 13, 1236
(2022).
23) Rao VR, Rolston JD. Unearthing the mechanisms of responsive
neurostimulation for epilepsy. Commun. Med. (Lond.), 3, 166
(2023).
24) Scangos KW, Khambhati AN, Daly PM, Makhoul GS, Sugrue LP, Zamanian H, Liu TX, Rao VR, Sellers KK, Dawes HE, Starr PA, Krystal AD, Chang EF. Closed-loop neuromodulation in an individ-
ual with treatment-resistant depression. Nat. Med., 27, 1696–1700
(2021).
25) Schreiner L, Wipprecht A, Olyanasab A, Sieghartsleitner S, Pretl
H, Guger C. Brain-computer-interface-driven artistic expression:
real-time cognitive visualization in the pangolin scales animatronic
dress and screen dress. Front. Hum. Neurosci., 19, 1516776 (2025).
26) Jade L, Gentle S. New ways of knowing ourselves. BCI facilitating
artistic exploration of our biology. Brain Art. Springer International
Publishing, Cham, pp. 229–262 (2019).
27) Fazel-Rezai R, Allison BZ, Guger C, Sellers EW, Kleih SC, Kübler
A. P300 brain computer interface: current challenges and emerging
trends. Front. Neuroeng., 5, 14 (2012).
28) Bakkum DJ, Gamblen PM, Ben-Ary G, Chao ZC, Potter SM. MEART: The semi-living artist. Front. Neurorobot., 1, 5 (2007).
29) Sargeant B, Dwyer J, Mueller F. ‘ﬂoyd’. The storytelling machine: A playful participatory automated system featuring crowd-sourced
story content, Proceedings of the 2018 Annual Symposium on Com-
puter-Human Interaction in Play Companion Extended Abstracts, Melbourne VIC Australia, on 2018/10/28–2018/10/31, 23 October,
2018, ACM, New York, NY, U. S. A.
30) Yamashiro K, Matsumoto N, Ikegaya Y. Diﬀusion model-based
image generation from rat brain activity. PLOS ONE, 19, e0309709
(2024).
31) Scharping N. Disabled musicians make music with their minds,
2016.
32) Deuel TA, Pampin J, Sundstrom J, Darvas F. The Encephaloph-
one: a novel musical biofeedback device using conscious control
of electroencephalogram (EEG). Front. Hum. Neurosci., 11, 213
(2017).
33) Neuralink monkey plays MindPong telepathically, 2021.
34) Kagan BJ, Kitchen AC, Tran NT, Habibollahi F, Khajehnejad M, Parker BJ, Bhat A, Rollo B, Razi A, Friston KJ. In vitro neurons
learn and exhibit sentience when embodied in a simulated game-
world. Neuron, 110, 3952–3969.e8 (2022).
35) Stein S. Moving objects with Mattel’s brainwave-reading Mindﬂex,
2009.
36) Kieliba P, Clode D, Maimon-Mor RO, Makin TR. Robotic hand
augmentation drives changes in neural body representation. Sci. Robot., 6, eabd7935 (2021).
37) Jiang L, Stocco A, Losey DM, Abernethy JA, Prat CS, Rao RPN. BrainNet: A multi-person brain-to-brain interface for direct col-
laboration between brains. Sci. Rep., 9, 6115 (2019).
38) Krause MR, Zanos TP, Csorba BA, Pilly PK, Choe J, Phillips ME, Datta A, Pack CC. Transcranial direct current stimulation facilitates
associative learning and alters functional connectivity in the pri-
mate brain. Curr. Biol., 27, 3086–3096.e3 (2017).
39) Norimoto H, Ikegaya Y. Visual cortical prosthesis with a geomag-
netic compass restores spatial navigation in blind rats. Curr. Biol.,
25, 1091–1095 (2015).
