# Hybrid weighted fuzzy production

**Year:** D:20

---

Hybrid weighted fuzzy production
rule extraction utilizing modified
harmony search and BPNN
Feng Qin1,2, Azlan Mohd Zain1, Kai-Qing Zhou2 & De-Bing Zhuo3
Weighted Fuzzy Production Rules (WFPRs) are vital for Clinical Decision Support Systems (CDSSs),
significantly impacting diagnostic accuracy and bridging the gap between data-driven insights and
actionable clinical decisions through knowledge engineering. This paper proposes an integrated
approach combining the Dynamic Dimension Adjustment Harmony Search (DDA-HS) Algorithm
and Back Propagation Neural Networks (BPNNs) to enhance WFPR extraction accuracy. DDA-HS
dynamically adjusts search space dimensions through fitness evaluations, optimizing initial weights
in BPNNs and leveraging an absorbing Markov chain to enhance transition probabilities, supporting
exploration and avoiding local optima in high-dimensional spaces. Evaluated against existing
optimization methods including Harmony Search (HS), Cuckoo Search (CS), Adaptive Global Optimal
Harmony Search (AGOHS), and Harmony Search with Cuckoo Search (HSCS) Algorithms, DDA-HS
achieves 74.48% accuracy for BPNN classification and 77.08% for WFPR classification on the PIMA
dataset, representing improvements of 3.6% and 6.5%, respectively. WFPR extraction enhances BPNN
interpretability by revealing feature influences on decision-making, improving both accuracy and
transparency. The proposed method offers a robust framework for reliable and interpretable CDSSs in
healthcare. Keywords  WFPRs, CDSSs, DDA-HS, BPNNs, Optimization, Interpretability
Clinical Decision Support Systems (CDSSs) have evolved from Expert Systems (ESs), which are knowledge-
driven frameworks aimed at mimicking expert-level decision-making. ESs are composed of three main
components: a knowledge/rule base, an inference engine, and a user interface1. In the healthcare sector, CDSSs
leverage these components to support clinicians in diagnosing and treating patients effectively2. By integrating
clinical guidelines with patient-specific data, CDSSs enhance the decision-making process, ultimately improving
patient outcomes. Knowledge-driven CDSSs utilize structured knowledge bases containing clinical guidelines,
protocols, and heuristics to guide healthcare professionals in their decision-making3. These systems rely on
expert-defined rules and clinical evidence to provide recommendations, which are particularly useful in
complex medical scenarios. Notable works in this area include the studies in4, which explored the integration
of expert knowledge into clinical settings, and later advancements in5, highlighting the evolution and impact of
knowledge-driven CDSSs in improving healthcare delivery. In contrast, data-driven CDSSs leverage machine
learning techniques, neural networks, and swarm intelligence optimization algorithms to analyze large datasets
and derive insights that inform clinical decisions. These systems focus on pattern recognition within patient
data, identifying trends and correlations that may not be evident through traditional expert-based approaches. Pioneering research in6 illustrates the potential of data-driven methods to enhance predictive analytics in
healthcare, while the work of7 emphasizes the effectiveness of combining neural networks with optimization
algorithms to develop robust CDSSs capable of adapting to dynamic clinical environments. At the core of CDSSs lie the knowledge/rule base and inference mechanism, both of which are crucial for
generating accurate and interpretable clinical recommendations. The knowledge/rule base, often structured
around fundamental IF-THEN rules, integrates clinical guidelines and decision protocols, guiding the system’s
reasoning process8. In these systems, IF-THEN statements define conditions under which specific clinical actions
or decisions should be recommended, such as If symptom X and test result Y are present, then consider diagnosis
Z. This approach not only supports reliable recommendations but also enhances the interpretability of CDSSs,
allowing clinicians to understand and verify the rationale behind each recommendation9. However, building a
comprehensive and precise knowledge/rule base that balances accuracy with interpretability poses significant
1Faculty of Computing, Universiti Teknologi Malaysia, Skudai 81310, Malaysia. 2School of Communication and
Electronic Engineering, Jishou University, Jishou 416000, China. 3School of Civil Engineering and Architecture, Jishou University, Zhangjiajie 427000, China. email: kqzhou@jsu.edu.cn
OPEN
Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports

challenges. The vast complexity of medical knowledge and patient variability require adaptable rules that can
account for nuanced clinical scenarios10, making rule base development a resource-intensive task. Additionally,
as medical guidelines evolve, regularly updating the rule base is essential to ensure recommendations remain
current, reliable, and transparent11. Research in12 emphasizes that well-curated and precise rule bases not only
improve CDSS accuracy but also increase clinician trust by providing recommendations that are both evidence-
based and easily understood. Recent advancements have introduced Weighted Fuzzy Production Rules (WFPRs) to improve CDSSs by
incorporating weights and fuzzy logic, offering a more nuanced representation of medical knowledge. WFPRs
address clinical uncertainty by assigning degrees of membership to inputs, which captures the inherent ambiguity
in clinical data. This approach has shown success in diabetes diagnosis13, enhancing prediction accuracy and
supporting better decision-making by accounting for variability in patient responses. Furthermore, WFPRs
contribute to the interpretability of clinical models, especially in managing complex, non-linear bioinformatics
data14,15, thereby enhancing both classification accuracy and clinical insight. To effectively extract WFPRs, Back Propagation Neural Networks (BPNNs) have proven valuable due to
their ability to learn complex relationships. However, BPNNs are highly sensitive to initial weight settings,
which significantly affect both convergence speed and model accuracy16. Inadequate initialization can lead to
convergence issues or entrapment in local minima, thus impacting rule extraction quality17. To address this
challenge, metaheuristic algorithms, such as the Harmony Search (HS) Algorithm, have been employed to
optimize the initial weights of BPNNs18. HS iteratively refines solutions by balancing the exploitation of past
information with random exploration, enabling a more thorough search across the solution space. Nevertheless, standard HS faces limitations, particularly with large or complex datasets, where it can struggle
to achieve an optimal balance between local and global search. To address these issues, several HS variants have
been developed. For instance, Adaptive Global Optimal Harmony Search (AGOHS)19 and Harmony Search
with Cuckoo Search (HSCS)20 Algorithms introduce enhancements that improve convergence and precision,
especially when integrated with BPNNs for clinical rule extraction. These advanced variants offer refined
optimization processes, allowing for more accurate and reliable rule extraction in complex clinical datasets. However, challenges persist, as these variants occasionally struggle to maintain an optimal balance between
exploration and exploitation during high-dimensional weight optimization in BPNNs, which can lead to
premature convergence or stagnation in local optima. Recent advancements in metaheuristic optimization algorithms have further improved the performance of
such methods in high-dimensional and complex optimization problems. For example, Adegboye and Deniz
Ülker21 proposed a hybrid artificial electric field algorithm that integrates cuckoo search with refraction
learning, demonstrating superior performance in engineering optimization problems. This approach leverages
the strengths of both cuckoo search and refraction learning to enhance exploration and exploitation capabilities,
particularly in high-dimensional spaces. The hybrid algorithm’s ability to dynamically adjust its search strategy
based on the problem’s fitness landscape makes it highly effective for complex optimization tasks, such as those
encountered in BPNN weight initialization. Similarly, Adegboye and Deniz Ülker22 introduced an improved
artificial electric field algorithm that incorporates Gaussian mutation and specular reflection learning with
a local escaping operator. This approach enhances the algorithm’s ability to escape local optima and explore
diverse regions of the search space, leading to improved convergence rates and solution quality. The integration
of Gaussian mutation and local escaping operators ensures that the algorithm maintains a balance between
exploration and exploitation, making it particularly suitable for high-dimensional optimization problems. These
advancements highlight the importance of hybrid and adaptive strategies in metaheuristic algorithms, which
can be effectively applied to optimize BPNN weights and improve the accuracy of WFPR extraction in CDSSs. HS is a metaheuristic optimization algorithm inspired by the process of musical improvisation. Since
its introduction by Geem, et al.23, HS has been widely applied to various optimization problems due to its
simplicity, flexibility, and effectiveness. Over the years, numerous variants of HS have been proposed to address
its limitations and improve its performance. The standard HS algorithm balances exploration and exploitation
through three key parameters: Harmony Memory Considering Rate (HMCR), Pitch Adjustment Rate
(PAR), and Bandwidth (bw). While effective for many problems, the standard HS has limitations in high-
dimensional and complex search spaces, where it may struggle with slow convergence and premature stagnation. Improved Harmony Search (IHS) Algorithm introduces dynamic adjustments to the PAR and bw parameters
to enhance the algorithm’s convergence speed and solution accuracy. By adaptively tuning these parameters, IHS improves the balance between exploration and exploitation, making it more effective than the standard
HS in many applications24. Global-Best Harmony Search (GHS) Algorithm incorporates information from
the global best solution to guide the search process. This approach enhances the algorithm’s ability to exploit
promising regions of the search space, leading to improved convergence and solution quality compared to the
standard HS25. Self-Adaptive Harmony Search (SAHS) Algorithm automates the adjustment of HS parameters
(HMCR, PAR, bw) based on the algorithm’s performance during the search process. This self-adaptive
mechanism reduces the need for manual parameter tuning and improves the algorithm’s robustness across
different problem domains26. Hybrid Harmony Search (HHS) Algorithm combines HS with other optimization
techniques, such as genetic algorithms, particle swarm optimization, or simulated annealing, to leverage the
strengths of multiple methods. These hybrid approaches often achieve better performance than the standard HS,
particularly in complex and high-dimensional problems27. Recent advancements in HS algorithm have focused on enhancing their performance through adaptive
parameter control, hybridization with machine learning techniques, and applications to real-world problems. For instance, a novel intelligent global harmony search algorithm based on dynamic parameter tuning has
been proposed, improving the algorithm’s ability to solve complex optimization problems28. The integration
of HS with machine learning techniques has been explored to enhance optimization efficiency. For example, a
Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

hybrid HS-Support Vector Machine (SVM) model has been proposed for feature selection and hyperparameter
tuning, demonstrating improved performance in credit scoring applications29. HS and its variants have also
been successfully employed in energy optimization. To illustrate, an improved version of HS called Equilibrium
Optimization-Based Harmony Search Algorithm with Nonlinear Dynamic Domains (EO-HS-NDD) has been
applied to optimize energy systems, demonstrating its effectiveness in managing complex energy distribution
networks30. These advancements highlight the versatility and robustness of HS algorithms in addressing diverse
and complex optimization tasks. However, despite these improvements, several gaps remain in the current
research on HS variants. These include challenges in high-dimensional optimization, exploration-exploitation
balance, robustness to noise and imbalanced data, and the need for stronger theoretical foundations. These gaps
highlight the necessity for more advanced HS variants, such as the Dynamic Dimension Adjustment Harmony
Search (DDA-HS) Algorithm, which is specifically designed to address these challenges through a dynamic
dimension adjustment mechanism and enhanced theoretical analysis. Building on these challenges, there is a critical need for an HS variant specifically tailored to high-
dimensional BPNN weight optimization, enhancing rule extraction accuracy in CDSSs. To address this, the
DDA-HS algorithm is introduced, designed for specialized optimization tasks like BPNN weight initialization. Traditional methods often struggle in high-dimensional spaces, leading to inefficient searches and suboptimal
convergence. DDA-HS employs a dynamic dimension adjustment mechanism that adapts the optimization
scope based on the fitness landscape. Our approach first conducts a Markov analysis on the basic HS, identifying
areas for enhancement in convergence behavior. Driven by this theoretical insight, DDA-HS refines HS’s
balance of exploration and exploitation, improving convergence speed and solution quality in high-dimensional
settings. Specifically designed for CDSS applications, DDA-HS, when integrated with BPNNs, achieves precise
rule extraction and enhances the reliability of the knowledge base. Utilizing WFPRs, this approach strengthens
diagnostic accuracy and interpretability, crucial for effective clinical support systems. The main contributions
of this paper are:
1)	 Markov analysis is applied to the standard HS, enabling the identification of specific areas for enhancement. This theoretical foundation informs the subsequent refinement of HS, leading to more efficient search strat­
egies and improved convergence properties.
2)	 DDA-HS is introduced, specifically designed with considerations from the No-Free-Lunch (NFL) Theorem. This design ensures that DDA-HS is particularly effective for high-dimensional BPNN weight optimiza­
tion, addressing the unique challenges presented by complex clinical datasets. By integrating DDA-HS with
BPNNs, precise rule extraction is achieved, which is critical for the reliability of CDSSs.
3)	 WFPRs are employed within the framework to enhance diagnostic accuracy and interpretability. This in­
tegration ensures that the generated knowledge/rule base is not only robust but also aligned with clinical
reasoning, ultimately improving the effectiveness of decision-making in medical settings. Materials and methods
HS
HS is a nature-inspired optimization algorithm modeled after the improvisational process in music. Known for
its simplicity, flexibility, and effectiveness, HS has gained widespread adoption in solving optimization problems. The algorithm mimics the process of musicians improvising to find the best harmony, which is analogous
to finding the optimal solution in an optimization problem. The key components and main steps of HS are
introduced. Key components of HS
1)	 Harmony Memory (HM): The HM stores a set of candidate solutions (harmonies), each representing a po­
tential solution to the optimization problem. The size of the HM is defined by the Harmony Memory Size
(HMS).
2)	 HMCR: The HMCR determines the probability of selecting a value from the HM for a new solution. A high HMCR value encourages exploitation of existing solutions, while a low HMCR value promotes
exploration of new solutions.
3)	 PAR: The PAR controls the probability of adjusting the selected value from the HM. This adjustment
is analogous to fine-tuning a musical pitch and helps the algorithm explore the local search space around
existing solutions.
4)	 bw: The bw defines the range within which the pitch adjustment occurs. A larger bw allows for broader
exploration, while a smaller bw focuses on fine-tuning the solution. Main steps of HS
The main steps of the standard HS are provided as follows:
1)	 initialization: the HM is initialized with random solutions within the search space
2)	 Improvisation: A new solution is generated by selecting values from the HM (based on HMCR) or ran­
domly generating new values. The selected values may be adjusted based on PAR and bw.
3)	 Update: If the new solution is better than the worst solution in the HM, it replaces the worst solution.
4)	 Termination: The algorithm repeats the improvisation and update steps until a stopping criterion (e.g., max­
imum iterations or convergence) is met. Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

The flowchart of the standard HS is provided, elucidating its operation in detail shown in Fig. 1. Strengths and limitations of HS
1)	 Strengths: HS is easy to implement and requires fewer parameters compared to other metaheuristic algo­
rithms, and it effectively balances exploration and exploitation, making it suitable for a wide range of opti­
mization problems31–33.
2)	 Limitations: In high-dimensional problems34, HS may struggle with slow convergence due to its fixed pa­
rameter settings. Moreover, the algorithm may get trapped in local optima, especially in complex and multi­
modal search spaces. Motivation for DDA-HS
The limitations of standard HS, particularly in high-dimensional and complex optimization problems, motivated
the development of the DDA-HS algorithm. By introducing a dynamic dimension adjustment mechanism, DDA-HS addresses these limitations and enhances the algorithm’s performance in challenging optimization
tasks. Following the background on HS, the DDA-HS algorithm is introduced, which builds upon the strengths
of HS while addressing its limitations. DDA-HS
In the context of optimization algorithms, particularly metaheuristic approaches like HS, understanding the
underlying behavior and convergence properties is crucial for enhancing both performance and reliability. One effective way to achieve this is through a theoretical analysis based on Markov processes35. By modeling
Fig. 1. Flowchart of HS. Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

the iterative steps of HS as a Markov chain, it becomes possible to assess the algorithm’s stochastic behavior,
convergence probability, and overall dynamics in a structured mathematical framework. This analysis not only
helps to understand how the algorithm explores the search space, but also provides insights into its development
mechanism to evaluate its convergence properties and provide a deeper theoretical understanding, ultimately
guiding the development of improved variants. HS theoretical analysis
HS’s optimization process can be modeled as an absorbing Markov chain. At each iteration, HS updates the
population of solutions, where the next state Xt+1 depends only on the current state Xt, following the
Markov property. Once the global optimal solution xopt appears in the population, it remains in all subsequent
populations, making it an absorbing state, which can be formally expressed as: P {xopt /∈Xt+1|xopt ∈Xt} = 0
(1)
Therefore, an absorbing Markov chain model with N states is proposed based on36, with state N as the absorbing
state representing optimal fitness, as illustrated in Fig. 2. The states are arranged from left to right according to
their fitness values. In a simplified scenario with a single individual in a one-dimensional problem, the transition
probability Pi→j indicates the likelihood of moving from state i to state j. Notably, each perturbation operation
either maintains the current state or advances it to the right, toward improved fitness. The transition probabilities can be categorized:
1)	 Self-transition
probability: The
probability
of
remaining
in
state
i
is
Pi→i = HMCR · PAR · 1/2 + HMCR · (1 −PAR) + (1 −HMCR) · i/N. It increases as the
algorithm approaches the absorbing state N, reflecting a risk of getting stuck in local optima due to incre­
mental adjustments in HS.
2)	 Forward-transition
probability: For
i < j ≤N, Pi→j = HMCR · PAR · 1/2 + (1 −HMCR) · (N −i)/N, indicating movement towards higher
fitness states. To improve global optimization, reducing Pi→i and increasing Pi→j helps the algorithm escape local optima
and explore better solutions. Additionally, the likelihood of finding the global optimal solution is crucial and can
be illustrated through probability analysis. In an N-dimensional problem with n possible values per dimension,
there are nN possible solutions, only one of which is optimal. To quantify the probability of discovering this
optimal solution, the probability ϵ is introduced, representing the minimum chance that a newly generated
individual, derived from existing individuals, will be optimal. The equation for ϵ is:
ϵ =
∑N
k=0Ck
N[(1 −HMCR) · 1/n]N−k[HMCR · PAR · 1/n]k > 0
(2)
Here, ϵ = P {xopt ∈Xt+1|xopt /∈Xt} indicates the probability that the optimal solution xopt enters the new
population Xt+1 given its absence in Xt. The equation captures the worst-case scenario, combining scenarios
of randomly selecting values in N −k dimensions and adjusting k dimensions from existing solutions. A
non-zero ϵ indicates a persistent, albeit small, chance of generating a new optimal solution in each iteration. Therefore, HS theoretically avoids getting trapped in local optima, maintaining a non-zero probability of
discovering the global optimal solution. Furthermore, the convergence of HS can be established by showing that, with sufficient iterations, the
algorithm will almost surely identify the optimal solution. Let P {xopt ∈Xt} denote the probability that the
optimal solution xopt is present in the population Xt at iteration t. The goal is to demonstrate that:
lim
t→∞P {xopt /∈Xt} = 0
(3)
This indicates that as t increases, the probability of xopt not being in Xt approaches 0. To prove this, the law
of total probability is applied: Fig. 2. Absorbing Markov chain model. Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

## P (A) = P (A|B) · P (B) + (A|¬ B) · P (¬ B)

(4)
Where A is the event xopt /∈Xt+1, B is xopt ∈Xt, and ¬ B is xopt /∈Xt. Thus, the probability
P {xopt /∈Xt+1} can be expressed in two cases:
1)	 xopt is in Xt but not in Xt+1. The probability for this scenario is P {xopt /∈Xt+1|xopt ∈Xt}, with
prior probability of P {xopt ∈Xt}.
2)	 xopt is not in Xt and remains absent in Xt+1. The probability for this scenario is P {xopt /∈Xt+1|xopt /∈Xt}, with the prior probability P {xopt /∈Xt}. Combining these cases yields: P {xopt /∈Xt+1} = P {xopt /∈Xt+1|xopt ∈Xt} · P {xopt ∈Xt} + P {xopt /∈Xt+1|xopt /∈Xt} · P {xopt /∈Xt}
(5)
Given that Eq. (1) and Eq. (2), it follows that 1 −ϵ = P {xopt /∈Xt+1|xopt /∈Xt}. Thus, Eq. (5) simplifies to: P {xopt /∈Xt+1} = 0 · P {xopt ∈Xt} + (1 −ϵ) · P {xopt /∈Xt} = (1 −ϵ) · P {xopt /∈Xt}
(6)
For t + n iterations, iterating this relationship yields: P {xopt /∈Xt+n} = (1 −ϵ)n · P {xopt /∈Xt}
(7)
As n →∞, (1 −ϵ)n →0, leading to:
lim
t→∞P {xopt /∈Xt} = 0
(8)
Consequently, with increasing iterations, the optimal solution xopt will almost certainly be present in Xt,
proving the convergence of HS. In summary, the Markov-based fundamental analysis of HS demonstrated that HS can theoretically discover
the optimal solution at any iteration. Furthermore, it was shown that given a sufficient number of iterations, HS is guaranteed to converge to the optimal solution. This theoretical analysis reinforces the robustness and
convergence properties of HS, confirming its ability to effectively navigate the search space. In addition, these
findings lay the groundwork for introducing an enhanced HS variant. Building on the guaranteed convergence
of HS, the proposed improvements aim to optimize performance by refining its efficiency and adaptability in
practical applications. Inspiration of HS
The feasible values for each decision variable are assumed to already exist within the HM, removing the need
for fine-tuning. After several iterations, only one decision variable per harmony remains suboptimal. Thus, the
HM is represented as:

## HM =



X1
X2... XHMS

=


x1

xopt

· · ·
xopt
n
xopt

x2

· · ·
xopt
n............
xopt

xopt

· · ·
xHMS
n


(9)
HS generates a new harmony Xnew by selecting values from the HM, where the probability that a given
dimension equals its optimal value is (HMS −1)/HMS. The probability of achieving optimal values across
all dimensions diminishes rapidly as the number of dimensions increases, denoted as (( HMS −1)/HMS)n. In contrast, a proposed method randomly selects a harmony from the HM and adjusts one dimension, giving
a probability of 1/n · (HMS −1)/HMS for achieving optimal values across all dimensions. As shown in
Fig. 3, the success rate of the HS method sharply declines as dimensionality increases, whereas the proposed
method’s performance remains more stable, outperforming HS in high-dimensional problems. This analysis
highlights that HS struggles with high-dimensional optimization, while the proposed method shows better
potential. Therefore, DDA-HS is proposed to leverage this insight. According to the NFL theorem, no algorithm is universally superior across all problem domains37. This
limitation highlights the necessity for a novel HS variant, specifically tailored to optimize BPNN initial
weights and improve the rule extraction in CDSSs. As a result, DDA-HS is introduced, specifically designed
for high-dimensional optimization challenges namely the initialization of weights in BPNNs. To be specific,
high-dimensional spaces often pose significant difficulties for traditional algorithms, leading to inefficient
search strategies and suboptimal convergence. DDA-HS addresses this by incorporating a dynamic dimension
adjustment mechanism, enabling the algorithm to adaptively adjust the number of dimensions optimized based
on the fitness landscape. The motivation for this advancement stems from the inherent strengths and weaknesses
of swarm intelligence methods38, such as HS. While these approaches balance exploration and exploitation
effectively in moderate-dimensional spaces, their performance degrades as dimensionality increases. DDA-
HS, through its adaptive adjustment mechanism, refines this balance, enhancing both convergence speed and
solution quality in high-dimensional settings. This improvement is particularly critical for tasks like BPNN
weight optimization, where dimensionality directly impacts the model’s training effectiveness. Once optimized, Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

BPNN is leveraged to extract WFPRs, constructing a reliable knowledge/rule base critical for CDSSs. The
introduction of DDA-HS thus represents a significant enhancement particularly for complex, high-dimensional
problems, positioning it as a more efficient and robust alternative for such challenges. Main steps of DDA-HS
The theoretical analysis of HS using Markov chains provided critical insights into the algorithm’s convergence
behavior and exploration-exploitation balance. HS was modeled as a Markov chain, and the transition
probabilities between states, which represent potential solutions in the search space, were analyzed39. This
analysis revealed two key aspects that directly influenced the design of DDA-HS. First, the self-transition
probability, which increases as the algorithm approaches the optimal solution, indicates a risk of getting stuck
in local optima due to incremental adjustments in HS. To address this, DDA-HS incorporates a dynamic
dimension adjustment mechanism that reduces the likelihood of self-transition by adaptively adjusting the
number of dimensions optimized based on the fitness landscape. Second, the forward-transition probability,
which governs the movement towards improved fitness states, was enhanced in DDA-HS to increase the
chances of escaping local optima and discovering the global optimum. This was achieved by refining the
balance between exploration and exploitation, allowing DDA-HS to focus on dimensions more likely to lead
to improved solutions. These insights from the Markov chain analysis directly influenced key design aspects
of DDA-HS, including its dynamic dimension adjustment mechanism, fitness-based dimension selection, and
cyclic dimension adjustment strategy, ensuring robust performance in high-dimensional and complex search
spaces. The specific steps of DDA-HS are as follows:
1)	 fitness standardization: Z-score standardization is applied to normalize the fitness values
fi =
fi −µ f
/σ f
(10)
Where fi represents the fitness of individual i, and µ f and σ f denote the mean and standard deviation of the
population’s fitness values, respectively.
2)	 Fitness normalization: Standardized fitness is normalized to [0, 1].
fi =
fi −min
f
max
f
−min
f

(11)
3)	 Dimension adjustment count calculation: Each individual’s dimension adjustment count Di is determined
based on fitness. Fig. 3. Success rate comparison. Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

Di = Dmin + fi · (Dmax −Dmin)
(12)
Where Dmin and Dmax are the predefined minimum and maximum number of dimensions to be adjusted. The resulting Di value is rounded to the nearest integer.
4)	 Dimension selection and adjustment: A cyclic approach selects dimensions based on Di, from start, ini­
tially set to 0, to end, calculated as:
end = (start + Di) %V 
(13)
Where V is the total number of dimensions. If end is less than start, the indices wrap around, and the selected
dimensions are given by:
indices =
{ {start,..., V −1} ∪{0,..., end −1}, if end < start
{start,..., end −1},
otherwise

(14)
Once the dimensions are selected, the adjustment process begins. For HMCR of the cases, the adjustment
follows this rule:
x(t+1)
i
= x(t)
i
+ 0.7 · r1 ·
(
xbest −x(t)
i
)
+ 0.3 · r2 · (x(t)
i
−xworst)
(15)
Where r1 and r2 are random numbers in [0, 1], and xbest and xworst represent the best and worst individuals,
respectively. The traditional PAR mechanism is removed, relying solely on HMCR. For the remaining
1 −HMCR cases, Levy flight is used to explore new regions of the solution space with the update rule:
x(t+1)
i
= r3 · (xbest + xworst) −xbest+ △
(16)
Where r3 is a random number in [0, 1], and △ represents the Levy flight step. start for the next individual is
updated after the dimension adjustments:
start ←end
(17)
5)	 Fitness evaluation and update: If the new fitness improves:
f (t+1)
i
< f (t)
i

(18)
the individual is updated. This process iteratively drives convergence by dynamically adjusting dimensions based
on fitness, improving solution diversity and performance. PIMA dataset preprocessing
The PIMA dataset, containing 768 records with 8 feature attributes and a binary classification label, underwent
key preprocessing steps:
1)	 Data import and formatting: The dataset was divided into feature data (first 8 columns) and classification
labels (last column).
2)	 Fuzzy k-means clustering: Each feature column was clustered into 3 groups. This process resulted in a mem­
bership matrix U of size 768 × 3 for each feature. Each element ui,j in U represents the degree of mem­
bership of data point xi to cluster j, with normalization ensuring that the sum of memberships for each
data point equals 1:










## U =



u1,1
u1,2
u1,3
u2,1
u2,2
u2,3.........
u768,1
u768,2
u768,3


∑3
j=1ui,j = 1, for i = 1,2,..., 768

(19)
3)	 Cluster center update: Cluster centers C = [c1, c2, c3] were iteratively updated using the weighted average
equation:
cj =
∑768
i=1(ui,j)m · xi/
∑768
i=1(ui,j)m, for j = 1,2, 3
(20)
Here, m is the fuzzification factor (typically m = 2), and xi is the feature value of data point i. This ensures
that cluster centers are adjusted toward data points with higher membership degrees.
4)	 Distance calculation and membership update: The Euclidean distance di,j between each data point xi and
cluster center cj was calculated: Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

di,j = ∥xi −cj∥
(21)
A distance matrix D of size 768 × 3 was formed:

## D =



d1,1
d1,2
d1,3
d2,1
d2,2
d2,3.........
d768,1
d768,2
d768,3


(22)
The membership values were updated using:
ui,j = 1/
∑3
k=1(di,j/di,k)(2/(m−1)), for i = 1,2,..., 768; j = 1,2, 3
(23)
This process was repeated until convergence, defined by:
max
i,j
ucurrent
i,j
−uprevious
i,j
< ϵ
(24)
with ϵ = 0.0000001 as the convergence threshold.
5)	 One-hot encoding of labels: The binary classification labels ( 1 for diabetic and 0 for non-diabetic) were
converted into one-hot encoded vectors. For diabetic samples, the one-hot encoding was [1, 0], and for
non-diabetic samples, it was [0, 1]. After fuzzy k-means clustering, the resulting membership matrices from each feature were combined into a final
matrix of size 768 × 24, reflecting the membership values for 3 clusters across the 8 features. The classification
labels were transformed into a one-hot encoded format (768 × 2). BPNN workflow
1)	 Data partitioning and normalization: The preprocessed PIMA dataset is randomly partitioned into training
(75%) and testing (25%) subsets, ensuring representativeness and reducing bias in the evaluation. This
results in 576 training samples and 192 testing samples. Subsequently, normalization is applied to both sets,
transforming each 24-dimensional vector x into a unit norm. For a feature vector x = [x1, x2,..., x24],
the Euclidean norm ( L2 norm) is computed as:
∥x∥2 =
√∑24
i=1x2
i 
(25)
The normalized vector
∼x is obtained by:
∼x= x/∥x∥2
(26)
Thus, each normalized vector satisfies:
∥
∼x ∥2 = 1
(27)
The normalized input matrix
∼
X, containing 768 samples characterized by 24 fuzzy attributes from fuzzy
k-means clustering, is represented as:
∼
X=


∼x1,1
∼x1,2
· · ·
∼x1,24
∼x2,1
∼x2,2
· · ·
∼x2,24............
∼x768,1
∼x768,2
· · ·
∼x768,24

,
∼

## X∈R768× 24

(28)
Here,
∼xi,j represents the normalized value of the j-th fuzzy attribute for the i-th sample.
2)	 Hyperparameter configuration: BPNN is configured with essential hyperparameters to optimize perfor­
mance. The input layer contains 24 neurons for the 24-dimensional feature vectors, while the output layer
has 2 neurons for binary classification. An empirical choice of 4 neurons is made for the hidden layer to
balance complexity and computational efficiency. Moreover, the performance of BPNN is highly dependent
on the choice of hyperparameters, such as the learning rate, regularization coefficient, batch size, and the
number of training epochs. To optimize the model, extensive experiments were conducted to determine the
most effective hyperparameter settings. The learning rate (η ) was set to 0.008 after testing values ranging
from 0.005 to 0.1, as this value provided the best balance between convergence speed and stability. A
regularization coefficient (λ ) of 0.001 was chosen to prevent overfitting without overly restricting the
Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

model’s ability to learn complex patterns. For efficient training, a batch size of 128 was selected, as it offered
a good trade-off between computational efficiency and training stability. The model was trained for 100
epochs, with each epoch comprising 5000 iterations, ensuring sufficient convergence without overfitting. These hyperparameter settings were determined through systematic experimentation, demonstrating the
robustness of the proposed method within a reasonable range of values. For instance, higher learning rates
(e.g., 0.05) led to unstable training, while smaller batch sizes (e.g., 16) introduced noise into the gradient
updates. The final configuration, namely η = 0.008, λ = 0.001, batch size = 128, epoch = 100, and
iteration = 5000, provided the best balance between model performance and computational efficiency.
3)	 BPNN construction: BPNN is constructed with an input layer, hidden layer, and output layer. It is trained
exclusively on the training set
∼
Xtraining, learning relationships between input fuzzy attributes and output
classifications.
∼
Xtraining =


∼x1,1
∼x1,2
· · ·
∼x1,24
∼x2,1
∼x2,2
· · ·
∼x2,24............
∼x576,1
∼x576,2
· · ·
∼x576,24

,
∼

## X∈R576× 24

(29)
The network’s weights are initialized using DDA-HS, generating a weight vector w divided into input-to-hidden
weights Wih and the hidden-to-output weights Who. The weight vector contains 104 elements structured as:
w =
[
w(ih)
1,1, w(ih)
1,2,..., w(ih)
24,4, w(ho)
1,1, w(ho)
1,2,..., w(ho)
4,2
], w ∈R24× 4+4× 2
(30)
The input-to-hidden weight matrix Wih is defined as: Wih =


w(ih)
1,1
w(ih)
1,2
· · ·
w(ih)
1,4
w(ih)
2,1
w(ih)
2,2
· · ·
w(ih)
2,4............
w(ih)
24,1
w(ih)
24,2
· · ·
w(ih)
24,4

, Wih ∈R24× 4
(31)
The hidden-to-output weight matrix Who is defined as: Who =


w(ho)
1,1
w(ho)
1,2
w(ho)
2,1
w(ho)
2,2
w(ho)
3,1
w(ho)
3,2
w(ho)
4,1
w(ho)
4,2

, Who ∈R4× 2
(32)
4)	 BPNN training: The training employs mini-batch gradient descent, processing each batch in a single iter­
ation. Forward propagation computes predicted outputs, while backpropagation updates weights based on
the loss function gradient. In forward propagation, the hidden layer’s output is computed using the sigmoid
activation function: H = σ (
∼
Xtraining · Wih)
(33)
Where H denotes the hidden layer output, and σ (z) = 1/(1 + exp(−z )) is applied elementwise. The output
layer activation O is calculated as: O = σ (H · Who)
(34)
In backpropagation, the error at the output layer is computed and propagated back to adjust weights. The Mean
Squared Error (MSE) measures the difference between true labels yi and predicted outputs yi:

## MSE = 1/N ·

N
i=1(yi −yi)2
(35)
Where N = 576 for the training set. The total loss function incorporates MSE and L1 regularization: Loss = MSE + λ · ∥w∥1
(36)
The L1 norm of ∥w∥1 is defined as:
∥w∥1 = ∥Wih∥1 + ∥Who∥1 =
∑104
i=1 |wi|
(37)
Once Loss is calculated, weights are updated to minimize it: Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

{ Wih ←Wih −η · ∂Loss/∂Wih
Who ←Who −η · ∂Loss/∂Who 
(38)
5)	 BPNN evaluation: BPNN is evaluated on both the training and testing datasets to assess its generalization
and learning effectiveness, which produces output matrices Otraining ∈R576× 2 and Otesting ∈R192× 2, where each element oi,j represents the raw output for sample i and class j. These outputs are converted to
class probabilities using the softmax function:
∼oi,j = exp (oi,j) /
∑2
k=1exp (oi,k), for i = 1,2,..., N; j = 1,2
(39)
Here N = 576 for training and N = 192 for testing. This ensures the sum of probabilities for each sample
equals 1. The normalized probability matrices are:



























∼
Otraining =


∼o1,1
∼o1,2
∼o2,1
∼o2,2......
∼o576,1
∼o576,2


∼
Otesting =


∼o1,1
∼o1,2
∼o2,1
∼o2,2......
∼o192,1
∼o192,2



(40)
True labels are stored in one-hot encoded matrices Ytraining ∈R576× 2 and Ytesting ∈R192× 2, where each
row represents the class label: Yi =
{ [ 1
0 ], if j = 1 (diabetic)
[ 0
1 ], if j = 2 (non −diabetic) 
(41)
For each sample i, the predicted class yi is the index of the highest probability:
yi = argmax
j
∼oi,j, for i = 1,2,..., N
(42)
The true class yi is similarly determined from the one-hot encoded labels. Accuracy is computed by comparing
the predicted and true class indices: Accuracytraining = 1/576 ·  576
i=11 (yi = yi)
Accuracytesting = 1/192 ·  192
i=11 (yi = yi)

(43)
Here 1 (yi = yi) is an indicator function that equals 1 if the predicted class matches the true class. WFPR extraction
1)	 Weight pruning: Elements in the weight matrices W ∗
ih and W ∗
ho are set to 0 if their absolute values are less
than or equal to 0.5 after BPNN training. The pruned matrix
∼
W
∗
ih is:
∼
W
∗
ih =


∼w
(ih,∗)
1,1
∼w
(ih,∗)
1,2
· · ·
∼w
(ih,∗)
1,4
∼w
(ih,∗)
2,1
∼w
(ih,∗)
2,2
· · ·
∼w
(ih,∗)
2,4............
∼w
(ih,∗)
24,1
∼w
(ih,∗)
24,2
· · ·
∼w
(ih,∗)
24,4



(44)
Where each element
∼w
(ih,∗)
i,j
= 0, if
w(ih,∗)
i,j
≤0.5; otherwise, it remains its value. Similarly, the pruned
matrix
∼
W
∗
ho is:
∼
W
∗
ho =


∼w
(ho,∗)
1,1
∼w
(ho,∗)
1,2
∼w
(ho,∗)
2,1
∼w
(ho,∗)
2,2
∼w
(ho,∗)
3,1
∼w
(ho,∗)
3,2
∼w
(ho,∗)
4,1
∼w
(ho,∗)
4,2


(45)
Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

Where
∼w
(ho,∗)
i,j
= 0 if
w(ho,∗)
i,j
≤0.5; otherwise, it retains its value. These pruned matrices represent the
simplified layer connections, removing smaller, less significant weights to streamline BPNN.
2)	 Acquisition of the weighted matrix: The new weighted matrix Wio, representing the relationship between
input and output layers, is obtained by taking the dot product of the pruned weight matrices
∼
W
∗
ih and
∼
W
∗
ho: Wio =
( ∼
W
∗
ih ·
∼
W
∗
ho
)T

(46)
The dot product results in a R24× 2 matrix, which is transposed to yield Wio ∈R2× 24, aligning it for
subsequent steps.
3)	 Preprocessing of the weighted matrix: The weighted matrix Wio (2 × 24) represents the contribution of
each input fuzzy attribute to the output classes. To facilitate rule extraction, each element is rounded to 2
decimal places:
∼w
(io)
i,j = round
(
w(io)
i,j, 2
)

(47)
The preprocessed matrix
∼
W io is:
∼
W io =
[
∼w
(io)
1,1
∼w
(io)
1,2
· · ·
∼w
(io)
1,24
∼w
(io)
2,1
∼w
(io)
2,2
· · ·
∼w
(io)
2,24
]

(48)
The input features A1, A2,..., A8 each have 3 fuzzy attributes An: {An,1, An,2, An,3}, and the output
classes C1 (diabetic) and C2 (non −diabetic) are linked to the fuzzy attributes. Thus, the matrix can be
expressed as:
∼
W io =
[
∼w
(io)
C1, A1,1
∼w
(io)
C1, A1,2
∼w
(io)
C1, A1,3
· · ·
∼w
(io)
C1, A8,3
∼w
(io)
C2, A1,1
∼w
(io)
C2, A1,2
∼w
(io)
C2, A1,3
· · ·
∼w
(io)
C2, A8,3
]

(49)
4)	 WFPR construction: A general WFPR for Class i is: IF Condition1 AND Condition2 AND · · · AND Condition8 THEN Class i
(50)
Each condition links an input feature to its fuzzy attributes, reflecting their contribution to the output class. For
example, a specific WFPR for Class 1 might be: IF A1 is A1,1
∼w
(io)
C1, A1,1
AND A4 is NOT A4,2
∼w
(io)
C1, A4,2
THEN Class 1
(51)
Here, An represent input features with 3 fuzzy attributes An,k. Positive contributions to a class are written
as An is An,k
∼w
(io)
Ci, An,k, while negative contributions are expressed as An is NOT An,k
∼w
(io)
Ci, An,k, where
∼w
(io)
Ci, An,k is the rounded weight value. In constructing WFPRs, only one non-zero fuzzy attribute per
feature is selected. If a feature has no non-zero attributes, it is skipped. The number of possible rules is based
on the non-zero fuzzy attributes of each feature, with a maximum of 38 = 6561 rules if all fuzzy attributes are
non-zero. If all fuzzy attributes are 0, no rules are generated. The total number of rules Ri for each output class
Class i is: Ri =
∏8
n=1nz (An)
(52)
Where nz (An) is the number of non-zero fuzzy attributes for feature An. The total number of WFPRs is:

## R =

∑2
i=1Ri
(53)
5)	 Confidence calculation: For each classification category Ci, a fuzzy rule r is formed by selecting one non-ze­
ro fuzzy weight
∼w
(io)
Ci, An,k from the fuzzy sets of each feature n ( 8 total). The confidence of a rule CF r is
calculated as: Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

CF r =

n=1






∼w
(io)
Ci, An,k
 ·

1 −
∼xAn,k
, if
∼w
(io)
Ci, An,k < 0
∼w
(io)
Ci, An,k ·
∼xAn,k,
otherwise


(54)
Where
∼xAn,k is the fuzzy membership value. If the weight is negative, the contribution is adjusted by subtracting
the membership value from 1. The total confidence CF Ci for category Ci is: CF Ci =
∑
r∈RCi
CF r
(55)
Only rules with CF r ≥0.5 are considered. For such rules: CF Ci =
r∈RCi

n=1






∼w
(io)
Ci, An,k
 ·

1 −
∼xAn,k

−0.5, if
∼w
(io)
Ci, An,k < 0
∼w
(io)
Ci, An,k ·
∼xAn,k −0.5,
otherwise


(56)
6)	 Effectiveness evaluation: Once the confidence for each data instance and category is calculated, the resulting
matrix is represented as:

## CF =




## CF (1)

## CF (1)

## CF (2)

## CF (2)......

## CF (N)

## CF (N)



(57)
Where N = 576 for the training set and N = 192 for the testing set. Each row represents the confidence values
for 2 classification categories, derived from the respective fuzzy rules. The category with the highest confidence
value determines the predicted class: If CF (N)

## > CF (N), the data instance is classified as Class 1; otherwise,
it is classified as Class 2. The accuracy for both the training and testing datasets is computed: Accuracytraining = 1/576 ·  576
i=11 (yi = yi)
Accuracytesting = 1/192 ·  192
i=11 (yi = yi)

(58)
Here, yi is the predicted class, yi is the true class, and 1 (yi = yi) is an indicator function that equals 1 if they
are the same. Experimental setup
The experiment is designed to evaluate the performance of DDA-HS against four algorithms: HS, Cuckoo Search
(CS), AGOHS, and HSCS algorithms. The parameter settings for each algorithm are listed in Table 1. Each
algorithm runs 30 times to account for stochastic variability. The experiment was conducted on a 2.3 GHz
quad-core Intel Core i5 processor with 8 GB RAM, using Python 3.7. The target function E (w) represents the total error of BPNN for a given set of weights w on the PIMA
training dataset. This objective function aims to minimize prediction error on the training set while incorporating
a regularization term to prevent overfitting. Its specific equation is: E (w) = 1/2 ·
N
i=1(yi −yi)2 + λ ·
M
j=1 |wj|
(59)
Here, yi and yi are the actual and predicted outputs for instance i, respectively. The regularization coefficient
λ is set at 0.001, and wj denotes the individual weight of BPNN. The number of training instances N is 576, and the total number of weights M is 104. Algorithm
Parameter setting
HS
HMS = 20, HMCR = 0.9, P AR = 0.7, bw = 0.01, Tmax = 100
CS
HMS = 20, α = 0.01, Pa = 0.25, λ = 1.5, Tmax = 100
AGOHS
HMS = 20, HMCRmin = 0.8, HMCRmax = 0.9, P ARmin = 0.1, P ARmax = 0.9, F = N (0.5, 0.3), Tmax = 100
HSCS
HMS = 20, HMCRmin = 0.8, HMCRmax = 0.9, P ARmin = 0.1, P ARmax = 0.9, α 0 = 0.01, Tmax = 100
DDA-HS
HMS = 20, HMCR = 0.95, Dmin = 8, Dmax = 52, Tmax = 100
Table 1. Parameter settings of the experimental algorithm. Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

Results
Quantitative analysis
The convergence curve in Fig. 4 shows the average fitness values over 100 iterations for 30 runs of the algorithms. DDA-HS exhibits a consistently faster convergence rate and achieves a lower final fitness value, indicating its
effective management of the exploration-exploitation trade-off for quick convergence to high-quality solutions. In contrast, other algorithms, particularly HS, display slower declines in fitness and higher final fitness values. Table 2 Provides quantitative results, revealing that DDA-HS has the best mean fitness of 1.03e + 02, significantly outperforming HS’s mean of 1.23e + 02. However, DDA-HS has a standard deviation of
6.68e + 00, suggesting more variability across runs. The median fitness for DDA-HS also stands at 1.03e + 02,
confirming its superior performance. While its worst fitness value of 1.16e + 02 is not the lowest as CS achieves
1.14e + 02, DDA-HS excels with a best-case fitness of 8.94e + 01. Furthermore, statistical significance of
performance differences was assessed using the Wilcoxon signed-rank test, yielding P-values consistently below
0.05 (e.g., 1.27e −10 for HS, 7.49e −04 for CS), indicating that DDA-HS significantly outperforms the
competing algorithms. All comparisons are marked with a ′ + ′ sign. DDA-HS proves to be a more effective optimization technique than standard HS and CS, and hybrid
variants namely AGOHS and HSCS. In contrast, slower convergence rates in HS, CS, AGOHS, and HSCS
result in suboptimal solutions, as reflected in both the convergence curve and statistical analysis. Overall, DDA-HS demonstrates superior accuracy, convergence speed, and robustness, validating its efficacy for
high-dimensional optimization tasks, such as in BPNN weight optimization. In addition, the proposed DDA-HS algorithm demonstrates superior performance compared to other
optimization methods, particularly in terms of convergence speed and solution accuracy. DDA-HS
dynamically adjusts the number of dimensions optimized based on the fitness landscape, allowing it
to focus on the most promising dimensions and significantly reduce the search space. This mechanism
accelerates convergence, especially in high-dimensional problems where standard HS and its variants (e.g., AGOHS, HSCS) struggle due to fixed search strategies. Additionally, DDA-HS refines the balance between
Algorithm
Dim
Mean
Std
Median
Worst
Best
P value
Sign
HS

1.23e + 02
6.22e + 00
1.25e + 02
1.35e + 02
1.11e + 02
1.27e −10
+
CS

1.08e + 02
3.28e + 00
1.08e + 02
1.14e + 02
1.01e + 02
7.49e −04
+
AGOHS

1.20e + 02
4.52e + 00
1.21e + 02
1.28e + 02
1.09e + 02
2.05e −10
+
HSCS

1.14e + 02
6.18e + 00
1.16e + 02
1.24e + 02
1.00e + 02
4.28e −07
+
DDA-HS

1.03e + 02
6.68e + 00
1.03e + 02
1.16e + 02
8.94e + 01
NA
NA
Table 2. Comparison of error fitness results. Significant values are in bold. Fig. 4. Error fitness mean convergence curves. Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

exploration and exploitation by adaptively adjusting the search scope, ensuring efficient exploration of
the search space while exploiting promising regions. This adaptability enables DDA-HS to escape local
optima and achieve higher solution accuracy, even in complex datasets with multiple local optima or non-
linear relationships. Furthermore, DDA-HS excels in handling imbalanced and noisy datasets, such as
medical datasets with high noise levels or imbalanced classes, by prioritizing relevant features and avoiding
overfitting. In contrast, HS, CS, and their variants often rely on random or heuristic-based adjustments,
which can lead to suboptimal solutions. Overall, DDA-HS’s robustness and adaptability make it highly
effective across a wide range of problem complexities, from low-dimensional to high-dimensional datasets,
and in scenarios involving non-linear relationships or noisy data. BPNN and WFPR classification accuracy
Table 3 Presents the classification accuracy of BPNN and WFPRs across different optimization methods. For
BPNN, the unoptimized BPNN achieved 77.78% training accuracy and 71.88% testing accuracy. Among
the optimized models, AGOHS attained the highest training accuracy (79.17%), yet its testing accuracy
(71.35%) showed limited improvement, suggesting overfitting. HSCS, on the other hand, exhibited more
balanced performance with a testing accuracy of 76.04%, outperforming other methods on unseen data. DDA-HS achieved 74.48% testing accuracy, surpassing HS, CS and AGOHS, while maintaining a solid
78.30% training accuracy, indicating effective training stabilization without overfitting. For WFPRs,
the BPNN model optimized by DDA-HS achieved the highest performance, with a training accuracy of
79.51% and a testing accuracy of 77.08%, indicating an effective balance between BPNN complexity and
generalization. In contrast, HSCS showed robust performance with a testing accuracy of 76.56%, although
its training accuracy of 77.95% was lower than that of DDA-HS. The unoptimized BPNN exhibited a
significant gap between training (76.22%) and testing accuracy (72.40%), underscoring its inefficiency
in capturing complex data patterns. Both HS and CS yielded moderate improvements, with HS achieving
a testing accuracy of 73.96% and CS slightly higher at 75.00%, reflecting limited enhancements over the
unoptimized BPNN. Generated WFPRs
WFPR extraction from the weighted matrix
∼
W io, is vital for understanding BPNN’s decision-making process
and improving its interpretability. This matrix summarizes the influence of input features on output classes,
with each weight reflecting a feature’s importance in determining the outcome:
∼
W io =
[ −0.69

8.1
−22.54

2.59

8.55

−2.89
−4.68

3.39
−5.12

−7.9

−2.52

−8.33

2.82
4.56

−3.31
4.98
]

(60)
WFPR extraction involves constructing logical rules from significant weights in the matrix. These rules follow
an IF Condition THEN Class format. From the matrix, 8 rules for each class are derived as WFPRs for
Class 1 (diabetic) and Class 2 (non −diabetic) ( 16 in total), as illustrated in Table 4. By extracting interpretable rules, clinicians gain insights into the relationships between features and diabetes
classification, fostering trust and facilitating informed decision-making in clinical contexts. Specifically, the
interpretability of WFPRs is a key advantage in CDSSs, as it allows clinicians to understand and act upon the
model’s predictions. For example, a WFPR extracted from the PIMA dataset might state: IF Glucose is High
[Weight: 8.1] AND BMI is High [Weight: 8.55] AND Diabetes Pedigree Function is NOT Low [Weight: 2.89], THEN Class 1 (Diabetic). This rule highlights the importance of elevated glucose and BMI levels, along with
a family history of diabetes, in predicting diabetes risk. Clinicians can use such rules to prioritize diagnostic
testing and early interventions for high-risk patients. Conversely, another WFPR might classify a patient as non-
diabetic based on normal glucose levels, such as IF Glucose is NOT High [Weight: 7.9] AND BMI is NOT High
[Weight: 8.33] AND Diabetes Pedigree Function is Low [Weight: 2.82], THEN Class 2 (Non-Diabetic), helping to
optimize screening resources by identifying low-risk individuals. The adaptability of fuzzy cluster thresholds
(e.g., Low, Medium, High) ensures that WFPRs remain clinically relevant across different healthcare settings. For instance, glucose level categories can be adjusted according to updated diagnostic criteria. By providing
transparent, interpretable rules, WFPRs enhance CDSSs by supporting personalized treatment decisions,
reducing unnecessary testing, and improving overall diagnostic accuracy. Method
Training (BPNN)
Testing (BPNN)
Training (WFPRs)
Testing (WFPRs)
Unoptimized BPNN
77.78
71.88
76.22
72.40
BPNN optimized by HS
78.30
71.88
77.43
73.96
BPNN optimized by CS
77.95
72.40
76.91
75.00
BPNN optimized by AGOHS
79.17
71.35
76.56
73.96
BPNN optimized by HSCS
77.26
76.04
77.95
76.56
BPNN optimized by DDA-HS
78.30
74.48
79.51
77.08
Table 3. Classification accuracy of BPNN and WFPRs. Significant values are in bold. Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

Discussion
The transition from IF-THEN rules to WFPRs marks a significant advancement in the development of
CDSSs. IF-THEN rules have long served as the foundation, providing a straightforward framework for
encoding medical expertise and guiding clinical decisions40. These rules rely on binary logic, where specific
conditions lead to definitive outcomes. While such rules are effective in simple, well-defined cases, they
often fail to capture the complexity and ambiguity inherent in medical data. For example, fever or pain
often exist on a continuum, and the relationships between medical conditions are highly non-linear and
context dependent. To overcome this issue, WFPRs offer a solution to these limitations by combining fuzzy
logic with rule weighting. Fuzzy logic allows for a more flexible interpretation of clinical data, representing
conditions along a spectrum rather than as binary states41. This nuanced representation more closely
mirrors the clinical reasoning of healthcare professionals. Moreover, the integration of weights into fuzzy
rules enables a dynamic prioritization of rules based on their relevance, reliability, or confidence level. This weighting mechanism ensures that rules of higher clinical significance exert a greater influence on
decision-making processes. WFPRs have proven to be effective in several CDSS applications, particularly in scenarios requiring the
simultaneous evaluation of multiple diagnostic factors. Their probabilistic framework enables CDSSs to provide
diagnoses accompanied by confidence levels, offering a significant advantage in complex clinical situations. This probabilistic approach allows clinicians to assess not only the likelihood of a diagnosis but also the level
of certainty attached to the system’s recommendations42. This capability is particularly valuable in complex or
ambiguous cases, where traditional rules might struggle to account for overlapping symptoms or uncertain
data. By enhancing the flexibility and granularity of decision-making, WFPRs have demonstrated significant
potential in improving diagnostic accuracy and reliability within CDSSs, ultimately contributing to better
patient outcomes. The quality of initial weights in BPNN is a crucial factor. Recent research emphasizes the importance of
weight optimization strategies43, proposing various techniques such as metaheuristic algorithms, which enhance
the initial weight distribution and improve overall convergence rates44. One such approach is the use of HS and
its variants, which have proven effective in optimizing BPNN weights for improved classification accuracy in
CDSSs45. As a result, BPNN is increasingly applied in WFPR extraction. The capacity to process and learn from
large and complex datasets makes it well-suited for identifying subtle and intricate relationships in medical
data. Unlike traditional rule extraction methods that rely heavily on expert knowledge, BPNN provides a data-
driven, automated approach to rule learning, reducing human bias and enhancing the objectivity of the derived
rules46. Therefore, it is possible to derive fuzzy rules that are interpretable and clinically relevant. These fuzzy
rules, grounded in fuzzy logic principles, allow the system to account for the inherent uncertainty and ambiguity
present in medical data, thus improving decision-making in uncertain environments. HS is a metaheuristic optimization technique inspired by the improvisation process in musical
performances. This analogy forms a framework, ideal for neural network weight optimization47. When
applied to BPNN weight initialization, HS explores the weight space to identify near-optimal configurations
No. WFPRs

IF A1 is NOT A1,1 [0.69]AND A2 is A2,1 [8.1]AND A4 is A4,2 [2.59]AND A6 is A6,1 [8.55]AND A7 is NOT A7,1 [2.89]AND A8 is A8,2 [3.39]
THEN Class 1

IF A1 is NOT A1,1 [0.69]AND A2 is A2,1 [8.1]AND A4 is A4,2 [2.59]AND A6 is A6,1 [8.55]AND A7 is NOT A7,1 [2.89]AND A8 is NOT A8,3
[5.12]THEN Class 1

IF A1 is NOT A1,1 [0.69]AND A2 is A2,1 [8.1]AND A4 is A4,2 [2.59]AND A6 is A6,1 [8.55]AND A7 is NOT A7,2 [4.68]AND A8 is A8,2 [3.39]
THEN Class 1

IF A1 is NOT A1,1 [0.69]AND A2 is A2,1 [8.1]AND A4 is A4,2 [2.59]AND A6 is A6,1 [8.55]AND A7 is NOT A7,2 [4.68]AND A8 is NOT A8,3
[5.12]THEN Class 1

IF A1 is NOT A1,1 [0.69]AND A2 is NOT A2,2 [22.54]AND A4 is A4,2 [2.59]AND A6 is A6,1 [8.55]AND A7 is NOT A7,1 [2.89]AND A8 is A8,2
[3.39]THEN Class 1

IF A1 is NOT A1,1 [0.69]AND A2 is NOT A2,2 [22.54]AND A4 is A4,2 [2.59]AND A6 is A6,1 [8.55]AND A7 is NOT A7,1 [2.89]AND A8 is
NOT A8,3 [5.12]THEN Class 1

IF A1 is NOT A1,1 [0.69]AND A2 is NOT A2,2 [22.54]AND A4 is A4,2 [2.59]AND A6 is A6,1 [8.55]AND A7 is NOT A7,2 [4.68]AND A8 is A8,2
[3.39]THEN Class 1

IF A1 is NOT A1,1 [0.69]AND A2 is NOT A2,2 [22.54]AND A4 is A4,2 [2.59]AND A6 is A6,1 [8.55]AND A7 is NOT A7,2 [4.68]AND A8 is
NOT A8,3 [5.12]THEN Class 1

IF A2 is NOT A2,1 [7.9]AND A4 is NOT A4,2 [2.52]AND A6 is NOT A6,1 [8.33]AND A7 is A7,1 [2.82]AND A8 is NOT A8,2 [3.31]THEN Class 2

IF A2 is NOT A2,1 [7.9]AND A4 is NOT A4,2 [2.52]AND A6 is NOT A6,1 [8.33]AND A7 is A7,1 [2.82]AND A8 is A8,3 [4.98]THEN Class 2

IF A2 is NOT A2,1 [7.9]AND A4 is NOT A4,2 [2.52]AND A6 is NOT A6,1 [8.33]AND A7 is A7,2 [4.56]AND A8 is NOT A8,2 [3.31]THEN Class 2

IF A2 is NOT A2,1 [7.9]AND A4 is NOT A4,2 [2.52]AND A6 is NOT A6,1 [8.33]AND A7 is A7,2 [4.56]AND A8 is A8,3 [4.98]THEN Class 2

IF A2 is A2,2 [23]AND A4 is NOT A4,2 [2.52]AND A6 is NOT A6,1 [8.33]AND A7 is A7,1 [2.82]AND A8 is NOT A8,2 [3.31]THEN Class 2

IF A2 is A2,2 [23]AND A4 is NOT A4,2 [2.52]AND A6 is NOT A6,1 [8.33]AND A7 is A7,1 [2.82]AND A8 is A8,3 [4.98]THEN Class 2

IF A2 is A2,2 [23]AND A4 is NOT A4,2 [2.52]AND A6 is NOT A6,1 [8.33]AND A7 is A7,2 [4.56]AND A8 is NOT A8,2 [3.31]THEN Class 2

IF A2 is A2,2 [23]AND A4 is NOT A4,2 [2.52]AND A6 is NOT A6,1 [8.33]AND A7 is A7,2 [4.56]AND A8 is A8,3 [4.98]THEN Class 2
Table 4. WFPRs for Class 1 (diabetic) and Class 2 (non −diabetic). Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

that lead to improved convergence during the training phase. Meanwhile, HS iteratively searches the weight
space and retains promising weight sets, which is particularly beneficial in BPNN, as better initial weights
significantly enhance the network’s ability to quickly converge to an accurate solution. Early studies have
shown that HS outperforms traditional random or heuristic-based initialization methods in neural network
training, leading to faster learning and improved classification accuracy48. Moreover, recent innovations in
HS have refined its effectiveness by incorporating dynamic parameter adjustments to balance exploration
and exploitation throughout the optimization process, and the introduction of advanced strategies like
mutation operations further increases diversity in the search space28,49. Therefore, these improvements
accelerate convergence and enhance classification performance, highlighting HS’s potential to address
weight initialization inefficiencies in machine learning. The comprehensive evaluation highlights the effectiveness of DDA-HS in optimizing BPNN and extracting
WFPRs. The method strikes a balance between enhancing training performance and generalizing to unseen
data, as evidenced by its superior testing accuracy in both cases. This indicates that DDA-HS facilitates more
flexible and adaptive weight initialization. Furthermore, the consistent improvements in classification accuracy
underscore the potential of WFPRs to enhance the interpretability of machine learning models, particularly
in critical areas like medical diagnostics, where transparent decision-making is essential. In summary, these
findings validate DDA-HS as a robust optimization tool for BPNN, especially in extracting actionable insights
from complex datasets namely the PIMA dataset. Conclusions
This paper provided a thorough evaluation of DDA-HS for optimizing BPNN performance using the PIMA
dataset. Key findings include:
1)	 Optimized performance: DDA-HS achieved a strong balance between complexity and generalization, with
78.30% training accuracy and 74.48% testing accuracy for BPNN. Additionally, the classification accuracy
of WFPRs on the training set reached 79.51%, and 77.08% on the testing set, outperforming traditional
methods like HS, CS, AGOHS, HSCS, and unoptimized BPNN. This demonstrates the effectiveness of DDA-
HS in both optimizing model performance and improving generalization.
2)	 Prediction interpretability: WFPR extraction from the weighted matrix offered transparency into BPNN’s
decision-making, revealing the impact of input features on classification outcomes.
3)	 Clinical implications: The interpretability of WFPRs enhances trust in machine learning models for clinical
diagnostics by providing clear reasoning for model predictions, aiding healthcare professionals. In conclusion, DDA-HS proves to be a robust method for improving both accuracy and interpretability in the
BPNN model. The primary goal of this study was to introduce and validate the DDA-HS algorithm for optimizing
the initial weights of BPNNs in the context of WFPR extraction, using the PIMA dataset as a benchmark. While the results on the PIMA dataset are promising, future work will focus on extending this framework to
larger and more complex datasets, such as MIMIC-III or eICU, to evaluate its scalability and robustness in
high-dimensional and diverse clinical environments. Additionally, challenges related to imbalanced classes and
noisy data are planned to be addressed, ensuring that DDA-HS remains effective in real-world scenarios where
data quality and class distribution may vary. Potential strategies for improving scalability and robustness, such
as adaptive hyperparameter tuning, will be explored to enhance the algorithm’s performance across various
healthcare applications. Cross-dataset validation across multiple healthcare domains will further enhance the
generalizability and robustness of the proposed method, paving the way for its broader application in CDSSs. Data availability
The datasets generated and/or analysed during the current study are available in the [KAGGLE] repository, [​h​t​t​
p​s​:​/​/​w​w​w​.​k​a​g​g​l​e​.​c​o​m​/​u​c​i​m​l​/​p​i​m​a​-​i​n​d​i​a​n​s​-​d​i​a​b​e​t​e​s​-​d​a​t​a​b​a​s​e]. Received: 15 November 2024; Accepted: 20 March 2025
References

### 1. Sümbül, H. & Yüzer, A. H. Design of a fuzzy input expert system visual information interface for classification of apnea and

hypopnea. Multimedia Tools Appl. 83, 21133–21152. https://doi.org/10.1007/s11042-023-16152-9 (2023).

### 2. Ackerhans, S., Huynh, T., Kaiser, C. & Schultz, C. Exploring the role of professional identity in the implementation of clinical

decision support systems—a narrative review. Implement. Sci. 19 https://doi.org/10.1186/s13012-024-01339-x (2024).

### 3. Spinelli, A. et al. Artificial intelligence in colorectal surgery: an AI-powered systematic review. Tech. Coloproctol. 27, 615–629.

https://doi.org/10.1007/s10151-023-02772-8 (2023).

### 4. Roy, K. et al. ProKnow: process knowledge for safety constrained and explainable question generation for mental health diagnostic

assistance. Front. Big Data. 5 https://doi.org/10.3389/fdata.2022.1056728 (2023).

### 5. Burdukiewicz, M., Chilimoniuk, J., Grzesiak, K., Krętowski, A. & Ciborowski, M. ML-based clinical decision support models based

on metabolomics data. TRAC Trends Anal. Chem. 178, 117819. https://doi.org/10.1016/j.trac.2024.117819 (2024).

### 6. Basile, L. J., Carbonara, N., Pellegrino, R. & Panniello, U. Business intelligence in the healthcare industry: the utilization of a data-

driven approach to support clinical decision making. Technovation 120, 102482. https://doi.org/10.1016/j.technovation.2022.102482
(2023).

### 7. Sharma, A. S. & Hota, H. S. 261–288 (Springer Nature Singapore, (2024).

### 8. Silva, B., Hak, F., Guimarães, T., Manuel, M. & Santos, M. F. Rule-based system for effective clinical decision support. Procedia

Comput. Sci. 220, 880–885. https://doi.org/10.1016/j.procs.2023.03.119 (2023).

### 9. K, N. & M․, B. Fuzzy rule based classifier model for evidence based clinical decision support systems. Intell. Syst. Appl. 22, 200393.

https://doi.org/10.1016/j.iswa.2024.200393 (2024). Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

### 10. Shahin, M., Chen, F. F., Hosseinzadeh, A. & Maghanaki, M. Deploying deep convolutional neural network to the battle against

cancer: towards flexible healthcare systems. Inf. Med. Unlocked. 47, 101494. https://doi.org/10.1016/j.imu.2024.101494 (2024).

### 11. Nasarian, E., Alizadehsani, R., Acharya, U. R. & Tsui, K. L. Designing interpretable ML system to enhance trust in healthcare: A

systematic review to proposed responsible clinician-AI-collaboration framework. Inform. Fusion. 108, 102412. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​
1​0​1​6​/​j​.​i​n​f​f​u​s​.​2​0​2​4​.​1​0​2​4​1​2​ (2024).

### 12. Evans, R. P., Bryant, L. D., Russell, G. & Absolom, K. Trust and acceptability of data-driven clinical recommendations in everyday

practice: A scoping review. Int. J. Med. Informatics. 183, 105342. https://doi.org/10.1016/j.ijmedinf.2024.105342 (2024).

### 13. Li, X. & Shen, Q. A hybrid framework based on knowledge distillation for explainable disease diagnosis. Expert Syst. Appl. 238,

121844. https://doi.org/10.1016/j.eswa.2023.121844 (2024).

### 14. Pugalendhi, G., Rathore, M. M., Shukla, D. & Paul, A. Handling big microarray data: A novel approach to design accurate Fuzzy-

Based medical expert system. IEEE Access. 11, 35182–35196. https://doi.org/10.1109/access.2023.3257875 (2023).

### 15. Ma, N., Hu, Q., Wu, K. & Yuan, Y. A. Dissimilarity measure powered feature weighted fuzzy C-Means algorithm for gene expression

data. IEEE Trans. Fuzzy Syst. 1–11. https://doi.org/10.1109/tfuzz.2024.3387465 (2024).

### 16. Liu, L. et al. Establishment of machine learning-based tool for early detection of pulmonary embolism. Comput. Methods Programs

Biomed. 244, 107977. https://doi.org/10.1016/j.cmpb.2023.107977 (2024).

### 17. Liu, K. et al. New methods based on a genetic algorithm back propagation (GABP) neural network and general regression neural

network (GRNN) for predicting the occurrence of trihalomethanes in tap water. Sci. Total Environ. 870, 161976. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​
0​.​1​0​1​6​/​j​.​s​c​i​t​o​t​e​n​v​.​2​0​2​3​.​1​6​1​9​7​6​ (2023).

### 18. Liu, X. et al. Study on compression bearing capacity of tapered Concrete-Filled Double-Skin steel tubular members based on

Heuristic-Algorithm-Optimized backpropagation neural network model. Buildings 14, 3375. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​3​3​9​0​/​b​u​i​l​d​i​n​g​s​1​4​
1​1​3​3​7​5​ (2024).

### 19. Li, H. C., Zhou, K. Q., Mo, L. P., Zain, A. M. & Qin, F. Weighted fuzzy production rule extraction using modified harmony

search algorithm and BP neural network framework. IEEE Access. 8, 186620–186637. https://doi.org/10.1109/access.2020.3029966
(2020).

### 20. Ye, S., Zhou, K., Zain, A. M., Wang, F. & Yusoff, Y. A modified harmony search algorithm and its applications in weighted fuzzy

production rule extraction. Front. Inform. Technol. Electron. Eng. 24, 1574–1590. https://doi.org/10.1631/fitee.2200334 (2023).

### 21. Adegboye, O. R. & Deniz Ülker, E. Hybrid artificial electric field employing cuckoo search algorithm with refraction learning for

engineering optimization problems. Sci. Rep. 13 https://doi.org/10.1038/s41598-023-31081-1 (2023).

### 22. Adegboye, O. R. & Deniz Ülker, E. Gaussian mutation specular reflection learning with local escaping operator based artificial

electric field algorithm and its engineering application. Appl. Sci. 13, 4157. https://doi.org/10.3390/app13074157 (2023).

### 23. Geem, Z. W., Kim, J. H. & Loganathan, G. V. A new heuristic optimization algorithm: Harmony search. SIMULATION 76, 60–68

(2001). https://doi.org/10.1177/003754970107600201

### 24. Mahdavi, M., Fesanghary, M. & Damangir, E. An improved harmony search algorithm for solving optimization problems. Appl. Math. Comput. 188, 1567–1579. https://doi.org/10.1016/j.amc.2006.11.033 (2007).

### 25. Omran, M. G. H. & Mahdavi, M. Global-best harmony search. Appl. Math. Comput. 198, 643–656. ​h​t​t​p​s​:​/​/​d​o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​a​m​c​.​

2​0​0​7​.​0​9​.​0​0​4​ (2008).

### 26. Wang, C. M. & Huang, Y. F. Self-adaptive harmony search algorithm for optimization. Expert Syst. Appl. 37, 2826–2837. ​h​t​t​p​s​:​/​/​d​

o​i​.​o​r​g​/​1​0​.​1​0​1​6​/​j​.​e​s​w​a​.​2​0​0​9​.​0​9​.​0​0​8​ (2010).

### 27. Alia, O. M. D. & Mandava, R. The variants of the harmony search algorithm: an overview. Artif. Intell. Rev. 36, 49–68. ​h​t​t​p​s​:​/​/​d​o​i​.​

o​r​g​/​1​0​.​1​0​0​7​/​s​1​0​4​6​2​-​0​1​0​-​9​2​0​1​-​y​ (2011).

### 28. Wang, J., Ouyang, H., Zhang, C., Li, S. & Xiang, J. A novel intelligent global harmony search algorithm based on improved search

stability strategy. Sci. Rep. 13 https://doi.org/10.1038/s41598-023-34736-1 (2023).

### 29. Goh, R. Y., Lee, L. S., Seow, H. V. & Gopal, K. Hybrid harmony Search–Artificial intelligence models in credit scoring. Entropy 22,

989. https://doi.org/10.3390/e22090989 (2020).

### 30. Wang, J., Ouyang, H., Li, S., Ding, W. & Gao, L. Equilibrium optimizer-based harmony search algorithm with nonlinear dynamic

domains and its application to real-world optimization problems. Artif. Intell. Rev. 57 https://doi.org/10.1007/s10462-024-10793-4
(2024).

### 31. Rautray, R., Dash, R., Dash, R., Chandra Balabantaray, R. & Parida, S. P. A review on metaheuristic approaches for optimization

problems. 33–55 (2024). https://doi.org/10.1007/978-981-99-8853-2_3

### 32. Qin, F. et al. Hybrid harmony search algorithm integrating differential evolution and lévy flight for engineering optimization. IEEE

Access. 13, 13534–13572. https://doi.org/10.1109/ACCESS.2025.3529714 (2025).

### 33. Mustyala, S. & Bisi, M. Ensembling harmony search algorithm with case-based reasoning for software development effort

Estimation. Cluster Comput. 28 https://doi.org/10.1007/s10586-024-04858-w (2025).

### 34. Hua, C., Cao, X., Liao, B. & Li, S. Advances on intelligent algorithms for scientific computing: an overview. Front. Neurorobotics.

17, 01–21. https://doi.org/10.3389/fnbot.2023.1190977 (2023).

### 35. Choudhary, S., Ram, M., Goyal, N. & Saini, S. Reliability and cost optimization of series–parallel system with metaheuristic

algorithm. Int. J. Syst. Assur. Eng. Manage. 15, 1456–1466. https://doi.org/10.1007/s13198-023-01905-4 (2024).

### 36. Kang, D. W. et al. An adaptive harmony search Part-of-Speech tagger for square Hmong corpus. Baghdad Sci. J. 21, 0622. ​h​t​t​p​s​:​/​/​d​

o​i​.​o​r​g​/​1​0​.​2​1​1​2​3​/​b​s​j​.​2​0​2​4​.​9​6​9​4​ (2024).

### 37. Wolpert, D. H. The implications of the No-Free-Lunch theorems for Meta-induction. J. Gen. Philos. Sci. 54, 421–432. ​h​t​t​p​s​:​/​/​d​o​i​.​o​

r​g​/​1​0​.​1​0​0​7​/​s​1​0​8​3​8​-​0​2​2​-​0​9​6​0​9​-​2​ (2023).

### 38. Huang, Z., Zhang, Z., Hua, C., Liao, B. & Li, S. Leveraging enhanced Egret swarm optimization algorithm and artificial intelligence-

driven prompt strategies for portfolio selection. Sci. Rep. 14 https://doi.org/10.1038/s41598-024-77925-2 (2024).

### 39. Peng, S., Gao, R., Zheng, W. & Lei, K. Adaptive algorithms for bayesian spectrum sensing based on Markov model. KSII Trans. Internet Inform. Syst. (TIIS). 12, 3095–3111 (2018).

### 40. Kolozali, Ş., White, S. L., Norris, S., Fasli, M. & Van Heerden, A. Explainable early prediction of gestational diabetes biomarkers by

combining medical background and wearable devices: A pilot study with a cohort group in South Africa. IEEE J. Biomedical Health
Inf. 28, 1860–1871. https://doi.org/10.1109/jbhi.2024.3361505 (2024).

### 41. Tanveer, M. et al. Fuzzy deep learning for the diagnosis of Alzheimer’s disease: approaches and challenges. IEEE Trans. Fuzzy Syst.

32, 5477–5492. https://doi.org/10.1109/tfuzz.2024.3409412 (2024).

### 42. Casal-Guisande, M. et al. Proposal and definition of an intelligent clinical decision support system applied to the screening and

early diagnosis of breast cancer. Cancers 15, 1711. https://doi.org/10.3390/cancers15061711 (2023).

### 43. Chen, Z. et al. Research on bearing fault diagnosis based on improved genetic algorithm and BP neural network. Sci. Rep. 14

https://doi.org/10.1038/s41598-024-66318-0 (2024).

### 44. Huang, J., Nan, J., Gao, M. & Wang, Y. Antenna modeling based on meta-heuristic intelligent algorithms and neural networks. Appl. Soft Comput. 159, 111623. https://doi.org/10.1016/j.asoc.2024.111623 (2024).

### 45. Alzahrani, S. Feature subset selection with artificial Intelligence-Based classification model for biomedical data. Computers Mater. Continua. 72, 4267–4281. https://doi.org/10.32604/cmc.2022.027369 (2022).

### 46. Zarei, E., Khan, F. & Abbassi, R. How to account artificial intelligence in human factor analysis of complex systems? Process Saf. Environ. Prot. 171, 736–750. https://doi.org/10.1016/j.psep.2023.01.067 (2023).

### 47. Qin, F., Zain, A. M. & Zhou, K. Q. Harmony search algorithm and related variants: A systematic review. Swarm Evol. Comput. 74,

101126. https://doi.org/10.1016/j.swevo.2022.101126 (2022). Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/

### 48. Raiaan, M. A. K. et al. A systematic review of hyperparameter optimization techniques in convolutional neural networks. Decis. Analytics J. 11, 100470. https://doi.org/10.1016/j.dajour.2024.100470 (2024).

### 49. Ding, Z. et al. Improved harmony search algorithm for enhancing efficiency and quality in optimization of the distillation process. ACS Omega. 8, 28487–28498. https://doi.org/10.1021/acsomega.3c02785 (2023). Acknowledgements
This research is supported in part by the Ministry of Higher Education Malaysia through the Fundamental
Research Grant Scheme (FRGS) under Grant FRGS/1/2022/ICT02/UTM/01/1, the National Natural Science
Foundation of China under grant numbers 62066016 and 52268049, the Natural Science Foundation of Hunan
Province of China under grant number 2024JJ7395, and the Scientific Research Project of Education Depart­
ment of Hunan Province of China under grant number 22B0549. Author contributions
F. Q.: Writing – original draft. A. M. Z.: Supervision. K. Q. Z.: Writing – review & editing. D. B. Z.: Validation. Declarations
Competing interests
The authors declare no competing interests. Additional information
Correspondence and requests for materials should be addressed to K.-Q. Z. Reprints and permissions information is available at www.nature.com/reprints. Publisher’s note  Springer Nature remains neutral with regard to jurisdictional claims in published maps and
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
Scientific Reports | (2025) 15:11012

| https://doi.org/10.1038/s41598-025-95406-y
www.nature.com/scientificreports/
