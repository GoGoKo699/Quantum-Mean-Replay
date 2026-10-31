# Related work and attribution

The contribution is a local-replay law for fresh sequential samplers with arbitrary changing output garbage. Its primitive components have established precedents. The comparison below concerns the stated access, error and query conventions; it is not an exhaustive priority claim for every related model.

## Non-identical mean estimation

[Hu, Li, Wang, Xue, Zhang and Zhong (TQC 2024)](https://doi.org/10.4230/LIPIcs.TQC.2024.9) formulate non-identical preparation oracles and analyze bounded and sub-Gaussian means. The comparison uses the published paper and [arXiv:2405.12838v1](https://arxiv.org/abs/2405.12838v1), especially the input model, bounded-mean upper bound and general-replay lower bound. Their bounded-mean algorithm requires logarithmic local reuse and has a logarithmic query overhead; their general-replay bound constrains fixed blocks. Their separate one-use argument uses a workspace restriction under its stronger construction.

Here two calls per source suffice for bounded means, with no logarithmic precision overhead. The known-scale rare-event law also identifies the crossover to the usual amplitude-estimation rate. The lower bound in [lower-bounds.md](../science/lower-bounds.md) treats adaptive stopping in actual paid queries, using real overlap and an explicit auxiliary-cost comparison. Its one-use finite-twirl construction uses arbitrary changing output phases; it does not assert that a stronger common-clean-column promise remains hard without a workspace restriction.

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

## Scope of the literature comparison

Primary sources were checked through 31 October 2026. The controlling comparison is against the explicitly stated non-identical mean-estimation model and the inherited circuit primitives above. The absence of a found identical theorem is not a certificate of exhaustive novelty. The contribution claimed here is the proved conjunction of model, access and asymptotic resource law, with every imported ingredient credited.

The [structured bibliography](bibliography.bib) records the sources used directly by the proofs. Educational background is separate from the primary attribution of the result.
