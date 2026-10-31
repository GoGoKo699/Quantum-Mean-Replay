# Keeping the phase while replacing the sampler

Suppose a sequence of devices can prepare quantum samples with the same success probability. Each device remains available only briefly. Its other output registers may look completely different from those of the preceding device. A classical experiment can measure each sample and average the outcomes. A quantum experiment would like to accumulate a small, useful phase across many samples, even though the preparation device keeps changing.

The project separates two things that an ordinary repeated-preparation algorithm keeps together: the source that creates a sample and the probe that preserves the estimation phase. One forward call and one matching inverse call can transfer the source's scalar probability to the probe. A measurement announces whether the transfer succeeded. On failure, a known correction restores the probe so that a new source can be tried.

This explanation follows the [settled milestone map](milestones.md): M01–M12 provide the background, M13–M21 build the estimator, and M22–M30 explain its limits and resource law. The [anchor bridge](anchor-and-bridge.md) gives the relevant Nielsen–Chuang sections. The small circuit below is a complete worked example, followed by the additional arguments required for the full theorem.

## 1. What the source promises

A source is a unitary $`U_i`$ on a workspace $`W`$ initialized in a known state $`|0\rangle_W`$. A known projector $`\Pi`$ marks the event being estimated. Its probability is

```math
p_i=\langle0|U_i^\dagger\Pi U_i|0\rangle.
```

With an explicit output flag, the prepared state has the form

```math
U_i|0\rangle
=\sqrt{1-p_i}\,|b_i\rangle
+\sqrt{p_i}\,|g_i\rangle,
\qquad
\Pi|b_i\rangle=0,\quad
\Pi|g_i\rangle=|g_i\rangle.
```

The two vectors include all source-specific output registers. They are normalized and orthogonal because they lie in different flag subspaces. Equal probabilities do not make these vectors equal across sources.

The algorithm receives an interface to $`U_i`$ and its exact inverse, not a classical description of their matrices. Forward and inverse calls share a limit of $`m`$ calls in the current window. After retiring it, the algorithm cannot return to that source. It may keep a separate probe qubit $`B`$ coherent.

These are access assumptions. Neither a measured classical sample nor a copy of an output state automatically supplies the inverse interface. See [the exact model](../science/model-and-results.md#1-oracle-and-access-model).

## 2. Turn a probability into a reflection expectation

A reflection changes a sign on one subspace and leaves its orthogonal complement unchanged. Define the known marking reflection

```math
S=I-2\Pi.
```

It has eigenvalue $`+1`$ on bad outcomes and $`-1`$ on good outcomes. For any preparation $`A`$ with marked probability $`q`$, unpreparing after this reflection gives

```math
R=A^\dagger S A,\qquad R^\dagger=R,\qquad R^2=I.
```

Its expectation on the known input is a scalar:

```math
z=\langle0|R|0\rangle
=(1-q)-q=1-2q.
```

The rest of $`R|0\rangle`$ may still contain an unknown direction. Write it as

```math
R|0\rangle=z|0\rangle+|w\rangle,
\qquad
\langle0|w\rangle=0,\qquad
\|w\|^2=1-z^2.
```

The useful fact is that the coefficient returning to the known input depends only on the probability. The direction $`|w\rangle`$ can depend on all the unknown details.

Couple the workspace to the probe between preparation and unpreparation:

```math
V=(A^\dagger\otimes I_B)
  e^{i\pi S\otimes Z_B/4}
  (A\otimes I_B)
 =\frac{I+iR\otimes Z_B}{\sqrt2}.
```

The last equality follows because $`(S\otimes Z_B)^2=I`$: its exponential separates into cosine times the identity plus sine times the involution. The middle operation is known. For a flag qubit, it is simply $`e^{i\pi Z_W Z_B/4}`$. This construction needs no controlled call to the unknown source.

## 3. A complete example at a marked probability of one quarter

Take one workspace qubit, $`\Pi=|1\rangle\langle1|`$, and

```math
A=U=
\begin{pmatrix}
\sqrt3/2&-1/2\\
1/2&\sqrt3/2
\end{pmatrix}.
```

Then $`U|0\rangle=(\sqrt3/2)|0\rangle+(1/2)|1\rangle`$, so the marked probability is $`p=q=1/4`$. The matrix is displayed so that the circuit can be checked; an estimation algorithm is not supplied these entries or told the answer.

This is the **unamplified case $`k=1`$ of the global bounded-mean corollary**. It lies outside the rare-event theorem: there $`p_0\le1/16`$ and $`p\le2p_0\le1/8`$. The example will illustrate the transducer, not prove the rare-event frontier.

Direct multiplication gives

```math
R=U^\dagger Z_W U
=
\begin{pmatrix}
1/2&-\sqrt3/2\\
-\sqrt3/2&-1/2
\end{pmatrix},
\qquad
R|0\rangle=\frac12|0\rangle-\frac{\sqrt3}{2}|1\rangle.
```

For an arbitrary probe state $`|\psi\rangle_B`$,

```math
V|0\rangle_W|\psi\rangle_B
=|0\rangle_W K_0|\psi\rangle_B
 +|1\rangle_W K_1|\psi\rangle_B,
```

where the two measurement operators are

```math
K_0=\frac{I+iZ_B/2}{\sqrt2},
\qquad
K_1=-i\sqrt{\frac38}\,Z_B.
```

Measuring the workspace after unpreparing records which operator acted on the probe. The probabilities follow from

```math
K_0^\dagger K_0=\frac58 I_B,
\qquad
K_1^\dagger K_1=\frac38 I_B.
```

They sum to the identity, so the two outcomes exhaust the possibilities. They are also scalar multiples of the identity, so neither probability depends on the incoming probe.

| Workspace outcome | Probability | Normalized probe operation | Next action |
|---|---:|---|---|
| Zero: accepted transfer | $`5/8`$ | $`T=(2I+iZ_B)/\sqrt5`$ | Keep the added phase. |
| One: failed transfer | $`3/8`$ | $`-iZ_B`$ | Apply $`Z_B`$, restoring the input up to a global phase. |

The original event probability $`1/4`$ and the transfer-success probability $`5/8`$ describe different measurements. The first concerns the marked output immediately after preparation. The second concerns the entire workspace returning to zero after the coupling and inverse.

Let $`\gamma=\arctan(1/2)`$. Since $`\cos\gamma=2/\sqrt5`$ and $`\sin\gamma=1/\sqrt5`$,

```math
T=\frac{2I+iZ_B}{\sqrt5}=e^{i\gamma Z_B}.
```

For the other branch, the corrected, unnormalized operator is

```math
Z_BK_1=-i\sqrt{\frac38}\,I_B.
```

After normalization, this is the identity up to the irrelevant overall phase $`-i`$. Failure consumes the two source calls but does not spoil a phase already stored on the probe.

## 4. Why the correction must preserve a reference too

Checking the probe alone can miss damage to its correlations with another system. Let $`E`$ be an untouched reference and let the probe and reference initially share the Bell state

```math
|\Phi^+\rangle_{BE}
=\frac{|00\rangle+|11\rangle}{\sqrt2}.
```

In the example, a successful transfer produces

```math
(T\otimes I_E)|\Phi^+\rangle
=\frac{e^{i\gamma}|00\rangle+e^{-i\gamma}|11\rangle}{\sqrt2}.
```

A failed transfer gives, up to a global phase,

```math
(Z_B\otimes I_E)|\Phi^+\rangle
=|\Phi^-\rangle
=\frac{|00\rangle-|11\rangle}{\sqrt2}.
```

The correction $`Z_B`$ returns $`|\Phi^-\rangle`$ to $`|\Phi^+\rangle`$. Thus it restores the correlation as well as the probe's marginal state.

The Bell example is illustrative; the operator identities establish more. For any joint density operator $`\rho_{BE}`$, the unnormalized branches are

```math
\begin{aligned}
\rho_{BE}&\longmapsto
 \frac58(T\otimes I_E)\rho_{BE}(T^\dagger\otimes I_E),
 &&\text{success},\\
\rho_{BE}&\longmapsto
 \frac38\rho_{BE},
 &&\text{corrected failure}.
\end{aligned}
```

Taking the trace gives probabilities $`5/8`$ and $`3/8`$ for every input, including entangled and mixed states. Dividing by those probabilities gives the normalized conditional operations. No information about the probe is revealed through the branch probabilities.

This conclusion assumes the source acts on its stated initialized workspace and the reference is untouched. It does not cover an uncontrolled environment shared between the source and probe.

## 5. What survives when the workspace changes completely

Return to the general decomposition in Section 2. Applying the circuit to any probe-reference vector gives

```math
\begin{aligned}
(V\otimes I_E)|0\rangle_W|\Psi\rangle_{BE}
={}&|0\rangle_W
 \left(\frac{I+i zZ_B}{\sqrt2}\otimes I_E\right)|\Psi\rangle_{BE}\\
&+\frac{i}{\sqrt2}|w\rangle_W
 (Z_B\otimes I_E)|\Psi\rangle_{BE}.
\end{aligned}
```

The zero outcome has probability

```math
s(q)=\frac{1+z^2}{2}=(1-q)^2+q^2\ge\frac12
```

and applies

```math
T(q)=e^{i\gamma(q)Z_B},
\qquad
\gamma(q)=\arctan(1-2q).
```

Every nonzero workspace outcome applies a scalar times $`Z_B`$. Its unknown scalar affects the probability and a global phase, but not which correction is required. Measuring all workspace qubits and checking whether the recorded string is zero therefore suffices. Measuring only the original flag would generally be inadequate.

For equal $`q`$, accepted sources apply the same probe gate even when their vectors $`|w\rangle`$ have unrelated directions. Corrected failures restore the probe. The source workspace can be discarded after every attempt, and the next attempt can use a fresh source.

This is the inherited gearbox/repeat-until-success mechanism, expressed for an arbitrary flagged preparation. The [scientific account](../science/phase-transduction.md#5-relation-to-the-original-gearbox) credits its precedents. The project uses its exact interface to establish a source-replay resource law; it does not claim a new measurement primitive.

## 6. Read the stored phase without controlling an accepted gate

Initialize the probe in $`|+\rangle=(|0\rangle+|1\rangle)/\sqrt2`$. After one accepted gate it is

```math
T(q)|+\rangle
=\frac{e^{i\gamma(q)}|0\rangle+e^{-i\gamma(q)}|1\rangle}{\sqrt2}.
```

The measurable relative phase is $`\varphi(q)=2\gamma(q)`$. Direct calculation with the Pauli matrices gives

```math
\langle X_B\rangle=\cos\varphi(q),
\qquad
\langle Y_B\rangle=-\sin\varphi(q).
```

The minus sign follows from the positive exponent in $`e^{i\gamma Z_B}`$. This is why the algorithm uses $`X_B`$ and $`-Y_B`$ measurements.

In the quarter-probability example,

```math
\cos(2\gamma)=\frac35,\qquad
\sin(2\gamma)=\frac45.
```

An $`X_B`$ measurement therefore returns $`+1`$ with probability $`4/5`$, while a $`-Y_B`$ measurement returns $`+1`$ with probability $`9/10`$. These are random outcomes, not direct numerical readouts of the mean. Repeated shots estimate the two expectation values.

After $`L`$ accepted transfers with a common probability, the phase becomes $`L\varphi(q)`$. Corrected failures do not contribute to it. Increasing $`L`$ magnifies a small phase difference, but the measured sine and cosine repeat every $`2\pi`$. A fine-resolution measurement therefore needs coarse information to identify the correct phase interval.

This uses unconditional transfer attempts and ordinary probe measurements. It does not assume that the measured, accepted gate itself is available as a coherent controlled oracle.

## 7. Recover the phase from coarse and fine experiments

Use repetition lengths $`L_j=2^j`$. At each length, estimate the cosine and sine with separate shots. Their angle gives $`L_j\varphi`$ modulo $`2\pi`$. The target phase starts in the known interval $`[-\pi/2,\pi/2]`$.

The lifting step has a simple geometric reason. Suppose the angle estimate at each stage has circular error at most $`\rho=\pi/8`$. At length $`L_j`$, the correct phase candidate is within $`\rho/L_j`$ of the target. The preceding estimate is within $`2\rho/L_j`$. Thus the correct new candidate lies within $`3\rho/L_j`$ of the old estimate. Other candidates are spaced by $`2\pi/L_j`$. Since $`3\rho\lt\pi`$, selecting the nearest candidate chooses the correct lift.

To obtain a total failure probability at most $`\beta`$ without an extra logarithm in inverse precision, allocate more repetitions to the cheap, coarse stages. The [explicit schedule](../science/replay-algorithm.md) uses a number of shots of order $`\log(1/\beta)+(K-j)`$ at stage $`j`$. Its accepted-transfer cost is controlled by

```math
\sum_{j=0}^{K}2^j\bigl(\log(1/\beta)+(K-j)\bigr)
=O\bigl(2^K\log(1/\beta)\bigr).
```

The geometric repetition lengths make the coarse stages cheap enough to absorb their stronger confidence demands. The canonical proof supplies the concentration constants and the final inversion of the phase map.

If sources have slightly different probabilities, accepted sources need not be an unbiased subset: their acceptance probabilities depend on their means. The proof uses a pointwise phase bound instead. With no amplification,

```math
|\varphi'(r)|=\frac4{1+(1-2r)^2}\le4,
```

so every accepted source satisfies $`|\varphi(p_i)-\varphi(p)|\le4\delta`$ when $`|p_i-p|\le\delta`$. Any particular history of $`L`$ successes then has phase error at most $`4L\delta`$. This remains true after success-dependent selection. The theorem's small drift ratio keeps that error within the slack of the phase-lifting procedure.

## 8. Pay for failed attempts and for coherence

For the exact quarter-probability example, an accepted transfer takes $`8/5`$ attempts on average. Each attempt uses one forward and one inverse call, so the expected source-call cost of $`L`$ accepted transfers is $`16L/5`$. Every individual source is used exactly twice and then retired.

An expectation is not a worst-case resource guarantee. If the entire estimation schedule requires $`N_{\rm acc}`$ accepted transfers, the proved algorithm caps attempts at

```math
N_{\rm try}
=\left\lceil4N_{\rm acc}
       +16\log\frac2\beta\right\rceil.
```

It declares failure if that cap is exhausted. Because each conditional acceptance probability is at least one-half, the failure from exhaustion is at most $`\beta/2`$; the inference schedule accounts for the remaining failure budget. The unamplified algorithm makes at most $`2N_{\rm try}`$ actual source calls. The [attempt-cap proof](../science/replay-algorithm.md) treats this explicitly.

The persistent quantum register is small, but it must remain coherent for the complete Ramsey shot. That shot includes many successful transfers and the intervening corrected failures. Resetting the probe after each source would erase the accumulated phase. The theorem separates local source lifetime from probe lifetime; it does not establish a constant-coherence-depth implementation.

## 9. How extra local replay changes rare-event estimation

The quarter-probability example has used no amplification. For the rare-event theorem, assume instead

```math
0\lt p_0\le\frac1{16},\qquad
p\in[p_0,2p_0],\qquad
0\lt\epsilon\le\frac{p_0}{64},\qquad
|p_i-p|\le\delta\le\frac{\epsilon}{32}.
```

The scale $`p_0`$ is supplied; the center $`p`$ is unknown. This upper construction assumes an integer replay cap $`m\ge2`$. All amplification is performed before leaving the current source. Define

```math
\begin{aligned}
R_0&=I-2|0\rangle\langle0|,\\
G_i&=-U_iR_0U_i^\dagger(I-2\Pi),\\
A_{i,k}&=G_i^{(k-1)/2}U_i,
\qquad k\text{ odd}.
\end{aligned}
```

The two-reflection geometry gives

```math
q_k(r)=\sin^2(k\arcsin\sqrt r).
```

Preparing with $`A_{i,k}`$ takes $`k`$ source calls, and unpreparing takes another $`k`$. Thus one transfer attempt costs $`2k`$ calls even when it fails. Both directions count against $`m`$.

The achieved construction chooses the largest positive odd $`k`$ with

```math
k\le\min\left\{\frac m2,\frac1{4\sqrt{p_0}}\right\}.
```

The actual source means lie in $`I=[p_0/2,3p_0]`$. The second restriction keeps amplification in its first monotone lobe throughout that interval, preventing a larger probability from being wrapped around to an indistinguishable amplified probability. Restricting $`k`$ to positive odd integers changes only constant factors: $`k=\Theta(\min\{m,p_0^{-1/2}\})`$.

To see the sensitivity gain, put $`\theta=\arcsin\sqrt r`$. Differentiation gives

```math
q_k'(r)=k\,\frac{\sin(2k\theta)}{\sin(2\theta)}.
```

On the allowed interval, the [first-lobe bounds](../science/replay-algorithm.md#22-a-uniform-first-lobe-bound) give

```math
\frac{2}{\pi}k^2\le q_k'(r)\le k^2.
```

The transferred relative phase is $`f_k(r)=2\arctan(1-2q_k(r))`$. Its derivative magnitude is between $`(4/\pi)k^2`$ and $`4k^2`$ there. A change $`\epsilon`$ in the underlying probability therefore changes the phase by order $`k^2\epsilon`$.

This explains the resource balance. Resolving that phase needs order $`1/(k^2\epsilon)`$ accepted transfers at constant confidence. Each attempt costs order $`k`$ source calls and succeeds with probability at least one-half. With the proved hard cap, total query cost is

```math
Q=O\!\left(\frac1{k\epsilon}\right)
 =O\!\left(
 \max\left\{\frac{\sqrt{p_0}}{\epsilon},
                 \frac1{m\epsilon}\right\}\right).
```

The same derivative bound sends mean drift to at most $`4k^2\delta`$ phase drift per accepted transfer. The largest repetition length is order $`1/(k^2\epsilon)`$, so the required drift-to-error ratio stays constant. This accounts for the fixed promise $`\delta\le\epsilon/32`$; it is not a statement about arbitrary physical gate errors.

The worked example establishes none of these optimality claims by itself. The amplification, robust inference and cost calculations supply the upper theorem; separate hard inputs supply the lower bounds.

## 10. Why the resource law also needs a converse

The [lower-bound proofs](../science/lower-bounds.md) cover algorithms with arbitrary persistent memory. Three complementary ideas are needed.

**One use can hide all useful phase in the worst case.** A hard source is a Bernoulli rotation decorated with fresh row, column and global phases. Averaging those nuisance phases removes the coherences that a single forward, inverse or coherently controlled direction call could exploit. The averaged call can be simulated with one classical Bernoulli draw and known quantum operations. This statement concerns the phase-twirled hard family, not every sampler. The resulting statistical lower bound is $`\Omega(p_0/\epsilon^2)`$ when $`m=1`$. Keeping more quantum memory does not undo an exact channel simulation.

**Even a repeatable source has a coherent limit.** For Bernoulli rotations, two means differing by order $`\epsilon`$ near $`p_0`$ have rotation angles differing by order $`\epsilon/\sqrt{p_0}`$. A hybrid argument bounds how much distinguishability each call can add. Constant testing advantage therefore needs $`\Omega(\sqrt{p_0}/\epsilon)`$ calls.

**Expiring sources impose an additional replay cost.** The fresh-source counting proof compares a Boolean string with strings differing at one initially unmarked position, flipped from zero to one. Within a short source window it bounds the average loss of real overlap while tracking which possible query slots contain actual paid calls. In its small-window regime, it selects a neighboring source obeying

```math
\Delta_i\le\frac{4m}{h}(C_0+C_i).
```

Here $`h`$ is the number of candidate positions, $`C_0,C_i`$ are expected actual costs inside that window, and $`\Delta_i`$ is a real-overlap decrease. The auxiliary-to-actual cost comparison is essential when stopping depends on outcomes. The selected sources are determined from unconditional purified states, so the construction produces fixed valid lists rather than an oracle that reacts to realized measurement results.

Summing this inequality and using $`h=\Theta(1/\epsilon)`$ yields the $`\Omega(1/(m\epsilon))`$ term where needed; the ordinary rotation bound covers the remaining regime. The full proof also explains why the lists remain valid and why one hard query budget must handle all the hard families. It uses $`O(\log(1/\epsilon))`$ local source qubits, so the complete frontier is not asserted for every fixed one-qubit source model.

## 11. The distinction the complete theorem establishes

At constant confidence, the [matched theorem](../science/model-and-results.md#2-main-theorem-the-local-replay-frontier) is

```math
Q_1=\Theta\!\left(\frac{p_0}{\epsilon^2}\right),
\qquad
Q_m=\Theta\!\left(
\max\left\{\frac{\sqrt{p_0}}{\epsilon},
                \frac1{m\epsilon}\right\}\right)
\quad(m\ge2).
```

A reversible pair changes the worst-case precision dependence in the full changing-garbage model. Further replay improves the rare-event dependence until $`m=\Theta(p_0^{-1/2})`$ reaches the usual amplitude-estimation order. That local reuse scale does not grow with the requested precision, although the probe's coherent experiment does.

Known reflections, the middle coupling, workspace measurement, reversible arithmetic and the implementation of each unknown-source call still have costs. A consistently compiled preparation paired with its exact compiled inverse preserves the instrument identity for its implemented probability; an independently faulty inverse need not. Neither the worked circuit nor the frontier supplies free QRAM, an inverse for an irreversible sampler, or tolerance to an unspecified noise process. Those boundaries are detailed in the [resource account](../science/resources-and-robustness.md).

The circuit example shows precisely where the scalar information goes: successful workspace return adds a phase to the probe, and a failed return supplies a correctable operation. The full theorem quantifies how far that source-local operation can be composed, what replay it requires, and which guarantees remain valid when the source workspace changes.
