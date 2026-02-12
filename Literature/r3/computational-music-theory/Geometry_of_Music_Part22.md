# 

**Author:**   
**Subject:**   
**Total Pages:** 469  
**Source File:** `Geometry_of_Music.pdf`

---

**Part 22 of 24** (Pages 421-440)

---

## Page 421

appendix b 402
pitches x and x + 12. We begin by constructing a region  of the original space contain-
ing one point for every pitch class. This is an ordinary line segment such as that in 
Figure B1b, consisting of all points greater than or equal to zero, and less than 12. 
(Note that our ﬁ  gure does not include the point 12, since it represents the same pitch 
class as zero; however, it contains every point less than 12, including points inﬁ  nitesi-
mally close to 12.) Because this is just a line segment, there is no reason (yet!) to say 
that the points at different ends are close together. It is only when we start to use the 
space to represent distances or trajectories in our original pitch space that we notice 
that it its endpoints are related: for instance, the motion shown in Figure B1c disap-
pears off the right edge of our line segment to reappear on the left. This tells us that 
the two edges of the line segment should be glued together, and that two points near 
Figure B1 (a) Pitch space is a line. ( b) The region 0 £ x < 12 contains one point for 
every pitch class. ( c) The line segment 59 ®64 disappears off the right edge of our region, 
reappearing on the left. ( d) This tells us that we should attach the right edge to the left, 
forming a quotient space . We can represent this quotient space as a circle in two dimensions. 
Alternatively, we could simply add a new point, 12, to the right edge of our space and declare 
it to be the same as the point at the left edge.

## Page 422

Appendix B 403
opposite ends are actually close together. We can express this visually by bending the 
line segment, producing the familiar pitch-class circle shown in Figure B1d. Alterna-
tively, we could simply add the point 12 to the right edge, declaring it to be the same 
as the point 0 on the left.1
Our goal, then, is to determine how to identify a region of n-dimensional Euclid-
ean space containing one point for every unordered set of n pitch classes.2 To  do  
this, we can choose the region containing all and only those chords whose pitches 
(1) are in nondescending order, (2) span no more than an octave, and (3) together 
sum to a number less than 12 and greater than or equal to zero.3 Clearly, by reorder-
ing and octave transposing, we can transform any sequence into one that meets the 
ﬁ rst two criteria: for instance, we can turn (G4, C3, E5) into (C4, E4, G4), which is in 
nondescending order and spans no more than an octave. However, the pitches (C4, 
E4, G4) do not meet the third criterion, since the numbers (60, 64, 67) sum to 191. 
Observe, though, that we can reduce their sum by 12 by transposing the last note 
down by octave and moving it to the front of the list. (In Chapter 4 we describe this 
process as transposition by one descending step along the “scale” C-E-G.) The result-
ing sequence, (G3, C4, E4), sums to 179 (or 191 – 12), while still meeting the other 
criteria. By repeating this process, therefore, we can eventually bring the sum into the 
range 0 £ x < 12.4
Our region is therefore bounded by the following mathematical inequalities:
 x1 £ x2 £  . . . £ xn £ x1 + 12 (B.1)
 0 £ x1 + x2+ x3 + . . . + xn < 12 (B.2)
Equation B.1 says that the pitches are in nondescending order, spanning no more 
than an octave. Equation B.2 says that the sum of the pitches is greater than or equal 
to zero, and less than 12. T ogether, these inequalities determine a region of inﬁ  nite 
n-dimensional Cartesian space, in which there is exactly one point for every collection 
of n unordered pitch classes. Of course, points in this region still represent ordered 
pitch sequences,  and not chords proper; in this sense the region, like a single tile of 
wallpaper, is a kind of steppingstone between our original “ordered pitch space” and 
the topologically complex “unordered chord space” we are trying to construct.
Before I try to explain what this region looks like, I should note that in some 
sense, complicated mathematics is unnecessary. For if we wanted to, we could sim-
ply program a computer to display the lower dimensional chord spaces directly. 
There are numerous computer graphics packages that allow users to draw in two- or 
1 In fact, this might be preferable since it shows that our quotient space is intrinsically one-dimensional; 
the circular representation may falsely suggest that the space has two dimensions.
2 There will actually be many different regions satisfying this criterion, of varying shapes; in what fol-
lows, I will describe a region that is particularly useful.
3 I use “nondescending” rather than “ascending” because I want to include chords that have pitch dupli-
cations, such as (C4, C4, C4, E4).
4 This process will never run afoul of the other two constraints, since the original ordering spans no 
more than an octave.

## Page 423

appendix b 404
 three-dimensional space; using the algorithm in Figure B2, we can transform any 
arbitrary ordered pitch sequence into a point lying in our region, and can thus graph 
arbitrary chords in the space. Furthermore, as explained in Chapters 2 and 3, we can 
graph voice leadings simply by imagining that each voice glides smoothly from its 
origin to the destination. (A computer can be programmed to provide the illusion 
of a smooth glide by taking discrete steps that are too small for the eye to follow.) At 
each stage along the glide, we project the current point into our fundamental region. 
Were we to do this, we would immediately see the shapes in Figures 3.3.1 and 3.8.2. 
Furthermore, as we plotted various voice leadings on the ﬁ  gure, we would ﬁ  nd that 
our algorithm automatically accounts for the space’s “exotic” boundary points: some 
boundaries would act like mirrors, while others would seem to be glued together. 
(That is, we would sometimes see a trajectories disappear off one part of the ﬁ  gure to 
reappear on another.) For someone who is not comfortable with geometry or abstract 
mathematics, or for someone who does not recognize what shapes Eqs. B.1 and B.2 
correspond to, this sort of direct, intuitive hands-on exploration may perhaps be the 
easiest way to proceed.
However, my job here is to try to explain—in a principled way—how to under-
stand the two sets of inequalities. In preparation for this task, I will review several 
elementary musico-geometrical facts.
 Fact 1 . Transposition is represented by adding a constant to every note in 
a chord: ( x1 + t, x2 + t, . . . , xn + t) is the transposition of ( x1, x2, . . . , xn) by 
t semitones (§2.1).
 Fact 2 . Geometrically, adding t to every note in a chord corresponds to moving 
in parallel to the “unit diagonal” that connects (0, 0, . . . , 0) to (1, 1, . . . , 1) 
(Figure B3).
Figure B2 An algorithm for moving any ordered pitch set into the fundamental region 
deﬁ ned by equations (1) and (2).

## Page 424

Appendix B 405
 Fact 3 . The equation x1 + x2 . . . xn = c determines a higher dimensional 
analogue to the plane—a “hyperplane”—perpendicular to the unit diagonal 
described in Fact 2 (Figure B3).5
 Fact 4 . There is exactly one transposition of any ordered pitch sequence 
with elements that sum to any particular value. The number t = (c − x1 − x2 
− . . . − xn)/n is the unique transposition such that ( x1 + t, x2 + t, . . . , xn + 
t) sums to c. Geometrically, this means that there is a unique way to move 
any point p parallel to the unit diagonal until it reaches an arbitrary plane 
perpendicular to that diagonal (Figure B3).
transposition       contains pairs
of pitches summing to 0
first notesecond note(a, b)
(1, 1)
(0, 0)(a/2 – b/2, b/2 – a/2)Figure B3 Transposition is 
represented by motion parallel to 
the line stretching from (0, 0) to 
(1, 1). The planes perpendicular 
to this line contain chords 
summing to a constant value.
Armed with these facts, let us return to our two equations:
 x1 £ x2 £  . . . £ xn £ x1 + 12 (B.1)
 0 £ x1 + x2+ x3 + . . . + xn < 12 (B.2)
Fact 3 tells us that Eq. B.2 determines a collection of hyperplanes perpendicular to 
the line connecting (0, 0, 0, . . . , 0) to (1, 1, 1 . . . , 1), with sums in the range 0 £ c < 12. 
By Fact 2, these hyperplanes are related by transposition.6 Next, we observe that if any 
5 The term “hyperplane” refers to a ﬂ  at Euclidean space with one fewer dimension than the n-dimen-
sional space in which it resides. T o see that the equation x1 + x2 + . . . + xn = c determines a hyperplane, it 
helps to know that any linear  equation a1x1 + a2x2 + . . . + anxn = c, with the ai all real numbers, determines 
a hyperplane. (Intuitively, we can freely choose n − 1 of the n coordinates, with the ﬁ  nal coordinate being 
determined by our earlier choices.) T o see that the plane is perpendicular to the line connecting (0, 0, . . . , 
0) to (1, 1, . . . , 1) recall that two vectors are perpendicular when x • y  = 0. (Here “•” is the dot product of 
linear algebra: x1  y1 + x2  y2 + . . . + xn  yn.) That is, ( x1, x2, . . . , xn) • (1, 1, . . . , 1) = 0, or x1 + x2 + . . . xn = 0. Thus 
the ( n − 1)-dimensional plane x1 + x2 + . . . xn = 0 contains vectors perpendicular to the vector (1, 1, . . . , 1). 
The expression ( x1, x2, . . . , xn) • (1, 1, . . . , 1) = c, or x1 + x2 + . . . xn = c, identiﬁ  es the hyperplane that is c units 
away along the line connecting (0, 0, . . . , 0) to (1, 1, . . . , 1).
6 If two of our hyperplanes sum to c1 and c2, then they are related by ( c2 − c1)/n semitone transposition, 
with n being the size of the chord.

## Page 425

appendix b 406
ordered pitch sequence satisﬁ  es the ﬁ  rst set of inequalities (Eq. B.1), then so do all its 
transpositions. (This is just to say that if an ordered pitch sequence is in nondescend-
ing order spanning less than an octave, then its transpositions are, too.) It follows 
that Eq. B.1 determines the same shape in each of the cross sections x1 + x2 . . . + xn = c. 
The space of musical chords is therefore some sort of prism:  the inequalities x1 £ x2 
£ . . . £ xn £ x1 + 12 determine the shape of the cross section, while the equation x1 + x2 
+ x3 + . . . + xn = c identiﬁ  es the particular cross section containing pitch sequences 
summing to c.
The next problem is to determine the shape of the cross section. We begin by 
reviewing the deﬁ  nition of a “simplex”—an n-dimensional ﬁ  gure bounded by the 
lines interconnecting n + 1 vertices.7 (A simplex is so-called because it is, in some 
sense, the “simplest” n-dimensional ﬁ  gure, with the minimal number of vertices.) In 
two dimensions, the simplex’s three vertices determine a triangle. In three dimen-
sions, the four vertices determine a tetrahedron. Mathematicians sometimes use the 
term “the standard simplex” to refer to the simplex bounded by the endpoints of the 
basis vectors in n-dimensional Cartesian space. Figure B4 shows that the basis vectors 
in two-dimensional space deﬁ  ne a one-dimensional simplex stretching from (0, 1) to 
(1, 0); the three basis vectors in three-dimensional space determine a simplex stretch-
ing from (1, 0, 0) to (0, 1, 0) to (0, 0, 1). (The higher dimensional ﬁ  gures, although 
harder to visualize, are analogous.) Every point in these two simplexes is represented 
by coordinates that are all nonnegative and sum to one. For this reason, these sim-
plexes are important in applications in which a total quantity of “stuff” is divided up 
into a ﬁ  xed number of parts: for example, the one-dimensional simplex in Figure B4 
might be used to represent the result of an election featuring two candidates, while 
the two-dimensional simplex might be used for a three-party election.
(0, 1)
(1, 0)(0, 1, 0)
(1, 0, 0)(0, 0, 1)
xxzyyFigure B4 The “standard simplex” in two-dimensional space is a one-dimensional 
line segment (i.e. a one-dimensional simplex) stretching from (1, 0) to (0, 1); in three 
dimensional space, it is a two-dimensional triangle (two-dimensional simplex) bounded by 
(1, 0, 0), (0, 1, 0), and (0, 0, 1). The standard simplex contains all points with nonnegative 
coordinates summing to 1.
7 Strictly speaking, the vertices must be “afﬁ  nely independent”—that is, that there should be no c-di-
mensional plane containing more than c + 1 of the points.

## Page 426

Appendix B 407
Now a mathematician would immediately recognize that the equation x1 £ x2 
£ . . . £ xn £ x1 + 12 determines a simplex in the hyperplane x1 + x2 + x3 + . . . + xn = 
c. There are a number of ways to see why this is so.8 Perhaps the most instructive is 
to note that there is a close relation between our equations and the standard sim-
plex described in the previous paragraph. T o see why, note that we can rewrite the 
inequalities x1 £ x2 £ . . . £ xn £ x1 + 12 as
 xi – xi–1 ³ 0 for 1 < i £ n
 x1 + 12 – xn ³ 0
Since xi − xi − 1 is the interval from note xi − 1 to xi , our new inequalities simply say that 
the intervals between adjacent notes in the sequence are all nondescending, including 
the “wraparound” interval from the last note, xn, to the note an octave above the ﬁ  rst, 
x1 + 12. Furthermore, these n positive numbers must sum to 12, since they begin with 
x1 and end with x1 + 12. Dividing by 12 therefore gives us the coordinates of a point 
in the standard simplex.9 Conversely, for any point in the standard simplex, we can 
multiply its coordinates by 12 and construct a pitch sequence with those numbers as 
its consecutive intervals. According to Fact 4, there will be one and only one transpo-
sition of this sequence lying in the hyperplane x1 + x2 + x3 + . . . + xn = c.10 We conclude 
that there is a “coordinate transforma-
tion” sending our original simplex, in 
which numbers represent pitches,  into 
the standard simplex, in which the 
numbers represent intervals,  as mea-
sured in fractions of an octave (Figure 
B5). Mathematicians will recognize 
that this coordinate change is an “afﬁ  ne 
transformation,” which means that it 
transforms one simplex into another. 
It follows that our original inequalities 
determine a simplex as well.11
 8 The simplest is to note that each of the inequalities xi £ xj carves the space into two halves, bounded 
by the hyperplane xi = xj . If n such half-spaces determine a ﬁ  nite region in ( n − 1)-dimensional space, then 
that region is bounded by n hyperplanes, which is just to say that it is a simplex.
 9 For example, beginning with the pitch sequence (60, 64, 67) we can construct the interval sequence 
(4, 3, 5) representing the interval from 60 to 64, from 64 to 67, and from 67 to the note an octave above 60. 
Dividing by 12 gives us (4/12, 3/12, 5/12) which is a point on the standard simplex.
10 For instance, we multiply (½, ½, 0) by 12 to obtain the sequence of intervals (6, 6, 0). We then 
 construct a sequence of pitches whose successive notes are separated by these intervals, for instance (F s2, 
C3, F s3) or (42, 48, 54). These values sum to 144; transposing down by four octaves gives (−6, 0, 6), which 
sums to zero.
11 Suppose x and y are two points that the coordinate transformation sends to x' and y'. An afﬁ  ne 
transformation sends the point x + b (y − x ) to the point x' + b (y' − x' ), thus transforming a line in the 
original space into a line in the second. (It is easily checked that the coordinate transformation in Figure 
B5 is afﬁ  ne.) Algebraically, afﬁ  ne transformations represent the new coordinates as linear functions of the 
old coordinates—e.g. functions like x1' = ax1 + bx2 + c, which do not involve higher powers of the original 
variables x1 and x2.Original
CoordinateNew
Coordinate 
x1 x2 – x1)/12
x2(
(x3 – x2)/12 
……  
xn ( x1 + 12 – xn)/12 Figure B5 The coordinate transformation 
from pitch-class space, in which coordinates 
represent numbers, to interval space, in which 
they represent intervals.

## Page 427

appendix b 408
We conclude, therefore, that our fundamental region is a prism whose face is a 
simplex. The lower face is determined by the equations
 x1 + x2 + x3 + . . . + xn = 0 and x1 £ x2 £ . . . £ xn £ x1 + 12
This simplex is “extruded” along the line connecting (0, 0, . . . , 0) to (1, 1, . . . , 1), a pro-
cess that corresponds musically to transposing upward, and algebraically to increas-
ing the sum of the chords in the cross section
 x1 + x2 + x3 + . . . + xn = c and x1 £ x2 £ . . . £ xn £ x1 + 12,
with the parameter c varying from 0 to 12. Each layer of the prism contains pitch 
sequences with a different sum; we can transpose until the sum is equal to 12, at 
which point we return to the chords that appear on the sum-zero face.
Fact 4 tells us that any ordered pitch sequence satisfying Eq. B.1 has exactly one 
transposition in each cross section of the space. This means that no two ordered 
pitch sequences in the same cross section are transpositionally related. However, the 
cross sections will contain sequences that are transpositionally related when we ignore 
octave and order . For suppose ( x1, x2, . . . , xn) satisﬁ  es Eqs. B.1 and B.2. Then,
 ( x2 – 12/n, x3 – 12/ n, . . . , xn – 12/n, x1 + 12 – 12/ n)
will as well. (Those of you who have read Chapter 4 will note that this operation 
combines a chromatic transposition by –12/ n semitones with a scalar transposition 
by one ascending step.12) As ordered pitch sequences, these are not transposition-
ally related, but if we disregard octave and order, they are.13 Thus, given an n-note 
sequence meeting our criteria, we can easily construct another by moving the ﬁ  rst 
note of the sequence to the end, adding 12 to it, and subtracting 12/ n from every note 
in the resulting sequence. For example, starting with (0, 4, 7), we generate (4 − 12/3, 
7 − 12/3, 12 − 12/3) or (0, 3, 8). Repeating this procedure gives (3 − 4, 8 − 4, 12 − 4) 
or (−1, 4, 8). A ﬁ  nal repetition returns us to (0, 4, 7), where we began. Musically, the 
sequences (0, 4, 7), (0, 3, 8), and (−1, 4, 8) represent C major, A f major, and E major 
triads, each in a different mode or registral inversion: (0, 4, 7) is a C major chord 
whose ﬁ  rst note is its root, (0, 3, 8) is an A f major chord starting on its third, and (−1, 
4, 8) is an E major chord starting with its ﬁ  fth.14 In general, every n-note chord type 
will appear in each cross section n times, in each of its modes.
T o determine the vertices of our cross section, we can exploit the relation with the 
standard simplex. In three dimensions, the standard simplex is bounded by the points 
(1, 0, 0), (0, 1, 0), and (0, 0, 1), which will correspond to the vertices of our cross sec-
tion. Multiplying by 12 transforms these numbers into the interval sequences (12, 0, 0), 
12 That is, it sends ( x1, x2, . . . , xn) to ( x2, . . . , xn, x1 + 12), transposing up by one scale step, and then sub-
tracts 12/ n from these coordinates, transposing chromatically downward by 12/ n.
13 If we ignore octave and order ( x1, x2, . . . , xn) is the same as ( x2, . . . , xn, x1 + 12). Subtracting 12/ n from 
each number transposes the chord downward.
14 Remember that to ﬁ  nd the pitch class to which a number belongs, add or subtract 12 until it lies in 
the range 0 £ x < 12. Thus the number −1 refers to the pitch class B.

## Page 428

Appendix B 409
(0, 12, 0), and (0, 0, 12). Each determines a unique sequence of pitches on the face that 
sums to 0: (−8, 4, 4), (−4, −4, 8), and (0, 0, 0), or in scientiﬁ  c pitch notation (E–2, E–1, 
E–1), (G s–2, G s–2, G s–1), and (C–1, C–1, C–1). In other words, they represent the three 
“modes” of the “scale” containing just one pitch class (Figure B6). The same procedure 
of course works in other dimensions: the boundaries of the cross section can always be 
determined by ﬁ  nding the pitch sequences summing to zero, and whose one-step scalar 
intervals are (12, 0, . . . , 0), (0, 12, 0, . . . , 0), (0, 0, 12, . . . , 0), . . . , and (0, 0, . . . , 0, 12).
Two Notes Three Notes Four Notes Five Notes 
(0, 0) (0, 0, 0) (0, 0, 0, 0) (0, 0, 0, 0, 0) 
(–6, 6) (–4, –4, 8) (–3, –3, –3, 9) (–2.4, –2.4, –2.4, –2.4, 9.6) 
(–8, 4, 4) (–6, –6, 6, 6) (–4.8, –4.8, –4.8, 7.2, 7.2) 
(–9, 3, 3, 3) (–7.2, –7.2, 4.8, 4.8, 4.8) 
(–9.6, 2.4, 2.4, 2.4, 2.4) Figure B6 
The vertices of 
the zero-sum 
cross section 
in various 
dimensions.
The ﬁ  nal step is to understand the “strange” points on the boundary of our region. 
We begin by considering how to attach the sum-zero face at one edge of the prism to 
the opposite, sum-12 face.15 Suppose that ( x1, x2, . . . , xn) lies on the face of the prism 
summing to zero. Recall that the following chords all lie on the same face.
 A1 = (x1, x2, . . . , xn)
 A2 = (x2 – 12/n, x3 – 12/ n, . . . , xn – 12/n, x1 + 12 – 12/ n)
 A3 = (x3 – 24/n, x4 – 24/ n, . . . , xn – 24/n, x1 + 12 – 24/ n, x2 + 12 – 24/ n)
 .
 .
 .
 An = (xn – 12 + 12/ n, x1 + 12/ n, . . . , xn–1 + 12/n)
If we transpose these chords up by 12/ n semitones, we obtain a series of chords that 
sum to 12:
 A1¢ = (x1 + 12/n, x2 + 12/ n, . . . , xn + 12/n)
 A2¢ = (x2, x3, . . . , xn, x1 + 12)
 A3¢ = (x3 – 12/n, x4 – 12/ n, . . . , xn – 12/n, x1 + 12 – 12/ n, x2 + 12 – 12/ n)
 .
 .
 .
 An¢ = (xn – 12 + 24/ n, x1 + 24/ n, . . . , xn–1 + 24/n)
15 Note that we have excluded this sum-12 face from our fundamental domain, since it contains the 
same chords as the sum-0 face. However, when we are constructing the quotient space, we need to think 
about how to attach various points on the boundaries. As in Figure B1d, we therefore add extra points, 
declaring them to be “the same” as some that we have already included.

## Page 429

appendix b 410
As ordered pitch sequences, A1¢ is the transposition of A1, A2¢ is the transposition of A2, 
and so on. But when we disregard octave and order, then A1 and A2¢ are the same chord , 
as are A2 and A3¢, A3 and A4¢, etc. Therefore we need to imagine that the sum-zero face 
of the prism should be attached to the opposite (sum-12) face with a “twist.” This 
twist acts as a cyclic permutation  of the simplex’s vertices, connecting Ai to A ¢i + 1.
Finally, we consider the boundary points such as ( x, y, y ), which contain pitch 
duplications. Consider a point in the interior of our simplex, such as ( x1, x2 − c, x2 
+ c), with c some small positive number. As c goes to zero, the point ( x1, x2 − c, x2 + 
c) approaches ( x1, x2, x2), moving in a line toward the boundary of the cross section. 
When c becomes negative, the ordered pitch sequence ( x1, x2 − c, x2 + c) lies outside 
of our fundamental region, since the second number is now greater than the third. 
According to the algorithm in Figure B2, then, we need to reorder the sequence so 
that it returns to our region. This reordering returns us to a point on the line segment 
along which we have just been traveling, since ( x1, x2 − (− c), x2 + (– c) ) is a reordering 
of (x1, x2 − c, x2 + c). It follows that the boundaries containing pitch duplications act 
like mirrors: a point moving directly toward the boundary is “reﬂ  ected” backward 
along its approaching trajectory.16
Putting it all together then, the space of n-note chords is an n-dimensional prism 
whose simplicial (“simplex-shaped”) faces are glued together with a twist, and whose 
remaining boundaries act like mirrors. By attributing this behavior to our bound-
ary points, we have ﬁ  nally managed to convert our fundamental region—an unre-
markable portion of ordinary Cartesian space—into a quotient space  (or orbifold ), 
an exotic mathematical space with a nontrivial topology. Mathematicians would 
describe our quotient space as “the n-torus modulo the symmetric group that acts 
on n elements”—symbolically, Tn/Sn. Here, Tn is the mathematical symbol for the 
n-torus, the space of ordered pitch-class sequences; Sn refers to the collection of oper-
ations that reorder n elements; and the division symbol instructs us to glue together 
points related by the operations that follow. Thus the mathematical symbol “ Tn/Sn” 
means “the space that results when you start with ordered pitch-class sequences and 
disregard order.” As discussed in Chapter 3, this is something very much like the space 
of chords  as musicians ordinarily conceive of them.17
Readers are now prepared to plot voice leadings in the space. T o do this, we must 
augment the algorithm in Figure B2 with two additional rules. First, when trans-
posing or reordering the notes in a voice leading, we must always do so uniformly, 
applying the same operations to both chords: if we transpose the ﬁ  rst note in the ﬁ  rst 
chord up by octave, then we must transpose the ﬁ  rst note in the second chord up by 
octave as well; similarly, if we exchange the ﬁ  rst and second notes in the ﬁ  rst chord, 
16 This argument considers trajectories moving perpendicular toward the boundary. More general tra-
jectories can be decomposed into a perpendicular and parallel components; the argument can then be 
applied to the perpendicular component.
17 Of course, musicians typically consider (C, C, E, G) to be the same as (C, E, G). When modeling voice 
leading, however, we often do not want to do this, as it can disrupt the relationship between distance and 
voice-leading size. See Callender, Quinn, and Tymoczko 2008.

## Page 430

Appendix B 411
then we must do the same in the second. Second, we may sometimes ﬁ  nd that we can 
move a line segment into our fundamental domain only by breaking it into pieces. 
For example, suppose we would like to plot the voice leading (C4, E f4, Gf4)®(Ef4, 
Gf4, C5), or (60, 63, 66) ®(63, 66, 72), which shifts the C diminished chord up by 
one scale step. T o get the sum of the ﬁ  rst chord’s notes to lie between 0 and 12, we 
must transpose down by ﬁ  ve octaves; this means we need to transpose the second 
chord down by ﬁ  ve octaves as well, producing (0, 3, 6) ®(3, 6, 12). Here we encoun-
ter a problem. The ﬁ  rst part of this line segment—from (0, 3, 6) to just before (1, 4, 
7)—lies within our region, since its chords sum to less than 12. However, the rest of 
the line segment—(1, 4, 7) ®(3, 6, 12)—sums to 12 or more. We therefore split the 
voice leading into two parts: (0, 3, 6) ®(1, 4, 7) and (1, 4, 7) ®(3, 6, 12). T o move the 
second part of the voice leading into our fundamental region, we lower the ﬁ  nal note 
in each chord by 12 and move it to the front of the list. (Once again, we do this uni-
formly, applying the same transposition and reordering to both chords.) This gives 
us (−5, 1, 4) ®(0, 3, 6), which is a line segment that begins on the lowest (sum-zero) 
face of the prism and moves to (0, 3, 6). Our voice leading (C4, E f4, G f4)®(Ef4, 
Gf4, C5) therefore disappears off the top face of the fundamental region, reappearing 
on the bottom. A little experimentation will show that any one-step ascending scalar 
transposition, in any chord space of any dimension, moves off the top face to reap-
pear on the bottom in a very similar way.
The fundamental idea here—and it is both simple and profound—is that ordi-
nary numbers provide a natural and musically meaningful set of geometrical coordi-
nates, with points representing chords and line segments representing voice leadings. 
Any sequence of numbers can be understood as an ordered list of pitches, while any 
pair of (equal-length) sequences can be understood as a voice leading in pitch space. 
When we disregard octave and order information, we are restricting our attention 
to a region of Cartesian space deﬁ  ned by Eqs. B.1 and B.2 above. This involves mov-
ing arbitrary points and line segments into our region. If we do this carefully and 
thoughtfully, we realize that the boundaries of this region have special properties. 
In other words, we make the transition from regions of ordinary Euclidean space to 
quotient spaces proper.18
18 Note that it is often possible to work with the original Cartesian coordinates: it is obvious that the 
voice leading (60, 64, 67) ®(64, 60, 67) exchanges two notes, and hence bounces off a mirror boundary, 
and that (60, 64, 67, 70) ®(64, 67, 70, 72) is an ascending one-step scalar transposition, and hence is rep-
resented by a path that disappears off the sum-12 face to reappear on the sum-zero face, returning to its 
starting point. After a little practice, you will start to feel comfortable with statements such as “there is a 
tritone halfway between (C4, G4) and (C s4, Fs4)”—and even with more difﬁ  cult tasks, such as imagining 
the cross section of an arbitrary voice leading in three-note chord space.

## Page 431

appendix c
Discrete V oice-Leading Lattices
In recent decades, music theorists have produced a number of graphs representing 
voice-leading relationships. Often, these graphs seem to imply something like the fol-
lowing methodology. First, one selects some interesting domain of chords and some 
interesting set of voice-leading relationships among them. (For example, semitonal 
voice leading among major, minor, and augmented triads.) Second, one constructs a 
graph representing all of the voice-leading relationships among all of the objects in 
question. Third, one interprets the resulting graph as providing a measure of distance 
between the objects it contains. Thus, for example, one might use the graph to ana-
lyze music that moves between nonadjacent chords, or claim that larger leaps on the 
graph are musically disfavored in some way.
However, this third step involves a subtle logical leap. For while the method generates 
graphs whose local  structure is perfectly clear, it does not follow that the graphs’ global  
structure is equally meaningful. Consider, for example, the familiar Tonnetz —invented 
by Leonhard Euler, made famous by Hugo Riemann, and resurrected by contemporary 
theorists such as Lewin, Hyer, and Cohn (Figure C1).1 Two triads are adjacent on the 
Tonnetz  if they can be linked by what Cohn calls “parsimonious” voice leading, voice 
leading in which a single voice moves, and it moves by just one or two semitones. How-
ever, there is no similarly intuitive way to characterize larger distances in the space. On 
the Tonnetz,  C major is two units away from F major but three  units from F minor—
even though it takes just two semitones to move from C major to F minor, and three 
to move from C major to F major (Figure C2). (This is precisely why F minor so often 
appears as a passing chord between F major and C major.) It follows that we cannot use 
the Tonnetz  to model the ubiquitous IV–iv–I progression, in which the two-semitone 
motion ^6®^5 is broken into the semitonal steps ^6®f^6®^5. More generally, it shows 
that Tonnetz  distances do not correspond to voice-leading distances. (Nor do they cor-
respond to common tone distances: both F minor and E f minor are three Tonnetz  steps 
away from C major, even though C major and F minor have one common tone, while 
C major and E f minor have none.) Indeed, it is an open question whether there is any 
intuitive notion of musical distance that is being modeled here.2
1 For a history of the Tonnetz,  see Mooney 1996. For a general discussion of recent work featuring vari-
ous analogous discrete lattices, see Cohn 1998a.
2 Tymoczko 2009a notes that the Tonnetz  may capture an acoustic  conception of distance, according to 
which C3 is particularly close to its second overtone G4; the point here is that this is very different from 
voice-leading or common-tone distance.

## Page 432

Appendix C 413
A surprising number of discrete music-theoretical graphs suffer from similar 
problems. For example, the graph in Figure C3 shows single-semitone voice leadings 
among diminished, dominant, French sixth, and half-diminished seventh chords.3 
While it would be entirely appropriate to use it to analyze a passage that moves by sin-
gle-semitone voice leading between these chords, it is problematic to use it to model 
voice-leading distance between nonadjacent chords: the graph contains no two-step 
path between C7 and Aø7, even though the chords can be connected by two-semitone 
voice leading. For another example, consider Figure C4a, which represents single 
semitone voice-leading among major thirds and perfect fourths. On this graph, {C, F} Figure C1 Two versions of the Tonnetz . In ( a) points represent notes, and chords are 
represented by triangles. In ( b), points represent chords, and hexagons represent single notes. 
(For example, the hexagon containing C and f can be associated with the note C, common to 
all six of its triads.)
3 This graph is quite similar to Douthett and Steinbach’s “Power T owers” (1998).

## Page 433

appendix c 414
Figure C2 (a) On the Tonnetz,  F major (triangle 3) is closer to C major (triangle 1) than F minor 
(triangle 4) is. Consequently, the voice leading (C, E, G) ®(C, F, A) is represented as a two-step 
motion, while it takes at least three  steps to represent (C, E, G) ®(C, F, A f). (b) In actual music, 
however, F minor frequently appears as a passing chord between F major and C major.
Figure C3 A graph of single-semitone voice-leading relations among diminished, dominant, 
half-diminished and French sixth chords. On the graph it takes four steps to get from C7 to 
Aø7, even though the chords can be connected by two single-semitone shifts.

## Page 434

Appendix C 415
and {F s, B} are twelve steps apart, even though the minimal voice leading between 
them moves each voice by just a semitone. Once again, local voice-leading concerns 
give rise to a graph whose global distances are difﬁ  cult to interpret.
This last example provides a key to understanding what is going on. Figure C4b 
embeds the circular graph within the Möbius strip representing two-note chords, 
showing that one can move from {C, F} to {B, F s} across the center of the larger 
space. We cannot take advantage of this shortcut if we stay on the discrete lattice, 
because the lattice forces us to go “the long way around”—off one side of the strip 
and onto the other. A little thought will show that these sorts of voice-leading “short-
cuts” always pass through chords dividing the octave at least as evenly  as those we 
happen to be interested in. (This is obvious in two-note chord space and less than 
obvious in higher dimensions; but the general principle holds there as well.) This 
leads to a very useful rule of thumb: in general, we should expect that a faithful rep-
resentation of voice-leading possibilities will contain whatever chords we are inter-
ested in, as well as all the chords that divide the octave at least as evenly as those chords . 
Thus if we are interested in voice leading among major thirds and perfect fourths, we 
should also include tritones. This is precisely why the lattices in §3.11 are all reliable: 
they include the most even chords in any given scale, and hence faithfully represent 
voice-leading distances.
More generally, we can specify criteria ensuring that a graph’s global structure 
faithfully represents voice-leading distances:
 1.  Every edge on the graph should represent voice leading in which a single 
voice moves by a single scale step or chromatic semitone (a condition violated 
by the Tonnetz ).Figure C4 (a) A graph of single-semitone voice-leading relations between major thirds and 
perfect fourths. ( b) Since it does not contain tritones, it cannot represent voice leadings such 
as (C, F) ®(B, F s), which move vertically across the center of the space.

## Page 435

appendix c 416
 2.  For any two of its chords, the graph should contain all the interscalar 
transpositions between them (§4.9). This implies that the graph should not 
present the appearance of multiple disjoint segments in a cross section of the 
space of all chords, a condition violated by Figure C4b.
 3.  The chords on the graph should all have the same size.4
 4.  The paths representing these interscalar transpositions should not involve 
ascending and descending motion in the same voice (a condition violated by 
the Tonnetz  and Figure C3 above).
 5. The graph should not contain any multisets.
It is relatively easy to see that any graph satisfying these three requirements will faith-
fully reﬂ  ect voice-leading distances, even between nonadjacent chords: condition 2 
implies that the graph contains the shortest voice leading between any of its chords 
(§4.9); condition 1 implies that edges have unit voice-leading length; and condition 3 
implies that the edges representing an interscalar transposition do not cancel each 
other out.5 The ﬁ  ve requirements are satisﬁ  ed by all of the lattices in §3.11.
Of course, geometry can also provide a deeper perspective on these “faithful” voice-
leading graphs. For instance, Douthett and Steinbach’s “Cube Dance” ( Figure C5a). 
4 For discussion of the problems arising when graphs combine chords of different sizes, see Callender, 
Quinn, and Tymoczko 2008 and Tymoczko 2010.
5 Note that if we are measuring paths by counting the number of edges they contain, then we are using 
the “taxicab” metric of voice-leading size.
Figure C5 Douthett and Steinbach’s “Cube Dance” ( a) and the lattice at the center of three-
note chord space ( b).

## Page 436

Appendix C 417
is virtually identical to the lattice at the center of three-note chord space, and was 
 discovered almost a decade before the continuous spaces of Chapter 3. However, 
it turns out that we can extract much more information from the graph when we 
understand how it is embedded within the continuous space. For example, geometry 
tells us that the graph represents all and only the strongly crossing-free voice leadings  
between its chords; that the three spatial axes correspond to motion in the three 
musical voices; that these spatial axes can only be deﬁ  ned locally, since the ﬁ  gure has 
a global topological twist; and that two paths on the ﬁ  gure represent the same voice 
leading if they have the same “winding number” (that is, if they take the same num-
ber of clockwise or counterclockwise steps). All of which shows that the geometrical 
perspective can do more than just reveal that some graphs  faithfully represent voice 
leading; it can also help us use these graphs in a more sophisticated and musical 
fashion.

## Page 437

appendix d
The Interscalar Interval Matrix
Chapter 4 noted that strongly crossing-free voice leadings can be decomposed into 
chromatic and interscalar transpositions. As it happens, there is a useful mathemati-
cal way to represent this idea. Figure D1 depicts what I call an interscalar interval 
matrix,  representing the four interscalar transpositions that take a half-diminished 
seventh chord to a dominant seventh chord with the same root. The numbers in 
the matrix are paths in pitch-class space, showing how far and in what direction 
each note moves. T o combine these scalar transpositions with chromatic transpo-
sitions, we simply add a constant value to the relevant matrix row. For instance, 
the ﬁ  rst row represents the voice leading 0, 1, 1, 0(C,E , G ,B ) (C, E,G,B ) ¾¾¾ ¾ ® ff f f , 
which sends the root of the C half-diminished chord to the root of the C domi-
nant seventh chord; by subtracting one from the values (0, 1, 1, 0), we get (−1, 0, 
0, −1), representing the voice leading 1, 0, 0, 1(C, E , G , B ) (B, D , F , A)--¾¾¾¾ ® fff s s . In 
effect, we have transposed the second chord down by chromatic semitone, from C7 
to B7. (The two voice leadings are individually T-related since they differ only by 
the transposition of their second chord.) Every strongly crossing-free (four-voice) 
voice leading from half-diminished to dominant seventh can be obtained by adding 
some constant to some row of the interscalar interval matrix: for example, to obtain 
0,0, 1, 1(C, E , G , B ) (C, E , F, A)--¾¾¾ ¾ ® fff f ,  subtract seven from the values in the third 
row. This is equivalent to combining interscalar transposition upward by two steps 
with chromatic transposition downward by seven semitones.
With a little practice, we can learn to “read” these matrices, seeing at a glance the 
voice-leading possibilities between all the transpositions of any two chord types. For 
example, suppose we want to ﬁ  nd the most efﬁ  cient voice leading between C half-
diminished and A dominant seventh. Our matrix contains voice leadings that send 
a half-diminished chord to the dominant seventh with the same root. Since we want 
a voice leading that moves the root down by third, we will be subtracting three from 
the numbers in some row of the matrix.1 To  ﬁ  nd the ascending scalar transposition 
that most nearly offsets descending chromatic transposition by three semitones, we 
1 Note that the matrix contains ascending scalar transpositions, which we will be attempting to neu-
tralize with descending chromatic transpositions; hence we transpose by subtracting three rather than by 
adding nine.

## Page 438

Appendix D 419
simply look for the row of the matrix whose values come closest to three. This is 
clearly the second row: subtracting three from these values gives (1, 1, 1, −1), repre-
senting 1, 1, 1, 1(C, E , G , B ) (C , E, G, A)-¾¾¾¾ ® fff s .2
After a bit of time, this sort of computation becomes automatic; one virtually starts 
to see the voice leading 1, 1, 1, 1(C, E , G , B ) (C , E, G, A)-¾¾¾¾ ® fff s  directly in the matrix 
in Figure D1. T o test yourself, try to use the matrix to identify the most efﬁ  cient voice 
leading from a C half-diminished chord to an E f dominant seventh chord.3 Then use Figure D1 (a) The rows of this matrix correspond to the voice leadings in ( b). All of the 
strongly crossing-free (four-voice) voice leadings from half-diminished to dominant seventh 
can be derived by adding a constant number to some row of this matrix. For example, to 
combine interscalar transposition up by two steps with chromatic transposition downward by 
seven semitones, subtract 7 from the values in the third row of the matrix, as illustrated by ( c).
2 Interscalar interval matrices provide another way to understand the relationship between near even-
ness and efﬁ  cient voice leading: for two nearly even chords, the rows of the interscalar interval matrix will 
all be very close to a constant value, which means that the interscalar transpositions and chromatic trans-
positions will nearly cancel each other out. Hence we can ﬁ  nd reasonably efﬁ  cient voice leadings between 
that chord and all of its various transpositions.
3 T o do this, simply subtract nine from the row of the matrix whose values are closest to nine. (Again, 
we want to combine a descending chromatic transposition with an ascending scalar transpositions in the 
matrix, and hence will be subtracting nine rather than adding three to some row.) In this case, the relevant 
row is the last one: subtracting nine from the values in the fourth row gives us (1, 0, 1, 0), representing 
1,0,1,0(C, E , G , B ) (D , E , G, B ) ¾¾¾ ® fff f f f .

## Page 439

appendix d 420
it to ﬁ  nd the minimal voice leading that maps the root of the half-diminished chord 
onto the ﬁ  fth of some dominant seventh.4
Analogous matrices can be constructed for any pair of chords, using the following 
algorithm5:
 1. Assign scale degree numbers to the two scales A and B.
 2.  Arrange chord A in pitch space in ascending scale degree order (i.e. with the 
ﬁ  rst scale degree at the bottom and the last scale degree at the top) such that 
the top and bottom notes are no more than an octave apart. Arrange chord B 
similarly.
 3.  Write down the voice leading that maps the lowest note of A to the lowest 
note of B, the second-lowest note of A to the second-lowest note of B, and 
so on. Write this voice leading as a pitch-class voice leading of the form 
¾¾¾¾ ¾ ®12 1212, ,...,( , , . . . , ) ( , , . . . , )nnn xx xaa a bb b  (§2.5). The numbers above the 
arrow are the ﬁ  rst row of the interscalar interval matrix.6
4 Here, we begin with the third row of the matrix (which maps root to ﬁ  fth) and ask what chromatic 
transposition comes closest to neutralizing these values. There are two equally good possibilities: sub-
tracting six gives us a two-semitone voice leading from Cø7 to F s7, while subtracting seven gives us a two-
semitone voice leading from Cø7 to F7.
5 It is assumed that A and B have the same number of notes. One can always add “doublings” to the 
smaller chord so that it has the same number of notes as the larger chord. However, there are multiple 
ways to do this.
6 Or more mathematically: the numbers are obtained by subtracting the pitches of B componentwise 
from those of A.Figure D2 Constructing the interscalar interval matrix from (C, D, E, F, G, A, B) to 
(C, D, E, F s, G, A, B f). The resulting matrix is shown in Figure D3.

## Page 440

Appendix D 421
 4.  Transpose the lowest note of B up by octave and move it to the end of the 
sequence, replacing ( b1, b2, …, bn) with ( b2, b3, …, bn, b1 + 12).
 5.  Repeat steps 3–4 to obtain the second row of the interscalar interval 
matrix. Continue repeating until the chord B has been transposed upward 
by octave.
Figure D2 generates the interscalar interval matrix that takes the C diatonic 
scale to the C acoustic scale. Note that the result is affected both by how we assign 
scale degrees to the two chords, and by how we arranged them register. For exam-
ple, suppose we had numbered the C acoustic scale so that D was its ﬁ  rst scale 
degree, and arranged it in register so that it began 10 semitones below middle C: 
(D3, E3, F s3, G3, A3, B f3, C4). This would yield an interscalar interval matrix 
whose ﬁ  rst row is (−10, −10, −10, −10, −10, −11, −11) rather than (0, 0, 0, 1, 0, 
0, −1). Figure D3 compares the matrix that results with the matrix we originally 
generated: each row of Figure D3b is either identical to a row in Figure D3a, or can 
be obtained from one by subtracting 12. In principle, the difference between these 
two matrices is immaterial; they contain the same information and can be used in 
more or less the same way. However, it is in practice easier to work with the matrix 
in Figure D3a.
In the special case where the second chord is the same as the ﬁ  rst, then we have a 
scalar  (rather than an interscalar) interval matrix. One can construct these matrices 
in exactly the same way, though we should always label the scale degrees so that the 
ﬁ rst row of the matrix contains only zeros. Figure D4 generates the scalar interval 
matrix that takes the dominant seventh chord to itself. Its four rows correspond to 
the voice leadings at the bottom of the ﬁ  gure.
Again, the matrix can be used to represent every combination of scalar and chro-
matic transpositions. For example, to combine scalar transposition by ascending step 
with chromatic transposition downward by three semitones, subtract three from the 
 second row of the matrix, giving 1,0,0, 1(C, E, G, B ) (C , E, G, A)-¾¾¾ ® fs .
Figure D3 Two equivalent interscalar interval matrices. Each of the ﬁ  rst six rows in the right 
matrix can be obtained by subtracting twelve from the next row down in the left matrix. The 
last row of the right matrix is identical to the ﬁ  rst row of the left.

