# Fresh samplers, local replay and the optimal query law

## The question

A coherent sampler is more useful than one measured sample when the same sampler can be run backward and forward. Ordinary amplitude estimation repeatedly rotates in a plane defined by one preparation unitary. That plane can change completely when a new sampler arrives, even if its success probability is unchanged.

This project asks how much **local replay** is needed when a sampler is available for only one window. The answer separates three resources: the number of uses of each source, the total number of oracle calls, and the coherence retained between sources. A single persistent probe can carry the useful phase while the source's changing workspace is measured and discarded.

The precise oracle model follows the non-identical preparation setting of [Hu et al. (2024)](../references/related-work.md#non-identical-mean-estimation). The result below concerns arbitrary changing output states and unitary completions. A stronger promise that all sources share a known clean two-dimensional preparation plane defines a different problem.

## 1. Oracle and access model

There is a known input state $`|0\rangle`$ in a finite source workspace and a known projector $`\Pi`$ marking success. Source $`i`$ is an otherwise arbitrary unitary $`U_i`$. Its success probability is

```math
p_i=\langle0|U_i^\dagger\Pi U_i|0\rangle.
```

With an explicit flag qubit this is equivalently

```math
U_i|0\rangle
=\sqrt{1-p_i}\,|\psi_{i,0}\rangle|0\rangle
+\sqrt{p_i}\,|\psi_{i,1}\rangle|1\rangle.
```

The two garbage states, their phases, and the action of $`U_i`$ away from the input can change arbitrarily with $`i`$. No classical descriptions of these unknown states or of $`U_i`$ are supplied. The flag projector and a reflection about the known input are available as ordinary local operations. The workspace size is finite for each instance; the minimax class allows it to depend on the requested accuracy.

### Sequential source windows

The algorithm receives sources in chronological order. In window $`i`$, it may invoke $`U_i`$ or its **exact inverse** $`U_i^\dagger`$ at most $`m`$ times in total. After retiring that window it cannot return to the source. There is no coherent SELECT oracle over different source identities.

Algorithms are finite protocols, possibly adaptive. Intermediate measurements, resets, classical stopping decisions and arbitrary persistent quantum memory are allowed. Source retirement and actual invocation decisions are classical, possibly conditioned on previous measurement records. A quantum-controlled use of the current oracle is permitted. One executed controlled invocation costs one call, regardless of its control amplitude. A call omitted after a classical stopping decision costs zero. Padding a proof with possible query slots does not make those slots paid calls.

The lower bounds also hold in a stronger model that gives, at unit cost, a coherent selector among the identity, forward and inverse operations for the **current** source. The upper algorithm needs only ordinary forward and inverse calls; it does not require this additional selector or a controlled version of an unknown successful gate.

The sources can be fixed adversarially before the experiment. No promise of independent random choices, common garbage states or common unitary completion is required. The upper bound remains valid when the next source is chosen from the past classical record, provided its stated probability promise holds conditionally and its unitary stays fixed during its window. The lower bound already uses fixed valid source sequences.

### Estimation and cost

The goal is to output $`\widehat p`$ with

```math
\Pr\bigl[|\widehat p-p|\le\epsilon\bigr]\ge 2/3.
```

The probability is over the algorithm's measurements and random choices. A worst-case total-query budget bounds the number of physical oracle calls on every outcome path. Write $`Q_m(p_0,\epsilon,\delta)`$ for the smallest such budget that works for every valid source sequence in the following promised class:

```math
0\lt p_0\le\frac1{16},\qquad
p\in[p_0,2p_0],\qquad
0<\epsilon\le\frac{p_0}{64},\qquad
|p_i-p|\le\delta\le\frac{\epsilon}{32}.
```

The scale $`p_0`$, target accuracy and replay cap are known; the center $`p`$ is not. Constants in asymptotic notation below are absolute. Both upper and lower bounds use the same worst-case total-call convention, while allowing adaptive stopping and charging only executed calls. The exact-common-mean subclass $`\delta=0`$ suffices for every lower bound.

## 2. Main theorem: the local-replay frontier

**Theorem 1.** In the preceding model,

```math
Q_1(p_0,\epsilon,\delta)
=\Theta\!\left(\frac{p_0}{\epsilon^2}\right),
```

and, for every integer $`m\ge2`$,

```math
Q_m(p_0,\epsilon,\delta)
=\Theta\!\left(
\max\!\left\{\frac{\sqrt{p_0}}{\epsilon},\frac1{m\epsilon}\right\}
\right).
```

The upper bound can achieve success probability at least $`1-\beta`$, for $`0<\beta\le1/2`$, by multiplying the displayed query bound by $`O(\log(1/\beta))`$. It uses one persistent probe qubit in addition to the current source's workspace and classical memory. The lower bound permits arbitrary persistent quantum memory.

The adaptive replay lower-bound family uses $`O(\log(1/\epsilon))`$ local source qubits. Thus the theorem is minimax over the stated arbitrary-workspace class. It does not assert the same complete frontier for every fixed one-qubit source model. The one-use endpoint and the ordinary amplitude-estimation lower bound do already have one-qubit hard instances.

### Proof dependencies

| Ingredient | Authoritative proof | What it establishes |
|---|---|---|
| Mean-to-phase transduction | [Phase transduction](phase-transduction.md) | A two-sided source call produces a useful probe rotation, or a perfectly correctable failure. |
| Local amplification and inference | [Replay algorithm](replay-algorithm.md) | The probability sensitivity grows quadratically with local amplification length, giving the full upper bound with a hard total-call budget. |
| Finite-twirl simulation | [Lower bounds](lower-bounds.md) | Each phase-twirled source in the one-use hard family can be simulated with one classical Bernoulli draw, even with quantum memory. |
| Rotation and fresh-count adversaries | [Lower bounds](lower-bounds.md) | The two lower-bound terms survive adaptive stopping and charge actual calls. |
| Implementation and error accounting | [Resources and robustness](resources-and-robustness.md) | The query law's access, arithmetic, coherence and noise assumptions. |

For $`m=1`$, measuring the flag of each fresh source gives Bernoulli observations with means within $`\delta`$ of $`p`$ and variances at most $`3p_0`$. A Bernstein bound gives the claimed upper bound, since the bias is at most $`\delta`$. The finite-twirl lower bound gives the matching order. For $`m\ge2`$, the two upper-bound components and the two matching lower bounds in the linked proofs complete the theorem.

## 3. What changes when replay becomes available?

| Replay regime | Optimal total-query order at constant confidence | Interpretation |
|---|---|---|
| $`m=1`$ | $`p_0/\epsilon^2`$ | In the worst case, changing sources hide all phase information beyond a classical coin. |
| $`2\le m\lesssim p_0^{-1/2}`$ | $`1/(m\epsilon)`$ | Local replay increases the phase sensitivity that can be transferred to the persistent probe. |
| $`m\gtrsim p_0^{-1/2}`$ | $`\sqrt{p_0}/\epsilon`$ | The usual rare-event amplitude-estimation order is reached. |

The crossover in the last two rows is a statement up to constant factors. It depends on the known probability scale, not on the precision: $`m=\Theta(p_0^{-1/2})`$ is sufficient and necessary, up to constants, to reach the ordinary $`\sqrt{p_0}/\epsilon`$ query order. In contrast, directly using a single source for amplitude estimation would require a coherent sequence whose length grows with the target precision.

For example, take relative error $`r=\epsilon/p_0\le1/64`$. The one-use cost is of order $`1/(p_0r^2)`$; the two-use cost is of order $`1/(p_0r)`$; and sufficient replay gives order $`1/(\sqrt{p_0}r)`$. The first gain improves precision dependence. The additional replay gain improves rare-event dependence. These are asymptotic resource statements, not gate-count or hardware-runtime forecasts.

### Bounded means

**Corollary 2.** For success probabilities throughout $`[0,1]`$, with $`|p_i-p|\le\epsilon/32`$ and small positive $`\epsilon`$, worst-case additive mean estimation requires $`\Theta(\epsilon^{-2})`$ calls when $`m=1`$, and $`\Theta(\epsilon^{-1})`$ calls when $`m\ge2`$, at constant confidence.

The two-use algorithm takes no local amplification: the base transducer's relative phase has derivative magnitude between 2 and 4 throughout the interval. The same multiscale inference proof applies, including the endpoints. A fixed interior probability interval supplies the lower bounds. For numeric outputs in a known interval $`[L,H]`$, an explicit reversible value-to-coin conversion gives the corresponding orders $`\Theta((H-L)^2/\epsilon^2)`$ and $`\Theta((H-L)/\epsilon)`$, subject to the precision and local-operation costs in the [resource ledger](resources-and-robustness.md).

## 4. Mechanism and physical interpretation

The useful invariant is the scalar expectation of a reflection about the success subspace. Sandwiching that reflection between a preparation and its inverse returns its mean information to the known input direction. A measured, correctable transducer converts the invariant to a phase on a separate probe. All source-specific output directions are then disposable.

Local amplitude amplification increases the derivative of the probability-to-phase map by a factor of order $`k^2`$ while using order $`k`$ source calls per attempt. Multiscale Ramsey measurements convert the accumulated phase into an estimate with no extra logarithm in $`1/\epsilon`$. The first amplification lobe limits useful $`k`$ to order $`p_0^{-1/2}`$; the replay cap also limits it to order $`m`$. These two limitations produce the two terms of Theorem 1.

The persistent probe is essential to the stated construction. A small quantum-memory size does not imply short coherence time: the finest Ramsey experiments retain a phase across many fresh sources. The result isolates **local source reuse** as a resource while allowing long-lived coherence in the probe. It does not give a copies-only protocol or a noise-resilient constant-depth estimator.

## 5. Boundaries of the result

The known scale, sequential access, uniform drift promise and exact within-window inverse are load-bearing assumptions. Arbitrary forward/inverse mismatch is not covered by the drift parameter. Error in a paired, consistently compiled sampler is different from an independently faulty inverse. Neither unrestricted source drift nor adaptation to an unknown rare-event scale is established here.

The phase transducer and amplitude-amplification identity are inherited ingredients. The contribution is their fresh-source composition and matching resource law, with an adaptive lower bound in actual paid queries. The [related-work account](../references/related-work.md) identifies the precise comparison and what is not claimed. Numerical checks in [verification](../verification/README.md) stress the identities and algorithm; the analytical proofs establish the asymptotic guarantees.
