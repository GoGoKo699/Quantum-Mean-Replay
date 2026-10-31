# Lower bounds with charged local replay

The lower bounds on this page allow arbitrary quantum memory, intermediate measurements, and adaptive stopping inside a source window. They count the oracle calls that are actually made. Padding a source window for analysis does not charge unused calls.

For a known scale $`p_0`$, an unknown common Bernoulli mean $`p\in[p_0,2p_0]`$, and additive error $`\epsilon`$, the bounds are

```math
Q_1=\Omega\!\left(\frac{p_0}{\epsilon^2}\right),
\qquad
Q_m=\Omega\!\left(
\max\left\{\frac{\sqrt{p_0}}{\epsilon},
                 \frac{1}{m\epsilon}\right\}
\right)\quad(m\ge2).
```

Here $`m`$ is the maximum **total** number of calls to one source, counting forward, inverse, and controlled calls together. The first bound uses one-qubit sources. The replay-dependent lower bound uses sources with $`O(\log(1/\epsilon))`$ local qubits. Consequently, the combined law is a minimax statement over the allowed arbitrary-workspace source class; it is not a fixed-local-dimension optimality theorem for every $`m`$.

## 1. Operational model and theorem

The input is a fixed ordered list of unitary samplers $`U_1,\ldots,U_T`$. For a known output flag projector $`\Pi`$, each source obeys

```math
\langle 0|U_i^\dagger\Pi U_i|0\rangle=p_i.
```

The states within the good and bad flag subspaces, their phases, and the remaining columns of each unitary are unrestricted. The algorithm receives black-box access, not a classical description of the unknown unitary.

A finite protocol visits the sources in their supplied order. It can decide classically how long to use the current source, subject to at most $`m`$ calls, and can skip a source or stop altogether. Once it advances to the next source, it cannot return to an earlier one. It may retain arbitrary quantum memory between windows and perform arbitrary known operations and measurements. Source identities are not coherently addressed or reordered.

For the lower bounds we grant the stronger single-call primitive

```math
\mathsf W(U)
=|\mathrm{idle}\rangle\langle\mathrm{idle}|_D\otimes I
 +|\mathrm{fwd}\rangle\langle\mathrm{fwd}|_D\otimes U
 +|\mathrm{inv}\rangle\langle\mathrm{inv}|_D\otimes U^\dagger.
\qquad\text{(1)}
```

The three displayed direction labels are mutually orthonormal basis states. The direction register $`D`$ may be coherent. Ordinary forward, inverse, and controlled calls are special cases. Each physical invocation of (1) costs one call, including an invocation with amplitude on its identity branch. A classical decision not to invoke the primitive costs no call. A lower bound under this stronger direction primitive also applies when only the separate controlled versions are supplied.

The protocol has a deterministic worst-case cap $`Q`$ on the number of physical calls, on every run and every valid input. The number actually used may depend on measurement outcomes. We do not replace the pathwise cap by an expected-query assumption. Expected active-call counts will appear only as an analytical device, and each of them is bounded by this cap.

Known counters may enforce the local and global caps on every input, returning an arbitrary answer if a cap would be exceeded. This does not alter any valid run of the original bounded protocol. We use that enforced version when evaluating auxiliary trajectories that need not themselves satisfy the common-mean promise.

All hard inputs below have exactly equal means within a sequence. They therefore remain valid when the larger problem permits $`|p_i-p|\le\delta`$: a lower bound on the zero-drift subclass is also a lower bound for that larger class.

**Theorem 1.** Suppose

```math
0\lt p_0\le\frac1{16},\qquad
0<\epsilon\le\frac{p_0}{64}.
\qquad\text{(2)}
```

Assume that, for every valid fixed source sequence with common mean $`p\in[p_0,2p_0]`$, the protocol outputs $`\widehat p`$ satisfying

```math
\Pr\{ |\widehat p-p|\le\epsilon\}\ge\frac23.
\qquad\text{(3)}
```

Then:

1. If $`m=1`$, one-qubit hard sources already imply

   ```math
   Q\ge\frac{p_0}{81\epsilon^2}.
   \qquad\text{(4)}
   ```

2. For every $`m\ge1`$, one-qubit hard sources imply

   ```math
   Q\ge\frac{\sqrt{p_0}}{9\epsilon}.
   \qquad\text{(5)}
   ```

3. In the arbitrary-workspace source class, every $`m\ge1`$ obeys the combined bound

   ```math
   Q\ge\frac1{4096}
   \max\left\{
      \frac{\sqrt{p_0}}{\epsilon},
      \frac1{m\epsilon}
   \right\}.
   \qquad\text{(6)}
   ```

The constants are deliberately conservative. The proof of the second term in (6) uses a source of dimension $`2n`$, where $`n=\lfloor1/(4\epsilon)\rfloor`$. A qubit implementation embeds this space in fewer than $`4n`$ dimensions. The same hard family embeds in larger workspaces by extending the oracle with an identity action on the unused subspace.

We use normalized trace distance

```math
D(\rho,\sigma)=\frac12\|\rho-\sigma\|_1.
```

For pure states, $`D(|\psi\rangle,|\phi\rangle)=\sqrt{1-|\langle\psi|\phi\rangle|^2}`$. Quantum channels cannot increase this distance.

## 2. Estimation forces a constant testing advantage

Two means separated by at least $`4\epsilon`$ can be distinguished by thresholding an estimator satisfying (3). Under the smaller mean, the probability of exceeding the midpoint is at most $`1/3`$; under the larger mean it is at least $`2/3`$. Their output distributions therefore have total-variation distance at least $`1/3`$.

This remains true after independently averaging each hypothesis over any distribution of valid fixed oracle sequences. It also implies that the final quantum states before readout have trace distance at least $`1/3`$.

If the full computation is purified, including all measurement records and discarded environments, its final pure states must consequently satisfy

```math
|\langle\Psi_0|\Psi_1\rangle|
\le\sqrt{1-\frac19}
=\frac{2\sqrt2}{3}.
\qquad\text{(7)}
```

Keeping these environments is only a proof device. It gives the algorithm no additional access to its discarded information.

## 3. The ordinary coherent-query lower bound

Let

```math
\theta(p)=\arcsin\sqrt p,\qquad
R_p=
\begin{pmatrix}
\sqrt{1-p}&-\sqrt p\\
\sqrt p&\sqrt{1-p}
\end{pmatrix}.
\qquad\text{(8)}
```

Take every source in a sequence to be the same $`R_p`$. These are legal fixed sequences for every local replay cap. Compare

```math
p=p_0,\qquad q=p_0+4\epsilon.
```

Condition (2) ensures that both means belong to $`[p_0,2p_0]`$ and that $`q<1/2`$. Since

```math
\theta'(x)=\frac1{2\sqrt{x(1-x)}},
```

we have

```math
0<\theta(q)-\theta(p)
\le\frac{4\epsilon}{\sqrt{2p_0}}
<\frac{3\epsilon}{\sqrt{p_0}}.
\qquad\text{(9)}
```

The operator-norm difference of the rotations is

```math
\|R_q-R_p\|
=2\left|\sin\frac{\theta(q)-\theta(p)}2\right|
\le\theta(q)-\theta(p).
\qquad\text{(10)}
```

The same norm bound holds for their inverses and for the coherent direction selectors (1), because the difference is block diagonal in the direction register.

Purify the algorithm and pad its **global physical-call count** to $`Q`$ using inactive slots after it stops. Replace the oracle in these slots one at a time. Each replacement changes the final state vector by at most $`\|R_q-R_p\|`$; intervening isometries preserve vector norm. The resulting output trace distance is at most

```math
Q\|R_q-R_p\|
\le\frac{3Q\epsilon}{\sqrt{p_0}}.
\qquad\text{(11)}
```

The testing advantage from Section 2 requires this to be at least $`1/3`$, proving (5). This global padding is legitimate because it uses at most $`Q`$ slots. Padding each source separately to $`m`$ **charged** slots would not prove the sharper replay-dependent statement below.

## 4. One use of a fresh source is statistically classical in the worst case

The next construction removes any restriction on retained quantum memory. It uses changing per-source phases in the prepared output, which are allowed as part of the arbitrary-garbage promise.

### 4.1 A finite family of legal unitary samplers

Let $`Z=\operatorname{diag}(1,-1)`$. Independently for each source, draw

```math
a,b\in\{0,1\},\qquad c\in\{0,1,2,3\}
```

uniformly, and define

```math
U_{a,b,c;p}=i^c Z^a R_p Z^b.
\qquad\text{(12)}
```

Each draw specifies one fixed unitary and its exact inverse. It is not redrawn during a call. Its output flag probability on $`|0\rangle`$ is exactly $`p`$, regardless of $`a,b,c`$. The phases of its two output components need not agree between sources.

For a source queried once, average the direction-selector channel

```math
\rho\longmapsto
\mathsf W(U_{a,b,c;p})\rho\,
\mathsf W(U_{a,b,c;p})^\dagger
```

over these three finite choices. The calculation below is valid with an arbitrary reference system entangled with the direction and data registers.

### 4.2 Global phases remove cross-direction terms

The identity, forward, and inverse blocks acquire phases $`1,i^c,i^{-c}`$, respectively. The difference of any two of their exponents is $`\pm1`$ or $`\pm2`$. Therefore

```math
\frac14\sum_{c=0}^3 i^{rc}=0,
\qquad r\in\{-2,-1,1,2\}.
\qquad\text{(13)}
```

Averaging over $`c`$ removes all off-diagonal blocks between the three direction labels. This covers a coherent superposition of forward and inverse calls, as well as ordinary use/no-use control within a physically invoked call.

### 4.3 Row and column phases give a Bernoulli channel

Write computational-basis dephasing on the data qubit as

```math
\Delta(\rho)
=|0\rangle\langle0|\rho|0\rangle\langle0|
 +|1\rangle\langle1|\rho|1\rangle\langle1|.
```

For the forward block, averaging the right factor $`Z^b`$ first dephases the input. Averaging the left factor $`Z^a`$ then dephases the output. The squared entries of $`R_p`$ form a binary symmetric channel. Thus the averaged forward channel is exactly

```math
\mathcal B_p(\rho)
=(1-p)\Delta(\rho)+pX\Delta(\rho)X.
\qquad\text{(14)}
```

For the inverse block,

```math
U_{a,b,c;p}^\dagger
=i^{-c}Z^b R_p^{\mathsf T} Z^a.
```

The two phase averages exchange roles, and $`R_p^{\mathsf T}`$ has the same squared-entry matrix. Its averaged channel is also (14).

Equations (13)–(14) give a parameter-independent simulation of the complete averaged call: dephase the direction register; on its identity branch do nothing to the data; on either nonidentity branch dephase the data and apply $`X^B`$, where

```math
B\sim\operatorname{Bernoulli}(p).
```

Only one classical Bernoulli draw is needed. All other operations are known quantum channels. The draw may be unused on the identity branch, but it is still at most one draw per physical call. The identities hold completely, so arbitrary entanglement with the algorithm's memory does not change the simulation.

### 4.4 The complete adaptive experiment consumes at most $`Q`$ coins

When $`m=1`$, a newly queried source has never interacted with the algorithm. Its phase choices in (12) are independent of the complete prior history. We may therefore replace its averaged interaction by the channel above, then continue inductively through the protocol.

After averaging over a fixed random sequence of phase choices, the algorithm's output is obtainable from at most $`Q`$ independent Bernoulli$`(p)`$ draws by a quantum channel that does not depend on $`p`$. Adaptive stopping causes no difficulty: supply $`Q`$ coins in advance, consume the next coin whenever a physical call is made, and discard the remaining coins after stopping.

The protocol is required to work for every fixed phase sequence. It must therefore work for this averaged experiment too. Let $`P_p^{\otimes Q}`$ and $`P_q^{\otimes Q}`$ denote the distributions of the supplied coins under $`p=p_0`$ and $`q=p_0+4\epsilon`$. Data processing gives

```math
D(\rho_p,\rho_q)
\le d_{\rm TV}(P_p^{\otimes Q},P_q^{\otimes Q}).
\qquad\text{(15)}
```

For completeness, the required classical distance bound follows directly from Cauchy–Schwarz. If two distributions have affinity $`A=\sum_x\sqrt{P(x)Q(x)}`$, then

```math
d_{\rm TV}(P,Q)
\le\frac12
\sqrt{\left(\sum_x(\sqrt{P(x)}-\sqrt{Q(x)})^2\right)
      \left(\sum_x(\sqrt{P(x)}+\sqrt{Q(x)})^2\right)}
=\sqrt{1-A^2}.
\qquad\text{(16)}
```

The single-coin affinity is

```math
A_1=\sqrt{pq}+\sqrt{(1-p)(1-q)}
=\cos(\theta(q)-\theta(p)).
```

Affinities multiply for independent products. Since $`1-x^Q\le Q(1-x)`$ for $`0\le x\le1`$, equations (9), (15), and (16) imply

```math
\begin{aligned}
D(\rho_p,\rho_q)
&\le\sqrt{1-A_1^{2Q}}\\
&\le\sqrt Q\,\sin(\theta(q)-\theta(p))\\
&\le\frac{3\sqrt Q\,\epsilon}{\sqrt{p_0}}.
\end{aligned}
\qquad\text{(17)}
```

The required trace distance $`1/3`$ proves (4).

This is a worst-case lower bound for changing output garbage, already represented here by phases. It does **not** assert a one-use lower bound when every source has the same clean first column. That stronger promise can preserve a useful common measurement basis even when the other columns change.

## 5. A cost-aware fresh-source window lemma

The replay-dependent converse uses a separate hard family. Its proof tracks real overlap and relates an auxiliary trajectory's query cost to the costs of actual hard alternatives.

Let $`s\in\{0,1\}^n`$ have $`h`$ zero positions, collected in $`\mathcal Z`$. Index positions are $`0,\ldots,n-1`$. For $`i\in\mathcal Z`$, let $`s^{(i)}`$ be obtained by flipping its $`i`$-th bit to one. The Boolean query is

```math
O_s|j,b\rangle=|j,b\oplus s_j\rangle.
\qquad\text{(18)}
```

We allow arbitrary controls on this query. A source window contains at most $`m`$ actual calls. After purifying measurements, represent it using $`m`$ possible call slots. Let $`P_\ell`$ be the projector onto the classical histories in which a physical call occurs in slot $`\ell`$. Once a branch leaves the window, its remaining slots are inactive. This padding is an analytical representation: cost is the expected number of active calls, not $`m`$.

Any coherent control inside a physical invocation can be included in a smaller effective-use projector $`E_\ell\le P_\ell`$. The latter does not discount the cost: $`P_\ell`$, rather than $`E_\ell`$, defines the charged active-call probability. The index projector $`\Pi_i`$ commutes with these flags because the query index, invocation history, and direction control occupy separate registers. Known routing gates are included in the interleaving circuit.

Consider two arbitrary normalized incoming purified states $`|\psi_0\rangle,|\psi_1\rangle`$. Starting from $`\psi_0`$, run the window with $`O_s`$. Starting from $`\psi_1`$, run it either with $`O_s`$, as an auxiliary baseline, or with one of the alternatives $`O_{s^{(i)}}`$. Just before slot $`\ell`$, denote these states by

```math
|\psi_{0,\ell}\rangle,\qquad
|\overline\psi_\ell\rangle,\qquad
|\psi_{i,\ell}\rangle.
```

The known interleaving operations are the same in all runs; they may be controlled by retained measurement histories. Define

```math
\begin{aligned}
a_\ell^2&=\|P_\ell\psi_{0,\ell}\|^2,
&C_0&=\sum_{\ell=1}^m a_\ell^2,\\
b_\ell^2&=\|P_\ell\overline\psi_\ell\|^2,
&\overline C&=\sum_{\ell=1}^m b_\ell^2,\\
C_i&=\sum_{\ell=1}^m\|P_\ell\psi_{i,\ell}\|^2.
\end{aligned}
\qquad\text{(19)}
```

These are expected numbers of actual physical calls within this window under the corresponding states and oracle. Let the real-overlap loss be

```math
\Delta_i
=\operatorname{Re}\langle\psi_0|\psi_1\rangle
 -\operatorname{Re}
   \langle\psi_{0,\mathrm{out}}|\psi_{i,\mathrm{out}}\rangle.
\qquad\text{(20)}
```

It may be negative.

**Lemma 2.** If $`m\le\sqrt h/16`$, some $`i\in\mathcal Z`$ satisfies

```math
\Delta_i\le\frac{4m}{h}(C_0+C_i).
\qquad\text{(21)}
```

### 5.1 Comparing an alternative to the auxiliary baseline

Set

```math
\delta_{i,\ell}=\|\psi_{i,\ell}-\overline\psi_\ell\|,
\qquad
x_{i,j}=\|\Pi_i E_j\overline\psi_j\|.
```

The two Boolean queries differ only at index $`i`$, and their difference has operator norm at most two there. Replacing the first $`\ell-1`$ queries one at a time therefore gives

```math
\delta_{i,\ell}\le2\sum_{j<\ell}x_{i,j}.
\qquad\text{(22)}
```

The input states of these two runs are identical, namely $`\psi_1`$, so there is no initial-state term in this bound. The index projectors are mutually orthogonal, hence

```math
\sum_{i\in\mathcal Z}x_{i,j}^2
\le\|P_j\overline\psi_j\|^2=b_j^2.
```

Cauchy–Schwarz in the sum over slots yields

```math
\frac1h\sum_{i\in\mathcal Z}\delta_{i,\ell}^2
\le\frac{4m}{h}\sum_{j<\ell}b_j^2
\le\frac{4m}{h}\overline C.
\qquad\text{(23)}
```

For any projector $`P`$ and normalized vectors $`u,v`$, writing $`u=v+(u-v)`$ gives

```math
\big|\|Pu\|^2-\|Pv\|^2\big|
\le2\|Pv\|\,\|u-v\|+\|u-v\|^2.
\qquad\text{(24)}
```

Apply this to each active-call projector, average over $`i`$, and sum over slots. Equations (23) and $`\sum_\ell b_\ell\le\sqrt{m\overline C}`$ give

```math
\begin{aligned}
\frac1h\sum_i|C_i-\overline C|
&\le\sum_{\ell=1}^m
 \left(
  2b_\ell\sqrt{\frac{4m\overline C}{h}}
  +\frac{4m\overline C}{h}
 \right)\\
&\le
 \left(\frac{4m}{\sqrt h}+\frac{4m^2}{h}\right)\overline C.
\end{aligned}
\qquad\text{(25)}
```

If $`m\le\sqrt h/16`$, the coefficient is at most $`17/64<1/2`$. In particular,

```math
\frac1h\sum_i C_i\ge\frac{\overline C}{2}.
\qquad\text{(26)}
```

Thus the auxiliary trajectory cannot have a large expected call cost while every actual neighboring alternative has negligible cost. This is the step that permits actual-call accounting under adaptive stopping.

### 5.2 Bounding the average real-overlap loss

Known interleaving isometries preserve inner products. In one query slot, the change in overlap between the low run and alternative $`i`$ is determined by

```math
F_{i,\ell}
=V_{s,\ell}^\dagger V_{s^{(i)},\ell}-I,
```

where $`V`$ includes the call's controls. Because $`i`$ is a zero position of $`s`$,

```math
F_{i,\ell}=\Pi_i E_\ell(X-I)
```

on the Boolean query target, with identity actions on other registers understood. It has norm at most two and is supported on index $`i`$ and the active invocation subspace on both sides.

Split the alternative state as

```math
\psi_{i,\ell}
=\overline\psi_\ell+
  (\psi_{i,\ell}-\overline\psi_\ell).
```

The sum of the baseline terms satisfies

```math
\left|\sum_i
 \langle\psi_{0,\ell}|F_{i,\ell}|\overline\psi_\ell\rangle
\right|
\le2a_\ell b_\ell,
\qquad\text{(27)}
```

because $`\sum_iF_{i,\ell}`$ still has norm at most two on the orthogonal index sectors. For the remaining terms, (22) gives

```math
\begin{aligned}
\sum_i
 \left|
  \langle\psi_{0,\ell}|F_{i,\ell}
        (\psi_{i,\ell}-\overline\psi_\ell)\rangle
 \right|
&\le2\sum_i\|\Pi_iP_\ell\psi_{0,\ell}\|\,\delta_{i,\ell}\\
&\le4\sum_{j<\ell}\sum_i
   \|\Pi_iP_\ell\psi_{0,\ell}\|\,x_{i,j}\\
&\le4a_\ell\sum_{j<\ell}b_j.
\end{aligned}
\qquad\text{(28)}
```

The last step is Cauchy–Schwarz over the index positions. Summing the one-slot changes and then taking the real part proves

```math
\begin{aligned}
\frac1h\sum_i\Delta_i
&\le\frac1h
 \sum_{\ell=1}^m
 \left(2a_\ell b_\ell
       +4a_\ell\sum_{j<\ell}b_j\right)\\
&\le\frac4h
       \left(\sum_\ell a_\ell\right)
       \left(\sum_\ell b_\ell\right)\\
&\le\frac{4m}{h}\sqrt{C_0\overline C}\\
&\le\frac{2m}{h}(C_0+\overline C).
\end{aligned}
\qquad\text{(29)}
```

This is a bound on the average **real decrease**. We do not infer a small absolute summand from the absolute value of an average complex number.

### 5.3 Choosing a hard neighboring source

If every index violated (21), then averaging those strict inequalities and using (26) would give

```math
\begin{aligned}
\frac1h\sum_i\Delta_i
&>\frac{4m}{h}
    \left(C_0+\frac1h\sum_iC_i\right)\\
&\ge\frac{4m}{h}C_0+\frac{2m}{h}\overline C\\
&\ge\frac{2m}{h}(C_0+\overline C),
\end{aligned}
```

contradicting (29). Thus some index satisfies (21), proving Lemma 2. The argument also covers zero costs and negative overlap losses.

## 6. From the window lemma to a fixed hard input sequence

### 6.1 A Bernoulli sampler built from a Boolean string

Choose

```math
n=\left\lfloor\frac1{4\epsilon}\right\rfloor,
\qquad k=\lceil np_0\rceil,
\qquad h=n-k.
\qquad\text{(30)}
```

Under (2),

```math
\frac1{8\epsilon}\le n\le\frac1{4\epsilon},
\qquad np_0\ge8,
\qquad h\ge\frac n2\ge\frac1{16\epsilon}.
\qquad\text{(31)}
```

Fix any weight-$`k`$ string $`s`$. Let $`W_n`$ be a known unitary preparing the uniform index state from $`|0\rangle`$, and define

```math
U_s=O_s(W_n\otimes I).
\qquad\text{(32)}
```

The unitary $`W_n`$ depends only on the known integer $`n`$. It is an exact uniform-state preparer on this known index space, not a claim that a tensor product of Hadamards prepares a non-power-of-two uniform state. No unknown input data or QRAM is used. Then

```math
U_s|0,0\rangle
=\frac1{\sqrt n}\sum_{j=0}^{n-1}|j,s_j\rangle.
\qquad\text{(33)}
```

The output flag is Bernoulli with mean $`k/n`$; the index is garbage. Flipping any zero position changes the mean to $`(k+1)/n`$. Both belong to the required scale interval, because

```math
p_0\le\frac{k}{n}<\frac{k+1}{n}
\le p_0+\frac2n\le\frac54p_0<2p_0.
\qquad\text{(34)}
```

Their separation is $`1/n\ge4\epsilon`$.

Every forward or inverse sampler call can be simulated with one Boolean query and known gates. This remains true for the stronger selector (1): apply $`W_n`$ before the Boolean query on the forward branch, apply $`W_n^\dagger`$ after it on the inverse branch, and apply the controlled Boolean query on either nonidentity branch. On the inverse branch,

```math
U_s^\dagger=(W_n^\dagger\otimes I)O_s,
```

since $`O_s^\dagger=O_s`$. Known controls and basis changes do not depend on the unknown string. This reduction preserves both the local cap and the actual physical-call count.

### 6.2 A fixed pair of sequences, not an outcome-adaptive oracle

Use $`U_s`$ in every source window of the low-mean sequence. Construct the high-mean sequence inductively. At the start of window $`t`$, the prefixes already chosen determine two unconditional purified states of the algorithm. Apply Lemma 2 to these states and choose one index $`i_t`$ satisfying (21). Set the high-mean source in that window to $`U_{s^{(i_t)}}`$.

This choice is a mathematical function of the algorithm and its full unconditional incoming states. It is not made after observing a realized measurement result. Once the construction is complete, it specifies two ordinary fixed oracle lists. Every source in the first list has mean $`k/n`$; every source in the second has mean $`(k+1)/n`$. Their changing garbage is legal.

Because source order is classical and a source cannot be revisited, all branches can be aligned at the same nominal window boundary by waiting on branches that have already left it. These waits use no oracle calls. Measurements are purified with their records retained, so this reordering of operations on distinct classical histories preserves the original experiment. Skipped windows and permanently stopped branches are inactive. The fixed finite list can include all windows that the protocol might reach.

Write $`C_{0,t}`$ and $`C_{1,t}`$ for the expected numbers of actual calls in window $`t`$ under the two constructed fixed sequences. Summing Lemma 2 over the windows gives

```math
\operatorname{Re}\langle\Psi_0|\Psi_1\rangle
\ge1-\frac{4m}{h}\sum_t(C_{0,t}+C_{1,t}).
\qquad\text{(35)}
```

The auxiliary baseline costs $`\overline C`$ have disappeared. Each sum of actual expected costs is bounded by the pathwise cap $`Q`$, so

```math
\operatorname{Re}\langle\Psi_0|\Psi_1\rangle
\ge1-\frac{8mQ}{h}.
\qquad\text{(36)}
```

The oracle lists used to evaluate these costs are valid inputs. Choosing their later entries does not change earlier prefix costs.

### 6.3 Finishing the bound

For $`m\le\sqrt h/16`$, the required testing bound (7) and equation (36) imply

```math
Q\ge
\left(1-\frac{2\sqrt2}{3}\right)\frac{h}{8m}
>\frac{h}{144m}
\ge\frac1{2304m\epsilon}.
\qquad\text{(37)}
```

For larger $`m`$, use (31) to obtain

```math
\frac1{m\epsilon}
<\frac{16}{\epsilon\sqrt h}
\le\frac{64}{\sqrt\epsilon}
\le8\frac{\sqrt{p_0}}{\epsilon},
\qquad\text{(38)}
```

where the last inequality uses $`\epsilon\le p_0/64`$. Thus the ordinary bound (5) already controls both terms of the maximum in this regime. Combining (5), (37), and (38) proves the conservative uniform constant in (6).

The different terms may use different hard families. This is legitimate because $`Q`$ is one worst-case cap for an algorithm required to work on every valid input in the same scale window.

## 7. Scope and relation to earlier lower bounds

The fresh-source approximate-counting approach is closely related to Lemma 4.8 and Appendix B.4 of [Hu et al., *Quantum Non-Identical Mean Estimation: Efficient Algorithms and Fundamental Limits*, full version arXiv:2405.12838v1](https://arxiv.org/abs/2405.12838v1), subsequently published at TQC 2024 with different numbering. The proof here makes the actual paid-query accounting explicit under adaptive within-window stopping. It tracks real overlap and proves the auxiliary-to-actual cost comparison (25) before selecting the next hard source. These steps are needed for the stated adaptive resource law; a source-count bound or a fixed padded block count is not substituted for total calls.

The one-use phase-twirl argument is a separate worst-case construction for the full changing-garbage model. It does not claim that Hu's stronger common-prepared-column lower-bound construction remains hard after removing its workspace restriction. A common clean column can retain useful coherent information across fresh completions, which the arbitrary-garbage promise does not guarantee.

The sequential, nonreturning access rule is essential to the window induction. The proof does not cover later revisits to old sources, a free coherent SELECT over source identities, quantum-controlled source reordering, or indefinite causal order. Conversely, it imposes no restriction on the quantum memory retained between legal windows and does not assume that the algorithm measures or resets that memory after a source expires.

The hard families require exact unitary access and exact inverses, as does the stated oracle model. They make no claim about a device supplied only through classical samples or a noisy irreversible channel. Known gates, local workspace, and sustained probe coherence are separate resources from the query lower bounds proved here.
