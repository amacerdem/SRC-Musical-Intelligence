# from brain activity using a prior

**Year:** D:20

---

Reconstructing music perception
from brain activity using a prior
guided diffusion model
Matteo Ciferri1, Matteo Ferrante1 & Nicola Toschi1,2
Reconstructing music directly from brain activity provides insight into the neural representations
underlying auditory processing and paves the way for future brain–computer interfaces. We introduce
a fully data-driven pipeline that combines cross-subject functional alignment with bayesian decoding
in the latent space of a diffusion-based audio generator. Functional alignment projects individual fMRI
responses onto a shared representational manifold, increasing the performance of cross-participant
accuracy with respect to anatomically normalized baselines. A bayesian search over latent trajectories
then selects the most plausible waveform candidate, stabilizing reconstructions against neural noise. Crucially, we bridge CLAP’s multi-modal embeddings to music-domain latents through a dedicated
aligner, eliminating the need for hand-crafted captions and preserving the intrinsic structure of musical
features. Evaluated on ten diverse genres, the model achieves a cross-subject-averaged identification
accuracy of 0.914 ± 0.019, and produces audio that human listeners recognize above chance in
85.7% of trials. Voxel-wise analyses locate the predictive signal within a bilateral circuit spanning
early auditory, inferior-frontal, and premotor cortices, consistent with hierarchical and sensorimotor
theories of music perception. The framework establishes a principled bridge between generative audio
models and cognitive neuroscience. Keywords  Brain decoding, Auditory perception, Cognitive science, Machine learning
Music exerts a profound influence on the human brain, involving distinct neural networks that modulate
emotions, trigger memory recall, and affect various neurological states1. Understanding how musical information
is represented in neural activity has implications for both basic neuroscience and potential clinical applications. For example, Brain–Computer Music Interfacing (BCMI)2 explores how musical features can be decoded or
modulated from brain signals, potentially supporting personalized auditory stimulation or communication for
individuals with motor impairments. In addition, music-based cognitive tasks could improve cognitive functions
such as mental flexibility and creativity3. This study investigates the intricate relationship between neural activity and music, focusing on the feasibility
of reconstructing musical stimuli from fMRI data using generative models. A key challenge is decoding high-
frequency musical information (in our case within the 0–8000 Hz range) given the lower temporal resolution
of fMRI data, which is further complicated by regional variations in the brain’s Haemodynamic Response
Function (HRF). The temporal resolution of fMRI inherently constrains the type of musical information that
can be captured. Fast-evolving rhythmic or transient features, which unfold on the order of tens to hundreds of
milliseconds, are effectively blurred in the BOLD signal. As a result, our reconstructions should be interpreted as
reflecting high-level representations rather than fine-grained rhythmic or dynamic aspects of the music. Denk et. al4 examined generative music decoding on the same fMRI corpus, yet our study introduces several
novelties in the decoding approach. First, we bypass the semantic bottleneck introduced by textual conditioning:
instead of prompting the generator with captions, we project neural activity directly into CLAP’s aligned
audio-text space5. Second, rather than relying on subject-specific masks derived from anatomical atlases and
proprietary embeddings such as MuLan and MusicLM6,7, we apply a fully data-driven voxel-selection strategy
based on cross-validated encoding accuracy, yielding a reproducible mask that generalizes across participants. Third, we formulate brain-to-music reconstruction as a bayesian maximum-a-posteriori inference problem that
combines the encoding-model likelihood with the prior imposed by MusicLDM, guiding the diffusion sampler
toward acoustically plausible yet neurally consistent solutions. Finally, in addition to objective similarity metrics,
1Department of Biomedicine and Prevention, University of Rome Tor Vergata, Rome, Italy.
2A. A. Martinos Center for Biomedical Imaging, Massachusetts General Hospital, Boston, USA.
email:
matteo.ciferri@students.uniroma2.eu
OPEN
Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports

we report a forced-choice listening test in which human listeners identify the correct reconstructions, providing
a human-centred benchmark of perceptual fidelity. Figure 1 provides an overview of our approach. Related works
The neural basis of music processing has been explored extensively in classical neuroscience8. Zatorre et al.9
emphasize the importance of auditory and premotor cortex in music perception and imagery, while Levitin
et al.10 highlight the contribution of distributed neural systems—including reward and memory networks—in
supporting music’s emotional and cognitive dimensions. These studies underscore that music engages a broad
cortical and subcortical network. However, recent advancements in artificial intelligence have enabled more detailed and data-driven analyses
of brain responses to musical stimuli11. Building upon prior research, significant progress has been made in
mapping fMRI activity to latent representations of diverse stimuli, including images, video, language, and music,
through techniques such as linear mappings and subject-specific models4,12–14. Takagi et al.15 demonstrate high-
resolution visual reconstruction from fMRI using latent diffusion models. Our work follows a similar philosophy,
extending this concept from vision to audition by coupling fMRI-derived latents with a diffusion-based audio
prior. Giordano et al.16 show that intermediate acoustic-to-semantic representations best explain responses in
the superior temporal gyrus (STG), supporting our choice of CLAP-aligned latent representations as targets
rather than relying on low-level acoustics or purely linguistic descriptors. Bellier et al.17 demonstrate that music
Fig. 1. The proposed pipeline is composed of three stages. In the top section, participants listened to
musical stimuli during the GTZAN-fMRI experiment, with concurrent fMRI recordings capturing their
brain activity. The middle section involves extracting latent representations of the stimuli using the CLAP-
audio model, followed by voxel-wise encoding to correlate brain responses with music, with a correlation
threshold identifying music-responsive regions. In the bottom section, a regression model predicts CLAP-
text embeddings from these regions, which are subsequently used to reconstruct new musical outputs via the
MusicLDM decoder. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

reconstruction can be performed using both linear and nonlinear approaches to decode the auditory experience
using EEG data. The advent of pre-trained models has further facilitated the extraction of latent representations capable of
driving retrieval tasks or conditioning generative models. Notably, the development of text-to-music models
has made it possible to generate high-fidelity music in a conditional framework, linking language-based
representations with the generation of coherent musical outputs7,18,19. Our work extends the approaches of Ferrante et al.20 and Denk et al.4, advancing previous methods by
decoding brain activity between subjects within a generative framework that operates independently from
empirically derived captions. Results
Encoding regions
We empirically set the Pearson Correlation threshold at 0.05, following a principled trade-off between signal
reliability and decoding performance. Lower thresholds (e.g., r < 0.05) increased voxel count but introduced
substantial noise, diluting informative signal and decreasing decoding performance. Conversely, higher
thresholds (e.g., r > 0.05) excluded a large number of moderately informative voxels, reducing the representational
capacity of the decoder. This threshold identified 3043 voxels involved in music processing. See Supplementary
Materials for details and statistical validation. The spatial distribution of these voxels is depicted in Fig. 2. The identified brain regions are primarily located
in the temporal lobes and lateral frontal areas, and are highly plausible as music-responsive regions. The superior
temporal gyrus, particularly in both hemispheres, plays a crucial role in auditory processing, with the right
temporal lobe being especially involved in melody and tonal perception21. Bilateral activation is consistent
with the known engagement of both hemispheres in different aspects of music, such as pitch, rhythm, and
harmony9,22. The involvement of frontal regions, such as the inferior frontal gyrus (IFG), is also expected, given
its association with complex aspects of music cognition, including rhythm processing, pattern recognition, and
musical syntax23,24. These findings align with established research that links music perception with both auditory
processing areas and higher-order cognitive regions. Decoding performance
Table 1 presents the performance of the proposed method, which utilizes functional alignment. The model
achieved an identification accuracy of 0.914 ± 0.019, outperforming several baseline methods from
brain2music4. The computed similarity matrix is visualized as a heatmap (Fig. 3), where each cell represents the cosine
similarity between a real target embedding (row) and a predicted embedding (column). The matrix illustrates
that the predicted latent representations of the stimuli are well-aligned with the real ones (along the diagonal) and,
in some cases, also between representations of closely related genres, such as rock, reggae, and blues. Visualizing
the distribution of cosine similarity values across different genres, we see that classical and jazz exhibited the
highest alignment scores, while genres with more complex rhythmic structures, such as dance and hip-hop,
showed slightly lower alignment. This suggests that certain musical features, like harmonic progression and
melodic consistency, may be more easily decoded from neural activity than rhythmic or textural components. Fig. 2. Spatial distribution and predictive power of music-responsive voxels. Cortical voxels whose BOLD
time series were predicted from the CLAP feature set (using five-fold cross-validated ridge regression)
are shown on the inflated fsaverage template brain. The colorbar represents the mean Pearson correlation
coefficient (r) between predicted and observed responses across participants; voxels with r below an empirical
threshold were excluded, resulting in a final set of 3043 significant voxels. This threshold excluded significant
but weakly predictive voxels. The resulting bilateral network spans: (i) the posterolateral superior temporal
gyrus and Heschl’s gyrus (early tonotopic cortex), (ii) anterior and posterior inferior frontal gyrus, and (iii)
supplementary motor and premotor cortices. Left and right hemispheres are shown in lateral views. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

We additionally performed an ablation varying the number of candidate samples and the inclusion of the
CLAP audio-text aligner. As shown in Table 2, performance metrics (identification accuracy, cosine similarity,
and SSIM) confirm that larger candidate sets improve reconstruction quality with a diminishing returns trend
(after 50 candidates), and that CLAP-based alignment provides a measurable gain. Note that the identification accuracy reported in this ablation refers to post-generation evaluation—that
is, correlations are computed between CLAP embeddings extracted from the generated audio samples and
their corresponding ground-truth embeddings. This differs from the identification metric in Table 1, which
is computed directly on brain-predicted embeddings. The post-generation metric thus reflects end-to-end
reconstruction fidelity, incorporating both latent prediction and diffusion decoding. Fig. 3. Heatmap of cosine similarity scores between real (rows) and predicted (columns) GTZAN embeddings. The colour scale ranges from − 0.2 (blue) to 1.0 (red), with red indicating higher similarity. The concentration
of red along the diagonal indicates a strong match between predicted embeddings and their corresponding real
embeddings. Embedding
Test identification accuracy
SoundStream-avg
0.674 ± 0.016
w2v-BERT-avg
0.837 ± 0.005
MuLantext
0.817 ± 0.014
MuLanmusic
0.876 ± 0.015
MusicLDM-anatomical
0.796 ± 0.017
MusicLDM-functional alignment
0.914 ± 0.019
Table 1. Comparison of test identification accuracy with literature baselines. Our best result reported a 95%
confidence interval of [0.887, 0.939]. A statistical comparison against the best baseline yielded z = 2.51, p =
0.006, assuming Gaussian-distributed accuracies. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

Human results
In the human experiment, participants’ average accuracy was 85.7% with respect to the chance level (50%),
indicating that the human ear can reliably detect the correspondence between the original musical stimulus and
its brain-generated counterpart. Participants were asked to choose the track they perceived as most similar to the
original stimulus before proceeding to the next trial. Individual accuracies ranged from 0.767 to 0.967 (mean ± SD = 0.857 ± 0.064). A one-sample t-test
against the 0.50 chance level confirmed that human performance was significantly above chance (one-sided
p = 1.55 × 10−8; 95% CI [0.807, 0.899]). Table 3 reports the identification accuracies by musical genre,
showing consistently high performance across categories, with particularly strong agreement for classical and
metal excerpts. Samples of the generated tracks compared to the original stimuli are available at: ​h​t​t​p​s​:​/​/​m​u​s​i​c​d​e​c​o​d​.​m​y​.​c​a​n​
v​a​.​s​i​t​e​/​d​e​c​o​d​i​n​g​-​m​u​s​i​c​a​l​-​p​e​r​c​e​p​t​i​o​n. Discussion
This study presents a principled framework for reconstructing musical stimuli from fMRI data, suggesting
potential relevance for future brain–computer interfaces and neuroadaptive applications. By leveraging
MusicLDM and CLAP, we obtain natural-sounding, genre-consistent reconstructions that emphasize a “brain
signature” of music tracks over temporally precise musical events (e.g., micro-timing, rhythmic transients). This
outcome is consistent with the temporal resolution and macroscopic nature of fMRI. The identification of music-responsive regions aligns with previous studies, with clusters in superior temporal
gyrus (STG), inferior frontal gyrus (IFG), and lateral prefrontal cortex. The bilateral distribution across temporal
areas indicates that information predictive of our CLAP embeddings is present in both hemispheres. This spatial
pattern is consistent with established roles of temporal cortex in auditory analysis (including pitch/timbre) and
frontal cortex in higher-order musical structure9,21,22. We interpret our results as compatible with models in
which STG supports spectral–acoustic analyses and IFG contributes to processing of structural regularities and
musical syntax, as suggested by prior literature24,25. While the novelty of our work does not lie in identifying new
brain regions, the convergence with canonical auditory circuits supports the validity of our decoding framework. Testing hypotheses about temporal integration windows or motor entrainment would require higher-temporal-
resolution modalities (e.g., MEG/iEEG). Among the competing audio embeddings, the two MuLan variants outrank SoundStream and w2v-
BERT, yet are themselves outperformed by the proposed CLAP ↔ MusicLDM latent. The pattern sketches a
spectrum: models that bind musical timbre to semantic captions (MuLan) fare better than purely signal-driven
representations (SoundStream), but the hybrid embedding that is explicitly optimized for generation captured
still more of the variance linked to brain responses. This suggests that cortical populations respond not just
Genre
Acc. (mean ± SD)

## 95% CI

Blues
0.800 ± 0.153
[0.690, 0.910]
Classical
0.963 ± 0.031
[0.938, 0.991]
Country
0.833 ± 0.176
[0.708, 0.959]
Disco
0.800 ± 0.172
[0.677, 0.923]
Hip-hop
0.783 ± 0.081
[0.726, 0.841]
Jazz
0.917 ± 0.088
[0.854, 0.980]
Metal
0.933 ± 0.076
[0.872, 0.995]
Pop
0.817 ± 0.183
[0.685, 0.948]
Reggae
0.821 ± 0.199
[0.675, 0.975]
Rock
0.833 ± 0.208
[0.685, 0.982]
Table 3. Human accuracy by musical genre (mean ± SD, 95% CI). Config. ID. Acc. Cosine Sim. SSIM
Our best (100 samples)
0.823 ± 0.029
0.548 ± 0.012
0.177 ± 0.011
50 samples
0.819 ± 0.018
0.547 ± 0.021
0.170 ± 0.015
20 samples
0.766 ± 0.031
0.521 ± 0.021
0.154 ± 0.014
1 sample
0.741 ± 0.024
0.492 ± 0.022
0.153 ± 0.013

### 100 NoAligner

0.736 ± 0.027
0.451 ± 0.026
0.149 ± 0.013
Table 2. Ablation study on the generative prior. Metrics are averaged over 5 subjects (test set, mean ± SD). Notably, all the configurations showed significant SSIM and cosine similarity (e.g. p = 0.001 for our best
configuration) compared to a null model obtained by random permutation of brain-audio mappings. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

to low-level acoustics, nor only to high-level semantic tags, but to an intermediate abstraction that generative
diffusion models are well suited to represent. Relatedly, cosine-similarity values reveal that classical and jazz
stimuli map most faithfully from cortex to embedding, whereas dance and hip-hop exhibit a lower degree of
alignment. A plausible account is temporal: fMRI’s 1.5 s TR smears rapid onsets and syncopated beats, depriving
the regression model of rhythmically diagnostic features while leaving slower-evolving harmonic progressions
largely intact. Interestingly, reggae, rock and blues cluster together off the diagonal of the similarity matrix,
implying that shared back-beat structure and guitar timbres co-activate overlapping voxel subsets; the decoder
finds these embeddings exchangeable in latent space, echoing behavioural confusions reported in genre-labelling
studies. Also, participants recognized the correct reconstructions 85.7% of the time, a figure that lags the embedding-
level accuracy yet still doubles chance performance. The gap between machine and human metrics likely reflects
musicality cues that reside outside the evaluated embedding dimensions—e.g. micro-timing and dynamic
range—that listeners notice even when the cosine test is passed. Put differently, the brain-to-embedding mapping
identifies “what song is it most similar to?” more often than “does it sound musically convincing?”, highlighting a
potential avenue for adversarial fine-tuning of the generative prior 26,27. Broader applications
The results emphasize the potential of functional alignment techniques in reducing inter-subject variability,
providing a more generalized model of music perception across individuals. This aspect is particularly relevant for
applications in brain–computer interfaces (BCI) and neuroprosthetics, where reliable and subject-independent
decoding is crucial. Put differently, gains over the best baseline are likely robust, signaling that between-person
variability is less intractable than often feared. Functional alignment here acts like a low-dimensional morph
of each individual cortical sheet into a shared computational space, suppressing idiosyncratic folding while
preserving representational geometry. The ability to reconstruct auditory experiences from neural signals could
support non-verbal communication in individuals with severe motor or cognitive impairments, such as patients
with locked-in syndrome or advanced neurodegenerative disease. Limitations
With a TR of 1.5 s, rapid temporal dynamics such as rhythmic transients, syncopation, and micro-timing
cannot be faithfully encoded in the neural signal. Accordingly, the present reconstructions should be regarded
as capturing static, timbral-genre features that characterize the overall acoustic profile of a piece, rather than
temporally precise musical events. Beyond temporal blurring, the subsampled and noisy nature of fMRI further enforces a macroscopic,
averaged representation of neural activity. Under these macroscopic conditions, linear mappings often provide
the most reliable predictive performance for fMRI data, as spatial/temporal averaging and measurement noise
can mask microscale non-linearities; thus we adopt ridge regression as a principled, well-validated baseline for
brain decoding mapping 28. This choice does not preclude non-linear decoders; rather, it reflects the data regime
studied here. Future work with higher-resolution modalities or larger datasets could profitably revisit non-linear
mappings to capture finer neural effects. Finally, while CLAP and MusicLDM enable robust feature extraction and generation, they also carry biases
from their training corpora, which may influence reconstructed content. We therefore interpret results as
reconstructions within these model priors, not as unbiased samples of the full musical space. Conclusions
Our framework offers several methodological advances. First, cross-subject functional alignment markedly
elevates decoding accuracy, enabling music reconstruction that generalizes across listeners rather than being
confined to single-participant models. Second, embedding the neural signals in the latent space of a diffusion
generator yields natural-sounding reconstructions that preserve perceptual consistency. Third, framing the
decoding step as a Bayesian inference problem represents a novel contribution: probabilistic sampling over
candidate latents selects the most plausible stimulus, thereby stabilizing the output against noise in the neural
data. Instead of relying on written captions, we map CLAP’s text embeddings directly onto music-domain
embeddings via a dedicated aligner. This strictly audio-driven, free-text bridge captures musical features without
the biases introduced by external verbal descriptions. Consistent with prior work, we find that genres with
pronounced structural signatures—classical and jazz—are encoded more robustly, whereas closely related styles
such as rock and blues remain harder to disambiguate, underscoring the need for finer-grained modelling. Several extensions suggest themselves. Comparative studies spanning varying levels of musical expertise and
culturally diverse cohorts could clarify how experience and enculturation shape neural encoding. Incorporating
modalities with superior temporal resolution (e.g., intracranial EEG) should improve decoding of rhythmic and
transient features that fMRI blurs. The capacity to reconstruct music directly from brain activity may contribute to several applications: thought-
driven composition for individuals with motor impairments, objective indices for music-based therapies in
neurodegenerative disease, and diagnostic assays for auditory-processing disorders, among others. In sum, this study lays groundwork for next-generation neural music decoding at the intersection of
generative modelling and cognitive neuroscience, opening new avenues for both basic research and translational
applications in technology and healthcare. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

Methods
This section details the dataset and methods employed in this study. The principal innovation of this study resides
in the decoding pipeline, which integrates feature alignment, generative modelling, and bayesian inference into a
multi-stage procedure (see Decoding Model section for details). First, we train a simple linear projection that maps CLAP’s audio embeddings into its text-embedding
subspace5. This step establishes a cross-modal bridge: although our conditioning variables originate from audio,
they are transformed into the same latent domain that the generative model natively expects for text prompts. Next, ridge regression model transforms fMRI patterns into CLAP-aligned latent coordinates, establishing a
direct interface between cortical signals and the representational space used for music synthesis. In this way, the
diffusion process can be conditioned directly by neural activity, without recourse to natural-language captions. MusicLDM, a diffusion model originally developed for text-to-music generation 29, is thus repurposed to render
audio waveforms from the brain-predicted latents. Finally, we cast the decoding task within a probabilistic inference problem: our goal is to infer the most likely
musical stimulus x given observed brain activity z, by maximizing the posterior p(x|z) ∝p(z|x)p(x). Here,
p(z|x) models the encoding likelihood, and p(x) represents a generative prior over realistic music samples
defined by MusicLDM. Inspired by recent work on brain-to-image decoding15,30, we adopt a two-stage approach:
we sample a candidate set of music stimuli from the generative prior, and select the one that best matches the
observed activity (maximum-a-posteriori estimation). This method implements a form of rejection sampling
that balances perceptual realism (via p(x)) and neural consistency (via p(z|x)). Model performance is assessed using identification accuracy4 (see “Evaluation” section), defined as the
proportion of test samples for which the brain-predicted embedding was closest (in CLAP space) to the true
embedding of the corresponding stimulus among all test candidates. This measure, standard in brain decoding
studies, reflects the model’s capacity to target the correct stimulus representation from neural activity. Dataset
We used the GTZAN fMRI public dataset31, which consists of fMRI data from five subjects (sub-001 to sub-005)
exposed to music stimuli drawn from ten distinct genres: blues, classical, country, disco, hip-hop, jazz, metal,
pop, reggae, and rock. Each genre was represented by 54 tracks (i.e. stimuli) sampled at 22.050 kHz. Subjects
underwent 18 fMRI runs, of which 12 were used for training and 6 for testing. Each run consisted of 40 music
clips, each 15 s in duration. The stimuli were RMS normalized and included a 2-s fade-in and fade-out. During
testing, each stimulus was presented four times, and the brain activity (i.e. fMRI signal) was averaged across
identical stimuli to enhance the signal-to-noise ratio. Scanning was performed using a 3.0T MRI scanner with a repetition time (TR) of 1500 ms, yielding 400
volumes per run. Preprocessing included motion correction, co-registration to Montreal Neurological Institute
(MNI) space using T1-weighted anatomical images, detrending, and run-level standardization. Brain activity
was time-shifted by 3 TRs (4.5 s) to account for the delayed hemodynamic response, and neural representations
were averaged over 10 volumes (15 s). This procedure provides a high-SNR estimate of the sustained BOLD
response, which is most relevant for track-level decoding32,33. The final dataset comprised 540 fMRI-stimulus
pairs per subject (480 for training and 60 for testing). Encoding model
Music processing in the brain involves complex, nonlinear mechanisms. To capture this, we used the CLAP model5,
a multimodal neural network employing contrastive learning for audio and text alignment. CLAP extracts audio
features using the SWINTransformer34 and log-Mel spectrograms, as well as text features using RoBERTa35,
projecting both into a shared latent space. Similarity is commonly used to measure the correspondence between
elements of this shared latent space. In order to identify brain regions most responsive to music, we trained a
voxel-wise encoding model that predicts fMRI responses z from CLAP’s audio embeddings h (extracted from each
stimulus x). Specifically, Ridge regression with cross-validation was applied independently to each voxel. Model
training incorporated a hyperparameter search for the regularization parameter α (ranging on a logarithmic
scale from 10−2 to 103) and we empirically determined a correlation threshold (in a discrete range of values
[0.01, 0.02, 0.05, 0.10, 0.15, 0.20]) to define music-responsive brain regions by choosing a value according to
maximizing decoding results and minimizing noise. Pearson correlation coefficients were used to create a voxel-
wise correlation map between real and predicted fMRI activity, identifying regions most responsive to music. Formally, for each subject i, we estimate whole-brain encoding weights β to predict brain activity z using
the latent representations of audio h as inputs. Specifically, we train a model ˆzi = hβi for each subject. To
optimize the weights β, we perform nested cross-validation on the training set, minimizing the loss function
L = |ztr
i −htrβi|2 + α|βi|2. In each fold, we predict the held-out data (20% of the training set not used to
train that specific model). When predicting on the entire training set, we compute the voxel-wise correlation
between the predicted and real brain activity, corr( ˆ
ztr
i, ztr
i ), selecting only voxels that exceed the correlation
threshold for further analysis. Functional alignment
In order to mitigate individual variability in brain structure and function, we employed cross-subject data
aggregation techniques following Ferrante et al.20. Anatomical alignment is widely used in neuroimaging as it
facilitates the direct comparison of localized brain activity across subjects. However, relying solely on the brain’s
physical structure for alignment and decoding lacks the precision needed for fine-grained tasks due to inherent
subject-specific anatomical variability, which may not exactly mirror functional differences. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

To account for individual variability in brain responses and to enable cross-subject generalization, we
implemented a functional alignment strategy based on Ridge regression, inspired by prior work on linear
alignment techniques36. The underlying assumption is that, although fMRI activity patterns vary across
individuals, they all encode information about the same stimulus content. Therefore, one subject’s activity
can be expressed as a linear transformation of another subject’s activity when exposed to the same stimuli. Concretely, given a source subject and a target subject (sub-001), we sought a linear mapping W such that
T ≈SW T, where S and T denote the matrices of voxel-wise brain responses for the same stimuli from the
source and target subjects, respectively. The mapping W is a matrix in which each column defines the weights
for reconstructing one voxel in the target subject as a linear combination of all source voxels. In order to
compute W, we employed Ridge regression with five-fold cross-validation to select the optimal regularization
parameter α ∈{0.1, 10, 102, 103, 104}. The model was fit independently for each subject, using the training
set to estimate W, and then applied to both training and test data from the source subject. Aligned activity was
further standardized and rescaled to match the distribution of the target subject (sub-001), ensuring consistency
across runs and subjects. The choice of sub-001 as the alignment target followed practical and methodological
considerations. This subject had high-quality recordings across all experimental runs and showed robust and
representative functional responses. More elaborate techniques, such as Hyperalignment37, estimate high-dimensional shared spaces or subject-
specific transformations; these additional parameters increase model complexity and can hinder interpretability. Hyperalignment performs a statistical shape analysis that iteratively rotates each subject’s representational
space so as to minimize pairwise dissimilarities with respect to a common template. In a recent comparison
of alignment strategies for cross-subject music decoding20, the regression-based method achieved the highest
accuracy while retaining the advantages of interpretability and generalization. Decoding model
Our decoding framework aims to generate music from brain activity by combining feature alignment, neural
regression, diffusion modeling, and probabilistic guidance for reconstruction. This process involves different
components, described below. We first established an alignment between audio and textual embeddings in CLAP’s joint latent space. Specifically, we used embeddings from the MusicCaps dataset7 and trained a linear projection from audio to
text representations by minimizing the mean squared error (MSE) between them. This transformation yields
a set of 512-dimensional aligned embeddings as conditioning vectors for stimuli generation. Given that CLAP
is pretrained to produce semantically consistent audio-text representations, a simple linear layer is enough to
refine this alignment without introducing overfitting or distorting the structure of the latent space. Then we trained a regression model to map brain activity to the CLAP-aligned latent space. We used Ridge
regression with five-fold cross-validation to predict embeddings from fMRI data in the GTZAN dataset. This
regression step effectively creates a bridge between brain signals and musical representations, enabling us to infer
CLAP embeddings directly from neural activity. These embeddings are then used to condition the generative
model. For the generation stage, we used the Music Latent Diffusion Model (MusicLDM)29, a state-of-the-art
generative model that synthesizes audio from text prompts. Importantly, MusicLDM internally uses CLAP text
embeddings as conditioning inputs for its latent diffusion process (U-Net based) and HiFi-GAN vocoder27 for
waveform reconstruction. In our framework, we replace these text-derived embeddings with brain-predicted
CLAP embeddings, keeping the generative process unchanged. This ensures full compatibility between the
decoding model and the conditioning space used by MusicLDM. The complete pipeline is illustrated in Fig. 4. Finally we framed the problem within a bayesian approach to decode music from brain activity, providing
a structured way to infer the most likely musical stimulus x given observed brain activity z. Bayesian inference
allows us to incorporate prior knowledge and systematically update our beliefs about potential solutions, leading
to more robust decoding results. Instead of directly modeling p(x|z), which is complex due to the stochastic
nature of generative models, we factorized the problem using Bayes’ theorem:
p(x|z) ∝p(z|x)p(x),
where p(z|x) represents how likely the observed brain activity is given a musical stimulus, and p(x) is a prior
over musical stimuli that constrains the possible solutions to realistic ones. This formulation allows us to
infer the musical stimulus by evaluating different candidate songs and selecting the one that best matches the
observed neural activity. Specifically, we select from 100 trials the one that maximizes the correlation between
the real brain activity z and the predicted brain response ˆz obtained by passing the candidate song x through
the encoding model p(z|x). A direct sampling from p(x) would be computationally prohibitive due to the
large space of possible musical pieces. To make this approach feasible, we introduce a guidance mechanism that
restricts sampling to a structured latent space, reducing the complexity of the problem. Specifically, we define a
mechanism based on CLAP latent space alignment:
p(x) = p(x|h)p(h|z),
where p(x|h) is the generative model (MusicLDM) conditioned on h representation from CLAP linear aligner,
and p(h|z) represents the mapping between neural activity and the CLAP-aligned latent space via Ridge
regression. This method provides a computationally tractable way to sample plausible musical outputs while
maintaining strong correspondence with neural data. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

Evaluation
We evaluated model performance using the identification accuracy metric defined in the Brain2Music
framework4, which quantifies the correspondence between predicted and target music embeddings using Pearson
correlation. A correct identification occurs when the correlation between a predicted and true embedding is
higher than with any other target embedding. We computed a correlation matrix C, where Ci,j represents the
Pearson correlation between the i-th predicted embedding and the j-th target embedding. The identification
accuracy was computed as:
id_acci =

n −1
n
∑
j=1
1 [Ci,i > Ci,j]
where 1[·] is the indicator function. The overall accuracy was averaged across all predictions. This metric ensures
the robustness of the model in discriminating between embeddings, which is crucial for applications requiring
high precision. We also evaluated the cosine similarity matrix between the real and brain-predicted CLAP embeddings using
the following formula:
cosine_simi,j =
ri · pj
∥ri∥∥pj∥
where ri and pj are the normalized real and predicted embeddings, respectively. Each score represents the
degree of alignment between these embeddings, which is critical for evaluating the model’s performance in
producing embeddings consistent with the target data. Finally, the structural similarity index (SSIM) was
computed between the Mel-spectrograms of the generated and ground-truth audio signals. SSIM quantifies the
structural fidelity of the reconstruction in the time–frequency domain, assessing how well the generated sample
preserves spectral and dynamic patterns of the original stimulus. As a qualitative evaluation, we developed a human metric to assess the perceived similarity between
reconstructed and original music stimuli. 10 participants listened to pairs of stimuli from the test set and were
asked to identify which of the two stimuli was the correct decoded version. Subsequently, we calculated the
percentage of correct identifications and averaged across subjects. We used Streamlit, a Python framework, to
develop a simple web interface for participants. Streamlit is an open-source library for turning data scripts into
web applications without requiring the implementation of a custom front end. The user experience consisted of
listening to three distinct audio stimuli: the original stimulus, the brain-decoded version of the target stimulus,
and a randomly selected brain-decoded track from the test set. In each trial, the randomly selected song was
Fig. 4. Overview of the music generation framework from fMRI. (1) GTZAN music stimuli transformed
by the CLAP-audio model into latent representations, used for inference. (2) MusicCaps stimuli processed
by CLAP-audio for music embeddings and CLAP-text encoder for captions. (3) A linear layer maps these
embeddings into a 512-dimensional latent space. (4) Music-responsive brain regions are used to estimate new
GTZAN embeddings via regression. (5) The predicted embeddings are passed to the MusicLDM decoder for
music generation. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

chosen without regard to genre, which permitted participants to encounter pairs from closely related genres
(e.g. ‘hip-hop’ vs. ‘pop’ or even ‘hip-hop’ vs. ‘hip-hop’) as well as contrasting genres (e.g. ‘hip-hop’ vs. ‘jazz’). See
Supplemetary Materials for human details. Data availability
The dataset is publicly accessible at: ​h​t​t​p​s​:​/​/​o​p​e​n​n​e​u​r​o​.​o​r​g​/​d​a​t​a​s​e​t​s​/​d​s​0​0​3​7​2​0​/​v​e​r​s​i​o​n​s​/​1​.​0​.​1. The present study
makes use of the publicly available GTZAN-fMRI dataset by38, which was collected under informed consent
and institutional ethical approval. The authors did not acquire new data. The code implementation is available
at this repository: https://github.com/neoayanami/fmri-music-gen. This manuscript represents the authors’ ​o​r​i​
g​i​n​a​l work, has not been previously published, and is not under consideration elsewhere. All authors have made
substantial contributions to the work, take full responsibility for its content, and have approved the final version. The manuscript properly credits prior work and the contributions of all co-authors. The human evaluation study
involved only listening to short musical excerpts and providing simple perceptual judgments. No clinical proce­
dures or sensitive personal data were collected, and the task involved no risk or discomfort. All participants were
informed about the nature of the study and provided their verbal consent prior to participation. Received: 5 August 2025; Accepted: 27 October 2025
References

### 1. Margulis, E. H., Wong, P. C. M., Simchy-Gross, R. & McAuley, J. D. What the music said: narrative listening across cultures. Palgrave Commun. 5, 146. https://doi.org/10.1057/s41599-019-0363-1 (2019).

### 2. Miranda, E., Wilson, N.-F., Palaniappan, R., Eaton, J. & Magee, W. Brain-computer music interfacing (BCMI) from basic research

to the real world of special needs. Music Med. 3, 134–140. https://doi.org/10.1177/1943862111399290 (2011).

### 3. Olszewska, A. M., Gaca, M., Herman, A. M., Jednoróg, K. & Marchewka, A. How musical training shapes the adult brain: Predispositions and neuroplasticity. Front. Neurosci. 15, https://doi.org/10.3389/fnins.2021.630829 (2021).

### 4. Denk, T. I. et al. Brain2music: Reconstructing music from human brain activity (2023). arxiv:2307.11078.

### 5. Elizalde, B., Deshmukh, S., Ismail, M. A. & Wang, H. Clap: Learning audio concepts from natural language supervision (2022).

arxiv:2206.04769.

### 6. Huang, Q. et al. Mulan: A joint embedding of music audio and natural language (2022). arxiv:2208.12415.

### 7. Agostinelli, A. et al. Musiclm: Generating music from text (2023). arxiv:2301.11325.

### 8. Raglio, A. et al. Music in the workplace: A narrative literature review of intervention studies. J. Complement. Integr. Med. ​h​t​t​p​s​:​/​/​d​

o​i​.​o​r​g​/​1​0​.​1​5​1​5​/​j​c​i​m​-​2​0​1​7​-​0​0​4​6​ (2019).

### 9. Zatorre, R. J., Chen, J. L. & Penhune, V. B. When the brain plays music: auditory-motor interactions in music perception and

production. Nat. Rev. Neurosci. 8, 547–558 (2007).

### 10. Levitin, D. J. & Tirovolas, A. K. Current advances in the cognitive neuroscience of music. Ann. N. Y. Acad. Sci. 1156, 211–231

(2009).

### 11. Oota, S. R. et al. Deep neural networks and brain alignment: Brain encoding and decoding (survey) (2023). arxiv:2307.10246.

### 12. Ferrante, M., Boccato, T., Ozcelik, F., VanRullen, R. & Toschi, N. Multimodal decoding of human brain activity into images and

text. In UniReps: the First Workshop on Unifying Representations in Neural Models (2023).

### 13. Scotti, P. S. et al. Reconstructing the mind’s eye: fmri-to-image with contrastive learning and diffusion priors (2023).

arxiv:2305.18274.

### 14. Chen, Z., Qing, J. & Zhou, J. H. Cinematic mindscapes: High-quality video reconstruction from brain activity (2023).

arxiv:2305.11675.

### 15. Takagi, Y. & Nishimoto, S. High-resolution image reconstruction with latent diffusion models from human brain activity. In

Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, 14453–14463 (2023).

### 16. Giordano, B. L., Esposito, M., Valente, G. & Formisano, E. Intermediate acoustic-to-semantic representations link behavioral and

neural responses to natural sounds. Nat. Neurosci. 26, 664–672 (2023).

### 17. Bellier, L. et al. Music can be reconstructed from human auditory cortex activity using nonlinear decoding models. PLoS Biol. 21,

e3002176. https://doi.org/10.1371/journal.pbio.3002176 (2023).

### 18. Lam, M. W. Y. et al. Efficient neural music generation (2023). arxiv:2305.15719.

### 19. Copet, J. et al. Simple and controllable music generation (2024). arxiv:2306.05284.

### 20. Ferrante, M., Ciferri, M. & Toschi, N. R &b—rhythm and brain: Cross-subject decoding of music from human brain activity

(2024). arxiv:2406.15537.

### 21. Peretz, I. Brain specialization for music. Neuroscientist 8, 372 (2002).

### 22. Norman-Haignere, S., Kanwisher, N. G. & McDermott, J. H. Distinct cortical pathways for music and speech revealed by

hypothesis-free voxel decomposition. Neuron. 88, 1281–1296 (2015).

### 23. Koelsch, S. & Siebel, W. A. Towards a neural basis of music perception. Trends Cogn. Sci. 9, 578–584 (2005).

### 24. Grahn, J. A. & Brett, M. Rhythm and beat perception in motor areas of the brain. J. Cogn. Neurosci. 19, 893–906 (2007).

### 25. Koelsch, S. Brain correlates of music-evoked emotions. Nat. Rev. Neurosci. 15, 170–180. https://doi.org/10.1038/nrn3666 (2014).

### 26. Shen, F. et al. Advancing pose-guided image synthesis with progressive conditional diffusion models. arXiv preprint

arXiv:2310.06313 (2023).

### 27. Kong, J., Kim, J. & Bae, J. Hifi-gan: Generative adversarial networks for efficient and high fidelity speech synthesis (2020).

arxiv:2010.05646.

### 28. Nozari, E. et al. Macroscopic resting-state brain dynamics are best described by linear models. Nat. Biomed. Eng. 8, 7–8. ​h​t​t​p​s​:​/​/​d​

o​i​.​o​r​g​/​1​0​.​1​0​3​8​/​s​4​1​5​5​1​-​0​2​3​-​0​1​1​1​7​-​y​ (2024).

### 29. Chen, K. et al. Musicldm: Enhancing novelty in text-to-music generation using beat-synchronous mixup strategies (2023).

arxiv:2308.01546.

### 30. Lin, S., Sprague, T. & Singh, A. K. Mind reader: Reconstructing complex images from brain activities. Adv. Neural. Inf. Process. Syst.

35, 29624–29636 (2022).

### 31. Nakai, T., Koide-Majima, N. & Nishimoto, S. Music genre FMRI dataset. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​8​1​1​2​/​o​p​e​n​n​e​u​r​o​.​d​s​0​0​3​7​2​0​.​v​1​.​0​.​1​(​2​0​

2​3​)​.​

### 32. Dupré la Tour, T., Visconti di Oleggio Castello, M. & Gallant, J. L. The voxelwise encoding model framework: a tutorial introduction

to fitting encoding models to FMRI data. Imaging Neurosci. 3, imag_a_00575 (2025).

### 33. Naselaris, T., Kay, K. N., Nishimoto, S. & Gallant, J. L. Encoding and decoding in FMRI. Neuroimage 56, 400–410 (2011).

### 34. Liu, Z. et al. Swin transformer: Hierarchical vision transformer using shifted windows (2021). arxiv:2103.14030.

### 35. Liu, Y. et al. Roberta: A robustly optimized bert pretraining approach (2019). arxiv:1907.11692. Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/

### 36. Ferrante, M., Boccato, T., Ozcelik, F., VanRullen, R. & Toschi, N. Through their eyes: multi-subject brain decoding with simple

alignment techniques. Imaging Neurosci. 2, 1–21 (2024).

### 37. Haxby, J. V. et al. A common, high-dimensional model of the representational space in human ventral temporal cortex. Neuron 72,

404–416 (2011).

### 38. Nakai, T., Koide-Majima, N. & Nishimoto, S. Music genre neuroimaging dataset. Data Brief 40, 107675. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​

d​i​b​.​2​0​2​1​.​1​0​7​6​7​5​ (2022). Acknowledgements
This work was supported by NEXTGENERATIONEU (NGEU) and funded by the Italian Ministry of Univer­
sity and Research (MUR), National Recovery and Resilience Plan (NRRP), project MNESYS (PE0000006) (to
NT)—A Multiscale integrated approach to the study of the nervous system in health and disease (DN. 1553
11.10.2022); by the MUR-PNRR M4C2I1.3 PE6 project PE00000019 Heal Italia (to NT); by the NATIONAL
CENTRE FOR HPC, BIG DATA AND QUANTUM COMPUTING, within the spoke “Multiscale Modeling and
Engineering Applications” (to NT); the EXPERIENCE project (European Union’s Horizon 2020 Research and
Innovation Programme under grant agreement No. 101017727); the CROSSBRAIN project (European Union’s
European Innovation Council under grant agreement No. 101070908). Author contributions
M. C.: Conceptualization, data curation, formal analysis, investigation, methodology, software, visualization,
writing—original draft. M. F.: Conceptualization, formal analysis, investigation, methodology, visualization. N. T.: Funding acquisition, project administration, resources, supervision, writing—review and editing. Declarations
Competing interests
The authors declare no competing interests. Additional information
Supplementary Information The online version contains supplementary material available at ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​3​8​/​s​4​1​5​9​8​-​0​2​5​-​2​6​0​9​5​-​w​.​
Correspondence and requests for materials should be addressed to M. C. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
institutional affiliations. Open Access  This article is licensed under a Creative Commons Attribution-NonCommercial-NoDerivatives
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
Scientific Reports | (2025) 15:42108

| https://doi.org/10.1038/s41598-025-26095-w
www.nature.com/scientificreports/
