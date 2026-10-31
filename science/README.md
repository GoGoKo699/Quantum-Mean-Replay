# Scientific account

The central question is how many times each fresh quantum sampler must remain available to retain a quantum advantage in mean estimation. The answer is a matching query frontier that distinguishes one use, a local preparation/inverse pair, and longer local amplification.

Read the pages in this order for the complete argument:

1. [Model and results](model-and-results.md): access rules, the rare-event minimax theorem, bounded-mean consequence and interpretation.
2. [Phase transduction](phase-transduction.md): exact instrument, failure correction, reference entanglement and inherited gearbox structure.
3. [Replay algorithm](replay-algorithm.md): local amplification, explicit robust Ramsey estimator, confidence allocation and physical-query budget.
4. [Lower bounds](lower-bounds.md): one-use classical simulation, ordinary rotation bound and adaptive fresh-source adversary.
5. [Resources and robustness](resources-and-robustness.md): oracle, memory, arithmetic and coherence costs, plus the precise error model.

For a shorter route, start with the main theorem and regime table in [Model and results](model-and-results.md), then read the transducer's Kraus calculation. For proof review, inspect the Ramsey unwrapping and the lower bound's window lemma; they carry the changing-source and actual-query accounting.

[Related work](../references/related-work.md) credits the imported ingredients and compares the exact model with earlier results. [Verification](../verification/README.md) gives reproducible numerical checks and states their limits. Each proof has one authoritative home; numerical verification supplements those proofs.
