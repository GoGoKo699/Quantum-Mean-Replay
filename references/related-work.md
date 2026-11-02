# Related work and attribution

The contribution is a local-replay law for fresh sequential samplers with arbitrary changing output garbage, together with a [shared all-time confidence theorem](../science/anytime-confidence.md). Its primitive components have established precedents. The comparison below concerns the stated access, error and query conventions; it is not an exhaustive priority claim for every related model.

## Non-identical mean estimation

[Hu, Li, Wang, Xue, Zhang and Zhong (TQC 2024)](https://doi.org/10.4230/LIPIcs.TQC.2024.9) formulate non-identical preparation oracles and analyze bounded and sub-Gaussian means. The comparison uses the published paper and [arXiv:2405.12838v1](https://arxiv.org/abs/2405.12838v1), especially the input model, bounded-mean upper bound and general-replay lower bound. Their bounded-mean algorithm requires logarithmic local reuse and has a logarithmic query overhead; their general-replay bound constrains fixed blocks. Their separate one-use argument uses a workspace restriction under its stronger construction.

Here two calls per source suffice for bounded means, with no logarithmic precision overhead in a terminal constant-confidence estimate. The known-scale rare-event law also identifies the crossover to the usual amplitude-estimation rate. The original lower bound in [lower-bounds.md](../science/lower-bounds.md) treats adaptive stopping in actual paid queries, using real overlap and an explicit auxiliary-cost comparison. The new [fresh-phase channel converse](../science/anytime-confidence.md#3-a-common-continuous-hard-family) establishes the replay lower order with one-qubit sources and strengthens it to multiscale all-time summability. Both phase constructions use arbitrary changing output phases; neither asserts that a stronger common-clean-column promise remains hard without a workspace restriction.

## Gearbox and repeat-until-success circuits

[Wiebe and Kliuchnikov (2013)](https://doi.org/10.1088/1367-2630/15/9/093041), Theorem 1, give gearbox circuits with a nonlinear angle transformation and correctable failure. [Wiebe and Roetteler (2016)](https://arxiv.org/abs/1406.2040v2) develop this structure for arithmetic and numerical analysis.

The reflection-based instrument in [phase-transduction.md](../science/phase-transduction.md) is an expression of this inherited mechanism for a general flagged preparation. The decisive composition property is that a failed attempt acts as a known correction on the probe, even with a reference system. A different fresh source can therefore be used next. We do not claim a new gearbox primitive or assume that an arbitrary controlled repeat-until-success operation preserves control amplitudes.

## Amplitude amplification and estimation

[Brassard, Høyer, Mosca and Tapp (2002)](https://doi.org/10.1090/conm/305/05215) supply the amplitude-amplification identity and the usual amplitude-estimation benchmark. For success probability $`p`$, their Theorem 12 has an error contribution of order $`\sqrt{p(1-p)}/M+1/M^2`$ after order $`M`$ uses of a fixed preparation and its inverse.

The present algorithm amplifies **within** one source window and then transfers a scalar phase to the common probe. It does not alternate Grover steps built from incompatible source-dependent planes. Its inferred replay threshold follows from combining local sensitivity with the matching lower bound, rather than directly applying fixed-source amplitude estimation.

## Distinguishing nearby models

| Model or guarantee | Relation to this project |
|---|---|
| Repeated access to one fixed preparation | Supplies amplitude-amplification ingredients, but removes the local lifetime constraint. |
| Fresh sources with one common known clean output plane | Can retain coherent information under stronger structural promises; it is not the arbitrary-garbage worst case. |
| Copies of output states without inverse access | Does not implement the source-local transducer analyzed here. |
| Fresh sources with close means but unrelated distributions | Covered after a charged reversible conversion to a flag, under the uniform drift promise. |
| General bounded-variance or sub-Gaussian means | Not established by the range-based result here. |
| Exact unbiased output with a prescribed variance | A separate estimator guarantee; the Ramsey estimate here is an additive-accuracy output. |

Additional fixed-source mean-estimation approaches, including quantum phase estimation for lattice field theory and generalized-Grover constructions, do not directly settle the fresh-source lifetime question. The main theorem neither claims those methods are invalid nor imports their distinct output guarantees.

## Committed confidence and the sister result

[Anytime Quantum Estimation](https://github.com/GoGoKo699/Anytime-Quantum-Estimation) studies one coherent run whose committed classical outputs remain simultaneously correct at progressively finer resolutions. Its [baseline scientific account](https://github.com/GoGoKo699/Anytime-Quantum-Estimation/tree/bd1e4d175f8c1c1ffa23c89493ccc0e6d9d86fcd/science) proves a coherent-phase multiscale summability law. That theorem follows a Cantor-tree first-error architecture related to [Duchi and Haque (COLT 2024)](https://proceedings.mlr.press/v247/duchi24a.html), replacing classical iid likelihood control with bounded query-polynomial probability propagation. Finite-query phase-polynomial methods and fixed-confidence phase-estimation bounds have antecedents including [Mande and de Wolf](https://arxiv.org/abs/2305.04908). The Cantor norming step specializes established Remez and norming theory; the sister account gives the needed interpolation proof explicitly.

The phase theorem alone transfers a confidence penalty only to the ordinary rare-event branch $`\sqrt{p_0}/\epsilon`$. Combining that statement with a separate constant-confidence replay floor $`1/(m\epsilon)`$ does not establish a confidence multiplier on the latter. This gap matters for $`m=2`$ and $`p_0\ll1/m^2`$.

The joint addition is a continuous fresh-phase hard family whose averaged unnormalized instruments are polynomial channels in $`p`$, followed by grouping complete source windows according to actual calls and applying channel-valued Markov derivative bounds. Together with the inherited Cantor first-error method, this gives a replay-sensitive law with exponent $`mT_k\epsilon_k`$. The independent ordinary rotation family gives exponent $`T_k\epsilon_k/\sqrt{p_0}`$. Selecting the stronger law yields the full $`A_m(p_0)=\max\{\sqrt{p_0},1/m\}`$-normalized confidence frontier. The upper bound allocates confidence across genuinely capped RUS/Ramsey runs and charges failed attempts explicitly.

Shared-result ownership is explicit: this repository owns the [canonical joint proof](../science/anytime-confidence.md), including the new replay-sensitive argument and charged upper schedule; the sister repository owns its [committed-confidence interpretation and transfer account](https://github.com/GoGoKo699/Anytime-Quantum-Estimation/blob/aa67f4809a19eba29aa3dbcc805f22dc25fdd74b/science/expiring-samplers.md). The shared theorem is one discovery, supported by complementary terminal-replay and all-time-phase antecedents. The long proof is not duplicated between the repositories. Each still states its operational model, main result and boundaries independently.

The theorem constrains summability, or maximum/average normalized deadlines over refinements. It does not force a $`\log K`$ price into a known final deadline alone. It assumes exact common means; the terminal drift theorem and expected-time phase extensions are not silently imported into the joint model.

## Scope of the literature comparison

The terminal comparison uses primary sources checked through 31 October 2026. The joint comparison additionally examines the two pinned scientific accounts and the cited time-uniform and phase-estimation antecedents through 2 November 2026. The controlling comparison is at the level of source access, committed-output promises and charged calls. The absence of a found identical theorem is not a certificate of exhaustive novelty. The contribution claimed here is the stated resource law and its replay-sensitive multiscale strengthening, with the imported ingredients credited above.

The [structured bibliography](bibliography.bib) records the research sources and the selected educational anchor. The [Nielsen–Chuang bridge](../learning/anchor-and-bridge.md) explains the textbook's role in the learning route; primary attribution of the research ingredients is given above.
