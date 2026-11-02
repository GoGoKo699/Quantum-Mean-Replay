# All-time confidence with bounded local replay

The terminal replay frontier also determines the cost of keeping every committed estimate trustworthy. Both its local-replay branch and its ordinary amplitude-estimation branch pay the all-time confidence overhead. The replay branch requires a new probability-propagation argument; multiplying the terminal replay lower bound by an existing phase-estimation penalty does not prove it.

This page is the canonical shared proof with [Anytime Quantum Estimation](https://github.com/GoGoKo699/Anytime-Quantum-Estimation). That sister account gives the [committed-confidence interpretation and transfer](https://github.com/GoGoKo699/Anytime-Quantum-Estimation/blob/4301198d91310e7e607db255e1cf35c2965d08c6/science/expiring-samplers.md). The baseline antecedents are [Quantum Mean Replay at 823616b](https://github.com/GoGoKo699/Quantum-Mean-Replay/tree/823616bb1aeb0acec995dc5bcbd4c52ce906c121) and [Anytime Quantum Estimation at bd1e4d1](https://github.com/GoGoKo699/Anytime-Quantum-Estimation/tree/bd1e4d175f8c1c1ffa23c89493ccc0e6d9d86fcd). The former supplies the transducer, local amplification and terminal estimator; the latter supplies Cantor norming and the unconditioned first-error method. The fresh-phase polynomial channel, charged-call block argument and replay-sensitive summability below are the joint addition.

## 1. Model and simultaneous guarantee

Use the [source-access model](model-and-results.md): source $`i`$ supplies an unknown unitary $`U_i`$ and its exact inverse during one chronological window. It receives at most $`m`$ total physical invocations, including forward, inverse and permitted controlled calls. After retirement it cannot be revisited. Source progression and decisions to invoke or retire a source are classical; a coherent direction selector is allowed within the current source. There is no coherent SELECT across identities. Arbitrary persistent quantum memory, retained old workspaces, parameter-independent controls and adaptive instruments are allowed.

Here the means have **zero drift**:

```math
\langle0|U_i^\dagger\Pi U_i|0\rangle=p,
\qquad
0\lt p_0\le\frac1{16},
\qquad p\in[p_0,2p_0],
\qquad m\ge2.
```

The scale $`p_0`$ and cap $`m`$ are known. Output garbage, its phases and unitary completions may change arbitrarily. Every executed source invocation costs one call, even with a coherent idle branch; an invocation omitted by a classical decision costs zero. A deterministic deadline bounds actual calls on every outcome path. In particular, unsuccessful repeat-until-success attempts are charged.

At each actual-call budget $`T`$, the algorithm has a committed classical estimate $`\widehat p_T`$ and a deterministic radius $`r(T)`$. Holding the latest output between updates is allowed. For every fixed valid source list, require

```math
\Pr\!\left\{
 |\widehat p_T-p|\le r(T)\text{ for every }T
\right\}\ge1-\alpha,
\qquad 0<\alpha\le\frac14.
\qquad\text{(1)}
```

Finite prefixes are finite protocols. The all-time statement means that every finite prefix obeys the same simultaneous guarantee, with a consistent horizon-free execution. A terminal output decoded only after choosing a horizon, or marginal correctness separately at each time, is a different guarantee. Expected stopping-cost deadlines are not asserted here.

## 2. Joint theorem and its meaning

Write

```math
A_m(p_0)=\max\{\sqrt{p_0},1/m\}.
\qquad\text{(2)}
```

**Theorem 1 — replay-sensitive all-time confidence.** There are universal positive constants $`c_0,B,D,C`$ with the following properties. Set

```math
\epsilon_k=c_0p_0\,3^{-k},\qquad k\ge1,
\qquad\text{(3)}
```

where $`c_0`$ is sufficiently small. If increasing deterministic charged-call deadlines $`T_k`$ reach radii $`r(T_k)<\epsilon_k`$ under (1), then

```math
\boxed{\displaystyle
\sum_{k\ge1}
 \exp\!\left[-D\frac{T_k\epsilon_k}{A_m(p_0)}\right]
\le B\alpha.}
\qquad\text{(4)}
```

The same assertion holds for any finite initial set of required refinements. Conversely, a horizon-free protocol satisfies (1) and reaches these accuracies at deterministic deadlines bounded by

```math
T_k\le
C\frac{A_m(p_0)}{\epsilon_k}
\left[\log(k+2)+\log\frac1\alpha\right].
\qquad\text{(5)}
```

Its upper construction uses one persistent probe, in addition to the current sampler workspace and classical records. The lower theorem allows unrestricted persistent memory and already has one-qubit source instances.

For fixed $`p_0,m`$, the resulting shrinking envelope has order

```math
r(T)=O\!\left(
\frac{A_m(p_0)}{T}
\left[\log\log T+\log\frac1\alpha\right]
\right)
\qquad\text{(6)}
```

after initialization, with a matching positive lower limit superior for

```math
\frac{T r(T)}{A_m(p_0)\log\log T}.
\qquad\text{(7)}
```

The summability statement is primary. It does not impose the displayed lower order at every time or every individual refinement. In particular, for $`K`$ prescribed refinements it gives

```math
\max_{1\le k\le K}
\frac{T_k\epsilon_k}{A_m(p_0)}
\ge\frac1D\log\frac{K}{B\alpha},
\qquad\text{(8)}
```

and Jensen's inequality gives the same lower bound for the average of these normalized deadlines. It is not a lower bound on the last deadline alone.

For $`m=2`$ and the stated range of $`p_0`$, $`A_2(p_0)=1/2`$. Thus even when $`p_0\ll1/m^2`$, the all-time radius has order $`[\log\log T+\log(1/\alpha)]/T`$, without a $`\sqrt{p_0}`$ reduction. Tiny $`p_0`$ still raises the first relative-accuracy deadline: at $`\epsilon=\eta p_0`$, the replay-limited cost is of order $`[\log(k+2)+\log(1/\alpha)]/(m\eta p_0)`$ along a uniformly efficient refinement schedule.

## 3. A common continuous hard family

The terminal [fresh-count adversary](lower-bounds.md#5-a-cost-aware-fresh-source-window-lemma) selects different nearby Boolean strings at each accuracy. Its additive overlap bound is not a probability-propagation theorem, and those separate adversaries do not by themselves define the common multiscale experiment needed for (4).

Instead, independently for every source draw

```math
a,b\in\{0,1\},\qquad c\in\{0,1,2,3\}
```

uniformly and supply

```math
U_{a,b,c;p}=i^c Z^a R_p Z^b,
\qquad
R_p=
\begin{pmatrix}
\sqrt{1-p}&-\sqrt p\\
\sqrt p&\sqrt{1-p}
\end{pmatrix}.
\qquad\text{(9)}
```

The tuple is drawn once per source and remains fixed throughout its window, including inverse calls. Every realization is a legal exact-mean-$`p`$ sequence. The label list can be fixed before the run. The protocol must satisfy (1) for every such list, so it also satisfies (1) after averaging the independent labels. The **same** label prior and continuous parameter $`p`$ are used at all deadlines.

### Lemma 2 — polynomial averaged instruments

Consider an algorithmic block that starts at a fresh-source boundary, uses no source outside that block, and makes at most $`L`$ actual calls on every branch. Its output may contain classical records and arbitrary persistent quantum memory. After averaging its fresh phase labels, its complete unnormalized instrument, including all recorded outcomes, is a channel-valued polynomial $`\Phi(p)`$ of degree at most $`L`$. For real $`p\in[0,1]`$, the complete map is CPTP.

**Proof.** Write $`x=\sqrt{1-p}`$, $`y=\sqrt p`$ and $`R(x,y)=\left(\begin{smallmatrix}x&-y\\y&x\end{smallmatrix}\right)`$. Every nonidle matrix entry of a forward or inverse call is linear in $`x,y`$. The identity branch of a direction selector is constant. A density-map term from a path of at most $`L`$ calls on each side therefore has total degree at most $`2L`$ in the variables $`x_i,y_i`$ of all visited sources. Classically omitted calls contribute no factors. Instruments remain unnormalized; no branch probability is divided out.

For each source separately, the phase ensemble is invariant under each sign change

```math
R(x,-y)=ZR(x,y)Z,
\qquad
R(-x,y)=-ZR(x,y)Z.
\qquad\text{(10)}
```

The first toggles $`a,b`$; the second also shifts $`c`$ by two. This relabelling represents the same transformed unitary and its inverse, so it also works for the coherent current-source direction selector. Averaging removes every monomial with an odd power of either $`x_i`$ or $`y_i`$. Substituting $`x_i^2=1-p`$ and $`y_i^2=p`$ gives degree at most $`L`$ in the common parameter.

Adaptive instruments give sums or integrals of these unnormalized maps. Finite-query polynomial degree is preserved. One can equivalently reconstruct the channel coefficients by interpolation at $`L+1`$ real parameter values; this gives a bounded-map polynomial without choosing coordinates for the persistent memory. For every real parameter the construction is the average of physical complete instruments, hence CPTP. Keeping rather than discarding classical records or old workspace does not change the argument. $`\square`$

## 4. Grouping by charged calls

**Lemma 3 — replay-sensitive derivative bound.** For a physical transcript event observable through at most $`Q\ge1`$ actual calls, let $`f_Q(p)`$ be its likelihood after the fresh-phase average. There is a universal $`C_1`$ such that

```math
0\le f_Q(p)\le1\quad(p\in[0,1]),
\qquad
\sup_{p\in[0,1]}|f_Q^{(j)}(p)|
\le[C_1 Q\min(m,Q)]^j
\quad(j\ge1).
\qquad\text{(11)}
```

**Proof.** Enforce the local and global call caps using known counters on all inputs, returning a fixed recorded output if a cap would be exceeded. This changes no promised run and makes the auxiliary maps physical for all $`p\in[0,1]`$.

Put $`h=\min(m,Q)`$. Starting at a source boundary, collect complete active source windows until the block has made at least $`h`$ calls, then end it at that boundary. A nonfinal block costs between $`h`$ and $`2h-1`$ actual calls, since its final source uses at most $`h`$. The last prefix may stop earlier at the global cap, even within its final source. There is no later block in this truncated experiment; the original horizon-free run may continue that source after the inspected deadline. There are at most

```math
N=\lfloor Q/h\rfloor+1
\qquad\text{(12)}
```

blocks. Pad halted histories by identity maps. Keep the full classical histories, counters, source pointer, committed outputs and persistent quantum memory at their interfaces.

No source crosses a block boundary. Untouched skipped sources reveal no information about their labels and can be integrated away. Since labels are independent and source retirement is classical, the next first-invoked source has a fresh independent label conditional on the complete past record. The chronological computation can consequently be represented by the composition of $`N`$ averaged block channels. Different classical histories can reach a boundary at different source indices; this is a reorganization of classical histories, not coherent source selection or return access. Retaining an earlier source's workspace does not reveal any unused label.

By Lemma 2 each block $`\Phi_t(p)`$ is a CPTP polynomial of degree $`d_t\le2h`$. Its diamond norm is one on real $`[0,1]`$. The Markov polynomial inequality on this interval, applied to norming real linear functionals of the Banach space of bounded maps, gives

```math
\sup_{p\in[0,1]}
\|\Phi_t^{(j)}(p)\|_\diamond
\le(2d_t^2)^j\le(8h^2)^j.
\qquad\text{(13)}
```

Indeed, the usual first-derivative inequality is $`\|P'\|_\infty\le2d^2\|P\|_\infty`$ on $`[0,1]`$. Repeating it gives (13); duality transfers the scalar inequality to these map norms. Derivatives above the degree vanish. This estimate is uniform over memory dimension and includes entangled references.

Leibniz's rule, the multinomial theorem and diamond-norm submultiplicativity now give

```math
\left\|
 \frac{d^j}{dp^j}(\Phi_N\cdots\Phi_1)(p)
\right\|_\diamond
\le(8Nh^2)^j
\le(16Qh)^j.
\qquad\text{(14)}
```

The last inequality uses $`h\le Q`$. Applying a transcript-event effect to the final state proves (11). A zero-call likelihood is constant and can be handled separately. $`\square`$

This step charges actual invocations, including failed attempts. Padding every source to $`m`$ paid calls would not give (11). Merely counting listed sources or averaging normalized conditional states would also be insufficient.

## 5. From derivatives to first-error summability

We use the following inherited Cantor norming fact. Let $`\mu`$ be the fair middle-thirds Cantor measure on $`[0,1]`$. There is a universal $`A>1`$ such that every real polynomial $`P`$ of degree $`d\ge1`$ satisfies

```math
|P(z)|\le A^d\int |P|\,d\mu,
\qquad -2\le z\le1.
\qquad\text{(15)}
```

The [baseline norming proof](https://github.com/GoGoKo699/Anytime-Quantum-Estimation/blob/bd1e4d175f8c1c1ffa23c89493ccc0e6d9d86fcd/science/cantor-propagation.md) selects alternating equal-mass Cantor quantile bins and applies Lagrange interpolation. Its Frostman estimate $`\mu(J)\le4|J|^{\log2/\log3}`$ bounds every denominator exponentially in $`d`$. No new general Remez theorem is claimed here.

### Local probability propagation

Suppose $`0\le f\le1`$ on $`[0,1]`$ and $`\|f^{(j)}\|_\infty\le M^j`$ for every $`j`$. Let $`\nu`$ be an affine Cantor measure on an interval $`[b,b+\ell]`$. If $`z\in[b-2\ell,b+\ell]\subset[0,1]`$ and $`f(z)\ge1/2`$, then

```math
\int f\,d\nu\ge
c\exp[-C(M\ell+1)].
\qquad\text{(16)}
```

To see this, Taylor-expand about $`b`$ to degree $`d`$. On the displayed interval its remainder obeys

```math
R\le\frac{(2M\ell)^{d+1}}{(d+1)!}
\le\left(\frac{2eM\ell}{d+1}\right)^{d+1}.
```

Choose $`d=\lceil K(M\ell+1)\rceil`$ with a sufficiently large universal $`K`$. Then $`R\le(4A)^{-d}`$. Apply (15) after rescaling the Taylor polynomial. Since $`f\ge0`$,

```math
\frac12\le
A^d\left(\int f\,d\nu+R\right)+R,
```

which gives (16). Thus Lemma 3 supplies propagation with $`M=C_1Q\min(m,Q)`$.

### Physical first errors

Place a scaled Cantor set in an interior parameter interval of width $`a=\Theta(p_0)`$ within $`[p_0,2p_0]`$. Its level-$`k`$ children have width and intervening gap $`\ell_k=a3^{-k}`$. Choose $`a`$ and the sufficiently small $`c_0`$ in (3) so that $`r(T_k)<\epsilon_k<\ell_k/2`$.

At $`T_k`$, project the reported estimate to the nearest level-$`k`$ cylinder and let $`W_k`$ be its $`k`$th decoded bit. On the simultaneous success event every decoded bit is correct. For a prefix $`s\in\{0,1\}^{k-1}`$, the event

```math
E_{s,k}=\{W_1\cdots W_{k-1}=s,\ W_k=0\}
\qquad\text{(17)}
```

is an ordinary event in the physical transcript through $`T_k`$. Its averaged likelihood is at least $`1-\alpha\ge1/2`$ everywhere in the left child $`s0`$. A point in that child lies within two child widths of the adjacent right child $`s1`$. Equation (16) therefore gives an average likelihood at least

```math
c\exp[-C(T_k\min(m,T_k)\ell_k+1)]
```

on $`s1`$. Under a true parameter in $`s1`$, event (17) is a first decoded error at $`k`$. The fair Cantor prior assigns mass $`2^{-k}`$ to each right child. Summing over its $`2^{k-1}`$ prefixes, then over disjoint first-error events, proves

```math
\sum_k
\exp[-D T_k\min(m,T_k)\epsilon_k]
\le B\alpha.
\qquad\text{(18)}
```

Both the source-label prior and Cantor prior describe one experiment across all deadlines. No independence between errors at different scales is used, and no event is conditioned on earlier correct outputs. Since $`\min(m,T_k)\le m`$, (18) also implies

```math
\sum_k\exp[-D mT_k\epsilon_k]\le B\alpha.
\qquad\text{(19)}
```

## 6. The ordinary rare-event branch

Independently take every source to be the same clean rotation $`R_p`$ in (9), now without averaging phase labels. Write $`p=\sin^2\theta`$. On the scale interval,

```math
\theta\in[\arcsin\sqrt{p_0},\arcsin\sqrt{2p_0}],
\qquad
\frac{dp}{d\theta}=\Theta(\sqrt{p_0}).
\qquad\text{(20)}
```

Each physical call, including its inverse and direction control, has matrix entries of trigonometric degree at most one in $`\theta`$. Every $`T`$-call transcript-event likelihood therefore has degree at most $`2T`$ and is bounded between zero and one on the full circle. The [phase-polynomial and first-error proof](https://github.com/GoGoKo699/Anytime-Quantum-Estimation/blob/bd1e4d175f8c1c1ffa23c89493ccc0e6d9d86fcd/science/first-error-summability.md) applies.

For precision, clip an estimate to $`[p_0,2p_0]`$ before applying $`\arcsin\sqrt{\cdot}`$. Its phase error is at most $`C\epsilon_k/\sqrt{p_0}`$. Place an affine Cantor set in an interior phase interval of width $`\Theta(\sqrt{p_0})`$ and take $`c_0`$ small enough that this error is less than half its level-$`k`$ gap. The same first-error reasoning gives

```math
\sum_k
\exp\!\left[-D\frac{T_k\epsilon_k}{\sqrt{p_0}}\right]
\le B\alpha.
\qquad\text{(21)}
```

When $`m\le p_0^{-1/2}`$, use (19); otherwise use (21). Increasing universal constants if necessary gives (4). These are two independently proved multiscale obstructions. The first attaches the confidence overhead to local replay; the second controls saturation at the ordinary amplitude-estimation rate.

As a further consequence, the derivative bound also strengthens the terminal replay converse to one-qubit source workspaces. For two means separated by $`4\epsilon`$, a constant-confidence estimator gives a transcript event whose probabilities differ by a constant. The mean value theorem and (11) imply $`Q=\Omega(1/(m\epsilon))`$. Together with the one-qubit rotation bound and the existing upper construction, this removes the older workspace-size restriction on the terminal frontier. The Boolean-string proof in [lower-bounds.md](lower-bounds.md) remains a separate valid converse.

## 7. Constructive upper bound with every attempt charged

Choose the largest positive odd integer

```math
\ell\le\min\{m/2,1/(4\sqrt{p_0})\}.
\qquad\text{(22)}
```

It exists and obeys $`\ell=\Theta(\min\{m,p_0^{-1/2}\})`$, so $`1/\ell=\Theta(A_m(p_0))`$. One locally amplified preparation and its exact inverse cost $`2\ell\le m`$ source calls per attempt. The [exact transducer](phase-transduction.md) has

```math
q_\ell(p)=\sin^2(\ell\arcsin\sqrt p),
\qquad
f_\ell(p)=2\arctan(1-2q_\ell(p)),
```

and on the known-scale interval

```math
\frac4\pi\ell^2\le|f_\ell'(p)|\le4\ell^2.
\qquad\text{(23)}
```

Its success probability $`(1-q_\ell)^2+q_\ell^2\ge1/2`$ is independent of the probe and any entangled reference. A success adds $`e^{if_\ell(p)Z/2}`$; a corrected failure restores the incoming probe exactly. At zero drift, accepted rotations from different sources have precisely the same phase. No coherent control of an accepted RUS gate is assumed.

For $`m=2`$, $`\ell=1`$ and each attempt costs exactly two calls, successful or failed. In this case

```math
|f_1'(p)|=\frac4{1+(1-2p)^2}\in[2,4].
```

### A capped terminal run

The explicit [Ramsey guarantee](replay-algorithm.md) prescribes a deterministic number $`S`$ of accepted rotations for target accuracy $`\epsilon`$ and failure budget $`\beta`$, with

```math
S\le\frac{C}{\ell^2\epsilon}\log\frac1\beta.
```

It uses geometrically growing Ramsey lengths and backward-geometric allocation of its internal confidence budget. Impose the actual attempt cap

```math
N=\left\lceil4S+16\log\frac2\beta\right\rceil.
\qquad\text{(24)}
```

Every attempt, including a failure, uses one new source and costs $`2\ell`$ calls. The total pathwise budget is therefore $`2\ell N`$, rather than $`2\ell S`$. Conditional success probabilities are at least $`1/2`$, so a Chernoff bound gives

```math
\Pr\{\text{fewer than }S\text{ successes by }N\}
\le e^{-N/16}\le\beta/2.
```

The remaining $`\beta/2`$ covers the Ramsey measurements. Exhausting the cap commits a clipped fallback output and is included in failure; it is never postselected away. Since $`\ell^2\epsilon\le\ell^2p_0/64\le1/1024`$, the extra cap term is absorbed, giving

```math
2\ell N\le
C\frac{A_m(p_0)}{\epsilon}\log\frac1\beta.
\qquad\text{(25)}
```

### A horizon-free sequence

At refinement $`k`$, run this terminal procedure to accuracy, for example, $`\epsilon_k/2`$, using

```math
\beta_k=\frac{\alpha}{k(k+1)},\qquad k\ge1.
\qquad\text{(26)}
```

All internal outputs can remain private; commit the final clipped result of each outer run. The source supply continues chronologically, with every attempt using a new source. The same guarantee applies conditional on past classical records, and $`\sum_k\beta_k=\alpha`$. A union bound therefore proves (1). Geometric accuracies and the increasing logarithmic budget give

```math
\sum_{j=1}^k
C\frac{A_m(p_0)}{\epsilon_j}\log\frac1{\beta_j}
\le
C'\frac{A_m(p_0)}{\epsilon_k}
\left[\log(k+2)+\log\frac1\alpha\right],
```

proving (5). These are deterministic caps on cumulative real calls; stages may finish earlier. Between deadlines use the latest committed estimate. Before the first useful refinement use the midpoint of $`[p_0,2p_0]`$ and radius $`p_0/2`$. Thus no gap in budget time is omitted from (1).

Inverting the geometric deadlines yields the scale-aware upper radius

```math
r(T)\le
C\frac{A_m(p_0)}{T}
\left[
\log\frac1\alpha+
\log\log\!\left(e^2+\frac{Tp_0}{A_m(p_0)}\right)
\right]
\qquad\text{(27)}
```

after $`T\ge C[A_m(p_0)/p_0]\log(1/\alpha)`$; the prior radius covers earlier times. For fixed $`p_0,m`$ this is (6). The matching positive limit superior follows from (4) exactly as in the phase case: deadlines proportional to $`[A_m(p_0)/p_0]3^k\log k`$ would make the summands dominate a divergent power series if that limit superior were too small.

## 8. Finite horizons, resources and limits

For $`K`$ prescribed refinements, $`\beta_k=\alpha/K`$ gives uniformly normalized deadlines of order $`\log(K/\alpha)`$, matching (8). If the final accuracy $`\epsilon_K`$ is known in advance, instead take

```math
\beta_k=\alpha\,2^{k-K-1},\qquad 1\le k\le K.
```

Their sum is below $`\alpha`$. Since $`\epsilon_k^{-1}=3^{k-K}\epsilon_K^{-1}`$, summing (25) gives

```math
T_K=O\!\left(
\frac{A_m(p_0)}{\epsilon_K}\log\frac1\alpha
\right).
\qquad\text{(28)}
```

All committed outputs remain simultaneously correct. Some earlier normalized deadlines are inefficient, so this does not violate (8). A mandatory final $`\log K`$ factor would be a false conclusion.

| Resource or promise | Joint theorem's accounting |
|---|---|
| Actual source calls | Every forward, inverse and permitted controlled invocation is charged. An amplified attempt costs $`2\ell`$ whether it succeeds or fails. |
| Local lifetime | One attempt uses a fresh source with $`2\ell\le m`$ calls; that source is then retired permanently. |
| Global budget | Each terminal run caps attempts as in (24); outer deadlines sum those hard caps. No expected-attempt count replaces them. |
| Persistent quantum memory | One probe for the upper bound, coherent through each Ramsey shot and its failed attempts; unrestricted memory for the converse. |
| Known local operations | Flag coupling, input reflections, corrections, readout, arithmetic and gate synthesis have the separate costs in the [resource ledger](resources-and-robustness.md). |
| Confidence | One event covers every committed output of one run. No independence across refinements or postselection is assumed. |
| Mean variation | This all-time shrinking theorem is zero drift. The existing terminal drift guarantee remains $`\delta\le\epsilon/32`$ for a specified accuracy. |

A fixed positive unrestricted drift tolerance cannot support radii shrinking indefinitely to zero. Neither unknown $`p_0`$, expected refinement costs, imperfect physical inverses nor general noise robustness follows from this theorem. The phase prior is continuous, and the twirl relies on unknown changing output phases; a known common clean preparation plane is a stronger promise. Revisits, coherent selection across source identities, or an uncontrolled environment shared with the probe require separate models.

The derivation extends the terminal resource frontier with a replay-sensitive multiscale converse and a fully charged confidence schedule. It does not convert oracle calls into hardware time or gate count. [Related work](../references/related-work.md#committed-confidence-and-the-sister-result) separates the inherited ingredients from the shared addition; finite checks in [verification](../verification/README.md) illustrate the algebra and budgets without certifying the universal analytical theorem.
