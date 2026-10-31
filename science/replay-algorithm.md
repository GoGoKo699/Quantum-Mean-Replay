# Mean estimation with a bounded lifetime for each sampler

This file proves the upper bound

```math
Q=O\!\left(
\max\left\{\frac{\sqrt{p_0}}{\epsilon},\frac{1}{m\epsilon}\right\}
\log\frac1\beta\right)
\tag{1}
```

for a stream of Bernoulli samplers whose means lie near one common target. Each individual sampler is used at most $`m`$ times, counting its forward and inverse calls together. The algorithm retains one probe qubit across source windows, while measuring and discarding each source workspace after a local preparation/unpreparation pair.

The construction combines ordinary amplitude amplification [1], the inherited gearbox instrument [2,3], and an explicit multiscale Ramsey estimator. The gearbox identity, including arbitrary reference entanglement and correctable failure, is proved in [phase-transduction.md](phase-transduction.md). The present file charges the amplification and inverse calls, handles success-dependent selection of non-identical sources, and gives a deterministic cap on the total number of actual calls.

## 1. The upper-bound theorem

Each current source is an unknown unitary $`U_i`$ on an initialized workspace $`W`$, with a known Bernoulli success projector $`\Pi`$. Its mean is

```math
p_i=\langle0|U_i^\dagger\Pi U_i|0\rangle.
\tag{2}
```

The source may have arbitrary output garbage and an arbitrary unitary completion away from $`|0\rangle`$. Its exact inverse is available during its current source window. After moving to the next source, the algorithm does not return to it. A primitive call means one physical application of $`U_i`$, $`U_i^\dagger`$, or a controlled version; the upper bound below needs only the uncontrolled forward and inverse calls. There is no coherent SELECT over source identities.

**Theorem 1 — rare-event upper bound.** Let

```math
0<p_0\le\frac1{16},\qquad
p\in[p_0,2p_0],\qquad
0<\epsilon\le\frac{p_0}{64},\qquad
0<\beta\le\frac12,
\tag{3}
```

where $`p_0`$ is supplied classically and $`p`$ is unknown. Suppose every source obeys

```math
|p_i-p|\le\delta,
\qquad
\delta\le\frac{\epsilon}{32}.
\tag{4}
```

For every integer $`m\ge2`$, there is an estimator with success probability at least $`1-\beta`$ and additive error at most $`\epsilon`$. It uses at most $`m`$ primitive calls to each source and satisfies (1), with a deterministic upper bound on total actual calls, including all failed attempts. A supply of $`N`$ fresh sources, with $`N`$ specified by (20), (24), (25) and (35), suffices.

The statement holds for a fixed source sequence. The same upper proof permits each next source to be selected using prior classical outcomes, provided its conditional mean continues to satisfy (4), it acts as a unitary on its initialized workspace, and its matching inverse remains available for the entire current attempt. This does not permit a source to act on an uncontrolled environment shared with the probe.

The supplied probability scale is a real assumption. Theorem 1 is a local-scale result; it does not claim that an unknown scale can be learned at zero cost. Its drift guarantee is the explicit sufficiently small ratio (4), rather than every possible fixed ratio below one.

## 2. Choose an amplification length that fits every replay budget

Define

```math
B=\min\left\{\frac m2,\frac{1}{4\sqrt{p_0}}\right\},
\qquad
k=\max\{r\in\mathbb N:r\text{ is odd and }r\le B\}.
\tag{5}
```

Because $`m\ge2`$ and $`p_0\le1/16`$, one has $`B\ge1`$, so $`k`$ exists. In particular,

```math
2k\le m,
\qquad
k^2p_0\le\frac1{16},
\qquad
k\ge\frac1{12}\min\{m,p_0^{-1/2}\}.
\tag{6}
```

For the last inequality, the largest positive odd integer at most $`B`$ is at least $`B/3`$, and
$`B\ge\tfrac14\min\{m,p_0^{-1/2}\}`$. The definition gives $`k=1`$ for every $`m\in\{2,3,4,5\}`$; no nonexistent fractional Grover iteration is being used.

The comparisons in (5) can equivalently use $`2k\le m`$ and $`16p_0k^2\le1`$. Thus a rational supplied scale permits certified selection of $`k`$ without evaluating an inverse trigonometric function.

### 2.1 Local Grover preparation

Write $`k=2t+1`$, let

```math
R_0=I-2|0\rangle\langle0|,
\qquad
S=I-2\Pi,
\qquad
G_i=-U_iR_0U_i^\dagger S,
\tag{7}
```

and define

```math
A_{i,k}=G_i^tU_i.
\tag{8}
```

This preparation uses exactly $`k`$ primitive calls. Its inverse also uses exactly $`k`$ calls. The known reflections $`R_0`$ and $`S`$ have their ordinary implementation costs; they are not extra sampler queries.

For $`\theta_i=\arcsin\sqrt{p_i}`$, decompose the prepared state into normalized bad and good components:

```math
U_i|0\rangle=\cos\theta_i\,|b_i\rangle+
\sin\theta_i\,|g_i\rangle.
\tag{9}
```

Here $`\Pi|b_i\rangle=0`$ and $`\Pi|g_i\rangle=|g_i\rangle`$. In this two-dimensional plane, $`G_i`$ is the rotation by $`2\theta_i`$. Consequently,

```math
A_{i,k}|0\rangle
=\cos(k\theta_i)|b_i\rangle+
\sin(k\theta_i)|g_i\rangle,
\qquad
q_k(p_i)=\sin^2(k\theta_i).
\tag{10}
```

This is the standard amplitude-amplification identity. [1] The plane may be completely different for the next source. All amplification in (8) occurs before leaving the current source, so no alignment of different sources' Grover planes is assumed.

### 2.2 A uniform first-lobe bound

Both the target interval and all the actual source means lie in

```math
I=[p_0/2,3p_0].
\tag{11}
```

Indeed, (3)–(4) give $`\delta\le p_0/2048`$. For $`r\in I`$, write $`\theta=\arcsin\sqrt r`$. The elementary bound $`\arcsin x\le(\pi/2)x`$, together with (5), gives

```math
k\theta\le
\frac{1}{4\sqrt{p_0}}\frac\pi2\sqrt{3p_0}
=\frac{\pi\sqrt3}{8}<\frac\pi4.
\tag{12}
```

Thus $`q_k`$ stays in its first monotone lobe and satisfies $`0<q_k(r)<1/2`$. Differentiating,

```math
q_k'(r)=k\frac{\sin(2k\theta)}{\sin(2\theta)}.
\tag{13}
```

The sine chord bound supplies the lower inequality below. The upper inequality follows because $`\sin x/x`$ is decreasing on $`(0,\pi)`$, with both arguments here in $`(0,\pi/2)`$:

```math
\frac{2}{\pi}k^2\le q_k'(r)\le k^2
\qquad(r\in I).
\tag{14}
```

No approximation $`q_k(r)\approx k^2r`$ is needed in the algorithm or its proof.

## 3. Convert each locally amplified source into a probe rotation

Apply the instrument of [phase-transduction.md](phase-transduction.md) with preparation $`A_{i,k}`$ and success projector $`\Pi`$. One attempt uses $`A_{i,k}`$ and $`A_{i,k}^\dagger`$, hence exactly **$`2k`$ primitive calls**. In fact, it uses $`k`$ forward and $`k`$ inverse calls to the original source. This is at most the shared budget $`m`$.

After the known failure correction, the attempt either leaves the probe unchanged or applies

```math
\exp\!\left(\frac i2 f_k(p_i)Z\right),
\qquad
f_k(r)=2\arctan\!\left(1-2\sin^2(k\arcsin\sqrt r)\right).
\tag{15}
```

Its conditional success probability is

```math
s_i=(1-q_k(p_i))^2+q_k(p_i)^2\ge\frac12.
\tag{16}
```

The complete outcome distribution is independent of the incoming probe and any reference entangled with it. The workspace can be measured and discarded after either outcome, and the next attempt uses a fresh source.

Set

```math
a=\frac4\pi,
\qquad
\varphi=f_k(p).
\tag{17}
```

Since $`q_k(r)\in[0,1/2]`$, (14) implies

```math
a k^2\le |f_k'(r)|\le4k^2
\qquad(r\in I),
\tag{18}
```

and $`f_k`$ is decreasing. In particular, every accepted phase obeys

```math
|f_k(p_i)-\varphi|\le4k^2\delta.
\tag{19}
```

This is a pointwise statement for every accepted source. It remains true even though acceptance probabilities depend on $`p_i`$, so selecting successful sources can change their relative frequencies.

## 4. An explicit Ramsey estimator without an extra $`\log(1/\epsilon)`$

The following procedure is used with the corrected phase attempts just described. It is useful to separate the estimation argument from the source implementation.

Suppose the unknown target phase belongs to a known interval
$`J\subseteq[-\pi/2,\pi/2]`$. Every successful attempt applies $`e^{i\varphi_i Z/2}`$, with
$`|\varphi_i-\varphi|\le\Delta`$; every corrected failure leaves the probe unchanged. The outcome probabilities are independent of the probe, and each conditional success probability is at least $`1/2`$.

Choose an integer $`K\ge0`$ and define

```math
\rho=\frac\pi8,
\qquad
L_j=2^j,
\qquad
\beta_j=\beta\,2^{j-K-2},
\qquad
r_j=\left\lceil128\log\frac4{\beta_j}\right\rceil
\quad(0\le j\le K).
\tag{20}
```

Natural logarithms are used in this file. Assume

```math
L_K\Delta\le\frac18.
\tag{21}
```

At each stage $`j`$, perform $`r_j`$ shots for an $`X`$ measurement and another $`r_j`$ shots for a $`-Y`$ measurement, each beginning with a fresh preparation of the probe in $`|+\rangle`$. Within each shot, accumulate exactly $`L_j`$ successful rotations. Correct every failure before trying the next source. Let $`\widehat c_j`$ and $`\widehat s_j`$ be the two empirical averages of the $`\pm1`$ outcomes, and let

```math
\alpha_j=\operatorname{atan2}(\widehat s_j,\widehat c_j)
\in(-\pi,\pi].
\tag{22}
```

If both averages vanish, set $`\alpha_j=0`$; this case will lie outside the good event used below.

Initialize $`\widehat\varphi_0=\alpha_0`$. For $`j\ge1`$, choose the lift

```math
\widehat\varphi_j=
\frac{\alpha_j+2\pi n_j}{L_j},
\qquad n_j\in\mathbb Z,
\tag{23}
```

nearest to $`\widehat\varphi_{j-1}`$. Resolve a tie arbitrarily. Finally, clip $`\widehat\varphi_K`$ to the known interval $`J`$.

The prescribed number of accepted rotations is deterministic:

```math
S=2\sum_{j=0}^{K}L_jr_j.
\tag{24}
```

Impose the hard attempt cap

```math
N=\left\lceil4S+16\log\frac2\beta\right\rceil.
\tag{25}
```

If the cap is exhausted before all the shots finish, declare failure. Otherwise return the clipped phase estimate.

**Lemma 2 — Ramsey guarantee.** Under (21), this procedure returns an estimate satisfying

```math
|\widehat\varphi-\varphi|\le\frac{\rho}{L_K}
\tag{26}
```

with probability at least $`1-\beta`$. It uses at most $`N`$ actual attempts. Moreover,

```math
S\le4L_K\left(128\log\frac{32}{\beta}+1\right),
\qquad
N=O\!\left(L_K\log\frac1\beta\right).
\tag{27}
```

**Proof.** First analyze a virtual protocol with enough valid sources to complete all the shots. The finite-cap implementation agrees with it whenever its first $`N`$ attempts suffice.

For any stage-$`j`$ shot, condition on its complete success/failure history and any earlier classical data. The accumulated phase $`\Phi`$ satisfies

```math
|\Phi-L_j\varphi|\le L_j\Delta.
\tag{28}
```

The corresponding coordinate expectation is $`\cos\Phi`$ or $`\sin\Phi`$. Both functions are 1-Lipschitz, so it differs from the appropriate ideal coordinate by at most $`L_j\Delta\le1/8`$. Averaging over that shot's success history preserves this bound. It also holds when the next source was selected from prior classical outcomes.

Let $`X_\ell\in\{-1,1\}`$ denote successive outcomes for one coordinate, and let $`\mu_\ell`$ be the conditional expectation given all the earlier data. Bounded martingale concentration gives

```math
\Pr\!\left[
\left|\frac1r\sum_{\ell=1}^{r}(X_\ell-\mu_\ell)\right|>u
\right]
\le2e^{-ru^2/2}.
\tag{29}
```

Thus, with $`u=1/8`$ and $`r=r_j`$, a coordinate's statistical error is at most $`1/8`$ except with probability $`\beta_j/2`$. Both coordinates at all stages satisfy their bounds except with probability

```math
\sum_{j=0}^{K}\beta_j<\frac\beta2.
\tag{30}
```

No identical-distribution or independence assumption on the shot phases was used. Each measurement samples its own conditional expectation, and (29) controls their centered fluctuations.

On this good event, each coordinate differs from its ideal value by at most $`1/4`$. Therefore

```math
\left\|
\begin{pmatrix}\widehat c_j\\\widehat s_j\end{pmatrix}
-\begin{pmatrix}\cos(L_j\varphi)\\\sin(L_j\varphi)\end{pmatrix}
\right\|_2
\le\frac{\sqrt2}{4}<\sin\rho.
\tag{31}
```

A disk of radius less than $`\sin\rho`$ around a unit vector subtends an angle less than $`\rho`$ at the origin. Hence $`\alpha_j`$ estimates $`L_j\varphi`$ modulo $`2\pi`$ to circular error at most $`\rho`$.

At $`j=0`$, the target belongs to $`[-\pi/2,\pi/2]`$, so the principal value in (22) already has the correct lift and error at most $`\rho`$. Inductively suppose the previous estimate has error at most $`\rho/L_{j-1}=2\rho/L_j`$. The correct new lift is within $`\rho/L_j`$ of the target, and hence within $`3\rho/L_j`$ of the previous estimate. Other lifts are separated by $`2\pi/L_j`$. Since $`3\rho<\pi`$, the nearest lift is the correct one. This proves (26). Clipping to $`J`$ cannot increase the error.

For the attempt budget, the success indicators have conditional probability at least $`1/2`$. They therefore stochastically dominate independent Bernoulli$`(1/2)`$ indicators. Since $`S\le N/4`$, a Chernoff lower-tail bound gives

```math
\Pr[\text{fewer than }S\text{ successes in }N\text{ attempts}]
\le e^{-N/16}\le\frac\beta2.
\tag{32}
```

Combining (30) and (32) proves the guarantee for the real capped protocol. This union bound does not condition the phase concentration statement on successful completion.

Finally,

```math
r_j\le128\left(\log\frac{16}{\beta}+(K-j)\log2\right)+1.
\tag{33}
```

Using

```math
\sum_{j=0}^{K}2^j<2L_K,
\qquad
\sum_{j=0}^{K}2^j(K-j)\le2L_K,
\tag{34}
```

in (24) gives (27). The geometric allocation of failure probabilities makes the coarse stages more accurate, where experiments are cheaper. It avoids multiplying the finest-scale cost by the number of scales. $`\square`$

## 5. Apply the estimator to the rare-event phase

For Theorem 1, use

```math
K=\left\lceil
\log_2\frac{\rho}{a k^2\epsilon}
\right\rceil,
\qquad
J=[f_k(2p_0),f_k(p_0)].
\tag{35}
```

The constraints imply $`k^2\epsilon\le1/1024`$, so the argument of the logarithm exceeds one and $`K\ge0`$. Its finest scale obeys

```math
\frac{\rho}{a k^2\epsilon}
\le L_K<
\frac{2\rho}{a k^2\epsilon}
=\frac{\pi^2}{16k^2\epsilon}.
\tag{36}
```

By (19), take $`\Delta=4k^2\delta`$. Then

```math
L_K\Delta
<\frac{\pi^2\delta}{4\epsilon}
\le\frac{\pi^2}{128}<\frac18.
\tag{37}
```

Lemma 2 applies. Because $`|f_k'|\ge a k^2`$ on the target interval, its inverse is $`1/(a k^2)`$-Lipschitz there. The clipped estimate therefore gives

```math
|\widehat p-p|
\le\frac{|\widehat\varphi-f_k(p)|}{a k^2}
\le\frac{\rho}{a k^2L_K}
\le\epsilon.
\tag{38}
```

An explicit inverse, with the principal branches appropriate to the first lobe, is

```math
\widehat p=
\sin^2\!\left[
\frac1k\arcsin\sqrt{
\frac{1-\tan(\widehat\varphi/2)}{2}}
\right].
\tag{39}
```

The argument is evaluated only after clipping to $`J`$, so it remains in the valid physical range.

Every attempt uses a fresh source and exactly $`2k`$ primitive calls. Thus a fully explicit hard query budget is

```math
Q_{\rm cap}=2k
\left\lceil
4\left(2\sum_{j=0}^{K}2^jr_j\right)
+16\log\frac2\beta
\right\rceil,
\tag{40}
```

with $`r_j`$ from (20). The algorithm may stop earlier if it obtains all required successes. It never exceeds this cap on any measurement history.

Equations (27) and (36) give

```math
Q_{\rm cap}
=O\!\left(\frac1{k\epsilon}\log\frac1\beta
+k\log\frac1\beta\right).
\tag{41}
```

The second term is absorbed by the first because $`k^2\epsilon\le1/1024`$. Finally, (6) yields (1). This proves Theorem 1, including failed attempts and all inverse calls.

### Classical arithmetic precision

The displayed estimator is specified in exact arithmetic. It has fixed slack for a finite implementation: the angle bound in (31) is actually
$`\rho_*:=\arcsin(\sqrt2/4)<\rho`$. The angle computations and lift comparisons can use certified intervals with total additional angular error smaller than a fixed fraction of $`\rho-\rho_*`$; division by $`L_j`$ requires correspondingly more classical bits at finer stages. The final inverse can be evaluated to an error smaller than the remaining fixed fraction of $`\epsilon`$. These changes leave the schedule and its asymptotic query cost unchanged. Known arithmetic incorporated into a sampler must separately use the matched compiled inverse and the mean-bias accounting in [phase-transduction.md](phase-transduction.md).

## 6. Two calls per source suffice for a globally bounded mean

The probability-scale promise is needed for the rare-event improvement in (1), not for the two-call bounded-mean result.

**Corollary 3 — uniform Bernoulli means.** Let $`p\in[0,1]`$, $`0<\epsilon\le1/2`$, and $`|p_i-p|\le\epsilon/32`$. Using one forward and one inverse call per source, an estimator achieves additive error $`\epsilon`$ with probability at least $`1-\beta`$ using

```math
O\!\left(\epsilon^{-1}\log\frac1\beta\right)
\tag{42}
```

primitive calls, with a hard total cap and one retained probe qubit.

**Proof.** Set $`k=1`$ without local amplification. The phase is

```math
f_1(p)=2\arctan(1-2p),
\qquad
2\le|f_1'(p)|\le4
\quad(0\le p\le1).
\tag{43}
```

Use Lemma 2 with

```math
J=[-\pi/2,\pi/2],
\qquad
K=\max\left\{0,
\left\lceil\log_2\frac{\rho}{2\epsilon}\right\rceil\right\}.
\tag{44}
```

If $`K\ge1`$, then $`L_K<\rho/\epsilon`$, so
$`4L_K\delta<4\rho\delta/\epsilon\le\pi/64<1/8`$.
If $`K=0`$, then $`4L_K\delta\le\epsilon/8\le1/16`$.
The inverse

```math
p=\frac{1-\tan(\varphi/2)}2
\tag{45}
```

is $`1/2`$-Lipschitz on $`J`$. Equations (26) and (44) therefore give error at most $`\epsilon`$. Also $`L_K=O(1/\epsilon)`$, so (27) gives (42). The arguments include $`p=0`$ and $`p=1`$; clipping keeps the inverse within its physical interval. $`\square`$

For a random variable supported in a known interval $`[\ell,h]`$, the standard reversible value-to-coin conversion encodes
$`p=(\mu-\ell)/(h-\ell)`$. The same argument gives

```math
O\!\left(\frac{h-\ell}{\epsilon}\log\frac1\beta\right)
\tag{46}
```

original sampler calls, with two calls per source, when the target mean accuracy is $`\epsilon`$ and the source means differ from the target by at most $`\epsilon/32`$. The conversion's arithmetic, synthesis and workspace costs remain separate. This is a range-based result, not a variance bound for every bounded distribution. Together with the matching worst-case lower bounds, it gives the $`\epsilon^{-2}`$ to $`\epsilon^{-1}`$ change between one allowed use and two allowed uses in the full changing-garbage model.

## 7. What must remain coherent

The sampler workspace must remain coherent through its $`2k`$-call local attempt, including the matching inverse. It is then measured and discarded. The probe persists across all attempts belonging to one Ramsey shot. At the finest scale, that shot contains

```math
L_K=\Theta\!\left(\frac1{k^2\epsilon}\right)
\tag{47}
```

accepted rotations, as well as any corrected failures between them. Its expected number of attempts is at most $`2L_K`$, and its expected primitive interrogation count is $`O(1/(k\epsilon))`$. The global hard cap (40) bounds every execution, including an unusually long sequence of failures.

The result therefore separates local sampler lifetime from long-lived probe coherence. It does not remove the latter requirement, turn a classical sample interface into reversible access, or establish tolerance to arbitrary channel noise. The precise source, gate, arithmetic and reset costs are kept explicit in [resources-and-robustness.md](resources-and-robustness.md).

## References

1. G. Brassard, P. Høyer, M. Mosca and A. Tapp, *Quantum Amplitude Amplification and Estimation* (2002), amplitude-amplification construction. [arXiv:quant-ph/0005055](https://arxiv.org/abs/quant-ph/0005055).
2. N. Wiebe and V. Kliuchnikov, *Floating Point Representations in Quantum Circuit Synthesis*, New Journal of Physics **15**, 093041 (2013), Theorem 1. [arXiv:1305.5528v3](https://arxiv.org/abs/1305.5528v3).
3. N. Wiebe and M. Roetteler, *Quantum arithmetic and numerical analysis using Repeat-Until-Success circuits*, Quantum Information and Computation **16**, 134–178 (2016), Section II.B, Theorem 3. [arXiv:1406.2040v2](https://arxiv.org/abs/1406.2040v2).
4. J. Hu, T. Li, X. Wang, Y. Xue, C. Zhang and H. Zhong, *Quantum Non-Identical Mean Estimation: Efficient Algorithms and Fundamental Limits*, TQC 2024, LIPIcs **310**, article 9. The source model and previous replay-dependent bounds are their Definitions 6–7, Task 8, Theorems 12 and 25. [Published primary source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2024.9); [full version, arXiv:2405.12838v1](https://arxiv.org/abs/2405.12838v1).
