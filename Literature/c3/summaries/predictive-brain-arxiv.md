# predictive-brain-arxiv

Tactile sensing
Lorenzo Natale, Giorgio Cannata
This is a post-peer-review, pre-copyedit version of an article published in Humanoid
Robotics: A Reference, Springer. The ﬁnal authenticated version is available online
at: https://doi.org/10.1007/978-94-007-7194-9 110-1
Cite this Chapter as:
Natale L., Cannata G. (2017) Tactile Sensing. In: Goswami A., Vadakkepat P. (eds)
Humanoid Robotics: A Reference. Springer, Dordrecht. https://doi.org/10.1007/978-
94-007-7194-9 110-1
Abstract Research on tactile sensing has been progressing at constant pace. In
robotics, tactile sensing is typically studied in the context of object grasping and
manipulation. In this domain, the development of robust, multi-modal, tactile sen-
sors for robotic hands has supported the study of novel algorithms for in-hand object
manipulation, material classiﬁcation and object perception. In the ﬁeld of humanoid
robotics, research has focused on solving the challenges that allow developing sys-
tems of tactile sensors that can cover large areas of the robot body, and can inte-
grate different types of transducers to measure pressure at various frequency bands,
acceleration and temperature. The availability of such systems has extended the
application of tactile sensing to whole-body control, autonomous calibration, self-
perception and human-robot interaction. The goal of this Chapter is to provide an
overview of the technologies for tactile sensing, with particular emphasis on the sys-
tems that have been deployed on humanoid robots. We describe the skills that have
Lorenzo Natale,
Istituto Italiano di Tecnologia, via Morego 30, 16163, Genova, Italy, e-mail:lorenzo.natale@
iit.it.
Giorgio Cannata,
DIBRIS, Universit `a degli Studi di Genova, Via All’Opera Pia, 13 – 16145 Genova, e-mail:
giorgio.cannata@unige.it.
1
arXiv:2105.05089v1  [cs.RO]  7 May 2021
2 Lorenzo Natale, Giorgio Cannata
been implemented with the adoption of these technologies and discuss the main
challenges that remain to be addressed.
1 Introduction
For many years robotic researchers have looked at vision as the primary source of
information to guide robot behavior, while control of interaction forces has been
approached mainly with the use of force sensors either at the end-effector or at the
joint level.
Operational safety, especially in human-populated environment requires that
robot can not only avoid but also detect collisions. Although the former can be done
efﬁciently with visual sensors (especially active sensors, like lasers or infrared) the
latter clearly needs to rely on sensors capable of measuring contacts. Force and
torque sensors can provide indirect measure of collisions, however, they can do so
only if contact happens in certain parts of the robot body and by relying on an ac-
curate model of the robot. Safety, especially in presence of humans, needs tactile
systems able to cover the whole robot so that unexpected collisions can be detected
anywhere.
If industrial robots are programmed to reduce contact with the environment as
much as possible, future robotic systems will actually rely on it for proper operation.
Researchers are developing algorithms for whole-body manipulation, in which the
robot exploits the interaction with the environment to achieve sophisticated behavior
(e.g. climbing a stair while holding to the rail, stepping up debris while leaning on
supports with the hands, etc).
Human-robot interaction can also greatly beneﬁt of distributed tactile systems.
Humans rely on physical contact for communication (like tapping on someone’s
arm or shoulder to attract his attention, grabbing him to teach how to carry out a
task), and likely they will expect a humanoid robot to be able to react appropriately
to similar forms of interaction.
Technologies for tactile sensors have been studied exensively in the literature and
researchers have proposed many prototypes of sensors which provide accurate re-
sponse to force or pressure. Implementing tactile systems, however, requires solving
additional problems. Tactile sensors are subject by nature to physical stress and need
to be reliable and robust against wear and tear. They should have large dynamical
range. The hands of a robot, for example, should be equipped with sensors capable
of detecting soft touch, when manipulating objects, but also large pressures when
supporting the weight of the robot. Similar considerations hold for the frequency
response: tactile sensors should detect static contact as well as respond to high tem-
poral and spatial frequency components for detecting slip and discriminate texture.
In terms of coverage, the sensor should detect multiple contacts possibly with no
dead spots, and even be suitable to cover movable parts of the robot (like the joints).
Tactile sensing 3
From the mechanical point of view, a favorable property is compliance. It helps
reducing damage either to the robot or the environment by dumping collisions, and
it aids manipulation by increasing contact friction.
Finally, a tactile system should be affordable. This implies low cost of manu-
facturing, deployment and calibration. To ﬁt on a robot a tactile system should use
small electronic components for signal conditioning and digital conversion and need
a reduced number of wires to route the information from the sensor to the processing
units.
For these reasons the development of appropriate tactile systems is an ambitious,
technological task which has challenged research for many years. However, some
tactile systems have been proposed in the literature and successfully deployed on
humanoid robots, including whole-body systems and compact tactile sensors for
humanoid hands. These systems, in turn, have allowed researchers to advance the
state-of-the-art in humanoid robot control and cognition. It is today not surprising
to see humanoid robots able to operate in contact with the environment, perform
delicate object manipulation and object discrimination tasks while relying on pure
touch.
The goal of this Chapter is to provide an overview of the recent advancement in
robotic touch. In Section 2 we begin with an overview of tactile technologies to give
the reader a general understanding of the transduction principles supporting tactile
sensing. Section 3 complements this overview with a description of tactile systems
that have been successfully deployed on humanoid robots, separated in full body
systems and sensors for hands. In Section 4 we discuss the problems of calibration of
tactile systems and representation for data processing. In Section 5 and Section 6 we
revise applications of tactile feedback respectively for robot control and perception.
Finally, in Section7 we draw the conclusions and discuss the open challenges in
tactile sensing.
2 Technologies
Most of them have been demonstrated at bench-top prototype level, some have been
integrated on robots for operational demonstrations, and ﬁnally, a few, have been
integrated into microcircuits. There exists a very large number of solutions and tech-
nologies proposed for the development of tactile sensors.
A tactile sensor is composed of a supporting element coupled with an electro-
mechanical transducer converting a pressure (stress) or a deformation (strain) into
a voltage or an electric current. Often, the transducer requires some type of driving
voltage or excitation (with the exception of piezoelectric transducers), while the
output signal always needs signal conditioning before sampling.
Therefore, the transducer technology is only one of the elements affecting the
design of a tactile sensor. In fact, at the system level the development of large scale
tactile systems involves signiﬁcant problems related to their deployment, i.e.wiring
(routing tactile and driving signal to matrices formed by several – up to thousands –
4 Lorenzo Natale, Giorgio Cannata
Fig. 1: Piezo-resistive transducer principle: a piezo-resistive elastomer is sand-
wiched between electrodes. Source [65].
taxels) and embedded electronics (required to develop self contained tactile systems
portable to different robot platforms).
2.1 Piezo-resistive Sensors
Piezo-resistive transducers are one the ﬁrst technologies adopted to develop tactile
sensors. The basic design consists of two electrodes (facing each other or inter-
digitated) bridged by a deformable elastomer loaded with a conductive ﬁller (e.g.
graphite) to reach the so called percolation threshold. In this condition the trans-
ducer has a high resistivity (typically> 10 MΩ ·cm) in absence of load. As an exter-
nal pressure is applied to the elastomer the resistance between the electrodes drops
down to resistances of the order of a few KΩ or less (Figure 1).
These devices require a constant driving voltage. Measurement can be easily
performed using a voltage divider formed by the sensor together with a precision
reference resistor. Since the resistance variation has quite a large range it is usu-
ally possible to exploit the analog-to-digital (A/D) converter input range of the data
acquisition system without the need of complex electronic front-end.
Noise can affect piezo-resistive sensors. A ﬁrst source of noise is intrinsic in the
transducer because the effect of the pressure is to change the resistivity of the mate-
rial by creating conductive pathways. In this respect, special elastomers, e.g. quan-
tum tunnel composites exhibit signiﬁcantly lower noise. The second one, typically
adopted in custom made designs, is originated at the electrode-elastomer interface;
silver coated electrodes and conductive adhesive can mitigate the problem, but can
make miniaturization difﬁcult and prevent manufacturing of large arrays of sensors.
The development of 2-dimensional arrays of piezo-resistive transducers is usu-
ally based on the sequential scanning of the rows and the columns: an input mul-
tiplexer drive the rows while a de-multiplexer scans the columns. This solution is
fairly simple: for a N × M array only N + M wires and a single A/D can be used
to acquire all the data. Unfortunately, cross-talk between adjacent taxels affects the
measurements [21]. This problem can be solved by grounding the inactive rows and
columns during the scanning [57], at the cost of increasing signiﬁcantly the com-
Tactile sensing 5
plexity of the driving electronics. An alternative, simpler solution, is to use a hybrid
hardware-software compensation methods [5].
The pressure response is generally non-linear and depends on the physical char-
acterization of the polymer and ﬁller which can be estimated using a calibration
procedure.
Resistive elastomers are commercially available, and are typically supplied as
sheets or laminated foils suitable for planar or cylindrical geometries; more complex
geometries (e.g. double curvature surfaces as in the ﬁngertips) may require different
manufacturing solutions.
In the past few years a relevant interest emerged for the development of pressure
transducers based on carbon nanotubes or graphene [8], because water based sus-
pensions of carbon nanotubes or graphene can be printed using ink-jet technology.
Finally, a very particular usage of piezo-resistive transducers for tactile sensing is
based on electro impedance tomography [31]. In this method no taxels are manu-
factured, but contacts can be reconstructed using voltage measurements taken at the
boundary of the sensitive area.
2.2 Capacitive Sensors
The basic principle of Capacitive sensors consists in two opposite electrodes sus-
tained by an elastic support and separated by a dielectric. This conﬁguration creates
a capacitor, whose value can be computed as:
C = ε0εr
A
x (1)
where x is the distance between the armatures, A is the area of the electrodes,
and ε0εr are the electric constant and the relative dielectric constant (speciﬁc of
the dielectric material), ﬁgure 2. As an external pressure is applied to the elastic
substrate the distance x between the electrodes changes increasing the capacitance
of the taxel. A complete model of the taxel response can be used for optimizing the
sensor design as described in [33].
Capacitive transducers require an active excitation and demodulation in order to
compute the measurement. For this reason, they have received increasing attention
in robotics only after their use in touch screens has pushed the development of af-
fordable capacitance-to-digital integrated circuits (CTDs). Time based techniques
or frequency based techniques are typically implemented into commercial CTDs
which embed fully integrated excitation circuits, electronic front-end and data ac-
quisition in a single chip. However, since most of these devices are designed to
detect large capacitance changes (e.g. to implement touch buttons), only a few pro-
vide a signal-to-noise ratio (S/N) suitable for accurate tactile sensing (S/N> 20 dB).
Another major limitation of existing CTDs is their response time. As the sensor out-
put is computed by averaging sequences of measurements, high S/N response is
typically obtained with output rates signiﬁcantly larger than 1 ms.
6 Lorenzo Natale, Giorgio Cannata
The development of 2-dimensional arrays of capacitive transducers is usually
done by driving groups of adjacent taxels with a single CTD (some models provide
interface for up to 30 taxels) and by transferring the read-out to a host computer
using serial lines or busses. Chip-to-chip data links [55] allow to largely reduce the
number of lines required to drive sensors with hundreds of taxels. Flexible printed
circuit boards (PCBs) [55] or semi-rigid PCBs [39] can be used to support the elec-
tronics and add additional ground layers to provide shielding against electrical in-
terference.
At circuit level a technique provided by some CTD manufacturers, calledshield-
ing, allows compensating for parasitic capacitance (among the circuit wires and
with external components) and eliminate cross-talk between taxels. The response
to pressure is generally non-linear and a calibration procedure is required to de-
termine numerically the accurate pressure-to-resistancerelationship, in particular if
the sensor is bent over curved surfaces.
Recently, carbon nanotube based conductive inks have been proposed to design
capacitive based tactile transducers [3]. This would make possible to simplify the
manufacturing process and to reduce the costs.
2.3 Piezo-electric Sensors
Piezoelectric transducers have been used for a long time as tactile and vibration
sensors in particular. Compared to other transduction technologies piezoelectric de-
vices do not respond at low frequencies (zero output in response to steady pressure),
but have quite a dynamic response, often larger than 10 KHz.
Piezoelectric transducers for the development of tactile sensors are largely based
on piezo polymers or ceramics. Among these the polyvinylidene-ﬂuoride (PVDF)
is perhaps the most widely used, ﬁgure 3. Piezo materials subject to mechanical
stress accumulate electric charges, which are collected by conductive electrodes and
Fig. 2: Capacitive sensor [5].
Tactile sensing 7
PDMS 
protective 
layer
Inkjet printed contacts on 
PVDF (continuous – TOP , 16 
patterned squares – BOTTOM)
PCB with 
patterned 
pads and 
tracks
7 cm
3 mm
Fig. 3: Piezoelectric sensor [18].
ampliﬁed to generate a voltage. Therefore, while piezo transducers do not require
external electrical excitation, the electronic front-end is complex because it requires
high input impedance and ampliﬁers with low noise. This makes the development
of embedded sensor difﬁcult with commercial components.
Since piezo materials are sensitive to different types of mechanical stresses (pres-
sure, bending moments etc.), the design of tactile systems must be done by carefully
designing the geometry of the system to capture the desired mechanical input.
Large area tactile systems based on piezoelectric transducers have been proposed.
In [59] each taxel is formed by a deformable PVDF foil sandwiched between two
polyurethane foam layers. Finally, integrated arrays have been developed by cou-
pling a pressure sensitive PVDF ﬁlm on the gate of a FET transistor creating the
so-called POSFET device [10].
2.4 Optical Sensors
Optical transducers have been used over the years in many different ways to develop
tactile sensors. The very ﬁrst large area robot skin developed by Lumelsky [6] used
optical transducers as proximity sensors, a technique also used in recent designs to
detect contact with light or extremely thin objects [39], [14]. Other implementations
are based on reﬂectivity measurements [46], [9], . In this case a Light Emitter Diode
(LED) and a photo detector are coupled and covered by a deformable opaque elas-
tomer. When pressure is applied the elastomer is subject to deformation and light is
scattered: the variation of reﬂected light is captured and processed, ﬁgure 4 (from
Optoforce Ltd.1).
The driving and front/end electronics is fairly simple and the transducer is robust
against electro-magnetic disturbances, this makes it possible to use high sampling
rates. The development of 2-dimensional arrays of optical transducers is usually
done by driving the taxels with a row-column scanning mechanism [47]. However,
1 https://optoforce.com/
8 Lorenzo Natale, Giorgio Cannata
in large implementations a critical aspect to consider is the power consumption of
the LEDs.
There is no analytic model for characterizing the response of the sensor, there-
fore, an empirical calibration of the device can be required as in [9].
2.5 Magnetic Sensors
Magnetic transducers, like capacitive transducers, have evolved in the past few years
along with the growth of the market of Hall-effect Integrated Circuits (ICs). The ba-
sic design consists of a magnet suspended by an elastic support over the sensitive
point of the Hall-effect IC. When external pressure is applied, the relative position
and orientation of the magnet changes as well as the measured intensity and orien-
tation of the magnetic ﬁeld [62, 61], ﬁgure 5.
Sensing surface
Reflective layer
Sensing element
Light emitter
Fig. 4: Commercial optic sensor (OptoForce Ltd.).
a) b)
c) d)
Fig. 5: Magnetic transducer principle. Image courtesy of Eduardo Torres-Jara [62].
Tactile sensing 9
One of the limitations of these systems is that they could interfere with surround-
ing ferro-magnetic materials and can be inﬂuenced by external magnetic ﬁelds. The
development of 2-dimensional arrays can be based on the same architectures de-
scribed for the capacitive based systems.
3 Tactile Systems
In this Section we describe a few signiﬁcant tactile systems that have been imple-
mented on humanoid robots, solving system level challenges that made these tactile
systems at least in principle portable to other robots. We have considered two major
classes of tactile systems: whole body tactile systems (robot skins) intended to cover
large parts of the robot body, and tactile systems for robotic hands and manipulation.
3.1 Whole-body systems
Early attempts to cover large areas of a humanoid robots are [26, 30, 27]. In [26]
the authors proposed a “sensor suit” to cover the entire body of a robot. The system
provided a binary output (contact versus non-contact), based on resistive principle
and it was made of 192 sensing regions on the whole body with variable spatial reso-
lution ranging from 10×5 cm for the legs to 5×5 cm for the arms. The sensitivity of
this system was relatively low (4900 KPa), however, it allowed the implementation
of simple touch driven orientation behaviors and whole-body grasping (i.e. caging).
In [30] the humanoid robot H4 was equipped with ﬁve tactile modules: the chest
was covered by a system of 96 sensing points; each upper and fore-arms had 64
sensing and 36 sensing points respectively. Pressure was estimated by measuring
change in resistance between electrodes separated by a soft, conductive gel. The
measurable pressure was within 0-40 KPa with minimum threshold of 2.5 KPa,
with a sampling time of 80 ms.
The ﬁrst tactile system capable of detecting force has been implemented on the
robot Wendy [27]. This system was made of modular units made of a rigid cover
integrating a 6 axis force-torque sensor and a set of Force Sensing Resistors (FSR)
on its surface. The magnitude, direction and location of the external force was com-
puted by integrating the information provided by the sensors, under the assumption
that no moments were generated at the contact point. A total of 6 units were mounted
on the arms and shoulders of the robot Wendy: the system allowed to sample data
at 100 Hz and measure 3D force vectors with average standard deviation of 1.2 mm
and 1.6 mm for the contact point on the surface and of 0.15 N for the force intensity.
The humanoid robot ARMAR III [1] was equipped with artiﬁcial skin made of
planar skin pads mounted on the front side and back side of each shoulder, and in-
terconnected by CAN-bus links. The sensors pads used resistive technology imple-
mented using a graphite loaded elastomer and electrodes obtained using a ﬂexible
10 Lorenzo Natale, Giorgio Cannata
PCB [32]. Data was acquired at the rate of 40 Hz with a 12 bits resolution, in the
range of 4-120 KPa.
The robot CB2 [38] was designed to support social interaction with humans and,
for this reason, it was fully covered with a soft skin, made of PVDF ﬁlms covered
by silicone rubber. Since PVDF detects the rate of change of the applied stress, this
information was integrated to reconstruct the actual contact pressure. Overall the
robot was covered by 197 tactile sensors, distributed on the arms, shoulders, torso
arms and head, sampled at the rate of 100 Hz.
The robot Kotaro [42] mounted two types of tactile sensors. The ﬁrst was a ﬂex-
ible “band” obtained as a sandwich of a force-sensitive conductive rubber and two
ﬂexible PCBs. The “bands” were wrapped around the robot links and represented
one of the ﬁrst examples of a modularrobot skinsystem. This system had 64 sensing
units which could be read individually. The second type of sensors used conductive
rubber foam in complex 3D shapes: pressure was estimated by measuring the change
of resistance between electrodes.
A highly modular system based on optical technology was described in [47]. The
system consisted in modules of 32 sensors which could be adapted to cover non-
ﬂat surfaces. Modular units could be connected in a LAN to achieve the maximum
number of 65536 sensors. The operational range of the sensing units was in the range
of 0-500 KPa. In [45] this system was used to cover a humanoid robot with 1864
sensors; this system was used to demonstrate lifting of a 32 Kg box with whole-body
contact.
Semiconductor pressure sensors were employed in the robot RI-MAN [43], with
the aim of supporting object manipulation and human-robot interaction. The au-
thors used piezoresistive semiconductor pressure sensors which had the diameter of
5.8 mm and could detect the absolute pressure between 40 KPa and 440 KPa. These
sensors were mounted on a comb-like ﬂexible PCB, which could bend and conform
to non-ﬂat surfaces. Tactile sensors on the RI-MAN were located in ﬁve places –
namely the chest, the arms and forearms – for a total of 320 sensing elements. The
tactile system was made by elements of 8×8 sensing elements which were refreshed
every 15 ms. The range of measured force varied between 0 to 8 Kg over an area of
25×25 mm2 (corresponding to a maximum pressure of 126 KPa). The tactile sys-
tem was employed to measure the force exerted by the robot while lifting a (dummy)
human body.
A multi-modal modular tactile system (called HEX-O SKIN) for whole-body
sensing was presented in [39] (Figure 6). Each module embeds sensors for temper-
ature, 3-axis acceleration and proximity to emulate the human senses of tempera-
ture, vibration and light touch. Modules have hexagonal shape, and can be intercon-
nected to form a mesh. Although individual modules are rigid the system can bend
at the intersection and conform to curved shapes. A local controller on each mod-
ule processes data from the sensors at the frequency of 1 Khz and routes it to other
modules. This conﬁguration greatly reduces the number of wires, with increased
robustness and scalability. A system with 8 modules was initially mounted on a
Kuka lightweight robotic arm [39]. The HEX-O SKIN patches have been recently
enhanced to include three capacitive sensors measuring normal force up to 10 N,
Tactile sensing 11
and Gigabit interface to read the data from a network of cells. A system of 74 mod-
ules has been deployed to cover the upper body of the robot HRP2 [41] and used to
implement various tactile behaviors, such as kinesthetic teaching using contact or
proximity and whole-body grasping of unknown objects.
The ROBOSKIN tactile system [56] uses capacitive technology (Figure 6). In this
case sensing units are capacitors obtained by layering a ﬂexible PCB, a deformable
dielectric, and conductive Lycra. Pressure deforms the dielectric and varies the dis-
tance between the conductive plates, resulting in a variation of capacitance that can
be measured by commercial components. Similarly to the HEX-O SKIN modular
elements are interconnected by a bus. In this case the modules are triangles, which
embed 10 pressure sensors and two thermal sensors each: up to 16 triangles can
be read at the frequency of 20 Hz by a processing units which broadcasts tactile
values on a CAN interface. The ROBOSKIN tactile system has been used to cover
various robots. The iCub robot [37] mounts a total of 4488 sensors distributed on
the hands (including the ﬁngertips, the arms, the torso, the legs and feet-soles). The
latest version of the tactile system achieves low hysteresis and good mechanical ro-
bustness using a sandwich of three fabrics which form the dielectric, the conductive
Lycra and a protective layer [35]. It can detect the minimal pressure of 2-3 KPa, and
the maximum value of 180 KPa. Experiments with the iCub have addressed control
of interaction forces on the whole-body [13, 17] and visuo-tactile calibration [52].
Other robots that have been covered with theROBOSKIN system are KASPAR (816
tactile elements) and NAO (324 tactile elements).
3.2 Tactile sensors for antropomorphic hands
In the area of grasping and manipulation a large number of solutions have been
investigated to provide hands with tactile sensorization. One of the early example is
the Gifu hand II, which is equipped with 6-axis force sensors on the ﬁngertips and
a distributed system of tactile sensors based on resistive technology with 624 points
on the surface.
Fig. 6: Examples of skin systems. Left: the HEX-O SKIN (image courtesy of A.
Heddergott Munich Institute of Technology). Right: the ROBOSKIN (image cour-
tesy of Istituto Italiano di Tecnologia).
12 Lorenzo Natale, Giorgio Cannata
Fig. 7: Examples of sensorized ﬁngertips. a) The BioTac [63] (image courtesy of
SynTouch, LLC). b) Resistive ﬁngertip realized with Laser-Direct-Structering tech-
nique [48] (image courtesy of Risto Koiva, Bielefeld University). c) The iCub ﬁn-
gertips [28] (image courtesy of Istituto Italiano di Tecnologia).
A sensorized glove for the NASA Robonaut hand was presented in [36]. The
basis for this technology was Quantum Tunneling Composite (QTC), a material
which changes resistance with the applied pressure. QTC can be produced in sheets
that conform to curved surfaces and are sensitive to forces from a fraction of a
Newton to 10 N. The glove provided 33 sensor elements and increased friction and
sensitivity by incorporating plastic beads that acted as force concentrators.
The hands of the robot Obrero was equipped with 80 tactile sensors [62]. Each
sensor unit had a dome-like shape made of silicone rubber, hosting a small magnet in
the inner tip. Four hall-effect sensors at the base of the dome measured the magnetic
ﬁeld: mechanical deformation of the dome modiﬁed the magnetic ﬁeld and allowed
estimating the applied pressure. These sensors can detect the minimum force of
0.094 N and were successfully used to grasp unknown objects using tactile feedback
alone [44].
[19] described a tactile system for an anthropomorphic hand. This system embed-
ded a PVDF sensor within a resistive pressure sensor. The resistive sensor was made
by a set of electrodes covered with a conductive foam: pressure changed the resis-
tance measured between a common, reference, electrode and the individual sensing
elements. The PVDF was embedded in the cover of the sensor. The mechanical
properties of the cover transmitted vibrations that were picked up by the sensor.
This system was used to sensorize the inner parts of the ﬁngers and palm of an an-
thropomorphic hand. It was used to detect slip, contact points and classify tactile
images.
The iCub hand was equipped with tactile sensors on the ﬁngertips [28] (Figure 7).
These sensors were a customization of the iCub tactile technology, adapted to ﬁt on
the space available on the ﬁngertips. The resulting system had 12 sensors: it was
made by layering a ﬂexible PCB and deformable fabric which provide the dielectric,
conductive and protective layers. It can detect the minimal pressure of 3-4 KPa up
to a maximum or approximately 50 KPa.
Laser-Direct-Structuring was used in [48] to deposit conductive tracks on a 3D
structure which formed the ﬁngertip for the Shadow Hand (Figure 7). This system
used resistive technology and it provided a total of 12 sensing elements with the res-
olution of about 5.5 mm that can be read by an integrated circuits at the frequency of
Tactile sensing 13
1 KHz. This ﬁngertip can sense forces up to 80 N, with a tradeoff between sensitivity
and maximum measurable load. It was used in experiments that involve manipula-
tion tasks such as opening and closing jars and folding paper, which are extremely
challenging to accomplish without tactile feedback.
Probably the most successful tactile sensor for hands is the BioTac from Syn-
touch [63] (Figure 7). It is a bioinspired, multimodal ﬁngertip which includes resis-
tive sensors, pressure transducers and temperature sensors. The sensor is made by an
elastomer which contains a conductive ﬂuid: deformations of the elastomer produce
change of resistance between the electrodes inside the ﬂuid, whereas vibrations are
captured by the pressure sensor. The ﬁngertips are therefore sensitive to forces and
vibrations. The sensor can detect contacts with the spatial resolution of 2 mm and
forces that vary from 0.1 N to 30 N The BioTac has been mounted on many robotic
hands: the Shadow Hand, the Barret Hand, the PR2 gripper, the Allegro Hand from
SimLab, the JACO Hand, the Hubo hand, the 3Finger Adaptive Gripper from Robo-
tiq and the SDH from Schunk 2. The BioTac has been successfully used to solve a
large number of tasks (e.g. material discrimination, object recognition, slip detec-
tion and re-grasp to improve stability). These tasks are usually solved using Machine
Learning because the activation of the sensing elements in response to pressure is
difﬁcult to model.
4 Calibration and Data Representation
Tactile data are generated using different types of transducers, and they are usually
placed at discrete points over the robot body. Data are expected to be collected and a
properly processed for implementing control and perception tasks. A similar prob-
lem is faced when the task at hand requires integration of information from various
sensors, attached to different, moving, reference frames (e.g. inertial units or cam-
eras). A possible way to solve these problem is to perform a spatial calibration of
the tactile system, so that tactile information can be referred to a reference frame
attached to the robot. Cross-calibration with other sensory modalities is another op-
tion, especially when the position of the other sensors is known with higher accuracy
or when the task requires it.
Another approach is to avoid spatial calibration and work directly on tactile im-
ages obtained by representing tactile data in two dimensional surfaces. This ap-
proach is based on an apparent analogy between tactile data and visual images. Un-
fortunately, this analogy is only superﬁcial. In fact, geometry and raw data format of
transducers for vision consist of 2-dimensional arrays arranged in a rectangular pat-
tern. Speciﬁc geometric and optical calibration (pixels’ size, image center, lens dis-
tortion), can be performed by state-of-the-art software (e.g. MATLAB: Computer
Vision System Toolbox). Secondly images captured by digital cameras encode a
well deﬁned physical quantity: the amount of light captured in a given time interval.
2 http://www.syntouchllc.com/
14 Lorenzo Natale, Giorgio Cannata
Therefore, visual images acquired by physically different cameras (namely devices
produced by different manufacturers) are in principle equivalent: it is therefore pos-
sible to develop image processing algorithms which are independent from the spe-
ciﬁc hardware used, and it is possible to deﬁne universal image features which rely
on standard camera models.
Tactile images are neither standard nor based on a standard model. In a generic
skin system taxels are placed over the robot body in order to provide a more or less
coarse spatial sampling of the contacts. This has various implications. First, because
a robot body can be modeled as a 2-dimensional manifold, taxels are geometrically
arranged in patterns that depend on the speciﬁc shape of the robot (i.e. different
robots, or even different links of the same robot, have different taxels arrangement).
Relative position of taxels belonging to the same robot can even change as the robot
moves. Second, taxels could be placed over the robot with a space-varying density
and size, to provide higher resolution in selected body areas (e.g. the hands or the
ﬁngers), and lower for others (e.g. the torso and the back). Finally, a robot could
mount different types of tactile transducers, in general acquired at different rates,
which require distinct representations.
A proper software abstraction layer for tactile system can support the develop-
ment of tactile data processing for control and perception that are unspeciﬁc to the
actual hardware. This idea, ﬁrst introduced in [24] has been recently implemented
in a system named Skinware [67, 66].
4.1 Calibration
Some control tasks driven by tactile feedback (see for example Section 5) require
knowledge of the precise location of taxels with respect to the robot body. In prin-
ciple the location of the taxels is known in advance when the skin is integrated on
the robot; in practice, this knowledge is often inaccurate and affected by uncertainty
arising during the deployment of the sensors on the robot surface. Sources of errors
are the positioning of the system itself and the deformation of ﬂexile parts when
they conform to the surface. The position of taxels, in addition, depends on the
robot shape and its kinematics. These observation motivates the need for automatic
techniques for the spatial calibration of tactile systems.
In [12] the authors used information from the F/T sensors on the robot to calibrate
the tactile system of the iCub robot. The idea is that, in absence of external torque,
it is possible to use the force/torque measures to estimate the point of application of
external forces and correlate the estimate with the tactile data. This calibration tech-
nique was validated in a real robotic system, and it allowed estimating the position
of taxels with the average error of about 7 mm.
An automatic calibration procedure for sensors and actuators is described in [40].
This technique allowed calibrating the position of the taxels on each HEK-O SKIN
module by exploiting its rigid structure. The authors used speciﬁc motion patterns
and the accelerometers embedded in the HEK-O SKIN tactile system to determine
Tactile sensing 15
the structure and parameters of the kinematics chain that describe the robot and the
placement of the individual units.
A different approach was described in [52], in which the robot performed a vi-
sual calibration of the tactile system. The idea in this case was to attach a spatial
receptive ﬁeld to each taxel and to adapt this representation using vision. Adapta-
tion took place by touching the tactile system repetitively in multiple locations using
objects. The robot tracked objects using vision and linked their spatial location be-
fore contact (as measured by the cameras) with a receptive ﬁeld anchored to the
taxel that got activated after touch. The interesting aspect of this approach is that the
tactile system was calibrated with respect to the reference system of the cameras.
The authors demonstrated how to use this representation for predicting and avoiding
collisions with objects in the visual space.
4.2 Data Representation
Tactile data representation is difﬁcult for various reasons. Taxels are located on
curved surfaces without a regular pattern, therefore concepts like proximity or dis-
tance, or operations like spatial ﬁltering cannot be readily applied. In [4] it has been
proposed to represent tactile regions (see below) as ﬂat 2-dimensional maps, also
called artiﬁcial somatosensory maps from their analogy with a similar representa-
tion found in the cortex of primates. These maps are obtained byﬂattening the robot
surface with minimal distortions to preserve the relative location of the taxels.
Once the tactile data are represented as 2-D maps, standard techniques for ﬁlter-
ing and processing (e.g. borrowed, from computer vision) can be used. In particular
the maps can be re-sampled by software leading to standard piecewise rectangular
grids. Figure 8 shows a simulated 3-D to 2-D transformation of a two parts of the
iCub robot.
A further advantage of somatosensory maps is that they can be used to calibrate
multi-modal systems, layering on a common reference frame data from different
sensors. Finally, such maps can be used to plan and control interaction tasks. The
Fig. 8: Simulated 3-D (a and b) to 2-D (c and d) transformation for 2 parts of the
iCub robot for a ﬁne taxel distribution. Source [15].
16 Lorenzo Natale, Giorgio Cannata
advantage is that contact location, force and task errors can be expressed in a bi-
dimensional space and conveniently back-projected to the 3-D space when needed
(for example to compute robot control actions).
5 Reactive control
In this Section we describe applications of tactile systems for control. We separate
the discussion in two parts: whole-body control and manipulation.
5.1 Whole body control
Whole-body tactile systems have been used to implement various behaviors. The
earliest applications involved control of the robot to perform tasks with the whole-
body like object caging using the arm and chest [26, 30] (and more recently [41]) ,
or lifting of heavy objects [45, 43].
The typical application of tactile sensors is, however, contact avoidance. For such
behaviors the main advantage of tactile sensors is that they directly measure or allow
to accurately estimate the contact forces. Computing the same information from the
torque sensors at the joints is more complicated because it requires computing and
removing the torque component that is due to the robot internal dynamics. An exam-
ple of this type of behavior can be found in [30] where the mobile base of the robot
H4 is controlled to retract to reduce the pressure on the chest. Similarly, evasive
movements have been implemented using the HEX-O SKIN on a Kuka lightweight
arm [39]. Touch-triggered withdrawal reﬂexes modeled on the basis of the results
of experiments performed with human subjects have been implemented on the NAO
robot and validated in the context of safety [11].
Precise control of interaction forces is another important application of tactile
systems. In fact conventional approaches using F/T sensors partially fail because
they assume that contact happens at a ﬁxed, known location (typically the end-
effector). For these reasons several work attempted to integrate contact information
from the tactile system and F/T sensors located on the kinematic chain [27, 13, 17].
The work in [13] discusses in details the beneﬁts of an accurate measure of the
contact point in the context of force control.
Work on whole-body force control strongly motivates the need for distributed
tactile systems. It also highlights the need for such systems to provide accurate
contact location in the robot’s reference system. For this reason several techniques
for automatic calibration of tactile systems have been proposed in the literature.
Some of these approaches have been illustrated in Section 4.1.
Tactile sensing 17
5.2 Manipulation
Conventional approaches to grasping are based on accurate models of the objects
to be manipulated, including shape, mass, surface texture etc. (see [49] for an
overview). In unstructured environments, however, these properties may be incom-
plete or unavailable. In addition, model based approaches require accurate mod-
els of the robot hand. Although hand modes may be easier to compute, model-free
grasping strategies are expected to be more robust and therefore easier to use. Fi-
nally, to cope with uncertainty it would be preferable to have tactile based control
strategies that allow the robot to adjust online the grip to an object.
To address these problems, researchers have proposed alternative approaches that
rely on tactile or force feedback to evaluate grasp stability [54, 20] and to learn con-
trol policies that allow the robot to improve the stability of the grasp using feedback
control [53, 34].
In [54] the authors trained a SVM to predict whether a grasp is stable or not.
The SVM uses features that integrate the current hand conﬁguration (as measured
by the encoders on the joints) and tactile feedback. As tactile features the authors
used statistical moments computed from the tactile image acquired by the sensors
on the robot ARMAR III [32]. A similar approach is adopted in [20], in which
Grasp stability is determined using a Gaussian Mixture Model trained off-line as
a function of the hand posture and raw tactile data. In these approaches the robot
use the learned model to determine, on-line, if a grasp is stable, and apply corrective
actions otherwise. Corrective strategies can be implemented using optimization [20]
or learned by relying on teaching by demonstration [60, 53, 51], or reinforcement
learning [23].
One of the limitations of approaches based on tactile sensors is that they require
accurate detection of contacts. Due to delays in the control loops or insufﬁcient
sensitivity the robot may have problems controlling the interaction with the object.
Unreliable contact detection may cause the objects to tip over with failures that are
difﬁcult to recover. To overcome these problems, alternative approaches based on
proximity sensors have been proposed in the literature [50, 25].
6 Perception and Cognition
Conventionally, robotics rely on vision to perceive and identify objects. Although
computer vision has recently made remarkable progress, touch can still provide
complementary information. This is because some material and object properties
are simply not accessible from vision (like the object weight), or may be hidden
by occlusions. In addition, many properties like surface roughness, and even edges
and corners, may be confused due to noise or ambiguous, pictorial cues. However,
the extraction of tactile features is an intrinsically active process which requires the
implementation of appropriate explorative strategies which range from simple be-
18 Lorenzo Natale, Giorgio Cannata
haviors, involving an individual ﬁnger (like static contact, contour follow or sliding)
to more complex manipulation operations performed with the whole hand.
The deﬁnition of tactile features is not so straightforward as it is in the case
of vision. Several types of features have been proposed in the literature for mate-
rial and object discrimination. The work of [22] reports a comprehensive investi-
gation and examination of tactile features. Temperature [22] and temperature vari-
ation [64, 22, 7] were used with static contact to estimate the type of material by
looking at how quickly temperature ﬂowed from the sensor to the contact surface.
Static pressure coupled with joint motion provided an estimation of the material
softness or compliancy [64, 22]. Texture was usually estimated by sliding the ﬁnger
on the surface and using features that encoded the frequency content of the resulting
pressure variation, like variance or features that characterize the frequency spectrum
of the signal [22, 64, 7, 29, 58]. Recently, [2] applied deep convolutional neural net-
work to the problem of material discrimination using touch demonstrating that the
learned features outperform features based on Fourier analysis for this task.
An important consideration is that texture discrimination requires that the inter-
action between the sensor and the object generates mechanical vibrations and that
the sensor itself can capture such vibrations with sufﬁcient accuracy. This can be
facilitated by adding ridges to the surface oft the sensor [16] and it requires em-
bedding in the sensors transducers that are capable of measuring vibrations like
microphones [16] or accelerometers [58].
Object discrimination based on material identiﬁcation has been achieved with
high accuracy ([22] reports 97.6% accuracy for a set of 49 objects). The main lim-
itation of the work in the literature is that the interaction between the robot and the
object happen in quite controlled situations, with behaviors that are stereotyped and
often open-loop. It is still an open challenge how to integrate such techniques with
autonomous object manipulation strategies.
7 Conclusions
In this Chapter we have provided an overview of the technologies that have been
developed in the past years to endow robots with the sense of touch, and how this
has contributed to the improvement of robot motor and perceptual skills.
The sense of touch in humanoid robots has gone a long way. Affordable and ro-
bust distributed systems of tactile sensors have been successfully built and deployed
to cover large areas of various humanoid robots. These systems provide sufﬁcient
spatial resolution and are sensitive enough to support sophisticated whole-body be-
haviors, controlling interaction forces and avoid obstacles. Miniaturized multimodal
sensors have been integrated in anthropomorphic hands and have greatly improved
the capability of robots to manipulate objects and to perform cognitive tasks like
object recognition and material classiﬁcation.
Yet, it is clear that to reach human-level performance there are still big challenges
to solve which involve all aspects of tactile sensing. Sensors need to become more
Tactile sensing 19
resilient to endure mechanical stress produced by continuous operation. Perhaps the
most difﬁcult challenge is achieving full coverage of the robot body, including mov-
ing areas. At this aim new materials and manufacturing techniques for electronic
devices will be required to produce stretchable sensors, embedding wiring and elec-
tronics. We expect that robotic hands will beneﬁt the most from such technology,
with consequent improvement in manipulation capabilities.
Large scale tactile systems also pose non-trivial challenge in terms of power
consumption and networking. Solving these problem requires advances in electronic
engineering and perhaps new encoding mechanisms to reduce the energy needed to
power individual sensors, acquire and route tactile data to the processing units.
References
1. Asfour, T., Regenstein, K., Azad, P., Schroder, J., Bierbaum, A., Vahrenkamp, N., Dillmann,
R.: ARMAR-III: An integrated humanoid platform for sensory-motor control. In: 2006 6th
IEEE-RAS International Conference on Humanoid Robots, pp. 169–175 (2006). DOI 10.
1109/ICHR.2006.321380
2. Baishya S., S., Berthold, B.: Robust Material Classiﬁcation with a Tactile Skin Using Deep
Learning. Daejeon, Korea (2016)
3. Cagatay, E., K ¨ohler, P., Lugli, P., Abdellah, A.: Flexible capacitive tactile sensors based on
carbon nanotube thin ﬁlms. IEEE Sensors Journal 15(6), 3225–3233 (2015). DOI 10.1109/
JSEN.2015.2404342
4. Cannata, G., Denei, S., Mastrogiovanni, F.: Tactile sensing: Steps to artiﬁcial somatosensory
maps. In: 19th International Symposium in Robot and Human Interactive Communication,
pp. 576–581 (2010). DOI 10.1109/ROMAN.2010.5598697
5. Cannata, G., Maggiali, M.: Processing of tactile/force measurements for a fully embedded
sensor. In: 2006 IEEE International Conference on Multisensor Fusion and Integration for
Intelligent Systems, pp. 160–166 (2006). DOI 10.1109/MFI.2006.265617
6. Cheung, E., Lumelsky, V .J.: Proximity sensing in robot manipulator motion planning: system
and implementation issues. IEEE Transactions on Robotics and Automation 5(6), 740–751
(1989). DOI 10.1109/70.88096
7. Chu, V ., McMahon, I., Riano, L., McDonald, C.G., He, Q., Perez-Tejada, J.M., Arrigo, M.,
Fitter, N., Nappo, J.C., Darrell, T., Kuchenbecker, K.J.: Using robotic exploratory procedures
to learn the meaning of haptic adjectives. In: IEEE International Conference on Robotics and
Automation, pp. 3048–3055 (2013). DOI 10.1109/ICRA.2013.6631000
8. Chun, S., Jung, H., Choi, Y ., Bae, G., Kil, J.P., Park, W.: A tactile sensor using a graphene ﬁlm
formed by the reduced graphene oxide ﬂakes and its detection of surface morphology. Carbon
94, 982 – 987 (2015). DOI http://dx.doi.org/10.1016/j.carbon.2015.07.088. URL http:
//www.sciencedirect.com/science/article/pii/S0008622315301111
9. Cirillo, A., Ficuciello, F., Natale, C., Pirozzi, S., Villani, L.: A conformable force/tactile skin
for physical human–robot interaction. IEEE Robotics and Automation Letters 1(1), 41–48
(2016). DOI 10.1109/LRA.2015.2505061
10. Dahiya, R.S., Adami, A., Pinna, L., Collini, C., Valle, M., Lorenzelli, L.: Tactile sensing chips
with posfet array and integrated interface electronics. IEEE Sensors Journal 14(10), 3448–
3457 (2014). DOI 10.1109/JSEN.2014.2346742
11. Dahl, T.S., Swere, E.A., Palmer, A.: Touch-triggered withdrawal reﬂexes for safer robots. New
Frontiers in Human-Robot Interaction pp. 281–304 (2011)
12. Del Prete, A., Denei, S., Natale, L., Mastrogiovanni, F., Nori, F., Cannata, G., Metta, G.: Skin
spatial calibration using force/torque measurements. In: IEEE/RSJ International Conference
on Intelligent Robots and Systems, pp. 3694–3700 (2011). DOI 10.1109/IROS.2011.6094896
20 Lorenzo Natale, Giorgio Cannata
13. Del Prete, A., Nori, F., Metta, G., Natale, L.: Control of contact forces: The role of tactile feed-
back for contact localization. In: IEEE/RSJ International Conference on Intelligent Robots and
Systems, pp. 4048–4053 (2012). DOI 10.1109/IROS.2012.6385803
14. Denei, S., Maiolino, P., Baglini, E., Cannata, G.: On the development of a tactile sensor for
fabric manipulation and classiﬁcation for industrial applications. In: Intelligent Robots and
Systems (IROS), 2015 IEEE/RSJ International Conference on, pp. 5081–5086 (2015). DOI
10.1109/IROS.2015.7354092
15. Denei, S., Mastrogiovanni, F., Cannata, G.: Towards the creation of tactile maps for
robots and their use in robot contact motion control. Robotics and Autonomous
Systems 63, Part 3 , 293 – 308 (2015). DOI http://dx.doi.org/10.1016/j.robot.2014.
09.011. URL http://www.sciencedirect.com/science/article/pii/
S0921889014001869. Advances in Tactile Sensing and Touch-based Human Robot In-
teraction
16. Fishel, J.A., Santos, V .J., Loeb, G.E.: A robust micro-vibration sensor for biomimetic ﬁnger-
tips. In: IEEE RAS EMBS International Conference on Biomedical Robotics and Biomecha-
tronics, pp. 659–663 (2008). DOI 10.1109/BIOROB.2008.4762917
17. Fumagalli, M., Ivaldi, S., Randazzo, M., Natale, L., Metta, G., Sandini, G., Nori, F.: Force
feedback exploiting tactile and proximal force/torque sensing. Autonomous Robots 33(4),
381–398 (2012). DOI 10.1007/s10514-012-9291-2
18. Gastaldo, P., Pinna, L., Seminara, L., Valle, M., Zunino, R.: Computational intelligence tech-
niques for tactile sensing systems. Sensors 14(6), 10,952–10,976 (2014). DOI 10.3390/
s140610952. URL http://www.mdpi.com/1424-8220/14/6/10952
19. Goger, D., Gorges, N., Worn, H.: Tactile sensing for an anthropomorphic robotic hand: Hard-
ware and signal processing. In: IEEE International Conference on Robotics and Automation,
pp. 895–901 (2009). DOI 10.1109/ROBOT.2009.5152650
20. Hang, K., Li, M., Stork, J.A., Bekiroglu, Y ., Pokorny, F.T., Billard, A., Kragic, D.: Hierarchical
Fingertip Space: A Uniﬁed Framework for Grasp Planning and In-Hand Grasp Adaptation.
IEEE Transactions on Robotics 32(4), 960–972 (2016). DOI 10.1109/TRO.2016.2588879.
URL http://ieeexplore.ieee.org/document/7530865/
21. Hillis, W.D.: A high-resolution imaging touch sensor. The International Journal of Robotics
Research 1(2), 33–44 (1982). DOI 10.1177/027836498200100202. URL http://ijr.
sagepub.com/content/1/2/33.abstract
22. Hoelscher, J., Peters, J., Hermans, T.: Evaluation of tactile feature extraction for interactive
object recognition. In: IEEE-RAS International Conference on Humanoid Robots, pp. 310–
317. IEEE (2015). URL http://ieeexplore.ieee.org/xpls/abs_all.jsp?
arnumber=7363560
23. Hoof, H.v., Hermans, T., Neumann, G., Peters, J.: Learning robot in-hand manipulation with
tactile features. In: IEEE-RAS International Conference on Humanoid Robots, pp. 121–127
(2015). DOI 10.1109/HUMANOIDS.2015.7363524
24. Hoshino, Y ., Inaba, M., Inoue, H.: Model and processing of whole-body tactile sensor suit
for human-robot contact interaction. In: Robotics and Automation, 1998. Proceedings. 1998
IEEE International Conference on, vol. 3, pp. 2281–2286 vol.3 (1998). DOI 10.1109/ROBOT.
1998.680663
25. Hsiao, K., Nangeroni, P., Huber, M., Saxena, A., Ng, A.Y .: Reactive grasping using optical
proximity sensors. In: IEEE International Conference on Robotics and Automation, pp. 2098–
2105 (2009). DOI 10.1109/ROBOT.2009.5152849
26. Inaba, M., Hoshino, Y ., Nagasaka, K., Ninomiya, T., Kagami, S., Inoue, H.: A full-body tac-
tile sensor suit using electrically conductive fabric and strings. In: IEEE/RSJ International
Conference on Intelligent Robots and Systems, vol. 2, pp. 450–457 vol.2 (1996). DOI
10.1109/IROS.1996.570816
27. Iwata, H., Sugano, S.: Whole-body covering tactile interface for human robot coordination.
In: IEEE International Conference on Robotics and Automation, vol. 4, pp. 3818–3824 vol.4
(2002). DOI 10.1109/ROBOT.2002.1014315
Tactile sensing 21
28. Jamali, N., Maggiali, M., Giovannini, F., Metta, G., Natale, L.: A new design of a ﬁngertip for
the icub hand. In: IEEE/RSJ International Conference on Intelligent Robots and Systems, pp.
2705–2710 (2015). DOI 10.1109/IROS.2015.7353747
29. Jamali, N., Sammut, C.: Material classiﬁcation by tactile sensing using surface textures.
In: IEEE International Conference on Robotics and Automation, pp. 2336–2341. IEEE
(2010). URL http://ieeexplore.ieee.org/xpls/abs_all.jsp?arnumber=
5509675
30. Kageyama, R., Kagami, S., Inaba, M., Inoue, H.: Development of soft and distributed tactile
sensors and the application to a humanoid robot. In: IEEE International Conference on Sys-
tems, Man, and Cybernetics, vol. 2, pp. 981–986 vol.2 (1999). DOI 10.1109/ICSMC.1999.
825396
31. Kato, Y ., Mukai, T., Hayakawa, T., Shibata, T.: Tactile sensor without wire and sensing ele-
ment in the tactile region based on eit method. In: Sensors, 2007 IEEE, pp. 792–795 (2007).
DOI 10.1109/ICSENS.2007.4388519
32. Kerpa, O., Weiss, K., Worn, H.: Development of a ﬂexible tactile sensor system for a humanoid
robot. In: Intelligent Robots and Systems, 2003. (IROS 2003). Proceedings. 2003 IEEE/RSJ
International Conference on, vol. 1, pp. 1–6 vol.1 (2003). DOI 10.1109/IROS.2003.1250596
33. Le, T.H.L., Maiolino, P., Mastrogiovanni, F., Cannata, G., Schmitz, A.: A toolbox for sup-
porting the design of large-scale capacitive tactile systems. In: Humanoid Robots (Hu-
manoids), 2011 11th IEEE-RAS International Conference on, pp. 153–158 (2011). DOI
10.1109/Humanoids.2011.6100866
34. Li, M., Bekiroglu, Y ., Kragic, D., Billard, A.: Learning of grasp adaptation through experi-
ence and tactile sensing. In: IEEE/RSJ International Conference on Intelligent Robots and
Systems, pp. 3339–3346. Ieee (2014). URL http://ieeexplore.ieee.org/xpls/
abs_all.jsp?arnumber=6943027
35. Maiolino, P., Maggiali, M., Cannata, G., Metta, G., Natale, L.: A ﬂexible and robust large
scale capacitive tactile system for robots. Sensors Journal, IEEE 13(10), 3910–3917 (2013).
DOI 10.1109/JSEN.2013.2258149
36. Martin, T.B., Ambrose, R.O., Diftler, M.A., Platt, R., Butzer, M.J.: Tactile gloves for au-
tonomous grasping with the nasa/darpa robonaut. In: IEEE International Conference on
Robotics and Automation, vol. 2, pp. 1713–1718 V ol.2 (2004). DOI 10.1109/ROBOT.2004.
1308071
37. Metta, G., Natale, L., Nori, F., Sandini, G., Vernon, D., Fadiga, L., von Hofsten, C., Rosander,
K., Lopes, M., Santos-Victor, J., Bernardino, A., Montesano, L.: The icub humanoid robot:
An open-systems platform for research in cognitive development. Neural Networks 23(8–9),
1125 – 1134 (2010). DOI http://dx.doi.org/10.1016/j.neunet.2010.08.010. URL http://
www.sciencedirect.com/science/article/pii/S0893608010001619. So-
cial Cognition: From Babies to Robots
38. Minato, T., Yoshikawa, Y ., Noda, T., Ikemoto, S., Ishiguro, H., Asada, M.: Cb2: A child robot
with biomimetic body for cognitive developmental robotics. In: IEEE-RAS International Con-
ference on Humanoid Robots, pp. 557–562 (2007). DOI 10.1109/ICHR.2007.4813926
39. Mittendorfer, P., Cheng, G.: Humanoid multimodal tactile-sensing modules. IEEE Transac-
tions on Robotics 27(3), 401–410 (2011). DOI 10.1109/TRO.2011.2106330
40. Mittendorfer, P., Cheng, G.: Open-loop self-calibration of articulated robots with artiﬁcial
skins. In: IEEE International Conference on Robotics and Automation, pp. 4539–4545 (2012).
DOI 10.1109/ICRA.2012.6224881
41. Mittendorfer, P., Yoshida, E., Cheng, G.: Realizing whole-body tactile interactions with a self-
organizing, multi-modal artiﬁcial skin on a humanoid robot. Advanced Robotics29(1), 51–67
(2015)
42. Mizuuchi, I., Yoshikai, T., Sodeyama, Y ., Nakanishi, Y ., Miyadera, A., Yamamoto, T.,
Niemela, T., Hayashi, M., Urata, J., Namiki, Y ., Nishino, T., Inaba, M.: Development of mus-
culoskeletal humanoid kotaro. In: IEEE International Conference on Robotics and Automa-
tion, pp. 82–87 (2006). DOI 10.1109/ROBOT.2006.1641165
22 Lorenzo Natale, Giorgio Cannata
43. Mukai, T., Onishi, M., Odashima, T., Hirano, S., Luo, Z.: Development of the tactile sensor
system of a human-interactive robot RI-MAN. IEEE Transactions on Robotics24(2), 505–512
(2008). DOI 10.1109/TRO.2008.917006
44. Natale, L., Torres-Jara, E.: A sensitive approach to grasping. In: Sixth International Confer-
ence on Epigenetic Robotics (2016)
45. Ohmura, Y ., Kuniyoshi, Y .: Humanoid robot which can lift a 30 kg box by whole body con-
tact and tactile feedback. In: IEEE/RSJ International Conference on Intelligent Robots and
Systems, pp. 1136–1141 (2007). DOI 10.1109/IROS.2007.4399592
46. Ohmura, Y ., Kuniyoshi, Y ., Nagakubo, A.: Conformable and scalable tactile sensor skin for
curved surfaces. In: Proceedings 2006 IEEE International Conference on Robotics and Au-
tomation, 2006. ICRA 2006., pp. 1348–1353 (2006). DOI 10.1109/ROBOT.2006.1641896
47. Ohmura, Y ., Kuniyoshi, Y ., Nagakubo, A.: Conformable and scalable tactile sensor skin for
curved surfaces. In: IEEE International Conference on Robotics and Automation, pp. 1348–
1353 (2006). DOI 10.1109/ROBOT.2006.1641896
48. oiva, R.K., Zenker, M., Sch ¨urmann, C., Haschke, R., Ritter, H.J.: A highly sensitive 3d-shaped
tactile sensor. In: IEEE/ASME International Conference on Advanced Intelligent Mechatron-
ics, pp. 1084–1089 (2013). DOI 10.1109/AIM.2013.6584238
49. Okamura, A.M., Smaby, N., Cutkosky, M.R.: An overview of dexterous manipulation. In:
IEEE International Conference on Robotics and Automation, vol. 1, pp. 255–262 vol.1 (2000).
DOI 10.1109/ROBOT.2000.844067
50. Petryk, G., Buehler, M.: Dynamic object localization via a proximity sensor network. In:
IEEE/SICE/RSJ International Conference on Multisensor Fusion and Integration for Intelli-
gent Systems, pp. 337–341 (1996). DOI 10.1109/MFI.1996.572197
51. Regoli, M., Pattacini, U., Metta, G., Natale, L.: Hierarchical grasp controller using tactile feed-
back. In: Proceedings of IEEE-RAS International Conference on Humanoid Robots (2016)
52. Roncone, A., Hoffmann, M., Pattacini, U., Metta, G.: Learning peripersonal space representa-
tion through artiﬁcial skin for avoidance and reaching with whole body surface. In: IEEE/RSJ
International Conference on Intelligent Robots and Systems, pp. 3366–3373 (2015). DOI
10.1109/IROS.2015.7353846
53. Sauser, E.L., Argall, B.D., Metta, G., Billard, A.G.: Iterative learning of grasp adaptation
through human corrections. Robotics and Autonomous Systems60(1), 55–71 (2012). DOI 10.
1016/j.robot.2011.08.012. URL http://linkinghub.elsevier.com/retrieve/
pii/S0921889011001631
54. Schill, J., Laaksonen, J., Przybylski, M., Kyrki, V ., Asfour, T., Dillmann, R.: Learning con-
tinuous grasp stability for a humanoid robot hand based on tactile sensing. In: IEEE RAS
& EMBS International Conference on Biomedical Robotics and Biomechatronics, pp. 1901–
1906. IEEE (2012). URL http://ieeexplore.ieee.org/xpls/abs_all.jsp?
arnumber=6290749
55. Schmitz, A., Maiolino, P., Maggiali, M., Natale, L., Cannata, G., Metta, G.: Methods and tech-
nologies for the implementation of large-scale robot tactile sensors. Robotics, IEEE Transac-
tions on (3), 389 –400 (2011). DOI 10.1109/TRO.2011.2132930
56. Schmitz, A., Pattacini, U., Nori, F., Natale, L., Metta, G.: Design, realization and sensorization
of a dextrous hand: the iCub design choices. In: IEEE-RAS International Conference on
Humanoid Robots (2010). DOI 10.1109/ICHR.2010.5686825
57. Shimojo, M., Namiki, A., Ishikawa, M., Makino, R., Mabuchi, K.: A tactile sensor sheet using
pressure conductive rubber with electrical-wires stitched method. IEEE Sensors Journal 4(5),
589–596 (2004). DOI 10.1109/JSEN.2004.833152
58. Sinapov, J., Sukhoy, V ., Sahai, R., Stoytchev, A.: Vibrotactile Recognition and Categorization
of Surfaces by a Humanoid Robot. IEEE Transactions on Robotics 27(3), 488–497 (2011).
DOI 10.1109/TRO.2011.2127130
59. Taichi, T., Takahiro, M., Hiroshi, I., Norihiro, H.: Automatic categorization of haptic inter-
actions -what are the typical haptic interactions between a human and a robot? In: 2006
6th IEEE-RAS International Conference on Humanoid Robots, pp. 490–496 (2006). DOI
10.1109/ICHR.2006.321318
Tactile sensing 23
60. Tegin, J., Ekvall, S., Kragic, D., Wikander, J., Iliev, B.: Demonstration-based learning and
control for automatic grasping. Intelligent Service Robotics 2(1), 23–30 (2009). URL http:
//link.springer.com/article/10.1007/s11370-008-0026-3
61. Tomo, T.P., Somlor, S., Schmitz, A., Hashimoto, S., Sugano, S., Jamone, L.: Development of
a hall-effect based skin sensor. In: SENSORS, 2015 IEEE, pp. 1–4 (2015). DOI 10.1109/
ICSENS.2015.7370435
62. Torres-Jara, E., Vasilescu, I., Coral, R.: A soft touch: Compliant tactile sensors for sensitive
manipulation (2016). URL http://hdl.handle.net/1721.1/31220
63. Wettels, N., Popovic, D., Santos, V .J., Johansson, R.S., Loeb, G.E.: Biomimetic tactile sensor
for control of grip. In: IEEE 10th International Conference on Rehabilitation Robotics, pp.
923–932 (2007). DOI 10.1109/ICORR.2007.4428534
64. Xu, D., Loeb, G.E., Fishel, J.A.: Tactile identiﬁcation of objects using Bayesian exploration.
In: IEEE International Conference on Robotics and Automation, pp. 3056–3061 (2013). DOI
10.1109/ICRA.2013.6631001
65. Yin, X., Vinod, T.P., Jelinek, R.: A ﬂexible high-sensitivity piezoresistive sensor comprising
a au nanoribbon-coated polymer sponge. J. Mater. Chem. C 3, 9247–9252 (2015). DOI
10.1039/C5TC01604E. URL http://dx.doi.org/10.1039/C5TC01604E
66. Yousseﬁ, S., Denei, S., Mastrogiovanni, F., Cannata, G.: A real-time data acquisition and pro-
cessing framework for large-scale robot skin. Robot. Auton. Syst. 68(C), 86–103 (2015).
DOI 10.1016/j.robot.2015.01.009. URL http://dx.doi.org/10.1016/j.robot.
2015.01.009
67. Yousseﬁ, S., Denei, S., Mastrogiovanni, F., Cannata, G.: Skinware 2.0: A real-time middle-
ware for robot skin. SoftwareX 3–4, 6 – 12 (2015). DOI http://dx.doi.org/10.1016/j.softx.
2015.09.001. URL http://www.sciencedirect.com/science/article/pii/
S2352711015000102
