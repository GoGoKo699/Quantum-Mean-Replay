# From Nielsen and Chuang to local replay

The educational anchor is Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, **10th Anniversary Edition (2010)**, Cambridge University Press, ISBN 9781107002173. The [publisher's book page](https://www.cambridge.org/highereducation/books/quantum-computation-and-quantum-information/01E10196D0A682A6AEFFEA52D53BE9AE) identifies the edition; its [official contents PDF](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf) verifies the section numbers and printed starting pages used below. These are contents-level checks, not a claim that every textbook argument has been independently audited.

This is the sole educational anchor. The [30-milestone map](milestones.md) organizes the project's understanding targets; it does not require reading the whole book first. The [worked walkthrough](walkthrough.md) supplies the missing connections. The research papers cited under [related work](../references/related-work.md) establish attribution and scientific dependencies; they are not additional introductory reading requirements.

## 1. A selective route through the anchor

The table selects the foundations needed for the settled map. Page numbers are the book's printed starting pages, not PDF page indices. The middle column explains their role here.

| Anchor sections | Foundation used in this project | Milestone connection |
|---|---|---|
| §§2.1.3, 2.1.6–2.1.8; §2.2.1 | Pauli matrices, adjoints, tensor products, operator functions, and state vectors. In particular, an operator squaring to the identity has a simple exponential. | M01–M03, M06 |
| §§2.2.2–2.2.3, 2.2.5 | Reversible evolution and the distinction between a measurement probability and its conditional state update. | M02, M04 |
| §§2.2.7–2.2.8; §§2.4, 2.4.3; §2.5 | Relative phase, composite registers, discarding a subsystem, and representing a mixed state using a larger pure state. | M03–M05, M15 |
| §3.2.1, p. 136; §§4.2–4.4, pp. 174, 177, 185 | Computational resources, single-qubit operations, controlled operations, and measurement in a circuit. | M05–M07, M12 |
| §5.2, **Phase estimation**, p. 221; §5.2.1, p. 223 | Why repeated rotations magnify a small phase, why phases are periodic, and why inference needs a success guarantee. | M07, M10 |
| §§6.1.1–6.1.4, pp. 248–253; §6.3, **Quantum counting**, p. 261 | Marking an event, composing reflections, and viewing search steps as a rotation in a two-dimensional plane. | M06, M08, M17 |
| Appendix 1, p. 608 | Basic probability language for outcomes, conditional distributions, averages, and uncertainty. | M09 |
| §§6.6–6.7, pp. 269, 271 | Oracle lower bounds and the distinction between a construction and an optimal resource law. | M11, M22–M28 |
| §§8.2.2–8.2.3, pp. 357, 360 | An auxiliary system, its measurement, and the induced operators on the retained system. Section 8.2.3 is **Operator-sum representation**. | M04, M14–M16, M23 |
| §9.1, p. 399; §§9.2.1–9.2.3, pp. 403–415 | Classical and quantum distinguishability and the relation between state overlap and measurement statistics. Section 9.2.1 is **Trace distance**. | M11, M22, M24–M28 |

In the background phase, M01–M08 build the local quantum objects, M09–M11 connect them to inference and limits, and M12 assembles the resource account. The narrative phase, M13–M30, develops the expiring-source problem, its upper construction, its converse, and the meaning of the matched result.

## 2. Notation and access translation

The book's general circuit vocabulary becomes a particular resource model here. A unitary can be mathematically invertible without an interface supplying its inverse. The project explicitly grants that interface during one source window and charges its use.

| Object | Meaning in this project |
|---|---|
| $`U_i`$ and $`U_i^\dagger`$ | One source and its exact inverse. The subscript identifies a supplied source window, not a freely addressable quantum index. Different sources can have unrelated unitary completions. |
| $`W`$ | The current source's full workspace, initialized in its known zero state. Its dimension need not be small. |
| $`\Pi`$ | A known projector marking the Bernoulli event. Its coherent implementation is a local resource; the theorem does not provide arbitrary data lookup for free. |
| $`p_i`$, $`p`$, $`p_0`$ | Respectively the current source's marked probability, the unknown target mean, and the supplied scale used by the rare-event theorem. |
| $`A_{i,k}`$ and $`q_k(p_i)`$ | A locally amplified preparation and its marked probability. When $`k=1`$, these are $`U_i`$ and $`p_i`$. |
| $`B`$ and $`E`$ | The retained probe qubit and an untouched reference system. The reference tests whether a correction preserves correlations, not just the probe's marginal state. |
| $`K_j`$ | The operator induced on the probe by a recorded workspace outcome. It includes that outcome's probability; the conditional state is obtained by normalization. |
| $`m`$ and $`Q`$ | Maximum total calls to one source, and worst-case total physical source calls. Forward and inverse uses count together. |
| $`\epsilon`$, $`\delta`$, $`\beta`$ | Target additive error, allowed per-source mean drift, and allowed failure probability. |

Keep three angles separate. With this project's convention,

```math
\theta=\arcsin\sqrt p,\qquad
\gamma(q)=\arctan(1-2q),\qquad
\varphi(q)=2\gamma(q).
```

The first is an amplitude angle: $`p=\sin^2\theta`$. The second appears in the probe gate $`T(q)=e^{i\gamma(q)Z}`$. The third is the phase difference visible in a Ramsey measurement. With the definition $`R_z(\lambda)=e^{-i\lambda Z/2}`$, the same gate is $`R_z(-2\gamma(q))`$. This fixes the sign and factor of two without depending on a textbook's choice of search-angle symbol.

For a probe initialized in $`|+\rangle=(|0\rangle+|1\rangle)/\sqrt2`$ and then acted on by $`T(q)`$, the corresponding readout is

```math
\langle X\rangle=\cos\varphi,\qquad
\langle-Y\rangle=\sin\varphi.
```

For lower bounds, the project's convention is $`D(\rho,\sigma)=\tfrac12\|\rho-\sigma\|_1`$. The factor one-half makes this trace distance directly comparable to the total-variation distance of outcome distributions.

## 3. The steps supplied by the project

### Reversible access during a limited window

The textbook circuit formalism describes a unitary and its adjoint. The input model instead supplies an unknown $`U_i`$ for a limited number of calls. Once its window is retired, it cannot be revisited. An allowed controlled invocation of the current source is one paid call regardless of its control amplitude. A classically omitted call is not paid. There is no coherent selector across source identities. These rules belong to [the model](../science/model-and-results.md#1-oracle-and-access-model), not to the textbook.

### A recorded measurement that preserves the useful quantum state

The bridge from the operator-sum formalism is to compute

```math
K_j=\langle j|_W V|0\rangle_W
```

for the entire prepare–couple–unprepare circuit. Finding $`K_j^\dagger K_j=s_jI_B`$ establishes that the outcome probability is independent of the incoming probe. It does not by itself identify the conditional operation: one must also calculate $`K_j/\sqrt{s_j}`$ for outcomes with $`s_j>0`$. A zero-probability outcome needs no conditional-state normalization. Here that operation is the desired phase gate on success and a known Pauli correction on failure. Tensoring these identities with $`I_E`$ verifies the statement for entangled inputs.

The [instrument proof](../science/phase-transduction.md#2-the-instrument-identity) supplies this calculation for an arbitrary preparation and workspace. Its circuit mechanism is inherited from gearbox/repeat-until-success work, credited there. The fresh-source resource conclusion comes from using the resulting interface correctly.

### Phase inference with the interface actually available

Section 5.2 motivates phase magnification, but its controlled-power viewpoint cannot simply be applied to an accepted, measured gate as though that gate were a coherent black box. The success record could reveal whether a controlled attempt occurred. The project instead runs each attempt unconditionally, corrects failures, and measures the probe after classically chosen numbers of accepted rotations.

The [Ramsey proof](../science/replay-algorithm.md) supplies phase lifting, a confidence schedule, and an attempt cap for this interface. Conditional concentration under changing sources, statistical error allocation across scales, and the cost of failed attempts are project-specific derivations; the contents map is not evidence that the book contains those results.

### Search geometry confined to one source

The search chapter supplies the geometry of two reflections. Here the good and bad directions can change with $`i`$, so a rotation plane defined by one source cannot be assumed to serve the next. The [local amplification construction](../science/replay-algorithm.md#2-choose-an-amplification-length-that-fits-every-replay-budget) makes all Grover steps within the current window. It then transfers a scalar phase to the common probe before discarding that workspace.

Sensitivity and cost must both be calculated: order $`k^2`$ probability sensitivity costs $`2k`$ primitive calls per attempt. A first-lobe restriction and the source cap determine which $`k`$ are legal. This is the bridge from search geometry to the rare-event frontier, not a claim that the anchor contains this project's theorem.

### A converse for the complete allowed algorithm

The textbook's distinguishability tools motivate a lower bound, but they do not supply the fresh-source theorem. The [lower-bound page](../science/lower-bounds.md) constructs a phase-twirled one-use hard family, an ordinary rotation obstruction, and a cost-aware Boolean-source adversary. The last argument selects a fixed source sequence from unconditional purified states and counts actual invocations under adaptive stopping.

Those quantifiers matter: the algorithm may retain arbitrary memory, the source sequence is fixed rather than reacting to observed outcomes, and the replay-dependent hard family uses $`O(\log(1/\epsilon))`$ local qubits. The accessible worked example does not replace these research-level proof dependencies.

## 4. Reading the complete result

The [walkthrough](walkthrough.md) follows the settled map through a complete small circuit and identifies the additional steps needed for the frontier. The [model and theorem](../science/model-and-results.md) remain authoritative for scope; the [resource account](../science/resources-and-robustness.md) separates query counts from known gates, arithmetic, workspace, readout and coherence.

Exact cancellation within one source window permits changing garbage between windows. Mean drift is therefore a different promise from a faulty inverse or general channel noise. The upper construction retains one probe, but its finest phase experiments still require that probe to remain coherent through many source windows. Both facts belong in the result's interpretation.
