# Thirty milestones for Quantum Mean Replay

This map follows the scientific argument from its mathematical ingredients to the complete resource theorem. It has exactly 30 milestones in two phases: **background/preliminaries** (M01–M12) and **narrative/innovation** (M13–M30). Within each phase, local objects and operations lead to an integrated account. M12 and M30 are the respective synthesis milestones.

The 12/18 allocation follows the project. Twelve milestones establish a shared language for reversible sampling, measurement, phase geometry, probability and distinguishability. Eighteen then develop the project-specific composition, robust inference and matching converse. The adaptive lower bound receives its own sequence because accounting for actual calls is a substantive part of the result. The allocation does not assume a particular reader's background or pace.

The sole educational anchor is Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, **10th Anniversary Edition (2010)**, abbreviated **N&C** below. Section numbers were verified against the [publisher's contents](https://assets.cambridge.org/97811070/02173/toc/9781107002173_toc.pdf). The [anchor and bridge](anchor-and-bridge.md) explains how those foundations connect to this project. N&C supplies the background; the linked scientific sections supply the source-expiration model and the actual project proofs. In particular, the textbook pointers do not attribute the fresh-source theorem, gearbox composition, robust Ramsey schedule or adaptive window lemma to N&C.

Dependencies below name only earlier milestones. They describe the conceptual order of the argument. The authoritative scientific account remains in [science/](../science/README.md); this map does not replace its proofs or extend its assumptions.

## Phase I — background/preliminaries

### M01 — Marked probabilities

**Phase:** background/preliminaries.

**Central question:** How does a quantum preparation specify the mean of a Bernoulli observation?

**Understanding target:** The Born rule associates the marked projector with a scalar probability. Amplitudes, relative phases, and the resulting probability are distinct objects; observing the success flag reveals only a binary outcome.

**Dependencies and story role:** None. This supplies the quantity that every later operation must preserve, transform or estimate.

**Conceptual connection:** A projector turns the quantum state into the statistical parameter of an estimation problem.

**Source pointers:** N&C §§2.2.1, 2.2.3 and 2.2.5. Project: [Model and results, §1](../science/model-and-results.md#1-oracle-and-access-model).

### M02 — Unitary preparation and exact inverse access

**Phase:** background/preliminaries.

**Central question:** What information and operations are supplied by reversible access to a sampler?

**Understanding target:** A preparation unitary specifies an operation on the entire workspace, not just its action on the initialized state. Its adjoint reverses that operation. Receiving a prepared state, receiving classical samples, knowing a circuit description and being able to invoke an unknown unitary and its inverse are different access assumptions.

**Dependencies and story role:** M01. This identifies the resource that will later be limited to one source window.

**Conceptual connection:** Reversibility is an operational capability; it cannot be inferred merely from a probability distribution.

**Source pointers:** N&C §§2.1.6, 2.2.2 and 4.6. Project: [Model and results, §1](../science/model-and-results.md#1-oracle-and-access-model) and [Resources and robustness, Scope](../science/resources-and-robustness.md#scope).

### M03 — Garbage, tensor products and reference systems

**Phase:** background/preliminaries.

**Central question:** Which parts of a prepared state can vary while its marked probability stays fixed?

**Understanding target:** The success flag can be correlated with arbitrary workspace states. A retained probe can also be entangled with an untouched reference. Tracing out a register and preserving an entangled state impose different requirements from checking a formula on an isolated qubit.

**Dependencies and story role:** M01–M02. This makes the arbitrary-garbage promise and the later reference-entanglement calculation precise.

**Conceptual connection:** Reduced states express the information locally available; purification exposes the correlations an operation must respect.

**Source pointers:** N&C §§2.1.7, 2.2.8, 2.4.3 and 2.5. Project: [Model and results, §1](../science/model-and-results.md#1-oracle-and-access-model) and [Phase transduction, §§1–2](../science/phase-transduction.md#1-access-and-notation).

### M04 — Measurement branches as quantum operations

**Phase:** background/preliminaries.

**Central question:** How can a measurement outcome describe both a probability and an operation on an unmeasured system?

**Understanding target:** A branch operator gives an unnormalized post-measurement state; its squared norm gives the branch probability. Normalization, averaging over outcomes and conditioning on one outcome are different operations. The operator-sum description remains meaningful when another system is entangled with the measured circuit.

**Dependencies and story role:** M02–M03. This supplies the language for a useful branch and a correctable failure branch.

**Conceptual connection:** A measurement record can identify a known reversible disturbance without revealing information about the retained quantum state.

**Source pointers:** N&C §§2.2.3, 2.2.6, 8.2.2 and 8.2.3. Project: [Phase transduction, §2](../science/phase-transduction.md#2-the-instrument-identity).

### M05 — Control and relative phase

**Phase:** background/preliminaries.

**Central question:** When can a phase affect a measurable interference pattern?

**Understanding target:** An overall phase on an isolated state is unobservable, while phases between coherent branches can affect interference. A supplied controlled oracle can expose a phase that was global for its uncontrolled action. Control of a known circuit and access to a controlled unknown oracle must therefore be stated separately.

**Dependencies and story role:** M02–M04. This supports the probe coupling and the converse's treatment of forward, inverse and idle branches.

**Conceptual connection:** The meaning of an apparently irrelevant phase depends on the full controlled operation in which it appears.

**Source pointers:** N&C §§2.2.7 and 4.3. Project: [Model and results, Sequential source windows](../science/model-and-results.md#sequential-source-windows) and [Lower bounds, §§1 and 4.2](../science/lower-bounds.md#1-operational-model-and-theorem).

### M06 — Reflections in known and prepared directions

**Phase:** background/preliminaries.

**Central question:** How does conjugating a reflection move its geometrical meaning between input and output spaces?

**Understanding target:** A projector defines a Hermitian involution through $`S=I-2\Pi`$. Conjugation by a unitary preserves this structure. A reflection about a known input and a reflection about a marked subspace play different circuit roles, with their implementation costs kept explicit.

**Dependencies and story role:** M01–M03 and M05. This prepares the common algebra underlying local amplification and phase transduction.

**Conceptual connection:** Geometry of subspaces becomes an implementable circuit through preparation, reflection and unpreparation.

**Source pointers:** N&C §§2.1.6, 2.1.8 and 6.1.2–6.1.3. Project: [Phase transduction, §1](../science/phase-transduction.md#1-access-and-notation) and [Replay algorithm, §2.1](../science/replay-algorithm.md#21-local-grover-preparation).

### M07 — Probe phase and Ramsey readout

**Phase:** background/preliminaries.

**Central question:** How can a single qubit store a phase and reveal its sine and cosine?

**Understanding target:** A rotation about the probe's $`Z`$ axis changes a relative phase. Two complementary measurement bases provide its quadratures. The sign convention matters: for the project's positive exponential convention, the observables are $`X`$ and $`-Y`$.

**Dependencies and story role:** M03–M05. This identifies the small persistent system that will retain information after a source disappears.

**Conceptual connection:** The Bloch-sphere description of a qubit turns a sequence of phase rotations into a classical inference problem.

**Source pointers:** N&C §§2.1.3, 2.2.7, 4.2 and 4.4. Project: [Phase transduction, §3](../science/phase-transduction.md#3-why-a-fresh-source-can-replace-a-failed-source).

### M08 — The Grover rotation plane

**Phase:** background/preliminaries.

**Central question:** Why do two reflections produce useful amplification of a marked probability?

**Understanding target:** A preparation separates into normalized good and bad components. Alternating the corresponding reflections rotates within their two-dimensional span. Amplification is periodic, and its monotone initial region matters when the goal is to recover an unknown probability.

**Dependencies and story role:** M01–M02 and M06. This establishes the local amplification mechanism before asking whether its plane persists across different sources.

**Conceptual connection:** Search geometry connects probability amplification to phase and counting problems; the relevant plane is determined by the current preparation.

**Source pointers:** N&C §§6.1.1–6.1.4 and 6.3. Project: [Replay algorithm, §§2.1–2.2](../science/replay-algorithm.md#21-local-grover-preparation). The project states the generalized preparation identity explicitly.

### M09 — Conditional probability, bias and confidence

**Phase:** background/preliminaries.

**Central question:** Which statistical statements survive when observations or accepted sources are non-identical?

**Understanding target:** Mean bias, statistical fluctuations and failure probability require separate accounting. Conditioning on acceptance can change a source mixture. A bound on every conditional mean is a different premise from independence or identical distributions; a hard execution cap is different from an expected cost.

**Dependencies and story role:** M01 and M04. This supplies the statistical distinctions needed for drift control and a finite query budget.

**Conceptual connection:** Classical probability remains necessary after coherent processing because the final estimator is built from measurement records.

**Source pointers:** N&C Appendix 1, *Notes on basic probability theory*, for probability foundations. Project: [Replay algorithm, §§3–4](../science/replay-algorithm.md#3-convert-each-locally-amplified-source-into-a-probe-rotation) and [Resources and robustness, What the drift guarantee covers](../science/resources-and-robustness.md#what-the-drift-guarantee-covers). The conditional concentration argument is supplied by the project.

### M10 — Coarse-to-fine phase inference

**Phase:** background/preliminaries.

**Central question:** How can multiple interrogation lengths remove phase ambiguity while improving precision?

**Understanding target:** A longer interrogation increases sensitivity but returns phase modulo a full turn. Coarser information can choose the correct representative at a finer scale. Textbook phase estimation provides the broader connection; its controlled powers of a common unitary are distinct from the project's measured phase-transfer implementation.

**Dependencies and story role:** M05, M07 and M09. This organizes the later Ramsey schedule into an inference problem with sensitivity, ambiguity and confidence costs.

**Conceptual connection:** Resolution and aliasing are coupled: accumulating more phase is useful only when the correct phase branch remains identifiable.

**Source pointers:** N&C §§5.2–5.2.1 and 6.3. Project: [Replay algorithm, §4](../science/replay-algorithm.md), whose explicit schedule and unwrapping proof are the project-specific bridge.

### M11 — Distinguishability and query hybrids

**Phase:** background/preliminaries.

**Central question:** How does a limit on distinguishability become a lower bound on oracle calls?

**Understanding target:** Trace distance bounds the advantage of every measurement, and quantum processing cannot increase distinguishability. A hybrid argument replaces one oracle use at a time and controls the accumulated change. Purification can retain measurement records for analysis without granting the implemented algorithm extra access.

**Dependencies and story role:** M02–M04 and M09. This provides the common proof language for the three lower-bound ingredients.

**Conceptual connection:** Estimation accuracy forces distinguishable hypotheses, whereas a query bound restricts how quickly those hypotheses can separate.

**Source pointers:** N&C §§2.2.4, 2.5, 6.6–6.7 and 9.2.1–9.2.3. Project: [Lower bounds, §§2–3](../science/lower-bounds.md#2-estimation-forces-a-constant-testing-advantage).

### M12 — Integrating reversible estimation and its resource ledger

**Phase:** background/preliminaries.

**Central question:** What must a complete coherent estimation argument specify beyond a useful state transformation?

**Understanding target:** The preparation, inverse, marking operations, measurement, inference and converse fit into one operational account. Query count, known-gate cost, workspace size, local source lifetime and persistent coherence are separate quantities. Standard amplification and phase-estimation mechanisms identify where repeated access to the same preparation enters.

**Dependencies and story role:** M01–M11. This integrates the first phase and isolates the question that the fresh-source model will change.

**Conceptual connection:** An algorithmic advantage is a statement about an access model and a resource budget, supported by both an implementation and a matching obstruction.

**Source pointers:** N&C §§3.2.1, 4.6, 5.2.1 and 6.7. Project: [Scientific account](../science/README.md), [Model and results, §1](../science/model-and-results.md#1-oracle-and-access-model), and [Resources and robustness, Explicit cost ledger](../science/resources-and-robustness.md#explicit-cost-ledger).

## Phase II — narrative/innovation

### M13 — The expiring-source problem and precise promises

**Phase:** narrative/innovation.

**Central question:** What changes when each sampler is available only in its current source window?

**Understanding target:** Sources have arbitrary changing garbage and unitary completions, with an exact paired inverse available during the current window. Forward, inverse and controlled physical invocations share the local cap $`m`$; retired sources cannot be revisited, and no coherent SELECT across source identities is supplied. The rare-event theorem assumes known $`0\lt p_0\le1/16`$, unknown $`p\in[p_0,2p_0]`$, $`0<\epsilon\le p_0/64`$, and pointwise drift $`|p_i-p|\le\delta\le\epsilon/32`$.

**Dependencies and story role:** M02–M03, M05 and M12. This establishes the exact problem before introducing the construction.

**Conceptual connection:** Equal or nearby probabilities do not imply a common output state or a common Grover plane.

**Source pointers:** N&C §§4.6 and 6.1.1 for the oracle-model background. Project: [Model and results, §1](../science/model-and-results.md#1-oracle-and-access-model) and [Replay algorithm, §1](../science/replay-algorithm.md#1-the-upper-bound-theorem).

### M14 — The local mean-to-phase circuit

**Phase:** narrative/innovation.

**Central question:** Which scalar information can be returned to the known input direction before a source expires?

**Understanding target:** The reflection expectation $`z=1-2q`$ survives arbitrary workspace directions. Sandwiching the known source–probe coupling between a preparation and its exact inverse produces a branch operator proportional to $`I+izZ`$ on the probe. A local preparation/inverse pair is therefore a candidate interface for transferring the marked probability.

**Dependencies and story role:** M04, M06–M07 and M13. This introduces the local circuit whose branches must be justified next.

**Conceptual connection:** Unpreparation converts information about a marked subspace into an amplitude on a known input direction.

**Source pointers:** N&C §§2.1.8, 4.3 and 8.2.3. Project: [Phase transduction, §§1–2](../science/phase-transduction.md#1-access-and-notation), particularly equations (7)–(10).

### M15 — Correctable failure with arbitrary reference entanglement

**Phase:** narrative/innovation.

**Central question:** Why can a failed local attempt leave the retained quantum information recoverable?

**Understanding target:** The complete workspace measurement has branch probabilities independent of the probe and its reference. The zero branch applies the stated probe rotation; every nonzero branch applies a scalar multiple of a known Pauli operation. Correction restores the full probe–reference state. The attempt's success herald checks whether the entire workspace returned to its initialized state; the sampler's original marking flag alone is generally insufficient.

**Dependencies and story role:** M03–M04 and M14. This establishes the exact composable instrument, including failures, rather than only a successful-state formula.

**Conceptual connection:** A branch operator proportional to a unitary separates classical outcome information from retained quantum information.

**Source pointers:** N&C §§2.5 and 8.2.2–8.2.3. Project: [Phase transduction, §2](../science/phase-transduction.md#2-the-instrument-identity) and [Resources and robustness, Explicit cost ledger](../science/resources-and-robustness.md#explicit-cost-ledger).

### M16 — Composition across changing sources and inherited gearbox credit

**Phase:** narrative/innovation.

**Central question:** Why can the next phase-transfer attempt use a completely different sampler?

**Understanding target:** Corrected failures restore the incoming probe, while successes add a phase determined only by the current marked probability. Source-specific workspace can therefore be measured and discarded. The phase map is the inherited gearbox/repeat-until-success mechanism; the project studies its composition across expiring sources. A coherent control of the accepted probabilistic gate is not assumed.

**Dependencies and story role:** M07 and M13–M15. This turns the local instrument into the stream-level primitive needed by the estimator.

**Conceptual connection:** A common scalar phase can compose even when the underlying source states and amplification planes do not.

**Source pointers:** N&C §§2.2.7 and 8.2.3 for the underlying phase and channel language. Project: [Phase transduction, §§3–5](../science/phase-transduction.md#3-why-a-fresh-source-can-replace-a-failed-source); original gearbox attribution is given in [§5](../science/phase-transduction.md#5-relation-to-the-original-gearbox) and [Related work](../references/related-work.md).

### M17 — Replay-capped amplification and phase sensitivity

**Phase:** narrative/innovation.

**Central question:** How much probability sensitivity can be created before one source must be retired?

**Understanding target:** The amplified preparation uses an odd length $`k`$ chosen to satisfy both the local replay cap and the first-lobe constraint. The amplified probability and transferred phase have derivative magnitudes of order $`k^2`$, while a complete attempt costs exactly $`2k`$ physical calls. The integer choice includes $`m=2,3,4,5`$ without fractional Grover iterations.

**Dependencies and story role:** M08 and M13–M16. This supplies the quantitative benefit of replay and the two limits on useful amplification.

**Conceptual connection:** A quadratic gain in local sensitivity competes with a linear cost per phase-transfer attempt.

**Source pointers:** N&C §§6.1.3–6.1.4 and 6.3 for search and counting geometry. Project: [Replay algorithm, §§2–3](../science/replay-algorithm.md#2-choose-an-amplification-length-that-fits-every-replay-budget).

### M18 — Drift after success-dependent selection

**Phase:** narrative/innovation.

**Central question:** How can the estimator remain controlled when successful attempts preferentially select some source means?

**Understanding target:** Success probabilities depend on the current source. The accepted sources therefore need not have an unbiased mean. The proof instead bounds every accepted phase pointwise, so its accumulated deviation is controlled on every success history. The promise also applies conditionally when later sources depend on earlier classical records.

**Dependencies and story role:** M09 and M15–M17. This supplies the robust input condition for phase inference without inserting an independence assumption.

**Conceptual connection:** Uniform deterministic error bounds can survive selection effects that would invalidate an average-case argument.

**Source pointers:** N&C Appendix 1 for conditioning and probability background. Project: [Replay algorithm, §3 and the proof in §4](../science/replay-algorithm.md#3-convert-each-locally-amplified-source-into-a-probe-rotation), and [Resources and robustness, What the drift guarantee covers](../science/resources-and-robustness.md#what-the-drift-guarantee-covers).

### M19 — Multiscale Ramsey inference without an extra precision logarithm

**Phase:** narrative/innovation.

**Central question:** How does the phase estimate gain fine resolution without paying the finest-scale cost at every scale?

**Understanding target:** Powers-of-two interrogation lengths provide increasingly fine phase information. Conditional concentration controls the two measured quadratures, and the nearest-lift argument resolves their modular ambiguity. Allocating failure probability geometrically across scales yields a convergent weighted cost rather than an extra factor of $`\log(1/\epsilon)`$.

**Dependencies and story role:** M07, M09–M10 and M18. This establishes the estimator's precision and confidence guarantee before imposing a finite attempt budget.

**Conceptual connection:** Coarse information is inexpensive and can be made more reliable to protect later phase unwrapping.

**Source pointers:** N&C §§5.2–5.2.1 for the phase-estimation connection and Appendix 1 for probability background. Project: [Replay algorithm, §4](../science/replay-algorithm.md), especially the schedule, concentration, nearest-lift induction and geometric sums.

### M20 — A hard budget for actual attempts and calls

**Phase:** narrative/innovation.

**Central question:** How does a random sequence of successful and failed transfers fit within a deterministic query cap?

**Understanding target:** The schedule specifies a deterministic number of accepted transfers. A conditional success probability of at least one half supports a finite attempt cap with controlled failure probability. Every attempted transfer, including each failure and inverse, is charged. The algorithm never exceeds its hard physical-call cap; an expected attempt count alone is not the theorem's budget.

**Dependencies and story role:** M09 and M15–M19. This converts the inference construction into a legal finite protocol under the model's cost convention.

**Conceptual connection:** Statistical confidence and worst-case execution cost can be guaranteed together by explicitly allocating probability to budget exhaustion.

**Source pointers:** N&C §3.2.1 and Appendix 1 for resource and probability foundations. Project: [Replay algorithm, §§4–5](../science/replay-algorithm.md), particularly the attempt cap and explicit query cap, and [Model and results, Estimation and cost](../science/model-and-results.md#estimation-and-cost).

### M21 — The achieved rare-event and bounded-mean upper bounds

**Phase:** narrative/innovation.

**Central question:** How do the amplification choice, phase sensitivity and attempt budget combine into the upper frontier?

**Understanding target:** Inverting the monotone phase map turns phase accuracy into mean accuracy. Optimizing the allowed odd amplification length yields the maximum of the rare-event coherent term and the replay-limited term. With $`k=1`$, the same inference framework covers all Bernoulli means, including the endpoints, without a supplied rare-event scale. Reversible bounded-value conversion has separate arithmetic and workspace costs.

**Dependencies and story role:** M13 and M17–M20. This completes the constructive side before the matching obstructions are developed.

**Conceptual connection:** Local amplification and global accumulation contribute different factors to precision; the unamplified endpoint isolates the benefit of a preparation/inverse pair.

**Source pointers:** N&C §§5.2.1, 6.1.4 and 6.3 for standard precision and amplification context. Project: [Replay algorithm, §§5–6](../science/replay-algorithm.md#5-apply-the-estimator-to-the-rare-event-phase), and [Phase transduction, §6](../science/phase-transduction.md#6-bounded-values-and-compiled-arithmetic).

### M22 — Estimation-to-testing and the ordinary coherent limit

**Phase:** narrative/innovation.

**Central question:** What lower bound remains even when source reuse is plentiful?

**Understanding target:** An accurate estimator distinguishes two separated means with constant advantage. Two neighboring one-qubit preparation rotations differ by an angle of order $`\epsilon/\sqrt{p_0}`$. A global query hybrid then gives the ordinary coherent lower bound. These fixed repeated-source instances are legal for every replay cap.

**Dependencies and story role:** M11 and M13. This supplies the first term in the matching converse and the testing requirement used by the other hard families.

**Conceptual connection:** A small change in an oracle's rotation angle limits the information obtainable per physical invocation.

**Source pointers:** N&C §§6.6–6.7 and 9.2.1–9.2.3. Project: [Lower bounds, §§2–3](../science/lower-bounds.md#2-estimation-forces-a-constant-testing-advantage).

### M23 — The finite phase-twirl channel

**Phase:** narrative/innovation.

**Central question:** Can legal changes of source phases remove coherent information from a one-use query?

**Understanding target:** Independent finite global, row and column phase choices preserve the marked probability. Averaging the global phase removes coherence among current-source idle, forward and inverse directions. The remaining phase averages turn either query direction into a known dephasing operation followed by a Bernoulli-controlled bit flip, valid with arbitrary entangled memory.

**Dependencies and story role:** M03–M05, M11 and M13. This constructs the exact one-call channel used in the one-use converse.

**Conceptual connection:** Randomizing legal nuisance phases can expose which information is available uniformly over an oracle class.

**Source pointers:** N&C §§2.2.7, 4.3 and 8.2.3. Project: [Lower bounds, §§4.1–4.3](../science/lower-bounds.md#41-a-finite-family-of-legal-unitary-samplers).

### M24 — The one-use classical statistical obstruction

**Phase:** narrative/innovation.

**Central question:** Why can arbitrary quantum memory fail to improve the worst-case one-use estimation rate?

**Understanding target:** At $`m=1`$, each fresh averaged interaction consumes at most one classical Bernoulli draw. The entire adaptive quantum experiment is a parameter-independent channel acting on at most the hard cap's number of draws. Data processing and the product affinity bound then impose the classical statistical rate. This argument uses changing prepared phases and does not establish a lower bound for the stronger common-clean-column promise.

**Dependencies and story role:** M09, M11, M22–M23. This completes the one-use endpoint and identifies its precise oracle-class dependence.

**Conceptual connection:** Quantum processing of a classical statistical experiment cannot create additional information about its parameter.

**Source pointers:** N&C §§9.1 and 9.2.1–9.2.3. Project: [Lower bounds, §4.4](../science/lower-bounds.md) and [Resources and robustness, Boundaries of the lower bound and interpretation](../science/resources-and-robustness.md#boundaries-of-the-lower-bound-and-interpretation).

### M25 — Active-call accounting within a source window

**Phase:** narrative/innovation.

**Central question:** How can a lower-bound proof represent adaptive stopping without charging unused query slots?

**Understanding target:** A window can be padded with possible slots for analysis, while a projector on classical invocation histories records actual calls. A coherent control within an executed invocation does not discount its physical cost. Expected active-call counts are intermediate analytical quantities under a hard pathwise cap, not a replacement expected-budget assumption.

**Dependencies and story role:** M05, M11, M13 and M20. This sets up the cost convention needed for the replay-dependent window lemma.

**Conceptual connection:** A mathematical representation of a circuit must preserve the operational resource being bounded.

**Source pointers:** N&C §§3.2.1, 4.3–4.4 and 6.7. Project: [Lower bounds, §§1 and 5](../science/lower-bounds.md#5-a-cost-aware-fresh-source-window-lemma).

### M26 — Comparing auxiliary and actual trajectory costs

**Phase:** narrative/innovation.

**Central question:** How can a helpful auxiliary trajectory be related to the costs of valid hard alternatives?

**Understanding target:** The window proof compares a Boolean source with alternatives that flip one unmarked position. A hybrid bounds their departure from an auxiliary baseline. Orthogonal index sectors and Cauchy–Schwarz convert that departure into a comparison between baseline active-call cost and the average actual cost of the alternatives.

**Dependencies and story role:** M11 and M25. This prevents the final lower bound from depending on an uncontrolled auxiliary cost.

**Conceptual connection:** Localized oracle differences constrain both distinguishability and the changes in an adaptive algorithm's later invocation decisions.

**Source pointers:** N&C §§6.6–6.7 for query-limit background and §§2.1.7, 2.2.5 for the underlying register and projector language. Project: [Lower bounds, §5.1](../science/lower-bounds.md#51-comparing-an-alternative-to-the-auxiliary-baseline).

### M27 — Real-overlap loss and a hard neighboring source

**Phase:** narrative/innovation.

**Central question:** Which quantity can telescope across windows while remaining controlled by actual calls?

**Understanding target:** The proof bounds the average real decrease of purified-state overlap, rather than an absolute change inferred from a complex average. Combining that bound with the auxiliary-to-actual cost comparison selects a neighboring source whose overlap loss is controlled by the two real trajectories' charged costs. The lemma allows arbitrary incoming memory states.

**Dependencies and story role:** M11 and M25–M26. This completes the local adversary statement that can be composed across expiring sources.

**Conceptual connection:** Choosing the right progress quantity is what makes a local indistinguishability estimate composable.

**Source pointers:** N&C §§2.5 and 9.2.2–9.2.3 for purified-state overlap and distinguishability. Project: [Lower bounds, §§5.2–5.3](../science/lower-bounds.md#52-bounding-the-average-real-overlap-loss).

### M28 — Fixed hard sequences and the replay lower bound

**Phase:** narrative/innovation.

**Central question:** How does the local window lemma produce a legal worst-case input for the entire protocol?

**Understanding target:** A Boolean-string sampler encodes neighboring means with a known uniform index preparation and no QRAM. Hard sources are selected from unconditional incoming states to define fixed oracle lists, not in response to realized outcomes. Overlap losses telescope, and the pathwise call cap bounds the summed actual costs. The replay-dependent family uses $`O(\log(1/\epsilon))`$ local qubits; the remaining regime is covered by the ordinary coherent bound.

**Dependencies and story role:** M13, M22 and M25–M27. This completes the second lower-bound term with the correct input and workspace quantifiers.

**Conceptual connection:** A local adversary becomes a global minimax lower bound only after its input construction and its cost accounting remain valid together.

**Source pointers:** N&C §§6.1.1, 6.7 and 9.2.1 for oracle and distinguishability foundations. Project: [Lower bounds, §§6–7](../science/lower-bounds.md#6-from-the-window-lemma-to-a-fixed-hard-input-sequence).

### M29 — Implementation, precision and exact-inverse boundaries

**Phase:** narrative/innovation.

**Central question:** Which physical and computational resources are still required after the query law is established?

**Understanding target:** The ledger charges known reflections, value-to-coin arithmetic, workspace measurement, reset and primitive source implementations separately. Consistent finite-precision encoding with its exact compiled inverse can change the mean within the drift budget; an unmatched physical inverse can destroy the instrument even at zero mean drift. One persistent qubit may require long coherence across many sources. Numerical checks support specific identities and implementations, while the proofs establish the asymptotic theorem.

**Dependencies and story role:** M12–M21 and M28. This reconnects the upper and lower arguments to their actual access, implementation and validation limits.

**Conceptual connection:** Memory size, coherence duration, input construction, numerical precision and query complexity measure different constraints.

**Source pointers:** N&C §§3.2.1, 4.6 and 8.2.2–8.2.3. Project: [Resources and robustness](../science/resources-and-robustness.md), [Replay algorithm, §7](../science/replay-algorithm.md#7-what-must-remain-coherent), and [Verification](../verification/README.md).

### M30 — The matched frontier, resource separation and contribution

**Phase:** narrative/innovation.

**Central question:** What does the complete argument establish about local source reuse and global estimation precision?

**Understanding target:** The constructive algorithm and three converse ingredients yield the same minimax orders: the one-use classical endpoint, the replay-limited quantum regime and saturation at the ordinary rare-event coherent rate. The crossover depends on the known probability scale. The result separates local sampler lifetime from retained probe coherence, within the sequential arbitrary-workspace model and its hard actual-query cap. The phase primitive and amplification are inherited; their fresh-source composition and matched adaptive resource law are the project contribution.

**Dependencies and story role:** M12–M29. This integrates the second phase into the full theorem, its assumptions, its bounded-mean consequence and its proper novelty claim.

**Conceptual connection:** A resource frontier is explained by the mechanisms achieving each regime and the distinct obstructions that prevent further improvement.

**Source pointers:** N&C §§3.2.1, 5.2.1, 6.3 and 6.7 as the standard resource, phase-estimation and query-limit frame. Project: [Model and results, §§2–5](../science/model-and-results.md#2-main-theorem-the-local-replay-frontier), [Lower bounds, §7](../science/lower-bounds.md#7-scope-and-relation-to-earlier-lower-bounds), and [Related work](../references/related-work.md).
