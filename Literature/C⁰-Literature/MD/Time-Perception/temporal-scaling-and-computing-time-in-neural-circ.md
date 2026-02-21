# temporal-scaling-and-computing-time-in-neural-circ

TYPE Hypothesis and Theory
PUBLISHED 08 December 2022
DOI 10.3389/fnbeh.2022.1022713
OPEN ACCESS
EDITED BY
Koji Toda,
Keio University, Japan
REVIEWED BY
Akihiro Shimbo,
National Institute on Drug Abuse (NIH),
United States
Youcef Bouchekioua,
Queens College (CUNY), United States
*CORRESPONDENCE
Peter D. Balsam
balsam@columbia.edu
SPECIALTY SECTION
This article was submitted to
Learning and Memory,
a section of the journal
Frontiers in Behavioral Neuroscience
RECEIVED 18 August 2022
ACCEPTED 31 October 2022
PUBLISHED 08 December 2022
CITATION
De Corte BJ, Akdo˘gan B and Balsam
PD (2022) Temporal scaling and
computing time in neural circuits:
Should we stop watching the clock and
look for its gears?
Front. Behav. Neurosci. 16:1022713.
doi: 10.3389/fnbeh.2022.1022713
COPYRIGHT
© 2022 De Corte, Akdo ˘gan and
Balsam. This is an open-access article
distributed under the terms of the
Creative Commons Attribution License
(CC BY). The use, distribution or
reproduction in other forums is
permitted, provided the original
author(s) and the copyright owner(s)
are credited and that the original
publication in this journal is cited, in
accordance with accepted academic
practice. No use, distribution or
reproduction is permitted which does
not comply with these terms.
Temporal scaling and
computing time in neural
circuits: Should we stop
watching the clock and look for
its gears?
Benjamin J. De Corte 1,2, Ba¸ sak Akdo˘gan 1,2 and Peter D.
Balsam 1,2,3*
1Department of Psychology, Columbia University, New York, NY, United States, 2Division of
Developmental Neuroscience, New York State Psychiatric Institute, New York, NY, United States,
3Department of Neuroscience and Behavior, Barnard College, New York, NY, United States
Timing underlies a variety of functions, from walking to perceiving causality.
Neural timing models typically fall into one of two categories—“ramping”
and “population-clock” theories. According to ramping models, individual
neurons track time by gradually increasing or decreasing their activity as
an event approaches. To time different intervals, ramping neurons adjust
their slopes, ramping steeply for short intervals and vice versa . In contrast,
according to “population-clock” models, multiple neurons track time as a
group, and each neuron can ﬁre nonlinearly. As each neuron changes its
rate at each point in time, a distinct pattern of activity emerges across
the population. To time different intervals, the brain learns the population
patterns that coincide with key events. Both model categories have empirical
support. However, they often differ in plausibility when applied to certain
behavioral effects. Speciﬁcally, behavioral data indicate that the timing system
has a rich computational capacity, allowing observers to spontaneously
compute novel intervals from previously learned ones. In population-clock
theories, population patterns map to time arbitrarily, making it difﬁcult to
explain how different patterns can be computationally combined. Ramping
models are viewed as more plausible, assuming upstream circuits can
set the slope of ramping neurons according to a given computation.
Critically, recent studies suggest that neurons with nonlinear ﬁring proﬁles
often scale to time different intervals—compressing for shorter intervals
and stretching for longer ones. This “temporal scaling” effect has led to
a hybrid-theory where, like a population-clock model, population patterns
encode time, yet like a ramping neuron adjusting its slope, the speed
of each neuron’s ﬁring adapts to different intervals. Here, we argue that
these “relative” population-clock models are as computationally plausible as
ramping theories, viewing population-speed and ramp-slope adjustments as
equivalent. Therefore, we view identifying these “speed-control” circuits as a
key direction for evaluating how the timing system performs computations.
Frontiers in Behavioral Neuroscience 01 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
Furthermore, temporal scaling highlights that a key distinction between
different neural models is whether they propose an absolute or relative time-
representation. However, we note that several behavioral studies suggest the
brain processes both scales, cautioning against a dichotomy.
KEYWORDS
time perception, drift-diffusion, population-clock, temporal scaling, temporal
averaging, ramping activity, timing
Introduction
Time is a fundamental dimension of the world, and our
nervous systems have likely been adapting to this fact since we
began evolving. At a basic level, most motor programs, such
as walking or riding a bicycle, require executing a series of
well-timed and appropriately ordered actions. However, time
also underlies many higher-order processes. For example, to
comprehend causality, we must be able to recognize that causes
precede their effects (Hume, 1739). When forming memories of
personal experiences, we not only encode what happened and
where, but also when different events occurred (Tulving, 1986).
Relatedly, when we engage in decision-making, we often draw on
prior experience to predict when future events will happen and
adapt our behavior accordingly. Time governs virtually all facets
of our daily lives, and in our view, the true challenge is ﬁnding
a process that we engage in where time is entirely irrelevant.
Therefore, uncovering how the brain represents time is a key
topic in neuroscience.
Admittedly, “how does the brain track time?” is a remarkably
broad question. However, there are ways to constrain the
problem. For example, many sense modalities have dedicated
organs (e.g., eyes for vision, cochlea for audition), yet there does
not seem to be an analogous organ for processing time. In many
ways, this aligns with common sense. We would be surprised if
the system that allows us to effectively coordinate our footsteps
in time were the same as the one that regulates our sleep-wake
cycles over daily periods. Consistent with this, we now know
that circadian timing is largely regulated by gene-expression
rhythms in the suprachiasmatic nucleus (Drucker-Colín et al.,
1984; Silver et al., 1996). In contrast, millisecond-timing, being
important for motor coordination/calibration, relies on neural
activity in regions such as primary sensory/motor areas (Long
et al., 2016), the cerebellum (Garcia and Mauk, 1998), and
central pattern generators in the spinal cord (Kudo and Y amada,
1987). Therefore, when asking how the brain tracks time, we can
hone the question by choosing a timescale of interest (for further
discussion see Buhusi and Meck, 2005; Paton and Buonomano,
2018).
In the present article, we will focus on “interval timing, ”
which generally falls in the seconds-to-hours range. Interval
timing underlies a variety of processes, such as associative
learning (Gallistel and Gibbon, 2000; Balsam and Gallistel,
2009), causal-inference (Roberts and Holder, 1984; Fereday
et al., 2019), and decision-making (Balci et al., 2009a; Gür
et al., 2018). It recruits a complex network, including (but
not limited to) several association cortices (Leon and Shadlen,
2003; Merchant et al., 2013; Bakhurin et al., 2017; Buhusi et al.,
2018), thalamic nuclei (Komura et al., 2001; Wang et al., 2018;
Lusk et al., 2020), the basal ganglia (Gouvêa et al., 2015; Mello
et al., 2015), and midbrain dopamine centers (Meck, 2006;
Soares et al., 2016; Howard et al., 2017). Despite extensive
investigation, little consensus has emerged over how these
areas encode time or interact to support temporal processing.
However, recent experiments have consistently pointed to a
general principle by which the brain might accomplish interval
timing—referred to as “temporal scaling. ” Part of this manuscript
will serve as a concise review of these data. However, we will
give more emphasis to how these ﬁndings: (1) recontextualize
past theoretical disputes in the ﬁeld; (2) reframe the distinctions
we draw between different timing models; and (3) provide clear
future directions for studying the neural mechanisms of timing.
The general schema of most interval
timing models
Theorists have developed a variety of neural models of
timing (Grossberg and Schmajuk, 1989; Matell and Meck, 2004;
Buonomano and Maass, 2009; Simen et al., 2011; Wang et al.,
2018). The speciﬁcs of one theory often differ substantially from
the others. However, at a general level, most models segregate the
timing system into the same core set of subprocesses. To frame a
more detailed theoretical discussion below, we will ﬁrst overview
these similarities.
To illustrate with a concrete example, consider how one
would develop a model that explains behavior during the “peak-
interval” procedure—a common interval timing task (Roberts,
1981). This task can be used with a variety of species (mice:
Balci et al., 2009b; rats: Roberts, 1981; goldﬁsh: Drew et al.,
2005; humans: Rakitin et al., 1998). However, as much of our
discussion will center on data from rats, we will illustrate how
the task applies to this species speciﬁcally (Figure 1). During this
task, experimenters place rats in an operant chamber, containing
a response-manipulandum (e.g., lever). Occasionally, a cue (e.g.,
light) turns on that signals that reward can be earned for
Frontiers in Behavioral Neuroscience 02 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
FIGURE 1
Peak-interval procedure. (A) Illustration of task equipment. (B)
Task-design diagram. (C) Illustration of ideal behavior during
probe trials with respect to mean response rates (top) and single-
trials (bottom).
responding after a speciﬁc duration elapses (e.g., 30 s). During
some trials, the ﬁrst response a rat makes after this interval has
passed causes the cue to turn off and the reward to be delivered.
However, experimenters also include a subset of “probe” trials
during which the cue remains on for much longer than normal
(e.g., 90–120 s) and no reward is provided (Figure 1B).
During a probe trial, a rat must know when to begin
responding in anticipation of a reward and when to stop
responding once the target-interval has passed. Consistent with
this, a trained rat will typically emit a discrete cluster of responses
that fall around the target interval–usually beginning before
and ending after it elapses ( Figure 1C ; Gibbon and Church,
1990). When the cluster starts and stops (simply referred to as
the start- and stop-times) will vary slightly from one trial to
the next. Consequently, when averaged across trials, response
rates plotted across time will resemble a normal distribution,
with a peak (i.e., “peak time”) centered over the target duration.
How close the peak-, start-, and stop-times fall to the true
target interval indicate how accurately a rat is performing.
Furthermore, the variability of start- and stop-times—as well
as the width of the mean response distribution—reﬂect how
precisely a rat is timing.
To construct a model that explains performance during this
task, we would want to capture three general processes that
the brain must implement to guide performance. First, it must
obviously contain a time-keeping mechanism that allows it to
track time as it passes, particularly the moment of reward.
Second, to use the time of reward during future trials, the
brain must be able to represent it in memory. Finally, the brain
must contain a decision-making mechanism that allows the two
above processes to guide behavior, executing responses near the
remembered interval. As highlighted below, virtually all neural
models of timing (and also most behavioral ones; e.g., Gibbon
et al., 1984; Killeen and Fetterman, 1988; Church and Broadbent,
1990; Machado, 1997) address these three core functions, yet
they can differ markedly in their proposals over how each is
implemented.
Classes of timing models
For brevity, we will avoid giving an exhaustive overview of
existing neural theories of timing. Instead, we will describe the
two most dominant model categories—ramping and population-
clock theories—and provide one speciﬁc example of each.
Ramping models
According to ramping models, time-keeping is accomplished
via individual neurons that gradually increase or decrease their
activity across time–aptly referred to as “ramping” neurons
(Figure 2; Durstewitz, 2003; Reutimann et al., 2004; Gavornik
et al., 2009; Simen et al., 2011). Subjects execute decisions
when these neurons reach particular ﬁring rates, referred to
as “decision thresholds. ” Importantly, to time these decisions
effectively, a ramping neuron will adjust its slope to reach these
thresholds near the target interval, ramping faster for shorter
intervals and slower for longer ones. The slope corresponds
to the temporal memory associated with the cue, as it varies
systematically with its trained interval. These proposals are
well supported by empirical data. For example, researchers
have repeatedly observed ramping neurons while subjects
perform timing tasks (Niki and Watanabe, 1979; Leon and
Shadlen, 2003; Matell et al., 2011; Xu et al., 2014; Jazayeri
and Shadlen, 2015). Furthermore, ramping neurons adapt their
slopes to different target intervals, and time-based decisions
often coincide with when they reach particular ﬁring rates
Frontiers in Behavioral Neuroscience 03 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
FIGURE 2
Ramping model. Summary of how a ramping model would apply
to a peak procedure where a tone and light signal reward after
10 and 30 s, respectively. Top: Simulated ramps for each cue
(blue) and start/stop thresholds (green and red, respectively).
Bottom: Simulated, idyllic behavior.
(Komura et al., 2001; Leon and Shadlen, 2003; Jazayeri and
Shadlen, 2015; Murakami et al., 2017).
In Figure 2 , we show how a ramping model would apply
to the peak-interval procedure speciﬁcally (Luzardo et al.,
2017a). To highlight the importance of slope adjustments for
timing different durations, we use an example where two
cues—presented during separate trials—signal reward after
different target intervals (tone=10s / light=30s). Regardless of
what cue is presented, the ramping neuron begins ascending at
the start of a trial. Furthermore, responding will begin when
it reaches the start-threshold and end when it reaches the
stop-threshold (green and red lines, respectively). However, to
reach these thresholds at the appropriate time for each cue, the
ramping neuron takes a steeper slope when the short-cue is
presented, relative to the long-cue.
Simen et al. (2011) proposed what is arguably the leading
ramping theory of timing.Figure 3 summarizes how it applies to
the peak-interval procedure (for further details on this particular
adaptation see De Corte, 2021). Speciﬁcally,Figure 3A overviews
the model’s architecture, which resembles a neural network
with four layers that interact hierarchically to generate ramping
activity and timed responding. Units in the top-layer function
much like simple sensory-neurons. When a cue is presented at
the start of a trial, units in this layer that code for the stimulus
will ﬁre transiently. These “cue-units” send excitation to the
second layer, containing what we will call “tonic units. ” Tonic
units possess strong self-excitation, causing each output they
produce to also act as a potent, depolarizing input. Consequently,
when initially excited by cue-units, they will quickly begin
ﬁring maximally throughout the trial (i.e., tonically), due to
recurrent-excitation alone. This steady excitation outputs to the
third layer, composed of ramping units. Ramping units also
possess recurrent-excitation. However, unlike tonic units, it is
too weak to cause them to ascend to their maximum ﬁring rates,
yet still strong enough to prevent ﬁring-rate decay. This tuned
recurrent-excitation effectively allows ramping units to summate
input from the tonic layer from one moment to the next. As a
result, ramping units will assume a linear proﬁle, with the slope
depending on the net excitation they receive from the tonic layer,
per unit time. Finally, the ramping layer outputs to “threshold”
units that only become active when the ramp reaches speciﬁc
ﬁring rates. These units control the circuit’s behavioral output.
Speciﬁcally, start-threshold units activate at a moderate input-
level from the ramping layer, initiating responses. Then, once
the ramp ascends to an even higher activity level, stop-threshold
units activate, terminating responding.
As noted above, the key parameter in any ramping model is
how to adjust the slope of the ramping neuron to time different
intervals. In Simen et al. ’s (2011) model, the slope is determined
by the net excitation the ramping layer receives from the tonic
layer (i.e., higher excitation = steeper slope). Therefore, to adjust
the slope, one simply adjusts the number of tonic units that the
cue-layer excites at the start of a trial (De Corte, 2021).Figure 3B
clariﬁes this more concretely, keeping with the example where a
tone and light signal a 10 and 30 s target interval, respectively.
When the tone is presented, one cue-unit activates all three
of the diagrammed tonic-units. With high-excitation from the
tonic layer, the ramp ascends at a steep slope, yielding responses
at 10 s. In contrast, when the light is presented, a different
cue-unit ﬁres that only activates one tonic unit. With less net
input from the tonic layer, the ramp takes a shallower slope,
yielding responses at 30 s.
Population-clock models
Population-clock theories of timing primarily differ
from ramping models with respect to how time-keeping is
accomplished. As described above, ramping models propose
that individual ramping neurons track time, and their rates at
any moment covary linearly with how much time has passed.
In contrast, according to population-clock models, a group of
neurons tracks time collectively, and the current rate of a given
Frontiers in Behavioral Neuroscience 04 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
FIGURE 3
Simen et al. (2011) ramping model. (A) Circuit architecture for cue, tonic, ramping, and threshold units, including purported ﬁring proﬁles of each
to the right according to the variant developed by De Corte (2021). (B) Slope control within the model during a task where a tone and light signal
a 10 and 30 s interval, respectively. Top: Circuit-architecture for a dual-cue task as proposed by De Corte (2021). Each cue elicits a response from
a different cue unit. Each unit activates the number of tonic units needed to achieve the ramp-slope for its respective interval. The middle and
bottom are analogous to Figure 2, showing simulated ramping and behavior.
neuron does not have to map systematically to elapsed time
(Ahrens and Sahani, 2007; Karmarkar and Buonomano, 2007;
Laje and Buonomano, 2013). In fact, the ﬁring proﬁle of each
individual neuron can effectively be random. The key point is
that, so long as each neuron repeats its temporal ﬁring-proﬁle
across trials, a distinct pattern of activity will emerge across the
population at each moment, providing a readout of elapsed time.
We ﬁnd it easiest to convey this point with a simple example,
as illustrated in Figure 4 for the peak-interval procedure.
At the start of a trial, three simulated neurons begin to
ﬁre. We have deliberately programmed each neuron’s rate to
ﬂuctuate erratically across time. By deﬁnition, there is no direct
relationship between an individual neuron’s current ﬁring rate
and elapsed time. However, if each neuron’s ﬁring proﬁle repeats
across trials, a unique pattern of activity will emerge across
the population for each moment within a trial. Therefore, if
the brain can learn the patterns that coincide with critical task
events (i.e., the times of reward for each cue), it can guide
behavior in time. Importantly, under this regime, the brain can
time any target interval by tuning to its corresponding activity
pattern. This is the premise of virtually all population-clock
models. Neurons do not encode time individually. Rather, time
is represented by an evolving pattern of activity across a group of
neurons, which functions as a population clock.
While individual neurons can take any shape to contribute
to a population-clock, some models propose constraints on
how time-keeping neurons ﬁre, based on in vivo data and/or
biophysically realistic assumptions. For example, some theories
align closely with the simple model above, proposing that
neurons contribute to timing via highly dynamic proﬁles
(Buonomano and Merzenich, 1995; Ahrens and Sahani, 2007).
However, others propose that neurons encode time via
gaussian-like proﬁles speciﬁcally, with different neurons peaking
at distinct moments within a timed-interval (Shankar and
Howard, 2012; Zhou et al., 2020). Consistent with this, neural
ensembles often display sequential activity during timing tasks
Frontiers in Behavioral Neuroscience 05 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
FIGURE 4
Population-clock model. Simple population-clock model during
a peak-procedure where a tone and light signal reward after
10 and 30 s, respectively. Top: Nonlinear population activity
from three neurons. Bottom: Behavior coincides with each cue’s
pattern.
that collectively “tiles” each moment between the start and end
of a target-interval (MacDonald et al., 2011; Mello et al., 2015;
Bakhurin et al., 2017; Tiganj et al., 2017; Shimbo et al., 2021).
These are often referred to as “time-cells, ” particularly when
observed in the hippocampus (Eichenbaum, 2014), and while
individual neurons do keep time to some degree within these
models, a full population is still required to encode the entire
interval. Y et, other models propose that individual neurons ﬁre
in an oscillatory manner, with periodicities that vary across
neurons in the population (Miall, 1989; Matell and Meck,
2004). These models are inspired by the known mechanisms
of circadian-timing—gene-expression oscillations (Silver et al.,
1996)—and behavioral theories of interval timing (Church
and Broadbent, 1990). Admittedly, there is some disagreement
over whether these models should be grouped together as
population-clock theories (for excellent discussion see Mauk and
Buonomano, 2004; Paton and Buonomano, 2018). Fortunately,
while this is important to note, we can avoid these nuances
for the present article. All of these models share the common
premise that time is encoded by patterns of activity across
groups of neurons rather than by individual neurons—the broad
deﬁnition of a population-clock theory we rely on here. As we
will see shortly, all the following claims will apply across them.
The Striatal-Beat Frequency (SBF) model is an example of
a population-clock model that has been applied extensively to
the peak-interval procedure (Matell and Meck, 2004; Oprisan
and Buhusi, 2014). Consistent with the oscillation-based models
mentioned above, SBF proposes that, when a trial starts, frontal
cortical neurons implement time-keeping by beginning to ﬁre in
an oscillatory manner ( Figure 5A, top). Different neurons ﬁre
at different periodicities, yielding a unique pattern of activity
across the population at each moment. These cortical oscillators
project to individual striatal neurons ( Figure 5A , bottom).
Striatal neurons implement both the memory and decision
processes, learning the cortical pattern that coincides with the
target interval and, once established, triggering responses when
it emerges. Speciﬁcally, early in training, reward-delivery elicits
a phasic burst of nigrostriatal dopamine (e.g., Amo et al.,
2022). Dopamine strengthens active corticostriatal synapses and
weakens inactive ones. As such, striatal neurons become more
responsive to the reward-related activity pattern. Once this
plasticity is established, midbrain dopamine neurons transition
to ﬁring at cue-onset. This purportedly resets striatal neurons
to their resting potentials, sharpening their sensitivity to the
critical cortical pattern. As the pattern emerges and dissipates,
striatal neurons ﬁre accordingly and, in turn, generate behavioral
output. To time a different interval, striatal neurons would
simply re-tune to its respective activity pattern (Figure 5B).
Evidence for population-clock and
ramping models: the importance of
behavioral work
Having covered the basics of population-clock and ramping
models in the prior section, we now turn to how they have been
empirically evaluated in the past. A common (and perhaps the
most obvious) approach is to monitor neural activity in vivo
during a timing task and assess how well the data match with
either model-class. However, most neurophysiological studies
have found mixed support for both types. As noted above,
experimenters have repeatedly documented ramping neurons
during timing tasks (Jazayeri and Shadlen, 2015; Li et al.,
2016). Nonetheless, consistent with population-clock models,
investigators typically ﬁnd neurons with nonlinear ﬁring proﬁles
as well, ranging from sequential gaussian-like activity to more
complex dynamics (Matell et al., 2011; Gouvêa et al., 2015; Mello
et al., 2015; Zhou et al., 2020). As such, the neurophysiological
data alone have been inconclusive.
In an ideal world, we would simply inhibit ramping or
nonlinear neurons selectively to evaluate the roles they might
play in timing. However, a key obstacle is that ramping and
Frontiers in Behavioral Neuroscience 06 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
FIGURE 5
Striatal beat frequency model. (A) Model overview showing cortical oscillators projecting onto a striatal unit. Firing proﬁles for each layer to the
right. (B) Timing different intervals. Striatal neurons tune to the cortical pattern appropriate for a given cue’s interval.
nonlinear neurons typically co-exist within the same population
(Matell et al., 2011; Zhou et al., 2020). Consequently, without
substantial advances in methods for manipulating speciﬁc
neurons in the same population in vivo (e.g., holographic
optogenetics Pégard et al., 2017), causally testing whether one
neuron-type plays a preferential role in timing will be effectively
impossible. Therefore, investigators have had to use alternative
approaches to assess the plausibility of ramping and population-
clock models.
Behavioral studies have been helpful in this regard.
Ultimately, all neural models must explain key behavioral effects
that occur during timing tasks. As a classic example, the standard
deviation of time-estimates often varies linearly with the target
interval–referred to as the “scalar property” of interval timing
(Gibbon, 1977). To illustrate with the peak-procedure, if a
cue’s target-interval suddenly doubles from 10 to 20 s, both
the mean and standard deviation of start and stop times will
double, in addition to the peak-time/spread of mean responding.
Explaining how this locked accuracy-precision relationship
emerges from neural circuits is often non-trivial. Therefore, the
scalar property is a standard starting-constraint on any neural
model of timing. Critically, other effects speak more directly to
the distinction between ramping and population-clock models.
A notable example is a behavioral effect referred to as
“temporal averaging” (Swanton et al., 2009). Originally, temporal
averaging experiments were developed to test how the timing
system handles conﬂicting time-information regarding when
an upcoming event will occur. Typically, experimenters begin
by training rats on a standard peak-interval procedure that
incorporates two cues—each associated with a distinct target
interval (e.g., tone=10s / light=30s). After training each cue
individually, experimenters introduce trials where both cues
are presented simultaneously as a “compound” stimulus. The
key question is how rats will spontaneously react to suddenly
being presented with two cues that predict reward after
different intervals (i.e., conﬂicting time-information). Therefore,
experimenters never train rats to respond at a speciﬁc time
during compound trials by delivering the reward. Remarkably,
during compound trials, rats often respond in between the two-
cue’s intervals in a unimodal, scalar manner (Swanton et al.,
2009; Swanton and Matell, 2011; Kurti et al., 2013; Matell and
Kurti, 2014; Delamater and Nicolas, 2015; De Corte and Matell,
2016a; Matell et al., 2016; Shapiro et al., 2018). In other words,
when conﬂicting temporal cues are presented, the timing system
appears to integrate the information each signal provides into
an average interval, timing this average in an otherwise normal
way. Figure 6A shows example data from De Corte (2017) who,
much like the example we have been using thus far, trained
rats to associate a tone and light with a 10 and 30 s duration,
respectively. While temporal averaging has been studied most
extensively in rats (for review see De Corte and Matell, 2016b),
it was originally documented in pigeons (Cheng and Roberts,
1991). Furthermore, humans show this effect (Zeng and Chen,
2019), in addition to various forms of non-temporal averaging
behavior during other tasks involving conﬂicting information
(for review see Fetsch et al., 2013).
While interesting in its own right, many have noted the
implications of temporal averaging for neural models of timing
Frontiers in Behavioral Neuroscience 07 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
FIGURE 6
Temporal averaging and neural models of timing. (A) Temporal averaging behavior. Left: Example task-schematic for a temporal averaging
experiment. Middle: Mean response rates across time during each trial type. Right: Peak-times for each trial type. Data adapted from De
Corte (2017). (B) Typical account of temporal averaging under a ramping model, wherein a ramping neuron takes an intermediate slope during
compound trials. (C) Application of a population-clock model (here, SBF) to temporal averaging. The question-mark emphasizes the ambiguity
over how two population patterns could be integrated to yield a pattern between the two target times.
(Matell and Henning, 2013; Matell, 2014; Matell and De Corte,
2016; Raphan et al., 2019). To illustrate, consider how a ramping
model might account for this effect, as summarized inFigure 6B.
When a cue is presented individually, ramping neurons would
set their slopes according to their respective interval, ramping
faster for the shorter cue than the long. Accordingly, during
compound trials, one might expect ramping neurons to take
an intermediate slope, thereby reaching the decision thresholds
at an intermediate-time (De Corte and Matell, 2016b; Luzardo
et al., 2017b). While straightforward, a deterministic explanation
for why a ramping neuron would adopt an intermediate slope
during compound trials has been more elusive. We recently
developed solutions under Simen et al. ’s (2011) model (De
Corte, 2021). However, for brevity, we will avoid detailing these
possibilities here. For present purposes, the primary point is
that, on its face, temporal averaging does not appear to be
fundamentally incompatible with ramping models.
In contrast, explanations for temporal averaging based
on population-clock theories have been more elusive (Matell
and Henning, 2013; Matell, 2014). Take SBF as an example
(Figure 6C). When a single cue is present, striatal neurons would
tune to the cortical oscillatory pattern coinciding with its target
interval. Following from this, during compound trials, striatal
neurons would presumably tune to a pattern that falls in etween
the two cues’ intervals. However, there are several problems with
this explanation. For example, as discussed above, SBF proposes
that striatal neurons only become responsive to a cortical pattern
via a reward-dependent learning process. As reward is never
delivered during compound trials, this explanation is not viable.
To resolve this, some have considered whether a more
“top-down” mechanism could be added to the model that
drives striatal neurons to the pattern associated with the
average interval (Matell and Henning, 2013). However, this
line of inquiry has led to what might be a more fundamental
problem with the model. Speciﬁcally, how could the pattern
associated with an average interval be computed from the
patterns associated with each cue’s duration? After all, time is
not represented in a “quantitative” way within SBF . Rather, in
statistical terms, the cortical patterns that occur at different
moments can be thought of as nominal variables. Each pattern
Frontiers in Behavioral Neuroscience 08 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
can be swapped for another, and as long as they unfold in a
consistent manner across trials, the method for timing would
remain the same. Therefore, “averaging” two cortical patterns
would be as meaningful as averaging two telephone numbers.
As such, how information can be integrated across cues that lead
to temporal averaging—or responding at any novel duration that
is systematic across subjects—is unclear.
Critically, because a deﬁning feature of all traditional
population-clock theories is a nominal mapping of population
activity to time, they will face the same challenge when applied
to temporal averaging. Moreover, temporal averaging is not the
only behavioral effect where this “computational intractability”
becomes a problem. Rather, it will emerge whenever subjects
appear to compute higher-order information across different
cues/intervals. The behavioral literature provides several added
examples worth noting.
One that relates closely to temporal averaging is an
effect referred to as “Vierordt’s law. ” This effect has been
documented most extensively in humans and occurs during
tasks where subjects time different intervals that vary from
one trial to the next. Under these conditions, a subject’s
estimate for a given interval will regress toward the mean of
all intervals they have previously learned, overshooting shorter
intervals and undershooting longer ones (Lejeune and Wearden,
2009; Jazayeri and Shadlen, 2010). Parkinson’s patients show
a pronounced form of Vierordt’s law, prompting a unique
label called the “migration effect” (Malapani et al., 1998,
2002). Bayesian models account for this effect by assuming
subjects offset potential errors in time-estimation during a
trial by integrating their current estimate with prior knowledge
regarding intervals that are typically presented in a given context
(Jazayeri and Shadlen, 2010; Shi et al., 2013). The more a given
estimate deviates from all previously learned intervals (i.e., the
more “unusual” it is for a given task), the more it will be
corrected based on prior knowledge. Consequently, all estimates
will naturally regress toward the mean of the prior distribution.
Again, population-clock theories face difﬁculty accounting for
this integration process. However, within ramping models, one
would assume that the slope of ramping neurons is biased toward
that associated with the mean interval, and again, mechanistic
explanations regarding why this would occur are beginning to
emerge (De Corte, 2021).
Averaging-related effects are not the only instances where
information is ﬂexibly integrated during timing tasks (for
excellent reviews see: Molet and Miller, 2014; Gür et al., 2018).
For example, in a recent series of experiments, we showed that
rats expect the intervals associated with distinct cues will covary
with one another (De Corte et al., 2018, 2022). In other words,
when one cue’s interval changes, they expect other cues’ intervals
to have changed in the same direction and can even ﬂexibly
update this covariance expectation based on task evidence. In
mathematical terms, computing expected covariance (or a rough
approximation to it) requires a unique set of operations relative
to averaging numbers, posing a distinct challenge for neural
models of timing. Furthermore, subjects also appear to be able to
integrate temporal and non-temporal information. For instance,
when timing two intervals that require a response at different
locations, mice will ﬂexibly integrate time-information with
reward-probability information at each location in a roughly
optimal manner (Balci et al., 2009a).
Again, while biophysically deterministic explanations for
these effects are forthcoming in any timing model, population-
clock network models face a particularly difﬁcult challenge due
to their nominal time-representation.
Temporal scaling: implications for
computation in population-clock
models
In the above section, we argue that: (1) behavioral
experiments have repeatedly demonstrated that the timing
system has a rich computational capacity, and (2) implementing
these computations using population-clock models is
particularly challenging. To be clear, we do not claim that
these “higher-order” behavioral effects are categorically
impossible within traditional population-clock theories. For
example, much like the arbitrary association between time
and population patterns they propose, computers use arbitrary
codes to represent numeric values–composed of unique bit-
sequences. However, to carry out mathematical operations on
these codes, computers must be equipped with speciﬁc circuits
that are tailored for a given mathematical function and built
around the agreed-upon mapping between a given sequence
and its corresponding quantity. In principle, population-clock
theories could be equipped with neural-parallels to these
circuits, along with a sequence-quantity convention. After
all, perceptron-circuits allow for Boolean logic gates—the
fundamental building block of any computer or computational
circuit—to be implemented in silico (McCulloch and Pitts,
1943). Nonetheless, this would entail a substantial revision to
current population-clock theories. Furthermore, once modiﬁed,
whether they would continue to capture basic patterns of
timing-behavior (e.g., the scalar property) and known-patterns
of neural activity during timing tasks would have to be re-
evaluated. Critically, recent data point to a simpler solution,
which we turn to next.
These data relate to a less obvious distinction between
population-clock and ramping models that we have not
emphasized thus far. To preface, note that the advantage of
ramping models when applied to the above behavioral effects
does not relate to the linear-shape of ramping proﬁles, per se .
Rather, it is the assumption that upstream circuits can ﬂexibly set
the slope of ramping neurons as needed for a given computation.
As an example, if these circuits can compress or stretch a
Frontiers in Behavioral Neuroscience 09 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
ramping proﬁle to time a short or long interval, we assume
they can do the same to time an intermediate interval during
a temporal averaging experiment. The key point here is that
slope adjustments produce a relative-mapping of neural activity
to time, as a ramping neuron’s rate at any moment will reﬂect the
fraction of the target-interval that has elapsed.
In contrast, traditional population-clock models propose
an absolute-mapping of neural activity to time. Regardless of
whether the target-interval is 10 or 30 s, the neural pattern at 5 s
will be the same. As it is unclear how these population patterns
can be combined in a computationally useful way, this absolute-
mapping produces the challenges discussed above.
Importantly, we should ask whether there is a way to
construct a population-clock model that engages in relative-
timing. Figure 7 outlines what this might look like, using the
simple model discussed above. All three neurons still ﬂuctuate
erratically across time. Y et, their ﬁring proﬁles now compress
or stretch to match the short or long interval, respectively. In
other words, much like a ramping neuron adjusting its slope,
the “speed” of their ﬁring proﬁles systematically scales with the
timed interval. However, much like a traditional population-
clock model, the pattern of activity across the population still
reﬂects elapsed time. Importantly, if we assume that upstream
circuits can set the population speed as needed for a given
computation, we can apply the same interpretations as we would
with a ramping model to the above behavioral effects. For
example, to account for temporal averaging, we would simply
say that the population moves at an intermediate speed, relative
to short or long trials. Critically, empirical data are beginning
to suggest that non-linear population activity indeed engages
in relative-timing, suggesting this modiﬁcation is biophysically
realistic.
Wang et al. (2018) recently provided an excellent illustration
of this principle, as summarized in Figure 8 . They recorded
from the medial frontal cortex, striatum, and thalamus during
a task where macaques timed a short- or long-cue from trial-
to-trial (0.8 and 1.5 s target intervals, respectively). Consistent
with prior work, they observed ramping neurons that scaled
their slopes according to the timed-interval. However, consistent
with population-clock models, they also found neurons with
complex, nonlinear proﬁles. Critically, these nonlinear neurons
often scaled their proﬁles according to the target-interval,
compressing for the shorter interval and stretching for the longer
one (Figure 8A). In other words, they appeared to ﬂexibly speed
up or slow down to time different intervals, much like a ramping
neuron adjusting its slope. This “temporal scaling” phenomenon
primarily occurred in the MFC and striatum. Nonetheless, the
thalamus appeared to set the speed of population dynamics
in these areas by modulating its tonic output. Wang et al.
(2018) integrated these data into a novel neural model of
timing.
Like the hypothetical model described above, their theory
is a hybrid between a ramping and traditional population-clock
FIGURE 7
Hypothetical relative population-clock model. Top and middle:
Hypothetical population activity that rescales when timing a
short or long interval, respectively. Green lines highlight the
same population pattern guides both intervals. Bottom: How
this model would correspond to behavior during a peak-interval
procedure where a tone and light are associated with 10 and 30 s,
respectively.
model and is summarized in Figure 8B . Speciﬁcally, complex
population dynamics still represent elapsed time, and decisions
are executed when a particular activity pattern emerges across
neurons, like a population-clock model. In addition, consistent
with ramping models, the proﬁles of all neurons slow down or
speed up according to the target-interval. Wang et al. (2018)
implemented this time-keeping population with a recurrent
neural network. Paralleling the apparent role of the thalamus in
their data, they delivered tonic input to the network that varied
systematically with the timed-interval, along with a “cue-pulse”
Frontiers in Behavioral Neuroscience 10 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
FIGURE 8
Temporal scaling in Wang et al. (2018).(A) Temporal scaling in neural data. Left: Electrode placement in medial-frontal cortex in Wang et al. (2018)
study. Firing proﬁles of neurons at the recording site that displayed temporal scaling, split by both interval (short = red-hued/long = blue-hued)
and within-subject variance for each interval (see color bars at the bottom). All ﬁgures adapted from Wang et al. (2018). (B) Wang et al.’s (2018)
neural network model of temporal scaling. Left: Model-schematic. Users send a cue-pulse and tonic (i.e., speed) input to the recurrent network,
which converges on the output node. Right: Proﬁles for the cue and tonic user-inputs (top two panels) and representative scaling activity in the
recurrent layer adapted from Wang et al. (2018).
that initiated communication between the tonic and recurrent
layer. When trained on their timing task, they found that units
in the recurrent layers naturally exhibited temporal scaling,
regardless of whether a given unit had developed a linear or
nonlinear proﬁle. Taken together, Wang et al. ’s (2018) study
provides an exhaustive empirical and theoretical illustration of
temporal scaling.
However, several recent studies have documented temporal
scaling; many of which predate Wang et al. ’s (2018) ﬁndings.
For instance, in rodents, temporal scaling occurs in a variety
of areas, such as frontal association cortices (Xu et al., 2014; Li
et al., 2016; Bakhurin et al., 2017; Emmons et al., 2017), the
striatum (Gouvêa et al., 2015; Mello et al., 2015; Bakhurin et al.,
2017), the hippocampus (Shikano et al., 2021; Shimbo et al.,
2021), and even the primary visual cortex (Gavornik et al., 2009).
Mello et al. (2015) provide a particularly relevant example. They
recorded in the striatum of rats trained on a task that is similar
to Wang et al. ’s (2018), where the target-interval varied randomly
across blocks of trials during a session. A subset of striatal
neurons showed Gaussian-like activity proﬁles, with different
neurons peaking at speciﬁc times between the start and end
of the interval. Importantly, when the timed-interval changed,
these neurons remapped in relative-time, peaking at the same
fraction of the prior interval rather than the same absolute
time within a trial. To illustrate, if the target interval switched
from 12 to 48 s, a neuron that initially peaked at 6 s would
Frontiers in Behavioral Neuroscience 11 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
switch to peaking at 24 s (i.e., half-way through either interval).
Furthermore, Hardy et al. (2018) recently showed that Wang
et al. ’s (2018) model captures patterns of motor timing exhibited
by humans that are difﬁcult to account for with ramping models
(for further discussion see Zhou and Buonomano, 2022; Zhou
et al., 2022).
Taken together, these data strongly suggest that temporal
scaling is a common neural phenomenon that deserves
further exploration. Furthermore, by giving population clock-
models a relative time-representation, these data help reconcile
this model-class with the behavioral effects discussed above.
Critically, if we keep the behavioral data in focus, we can derive
clear future directions for neural work on temporal scaling,
which we highlight next.
What sets the speed? A key direction
for future neural work on timing
Our essential point in the above section is that any model
containing a relative timing signal will show promise in
accounting for higher-order timing effects, regardless of whether
it is a ramping or population-clock theory. Nonetheless, this
argument contains a “leap-of-faith” that deserves clear emphasis.
Speciﬁcally, from the behavioral inferences above, the circuits
that set the speed of scaling activity should play a prominent
role in higher-order timing behavior. In fact, our argument
assumes that these speed-control circuits implement virtually
all computations discussed above, with downstream scaling
populations doing little of the “work. ” Generally, prior empirical
research has given more focus to characterizing scaling activity
itself—be it ramping activity or nonlinear dynamics—than the
upstream signals that drive it. At this point, one can posit that
these circuits are as computationally sophisticated as one would
like. However, to formally vet the plausibility of this assumption,
we must achieve a more mechanistic understanding of speed-
control. Without this, ramping and relative population-clock
theories will only be able to give a prima facie account of higher-
order timing effects, making it a key direction for future work.
Interestingly, there are often strong parallels in how speed-
control has been implemented within ramping and relative
population-clock models. We highlight this point in Figure 9
by diagramming Wang et al. ’s (2018) relative population-
clock theory alongside Simen et al. ’s (2011) ramping model.
Conceptually, both contain a scaling layer, corresponding to the
recurrent network in Wang et al. ’s (2018) model and the ramping
layer in Simen et al. ’s (2011) theory. Furthermore, there are
more apparent similarities at the upper layers, which implement
speed control. For example, both contain some form of a “start-
pulse” that initiates the scaling circuit. More importantly, both
control the speed of the scaling circuit with a tonic signal, whose
magnitude covaries with the to-be-timed interval. What both
models lack is a mechanistic explanation for higher-order timing
effects based on connectivity within the speed-control layers.
However, these similarities suggest that any solutions found
for one model-type will likely generalize to the other. For
example, to obtain temporal averaging in either model, one
would want the tonic signal to output at an intermediate
FIGURE 9
Speed control across relative population-clock and ramping models. (A) Wang et al. (2018) relative population-clock model as depicted in
Figure 8 . (B) Simen et al. (2011) ramping model as described in Figure 3 . Boxes spanning both panels emphasize the conceptual similarities
between both models with respect to the speed-control and scaling layers (top and bottom, respectively).
Frontiers in Behavioral Neuroscience 12 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
rate when two cues are present, causing the scaling layer to
evolve at an intermediate speed during compound trials. As
the experimenter sets the tonic signal manually in Wang et al. ’s
(2018) model, the circuit is currently not developed enough
to predict this pattern. As noted above, we are exploring ways
to account for this effect by modifying how the cue and tonic
layers of Simen et al. ’s (2011) model interact, which appear
promising (De Corte, 2021). Importantly, even if successful,
we would be surprised if an analogous solution could not be
adapted for the speed-control layer of Wang et al. ’s (2018) model.
Therefore, while deterministic explanations for higher-order
timing are lacking in either model, the emerging parallels allow
for cross-talk between the two theoretical domains.
Notably, these similarities are not isolated to these two
relative/scaling models. For example, while relative population-
clock models are still fairly new, several mechanistic ramping
models have been proposed. Typically, these models differ with
respect to the mechanism that drives ramping activity itself.
For example, Durstewitz (2003) proposed that ramping activity
emerges via intracellular calcium signaling, differing from
Simen et al. ’s (2011) proposition that recurrent excitation drives
climbing activity. In contrast, Reutimann et al. (2004) proposed
that ramping activity emerges via the adaptation of inhibitory
projections onto excitatory cells (i.e., a graded decrease in
inhibition leads to a graded increase in excitatory activity).
Critically, while these models make different assumptions about
the mechanisms that drive ramping, all propose that the slope of
ramping activity is driven by the magnitude of an external tonic
drive.
Importantly, to empirically test and biophysically constrain
any theoretical proposals, we must understand where speed-
control is implemented in the brain. From the above work, we
should look for a circuit that can: (1) detect when a temporal
cue is initially presented, and (2) modulate downstream scaling
neurons according to their interval. Of course, this process
likely involves complex interactions between several areas and
pathways implicated in timing (e.g., frontostriatal Matell, 2014;
nigrotectal Toda et al., 2017). Nonetheless, while we can only
make speculative hypotheses at this point, we view the thalamus
as a good starting point for several reasons. For one, the thalamus
is a known sensory relay between brain regions, making it
a likely participant in the chain between cue-detection and
the initiation of timing circuitry. Furthermore, Wang et al. ’s
(2018) data already suggest that thalamic output sets the
speed of scaling activity in downstream areas. However, the
thalamus is a remarkably diverse structure, composed of several
subnuclei that vary markedly in function. Wang et al. (2018)
primarily guided their recordings by ﬁnding thalamic neurons
that projected monosynaptically to the PFC, via antidromic
stimulation. Therefore, a key question is which thalamic nuclei
participate in speed-control.
For our assessment, Wang et al. (2018) predominantly
recorded in or near Area X, (roughly) corresponding to
the rodent ventrolateral thalamus, making it an obvious
candidate. However, we also view the mediodorsal nucleus
(MD) of the thalamus—often sitting just above Area X in
macaques—as a region of interest. Neuroanatomically, the
MD integrates multisensory information, primarily trafﬁcking
between association cortices. As effects such as temporal
averaging, Vierordt’s law, and covariance expectations often
operate cross-modally, one might expect a multisensory area
to be involved. Functionally, the MD plays a broad role in
cognition (Markowitsch, 1982; Peräkylä et al., 2017), and while
data are limited, manipulations of the MD disrupt baseline
timing performance (Yu et al., 2010; Lusk et al., 2020; De Corte
et al., 2021). As a notable example, Lusk et al. (2020) recently
inhibited the MD optogenetically during the peak-procedure
and found that peak times shifted later. For a relative timing
model, this result is consistent with partial inhibition of a tonic
drive that modulates downstream scaling activity. Importantly,
the MD’s role in cognition presumably relates to the fact that
it is the primary source of thalamic input to the PFC—where
temporal scaling has been repeatedly documented (Ray and
Price, 1993; Georgescu et al., 2020). Consistent with this,
disorders that preferentially disrupt MD-PFC communication,
such as Schizophrenia, also disrupt timing (Ward et al., 2012;
Singh et al., 2019). Furthermore, we recently provided initial
causal data suggesting that selectively blocking communication
between the MD and the prelimbic cortex—a rodent analog
of the PFC—markedly disrupts timing (De Corte et al.,
2021). Importantly, while monosynaptic MD-PFC projections
are particularly relevant to Wang et al. ’s (2018) data, the
MD is well positioned to modulate scaling in other areas,
projecting heavily to the striatum, virtually all association
cortices, and communicating with the hippocampus, presumably
via reciprocal connections with parahippocampal structures
(for excellent reviews see Saunders et al., 2005; Mitchell and
Chakraborty, 2013; Pergola et al., 2018; Georgescu et al., 2020).
Whatever nuclei might be involved, we view studying the
thalamus in the context of speed-control as a promising future
direction.
Beyond the thalamus, we view midbrain dopamine centers
as another likely participant in speed-control. Dopamine has
been implicated in a variety of timing processes, ranging
from temporal memory storage/retrieval (Malapani et al.,
2002), temporal prediction error-coding (Schultz, 2016; Sharpe
et al., 2017), and time-based decision-making (Howard et al.,
2017; Guru et al., 2020). More importantly, data have
repeatedly implicated dopamine in modulating “clock-speed, ”
which, with respect to the current article, corresponds to
biasing the speed of scaling activity. For example, during the
peak-procedure, systemic injections of dopamine D2-receptor
agonists or antagonists often cause peak-times to shift
leftward/rightward, respectively (Meck, 1986; MacDonald and
Meck, 2005; Matell et al., 2006). While understudied, recent
work suggests this effect may be mediated by nigrostriatal
Frontiers in Behavioral Neuroscience 13 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
dopamine speciﬁcally, with focal D2-antagonist infusions
producing rightward shifts in the striatum (De Corte et al., 2019)
and no reliable effects in frontal-cortical areas (Heslin, 2021).
Interestingly, Soares et al. (2016) showed that optogenetically
activating/inactivating striatal dopamine inputs produces the
reverse pattern—under/overestimation of time, respectively.
Nonetheless, regardless of directionality, these data collectively
suggest that dopamine modulates the speed of scaling activity,
making it another prime target for future work.
Relative vs. absolute timing: do we
need another dichotomy?
From the above discussion, we can see that a key distinction
between timing models is whether they propose an absolute
or relative representation of time. For the behavioral effects
discussed thus far, relative models appear more plausible than
absolute ones. However, should we always expect the brain to
represent time in a relative manner? After all, timing is critical
in a variety of situations. Relative timing might be useful in
some contexts, yet absolute timing could still be important
in others. Therefore, one might expect the brain to represent
both scales, either in parallel or by converting from one to
the other. Consistent with this, many neural studies that ﬁnd
evidence of scaling activity also ﬁnd a subset of neurons that
encode absolute-time (MacDonald et al., 2011; Gouvêa et al.,
2015; Shimbo et al., 2021). Furthermore, other facets of the
behavioral literature support this proposal, cautioning us against
a dichotomy.
For example, many have directly tested whether time is
represented in absolute or relative terms (Fetterman et al., 1989,
1993; Zentall et al., 2004; Maia and Machado, 2009; Pinheiro de
Carvalho and Machado, 2012; de Carvalho et al., 2016). These
studies often use a “temporal discrimination” task. During this
task, subjects are presented with a cue that lasts either a short
or long duration and, once it terminates, are trained to map
each duration to a distinct response-option. To use a concrete
example, in Akdo ˘gan et al. (2020), we recently trained mice to
press a left lever if a cue lasted 2-s and a right lever if it lasted 6-s
(Figure 10A ; 2-s = left/6-s = right). Consider how two brains
would solve this task–one that exclusively represents absolute
time and another that represents relative time. The relative brain
would use a relational decision-rule such as, “the shorter interval
goes to the left and longer one goes to the right. ” In contrast, the
absolute brain would use a more nominal mapping such as, “the
2-s interval goes to the left and the 6-s one goes to the right. ”
To test these accounts, we introduced a second phase where we
changed the short and/or long durations, disrupting either their
relative or absolute mapping to the response-locations across
different groups.
For instance, in one group, we increased the short duration
to 6-s and the long duration to 18-s (i.e., 6-s = left/18-s = right).
FIGURE 10
Absolute vs. relative timing. (A) Temporal discrimination task-
design. (B) Task-designs for the three groups included in
Akdo˘gan et al. (2020) at the top. Mean accuracy during phase
2 across all trial types are plotted in the middle. Accuracy for 6-s
trials alone during phase 2 is plotted at the bottom.
Note that, relative to the ﬁrst phase, the 6-s duration
switches from the right lever to the left ( Figure 10B ).
Therefore, the absolute brain must remap this duration-
response association, in addition to mapping the new 18-s
duration appropriately. The relative brain would have an easier
time—even though the durations have changed, the shorter
interval still goes left and longer one goes right. Therefore,
we refer to this as the “relative group. ” In a comparison
group, we continued associating the 6-s duration with the
right lever during the second phase and mapped the 18-s
Frontiers in Behavioral Neuroscience 14 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
duration to the left lever (i.e., 18-s = left/6-s = right).
Here, as the 6-s interval’s mapping never changed across
phases, the absolute brain only needs to map the new
18-s interval ( Figure 10B ). In contrast, the relative brain
is at a disadvantage, as the relational mappings reversed.
Consistent with a relative brain, mice in this “absolute
group” performed worse than the relative group, although
they did show some absolute transfer during early sessions
(Figure 10B , bottom; see full manuscript for more detailed
analyses/conditions).
Importantly, this result does not rule out absolute timing
entirely. For example, the brain might engage in both
strategies, yet be preferential to relative processing. To
address this, we also incorporated a third comparison group
where we simply reversed the duration-response pairings
(i.e., 6-s = left/2-s = right). As both the absolute and relative
mappings ﬂipped, both brains should have been disadvantaged
(Figure 10B ). This “reversal group” was more impaired at the
start of the transfer test than both the relative and absolute
groups. Therefore, the brain indeed appears to accommodate
both absolute and relative time, even if it might give more weight
to relative processing. In further support of this conclusion,
prior studies using similar approaches to ours often ﬁnd mixed
support for absolute (de Carvalho et al., 2016) and relative
timing (Zentall et al., 2004).
As a more indirect approach, we can look for behavioral
effects in the literature that necessarily imply that the brain
processes absolute time. After all, while the higher-order effects
we focus on here are more plausible under relative models,
they represent a narrow subset of the behavioral literature. By
expanding our horizons, we can ﬁnd clear cases that imply
absolute processing at some level.
We view research on “temporal maps” as a key example
(Honig, 1981; Matzel et al., 1988). This literature complements
work showing that animals construct “spatial maps” of the
environment that they use to track the physical locations of
objects (Tolman, 1948; Blaisdell et al., 2018; Widloski and Foster,
2022). The question here is whether animals do the same with
time, tracking the “temporal locations” of events as they unfold
during a learning episode on an underlying temporal map.
Researchers have developed a variety of designs to address
this question (Matzel et al., 1988; Arcediano and Miller, 2002;
Leising et al., 2007; Molet et al., 2012; Molet and Miller,
2014). However, a simple experiment with rats would run
as follows, as summarized in Figure 11A . During Phase 1,
experimenters repeatedly present rats with two cues that are
separated by a certain time-interval (Cue A →Cue B). On
a subsequent training day (i.e., Phase 2), rats return to the
chamber and are presented with a reward that is followed
soon after by the second cue from Phase 1 (Reward →Cue
FIGURE 11
Temporal maps and absolute time. (A) Temporal map concept and design. Left: Task-structure across the three phases. Right: Hypothetical
integration of phases 1 and 2 into a temporal map that is then used during testing. (B) Converting between relative and absolute time with a
ramping model during a temporal map experiment.
Frontiers in Behavioral Neuroscience 15 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
B). Importantly, experimenters set the interval separating the
reward and Cue B to where, in the context of Phase 1,
the reward should have occurred at a certain time between
the cues (Cue A →Reward→Cue B). As an example, if the
Cue A →Cue B duration was 4 s and the Reward →Cue B
duration was 1 s, the “inferred” delay between Cue A and
reward would be 3 s. As illustrated in Figure 11A , if animals
generate temporal maps of the two learning episodes and
can overlay them, they should be able to estimate the Cue
A→Reward interval, without directly experiencing it. To test
this, experimenters present rats with Cue A during a ﬁnal phase,
and subjects indeed show conditioned behavior, even though it
was never explicitly paired with reinforcement (e.g., Molet et al.,
2012).
To our assessment, temporal map learning requires the
assumption that the brain represents absolute time, at least at
some level. To illustrate, consider what would have to happen
for a purely relative model to account for the above experiment.
In Figure 11B, we overview one possibility in which a ramping
model encodes each interval strictly via slope-adaptation. The
two blue lines in Figure 11B represent the “knowns” during
the above experiment. Speciﬁcally, subjects experience Cue
A→Cue B and Reward →Cue B pairings during the ﬁrst two
phases, and a ramping neuron could represent these intervals
by tuning its slope appropriately. The critical component is
the gray line–a ramp encoding the Cue A →Reward interval.
Subjects never explicitly experience this interval. However,
to account for the emergence of conditioned behavior to
Cue A during the ﬁnal test phase with slope-adaptation, one
would assume the ramping neuron assumes this slope during
testing.
To set the Cue A →Reward slope appropriately, the brain
would have to extrapolate from the two known intervals. On
paper, this is trivial, as outlined to the right in Figure 11B .
To solve for the slope of any line, one only needs a value
on the y-axis and its corresponding value on the x-axis (here,
ﬁring rate and time, respectively). With the threshold (i.e., y-
value) being shared across intervals, the only “unknown” is the
absolute delay between Cue A and Reward. As illustrated on the
bottom right, this can be computed by rearranging the linear
equations associated with the two known intervals to solve for
t. We can leave the question of how this computation could
be mechanistically implemented in neural circuits for another
time. The key here is that this computation equates to converting
from relative to absolute time. Moreover, to explain responding
to Cue A during testing, this conversion would have to occur
spontaneously, requiring the assumption that the relative brain
accounts for an absolute time a priori . Of course, there are a
variety of other theoretical interpretations that we can apply to
temporal map learning (e.g., threshold-adaptation with a relative
model, explicitly absolute models, etc.). However, we are unable
to ﬁnd a solution that accounts for these effects with purely
relative processing.
Collectively, the above discussion highlights that exploring
whether the brain represents absolute and/or relative time is a
question that is prime for further exploration for future neural
and neuro-focused behavioral studies.
Conclusion
In conclusion, behavioral data have long suggested that
the timing system has a remarkable computational capacity.
Inferences from these data have proved valuable in evaluating
the plausibility of ramping and population-clock models.
Traditionally, ramping models appeared to have the upper-
hand. However, we argue that population-clock models that
capture the recent discovery of temporal scaling prove equally
plausible in most cases. Moving forward, we view exploring
the mechanisms of speed-control and evaluating whether neural
timing is absolute and/or relative as important future directions.
Of course, temporal scaling prompts several other avenues for
future research, such as whether ramping neurons have a special
status compared to nonlinear ones. Y et, with respect to the
integration of behavioral and neural timing data, we view these
questions as key.
Data availability statement
The original contributions presented in the study are
included in the article, further inquiries can be directed to the
corresponding author.
Author contributions
BC: concept development, writing manuscript, ﬁgure
generation. BA and PB: conceptual development, manuscript
revisions, and feedback. All authors contributed to the article
and approved the submitted version.
Funding
This work was supported by National Institute of Mental
Health: Grant No. R01MH068073 and National Institute of
Neurological Disorders and Stroke: Grant No. F31NS106737.
Conﬂict of interest
The authors declare that the research was conducted in the
absence of any commercial or ﬁnancial relationships that could
be construed as a potential conﬂict of interest.
Frontiers in Behavioral Neuroscience 16 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
Publisher’s note
All claims expressed in this article are solely those of the
authors and do not necessarily represent those of their afﬁliated
organizations, or those of the publisher, the editors and the
reviewers. Any product that may be evaluated in this article, or
claim that may be made by its manufacturer, is not guaranteed
or endorsed by the publisher.
References
Ahrens, M., and Sahani, M. (2007). “Inferring elapsed time from stochastic
neural processes, ” in Advances in Neural Information Processing Systems , Vol. 20,
eds J. Platt, D. Koller, Y . Singer, and S. Roweis (Red Hook, New Y ork: Curran
Associates, Inc). Available online at: https://proceedings.neurips.cc/paper/2007/
ﬁle/0d352b4d3a317e3eae221199fdb49651-Paper.pdf.
Akdo˘gan, B., Wanar, A., Gersten, B. K., Gallistel, C. R., and Balsam, P . D. (2020).
Temporal encoding: relative and absolute representations of time guide behavior.
PsyArXiv [Preprint]. doi: 10.31234/osf.io/p6v2j
Amo, R., Matias, S., Y amanaka, A., Tanaka, K. F ., Uchida, N., and Watabe-
Uchida, M. (2022). A gradual temporal shift of dopamine responses mirrors the
progression of temporal difference error in machine learning. Nat. Neurosci. 25,
1082–1092. doi: 10.1038/s41593-022-01109-2
Arcediano, F ., and Miller, R. R. (2002). Some constraints for models of
timing: a temporal coding hypothesis perspective. Learn. Motiv. 33, 105–123.
doi: 10.1006/lmot.2001.1102
Bakhurin, K. I., Goudar, V ., Shobe, J. L., Claar, L. D., Buonomano, D. V ., and
Masmanidis, S. C. (2017). Differential encoding of time by prefrontal and striatal
network dynamics. J. Neurosci. 37, 854–870. doi: 10.1523/JNEUROSCI.1789-16.
2016
Balci, F ., Freestone, D., and Gallistel, C. R. (2009a). Risk assessment in man and
mouse. Proc. Natl. Acad. Sci. U S A 106, 2459–2463. doi: 10.1073/pnas.0812709106
Balci, F ., Gallistel, C. R., Allen, B. D., Frank, K. M., Gibson, J. M., and Brunner, D.
(2009b). Acquisition of peak responding: what is learned? Behav. Processes 80,
67–75. doi: 10.1016/j.beproc.2008.09.010
Balsam, P . D., and Gallistel, C. R. (2009). Temporal maps and informativeness in
associative learning. Trends Neurosci.32, 73–78. doi: 10.1016/j.tins.2008.10.004
Blaisdell, A. P ., Schroeder, J. E., and Fast, C. D. (2018). Spatial integration during
performance in pigeons. Behav. Processes 154, 73–80. doi: 10.1016/j.beproc.2017.
12.012
Buhusi, C. V ., and Meck, W . H. (2005). What makes us tick? Functional
and neural mechanisms of interval timing. Nat. Rev. Neurosci. 6, 755–765.
doi: 10.1038/nrn1764
Buhusi, C. V ., Reyes, M. B., Gathers, C.-A., Oprisan, S. A., and Buhusi, M. (2018).
Inactivation of the medial-prefrontal cortex impairs interval timing precision, but
not timing accuracy or scalar timing in a peak-interval procedure in rats. Front.
Integr. Neurosci.12:20. doi: 10.3389/fnint.2018.00020
Buonomano, D. V ., and Maass, W . (2009). State-dependent computations:
spatiotemporal processing in cortical networks. Nat. Rev. Neurosci. 10, 113–125.
doi: 10.1038/nrn2558
Buonomano, D. V ., and Merzenich, M. M. (1995). Temporal information
transformed into a spatial code by a neural network with realistic properties.
Science 267, 1028–1030. doi: 10.1126/science.7863330
Cheng, K., and Roberts, W . A. (1991). Three psychophysical principles of timing
in pigeons. Learn. Motiv. 22, 112–128. doi: 10.1016/0023-9690(91)90019-5
Church, R. M., and Broadbent, H. A. (1990). Alternative representations
of time, number and rate. Cognition 37, 55–81. doi: 10.1016/0010-0277(90)
90018-f
de Carvalho, M. P ., Machado, A., and Tonneau, F . (2016). Learning in the
temporal bisection task: relative or absolute?J. Exp. Psychology. Anim. Learn. Cogn.
42, 67–81. doi: 10.1037/xan0000089
De Corte, B. J. (2017). T emporal Averaging and Bayesian Decision Theory .
Villanova, Pennsylvania: Villanova University.
De Corte, B. J. (2021). What Are the Neural Mechanisms of “Higher-Order”
Timing? Complex Behavior from Low-Level Circuits . Laurel Hollow, New Y ork:
ProQuest Dissertations Publishing. doi: 10.17077/etd.006279
De Corte, B. J., and Matell, M. S. (2016a). Temporal averaging across multiple
response options: insight into the mechanisms underlying integration. Anim.
Cogn. 19, 329–342. doi: 10.1007/s10071-015-0935-4
De Corte, B. J., and Matell, M. S. (2016b). Interval timing, temporal averaging
and cue integration. Curr. Opin. Behav. Sci. 8, 60–66. doi: 10.1016/j.cobeha.2016.
02.004
De Corte, B. J., Della Valle, R. R., and Matell, M. S. (2018). Recalibrating
timing behavior via expected covariance between temporal cues. eLife 7:e38790.
doi: 10.7554/eLife.38790
De Corte, B. J., Farley, S. J., Heslin, K. A., Parker, K. L., and Freeman, J. H. (2022).
The dorsal hippocampus’ role in context-based timing in rodents. Neurobiol.
Learn. Mem. 194:107673. doi: 10.1016/j.nlm.2022.107673
De Corte, B. J., Heslin, K. A., Cremers, N. S., Freeman, J. H., and Parker, K. L.
(2021). Communication between the mediodorsal thalamus and prelimbic cortex
regulates timing performance in rats. bioRxiv [Preprint]. doi: 10.1101/2021.06.18.
449036
De Corte, B. J., Wagner, L. M., Matell, M. S., and Narayanan, N. S. (2019). Striatal
dopamine and the temporal control of behavior. Behav. Brain Res. 356, 375–379.
doi: 10.1016/j.bbr.2018.08.030
Delamater, A. R., and Nicolas, D.-M. (2015). Temporal averaging across stimuli
signaling the same or different reinforcing outcomes in the peak procedure. Int.
J. Comp. Psychol. 28:uclapsych_ijcp_28552.
Drew, M. R., Zupan, B., Cooke, A., Couvillon, P . A., and Balsam, P . D. (2005).
Temporal control of conditioned responding in goldﬁsh. J. Exp. Psychol. Anim.
Behav. Processes31, 31–39. doi: 10.1037/0097-7403.31.1.31
Drucker-Colín, R., Aguilar-Roblero, R., García-Hernández, F ., Fernández-
Cancino, F ., and Bermudez Rattoni, F . (1984). Fetal suprachiasmatic nucleus
transplants: diurnal rhythm recovery of lesioned rats. Brain Res. 311, 353–357.
doi: 10.1016/0006-8993(84)90099-4
Durstewitz, D. (2003). Self-organizing neural integrator predicts interval times
through climbing activity. J. Neurosci. 23, 5342–5353. doi: 10.1523/JNEUROSCI.
23-12-05342.2003
Eichenbaum, H. (2014). Time cells in the hippocampus: a new dimension for
mapping memories. Nat. Rev. Neurosci. 15, 732–744. doi: 10.1038/nrn3827
Emmons, E. B., De Corte, B. J., Kim, Y ., Parker, K. L., Matell, M. S., and
Narayanan, N. S. (2017). Rodent medial frontal control of temporal processing in
the dorsomedial striatum. J. Neurosci. 37, 8718–8733. doi: 10.1523/JNEUROSCI.
1376-17.2017
Fereday, R., Buehner, M. J., and Rushton, S. K. (2019). The role of time
perception in temporal binding: impaired temporal resolution in causal sequences.
Cognition 193:104005. doi: 10.1016/j.cognition.2019.06.017
Fetsch, C. R., DeAngelis, G. C., and Angelaki, D. E. (2013). Bridging the gap
between theories of sensory cue integration and the physiology of multisensory
neurons. Nat. Rev. Neurosci. 14, 429–442. doi: 10.1038/nrn3503
Fetterman, J. G., Dreyfus, L. R., and Stubbs, D. A. (1989). Discrimination of
duration ratios. J. Exp. Psychol. Anim. Behav. Processes15, 253–263.
Fetterman, J. G., Dreyfus, L. R., and Stubbs, D. A. (1993). Discrimination of
duration ratios by pigeons (Columba livia) and humans (Homo sapiens). J. Comp.
Psychol. 107, 3–11. doi: 10.1037/0735-7036.107.1.3
Gallistel, C. R., and Gibbon, J. (2000). Time, rate and conditioning.Psychol. Rev.
107, 289–344. doi: 10.1037/0033-295x.107.2.289
Garcia, K. S., and Mauk, M. D. (1998). Pharmacological analysis of cerebellar
contributions to the timing and expression of conditioned eyelid responses.
Neuropharmacology 37, 471–480. doi: 10.1016/s0028-3908(98)00055-0
Gavornik, J. P ., Shuler, M. G. H., Loewenstein, Y ., Bear, M. F ., and Shouval, H. Z.
(2009). Learning reward timing in cortex through reward dependent expression of
synaptic plasticity. Proc. Natl. Acad. Sci. U S A 106, 6826–6831. doi: 10.1073/pnas.
0901835106
Georgescu, I. A., Popa, D., and Zagrean, L. (2020). The anatomical and
functional heterogeneity of the mediodorsal thalamus. Brain Sci. 10:624.
doi: 10.3390/brainsci10090624
Frontiers in Behavioral Neuroscience 17 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
Gibbon, J. (1977). Scalar expectancy theory and Weber’s law in animal timing.
Psychol. Rev. 84, 279–325. doi: 10.1037/0033-295X.84.3.279
Gibbon, J., and Church, R. M. (1990). Representation of time. Cognition 37,
23–54. doi: 10.1016/0010-0277(90)90017-e
Gibbon, J., Church, R. M., and Meck, W . H. (1984). Scalar timing in memory.
Ann. N Y Acad. Sci. 423, 52–77. doi: 10.1111/j.1749-6632.1984.tb23417.x
Gouvêa, T. S., Monteiro, T., Motiwala, A., Soares, S., Machens, C., and
Paton, J. J. (2015). Striatal dynamics explain duration judgments. eLife 4:e11386.
doi: 10.7554/eLife.11386
Grossberg, S., and Schmajuk, N. A. (1989). Neural dynamics of adaptive timing
and temporal discrimination during associative learning. Neural Netw. 2, 79–102.
doi: 10.1016/0893-6080(89)90026-9
Gür, E., Duyan, Y . A., and Balcı, F . (2018). Spontaneous integration of temporal
information: implications for representational/computational capacity of animals.
Anim. Cogn. 21, 3–19. doi: 10.1007/s10071-017-1137-z
Guru, A., Seo, C., Post, R. J., Kullakanda, D. S., Schaffer, J. A., and Warden, M. R.
(2020). Ramping activity in midbrain dopamine neurons signiﬁes the use of a
cognitive map. bioRxiv [Preprint]. doi: 10.1101/2020.05.21.108886
Hardy, N. F ., Goudar, V ., Romero-Sosa, J. L., and Buonomano, D. V . (2018).
A model of temporal scaling correctly predicts that motor timing improves with
speed. Nat. Commun. 9:4732. doi: 10.1038/s41467-018-07161-6
Heslin, K. A. (2021). Flexible timing in the rat medial frontal cortex and
cerebellum. ProQuest Dissertations Publishing. doi: 10.17077/etd.006278
Honig, W . K. (1981). “Working memory and the temporal map, ” inInformation
Processing in Animals: Memory Mechanisms, Vol. 9, eds N. E. Spear, and R. R. Miller
(Hillsdale, NJ: Erlbaum), 167–197.
Howard, C. D., Li, H., Geddes, C. E., and Jin, X. (2017). Dynamic nigrostriatal
dopamine biases action selection.Neuron 93, 1436–1450.e8. doi: 10.1016/j.neuron.
2017.02.029
Hume, D. (1739). A Treatise of Human Nature/by David
Hume; Reprinted From the Original Edition in Three Volumes and
Edited, With An Analytical Index , by L. A. Selby-Bigge . Oxford:
Clarendon press, William SHein & Company. Available online at:
http://www.heinonline.org/HOL/Page?handle=hein.beal/trhumn0001&id=1&size
=2&collection=beal&index=beal#5.
Jazayeri, M., and Shadlen, M. N. (2010). Temporal context calibrates interval
timing. Nat. Neurosci. 13, 1020–1026. doi: 10.1038/nn.2590
Jazayeri, M., and Shadlen, M. N. (2015). A neural mechanism for sensing and
reproducing a time interval. Curr. Biol. 25, 2599–2609. doi: 10.1016/j.cub.2015.08.
038
Karmarkar, U. R., and Buonomano, D. V . (2007). Timing in the absence of
clocks: encoding time in neural network states.Neuron 53, 427–438. doi: 10.1016/j.
neuron.2007.01.006
Killeen, P . R., and Fetterman, J. G. (1988). A behavioral theory of timing.Psychol.
Rev. 95, 274–295. doi: 10.1037/0033-295x.95.2.274
Komura, Y ., Tamura, R., Uwano, T., Nishijo, H., Kaga, K., and Ono, T.
(2001). Retrospective and prospective coding for predicted reward in the sensory
thalamus. Nature 412, 546–549. doi: 10.1038/35087595
Kudo, N., and Y amada, T. (1987). N-methyl-D,L-aspartate-induced locomotor
activity in a spinal cord-hindlimb muscles preparation of the newborn rat studied
in vitro. Neurosci. Lett. 75, 43–48. doi: 10.1016/0304-3940(87)90072-3
Kurti, A., Swanton, D. N., and Matell, M. S. (2013). “The potential link between
temporal averaging and drug-taking behavior, ” inSubjective Time: The Philosophy,
Psychology and Neuroscience of T emporality , (Cambridge: MIT Press), 599–620.
doi: 10.7551/mitpress/8516.003.0040
Laje, R., and Buonomano, D. V . (2013). Robust timing and motor patterns
by taming chaos in recurrent neural networks. Nat. Neurosci. 16, 925–933.
doi: 10.1038/nn.3405
Leising, K. J., Sawa, K., and Blaisdell, A. P . (2007). Temporal integration
in Pavlovian appetitive conditioning in rats. Learn. Behav. 35, 11–18.
doi: 10.3758/bf03196069
Lejeune, H., and Wearden, J. H. (2009). Vierordt’s the experimental study
of the time sense (1868) and its legacy. Eur. J. Cogn. Psychol. 21, 941–960.
doi: 10.1080/09541440802453006
Leon, M. I., and Shadlen, M. N. (2003). Representation of time by neurons in the
posterior parietal cortex of the macaque. Neuron 38, 317–327. doi: 10.1016/s0896-
6273(03)00185-5
Li, N., Daie, K., Svoboda, K., and Druckmann, S. (2016). Robust neuronal
dynamics in premotor cortex during motor planning. Nature 532, 459–464.
doi: 10.1038/nature17643
Long, M. A., Katlowitz, K. A., Svirsky, M. A., Clary, R. C., Byun, T. M., Majaj, N.,
et al. (2016). Functional segregation of cortical regions underlying speech timing
and articulation. Neuron 89, 1187–1193. doi: 10.1016/j.neuron.2016.01.032
Lusk, N., Meck, W . H., and Yin, H. H. (2020). Mediodorsal thalamus
contributes to the timing of instrumental actions. J. Neurosci. 40, 6379–6388.
doi: 10.1523/JNEUROSCI.0695-20.2020
Luzardo, A., Rivest, F ., Alonso, E., and Ludvig, E. A. (2017a). A drift-diffusion
model of interval timing in the peak procedure. J. Math. Psychol. 77, 111–123.
doi: 10.1016/j.jmp.2016.10.002
Luzardo, A., Alonso, E., and Mondragón, E. (2017b). A Rescorla-Wagner drift-
diffusion model of conditioning and timing. PLoS Comput. Biol. 13:e1005796.
doi: 10.1371/journal.pcbi.1005796
MacDonald, C. J., Lepage, K. Q., Eden, U. T., and Eichenbaum, H. (2011).
Hippocampal “time cells” bridge the gap in memory for discontiguous events.
Neuron 71, 737–749. doi: 10.1016/j.neuron.2011.07.012
MacDonald, C. J., and Meck, W . H. (2005). Differential effects of clozapine and
haloperidol on interval timing in the supraseconds range. Psychopharmacology
(Berl) 182, 232–244. doi: 10.1007/s00213-005-0074-8
Machado, A. (1997). Learning the temporal dynamics of behavior. Psychol. Rev.
104, 241–265. doi: 10.1037/0033-295x.104.2.241
Maia, S., and Machado, A. (2009). Representation of time intervals in a double
bisection task: relative or absolute? Behav. Processes 81, 280–285. doi: 10.1016/j.
beproc.2008.10.012
Malapani, C., Deweer, B., and Gibbon, J. (2002). Separating storage from
retrieval dysfunction of temporal memory in Parkinson’s disease.J. Cogn. Neurosci.
14, 311–322. doi: 10.1162/089892902317236920
Malapani, C., Rakitin, B., Levy, R., Meck, W . H., Deweer, B., Dubois, B., et al.
(1998). Coupled temporal memories in Parkinson’s disease: a dopamine-related
dysfunction. J. Cogn. Neurosci. 10, 316–331. doi: 10.1162/089892998562762
Markowitsch, H. J. (1982). Thalamic mediodorsal nucleus and memory: a critical
evaluation of studies in animals and man. Neurosci. Biobehav. Rev. 6, 351–380.
doi: 10.1016/0149-7634(82)90046-x
Matell, M. S. (2014). Searching for the holy grail: temporally informative ﬁring
patterns in the rat. Adv. Exp. Med. Biol. 829, 209–234. doi: 10.1007/978-1-4939-
1782-2_12
Matell, M. S., Bateson, M., and Meck, W . H. (2006). Single-trials analyses
demonstrate that increases in clock speed contribute to the methamphetamine-
induced horizontal shifts in peak-interval timing functions. Psychopharmacology
188, 201–212. doi: 10.1007/s00213-006-0489-x
Matell, M. S., and De Corte, B. J. (2016). Temporal memory averaging:
Resolution of conﬂict in temporal expectations. Jpn. J. Animal Psychol. 66, 1–9.
doi: 10.2502/janip.66.1.3
Matell, M. S., De Corte, B., Kerrigan, T., and DeLussey, C. M. (2016).
Temporal averaging in response to change. Timing Time Percept. 4, 223–247.
doi: 10.1163/22134468-00002068
Matell, M. S., and Henning, A. M. (2013). Temporal memory averaging and
post-encoding alterations in temporal expectation. Behav. Processes 95, 31–39.
doi: 10.1016/j.beproc.2013.02.009
Matell, M. S., and Kurti, A. N. (2014). Reinforcement probability modulates
temporal memory selection and integration Processes. Acta Psychol. 147, 80–91.
doi: 10.1016/j.actpsy.2013.06.006
Matell, M. S., and Meck, W . H. (2004). Cortico-striatal circuits and interval
timing: coincidence detection of oscillatory Processes. Brain Res. Cogn. Brain Res.
21, 139–170. doi: 10.1016/j.cogbrainres.2004.06.012
Matell, M. S., Shea-Brown, E., Gooch, C., Wilson, A. G., and Rinzel, J. (2011).
A heterogeneous population code for elapsed time in rat medial agranular cortex.
Behav. Neurosci.125, 54–73. doi: 10.1037/a0021954
Matzel, L. D., Held, F . P ., and Miller, R. R. (1988). Information and expression of
simultaneous and backward associations: implications for contiguity theory.Learn.
Motiv.19, 317–344. doi: 10.1016/0023-9690(88)90044-6
Mauk, M. D., and Buonomano, D. V . (2004). The neural basis of temporal
Processing. Annu. Rev. Neurosci. 27, 307–340. doi: 10.1146/annurev.neuro.27.
070203.144247
McCulloch, W . S., and Pitts, W . (1943). A logical calculus of the ideas immanent
in nervous activity. Bull. Math. Biol. 5, 115–133.
Meck, W . H. (1986). Afﬁnity for the dopamine D2 receptor predicts neuroleptic
potency in decreasing the speed of an internal clock. Pharmacol. Biochem. Behav.
25, 1185–1189. doi: 10.1016/0091-3057(86)90109-7
Meck, W . H. (2006). Neuroanatomical localization of an internal clock: a
functional link between mesolimbic, nigrostriatal and mesocortical dopaminergic
systems. Brain Res. 1109, 93–107. doi: 10.1016/j.brainres.2006.06.031
Frontiers in Behavioral Neuroscience 18 frontiersin.org
De Corte et al. 10.3389/fnbeh.2022.1022713
Mello, G. B. M., Soares, S., and Paton, J. J. (2015). A scalable population code for
time in the striatum. Curr. Biol. 25, 1113–1122. doi: 10.1016/j.cub.2015.02.036
Merchant, H., Pérez, O., Zarco, W ., and Gámez, J. (2013). Interval tuning in the
primate medial premotor cortex as a general timing mechanism. J. Neurosci. 33,
9082–9096. doi: 10.1523/JNEUROSCI.5513-12.2013
Miall, C. (1989). The storage of time intervals using oscillating neurons. Neural
Comput. 1, 359–371.
Mitchell, A. S., and Chakraborty, S. (2013). What does the mediodorsal thalamus
do? Front. Syst. Neurosci.7:37. doi: 10.3389/fnsys.2013.00037
Molet, M., Miguez, G., Cham, H. X., and Miller, R. R. (2012). When does
integration of independently acquired temporal relationships take place? J. Exp.
Psychol. Anim. Behav. Processes38, 369–380. doi: 10.1037/a0029379
Molet, M., and Miller, R. R. (2014). Timing: an attribute of associative learning.
Behav. Processes101, 4–14. doi: 10.1016/j.beproc.2013.05.015
Murakami, M., Shteingart, H., Loewenstein, Y ., and Mainen, Z. F . (2017).
Distinct sources of deterministic and stochastic components of action timing
decisions in rodent frontal cortex. Neuron 94, e7908–e7919. doi: 10.1016/j.neuron.
2017.04.040
Niki, H., and Watanabe, M. (1979). Prefrontal and cingulate unit activity during
timing behavior in the monkey. Brain Res. 171, 213–224. doi: 10.1016/0006-
8993(79)90328-7
Oprisan, S. A., and Buhusi, C. V . (2014). What is all the noise about in interval
timing? Philos. Trans. R. Soc. Lond. B Biol. Sci. 369:20120459. doi: 10.1098/rstb.
2012.0459
Paton, J. J., and Buonomano, D. V . (2018). The neural basis of timing: distributed
mechanisms for diverse functions. Neuron 98, 687–705. doi: 10.1016/j.neuron.
2018.03.045
Pégard, N. C., Mardinly, A. R., Oldenburg, I. A., Sridharan, S., Waller, L.,
Adesnik, H., et al. (2017). Three-dimensional scanless holographic optogenetics
with temporal focusing (3D-SHOT). Nat. Commun. 8:1228. doi: 10.1016/j.neuron.
2018.03.045
Peräkylä, J., Sun, L., Lehtimäki, K., Peltola, J., Öhman, J., Möttönen, T.,
et al. (2017). Causal evidence from humans for the role of mediodorsal
nucleus of the thalamus in working memory. J. Cogn. Neurosci. 29, 2090–2102.
doi: 10.1162/jocn_a_01176
Pergola, G., Danet, L., Pitel, A.-L., Carlesimo, G. A., Segobin, S., Pariente, J., et al.
(2018). The regulatory role of the human mediodorsal thalamus. Trends Cogn. Sci.
22, 1011–1025. doi: 10.1016/j.tics.2018.08.006
Pinheiro de Carvalho, M., and Machado, A. (2012). Relative versus absolute
stimulus control in the temporal bisection task. J. Exp. Anal. Behav. 98, 23–44.
doi: 10.1901/jeab.2012.98-23
Rakitin, B. C., Gibbon, J., Penney, T. B., Malapani, C., Hinton, S. C., Meck, W . H.,
et al. (1998). Scalar expectancy theory and peak-interval timing in humans. J. Exp.
Psychol. Anim. Behav. Processes24, 15–33. doi: 10.1037//0097-7403.24.1.15
Raphan, T., Dorokhin, E., and Delamater, A. R. (2019). Modeling interval timing
by recurrent neural nets. Front. Integr. Neurosci. 13:46. doi: 10.3389/fnint.2019.
00046
Ray, J. P ., and Price, J. L. (1993). The organization of projections from the
mediodorsal nucleus of the thalamus to orbital and medial prefrontal cortex in
macaque monkeys. J. Comp. Neurol. 337, 1–31. doi: 10.1002/cne.903370102
Reutimann, J., Y akovlev, V ., Fusi, S., and Senn, W . (2004). Climbing neuronal
activity as an event-based cortical representation of time. J. Neurosci. 24,
3295–3303. doi: 10.1523/JNEUROSCI.4098-03.2004
Roberts, S. (1981). Isolation of an internal clock. J. Exp. Psychol. Anim. Behav.
Processes 7, 242–268.
Roberts, S., and Holder, M. D. (1984). The function of time discrimination and
classical conditioning. Ann. N Y Acad. Sci. 423, 228–241. doi: 10.1111/j.1749-6632.
1984.tb23433.x
Saunders, R. C., Mishkin, M., and Aggleton, J. P . (2005). Projections from
the entorhinal cortex, perirhinal cortex, presubiculum and parasubiculum to
the medial thalamus in macaque monkeys: identifying different pathways using
disconnection techniques. Exp. Brain Res. 167, 1–16. doi: 10.1007/s00221-005-
2361-3
Schultz, W . (2016). Dopamine reward prediction-error signalling: a
two-component response. Nat. Rev. Neurosci. 17, 183–195. doi: 10.1038/nrn.
2015.26
Shankar, K. H., and Howard, M. W . (2012). A scale-invariant internal
representation of time.Neural Comput.24, 134–193. doi: 10.1162/NECO_a_00212
Shapiro, Z. R., Cerasiello, S., Hartshorne, L., and Matell, M. S. (2018). 5-
HT1a receptor involvement in temporal memory and the response to temporal
ambiguity. Front. Neurosci. 12:439. doi: 10.3389/fnins.2018.00439
Sharpe, M. J., Chang, C. Y ., Liu, M. A., Batchelor, H. M., Mueller, L. E., Jones, J. L.,
et al. (2017). Dopamine transients are sufﬁcient and necessary for acquisition of
model-based associations. Nat. Neurosci. 20, 735–742. doi: 10.1038/nn.4538
Shi, Z., Church, R. M., and Meck, W . H. (2013). Bayesian optimization of time
perception. Trends Cogn. Sci. 17, 556–564. doi: 10.1016/j.tics.2013.09.009
Shikano, Y ., Ikegaya, Y ., and Sasaki, T. (2021). Minute-encoding neurons in
hippocampal-striatal circuits. Curr. Biol. 31, e61438–e61449. doi: 10.1016/j.cub.
2021.01.032
Shimbo, A., Izawa, E.-I., and Fujisawa, S. (2021). Scalable representation of time
in the hippocampus. Sci. Adv. 7:eabd7013. doi: 10.1126/sciadv.abd7013
Silver, R., LeSauter, J., Tresco, P . A., and Lehman, M. N. (1996). A diffusible
coupling signal from the transplanted suprachiasmatic nucleus controlling
circadian locomotor rhythms. Nature 382, 810–813. doi: 10.1038/382810a0
Simen, P ., Balci, F ., deSouza, L., Cohen, J. D., and Holmes, P . (2011). A
model of interval timing by neural integration. J. Neurosci. 31, 9238–9253.
doi: 10.1523/JNEUROSCI.3121-10.2011
Singh, A., Trapp, N. T., De Corte, B., Cao, S., Kingyon, J., Boes, A. D., et al.
(2019). Cerebellar theta frequency transcranial pulsed stimulation increases frontal
theta oscillations in patients with schizophrenia.Cerebellum (London, England)18,
489–499. doi: 10.1007/s12311-019-01013-9
Soares, S., Atallah, B. V ., and Paton, J. J. (2016). Midbrain dopamine
neurons control judgment of time. Science (New Y ork, NY) 354, 1273–1277.
doi: 10.1126/science.aah5234
Swanton, D. N., Gooch, C. M., and Matell, M. S. (2009). Averaging of
temporal memories by rats. J. Exp. Psychol. Anim. Behav. Processes 35, 434–439.
doi: 10.1037/a0014021
Swanton, D. N., and Matell, M. S. (2011). Stimulus compounding in interval
timing: the modality-duration relationship of the anchor durations results in
qualitatively different response patterns to the compound cue. J. Exp. Psychol.
Anim. Behav. Processes37, 94–107. doi: 10.1037/a0020200
Tiganj, Z., Jung, M. W ., Kim, J., and Howard, M. W . (2017). Sequential ﬁring
codes for time in rodent medial prefrontal cortex. Cereb. Cortex (New Y ork, NY)
27, 5663–5671. doi: 10.1093/cercor/bhw336
Toda, K., Lusk, N. A., Watson, G. D. R., Kim, N., Lu, D., Li, H. E., et al.
(2017). Nigrotectal stimulation stops interval timing in mice. Curr. Biol. 27,
e33763–e33770. doi: 10.1016/j.cub.2017.11.003
Tolman, E. C. (1948). Cognitive maps in rats and men.Psychol. Rev.55, 189–208.
doi: 10.1037/h0061626
Tulving, E. (1986). Episodic and semantic memory: where should we go from
here? Behav. Brain Sci. 9, 573–577.
Wang, J., Narain, D., Hosseini, E. A., and Jazayeri, M. (2018). Flexible
timing by temporal scaling of cortical responses. Nat. Neurosci. 21, 102–110.
doi: 10.1038/s41593-017-0028-6
Ward, R. D., Kellendonk, C., Kandel, E. R., and Balsam, P . D. (2012). Timing
as a window on cognition in schizophrenia. Neuropharmacology 62, 1175–1181.
doi: 10.1016/j.neuropharm.2011.04.014
Widloski, J., and Foster, D. J. (2022). Flexible rerouting of hippocampal replay
sequences around changing barriers in the absence of global place ﬁeld remapping.
Neuron 110, e81547–e81558. doi: 10.1016/j.neuron.2022.02.002
Xu, M., Zhang, S., Dan, Y ., and Poo, M. (2014). Representation of interval timing
by temporally scalable ﬁring patterns in rat prefrontal cortex. Proc. Natl. Acad. Sci.
U S A 111, 480–485. doi: 10.1073/pnas.1321314111
Yu, C., Gupta, J., and Yin, H. H. (2010). The role of mediodorsal thalamus in
temporal differentiation of reward-guided actions. Front. Integr. Neurosci. 4:14.
doi: 10.3389/fnint.2010.00014
Zeng, H., and Chen, L. (2019). Robust temporal averaging of time intervals
between action and sensation. Front. Psychol. 10:511. doi: 10.3389/fpsyg.2019.
00511
Zentall, T. R., Weaver, J. E., and Clement, T. S. (2004). Pigeons group time
intervals according to their relative duration. Psychon. Bull. Rev. 11, 113–117.
doi: 10.3758/bf03206469
Zhou, S., and Buonomano, D. V . (2022). Neural population clocks: encoding
time in dynamic patterns of neural activity. Behav. Neurosci. 11, 374–382.
doi: 10.1037/bne0000515
Zhou, S., Masmanidis, S. C., and Buonomano, D. V . (2020). Neural sequences as
an optimal dynamical regime for the readout of time. Neuron 108, e5651–e5658.
doi: 10.1016/j.neuron.2020.08.020
Zhou, S., Masmanidis, S. C., and Buonomano, D. V . (2022). Encoding time in
neural dynamic regimes with distinct computational tradeoffs.PLoS Comput. Biol.
18:e1009271. doi: 10.1371/journal.pcbi.1009271
Frontiers in Behavioral Neuroscience 19 frontiersin.org
