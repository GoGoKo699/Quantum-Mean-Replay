# Quantum Mean Replay

**How many times must each fresh quantum sampler remain available to estimate a mean efficiently?**

This repository develops a matching query law for sequential samplers whose output states and unitary completions may change arbitrarily. Each source is available for one window, with a cap on its total forward and inverse calls. A correctable phase-transduction circuit transfers the source's mean information to one persistent probe qubit.

**Sister project: [Anytime Quantum Estimation](https://github.com/GoGoKo699/Anytime-Quantum-Estimation).** The two projects jointly determine what local replay costs when an entire history of committed estimates must remain reliable. This repository owns the [shared sampler theorem and full proof](science/anytime-confidence.md); its sister develops the [all-time confidence interpretation](https://github.com/GoGoKo699/Anytime-Quantum-Estimation/blob/4301198d91310e7e607db255e1cf35c2965d08c6/science/expiring-samplers.md).

## Principal result

Let $`m`$ be the maximum number of calls to one source. For a known probability scale $`p_0`$, an unknown mean $`p\in[p_0,2p_0]`$, and additive accuracy $`\epsilon`$, the optimal worst-case total number of queries at constant confidence is

```math
Q_1=\Theta\!\left(\frac{p_0}{\epsilon^2}\right),
```

and

```math
Q_m=\Theta\!\left(
\max\!\left\{\frac{\sqrt{p_0}}{\epsilon},\frac1{m\epsilon}\right\}
\right),\qquad m\ge2.
```

The theorem assumes $`0\lt p_0\le1/16`$, $`0<\epsilon\le p_0/64`$, exact inverse access within each window, and source means satisfying $`|p_i-p|\le\epsilon/32`$. A controlled physical invocation costs one query. Sources cannot be revisited or coherently selected across identities. The lower bound allows unrestricted persistent quantum memory; the fresh-phase converse already holds with one-qubit sources. See the [complete model and theorem](science/model-and-results.md).

| Resource regime | Consequence |
|---|---|
| One use per source | The worst-case query cost is classical. |
| Two uses per source | A preparation/inverse pair suffices for order $`1/\epsilon`$ bounded-mean estimation. |
| More local replay | Local amplification improves rare-event sensitivity, with cost of order $`1/(m\epsilon)`$ before saturation. |
| Replay of order $`p_0^{-1/2}`$ | The usual rare-event amplitude-estimation order $`\sqrt{p_0}/\epsilon`$ is reached. |

The mechanism uses an established gearbox/repeat-until-success circuit. On success it adds a useful probe phase; on failure a known Pauli correction restores the probe. Each attempt can therefore use a different source. The new resource statement combines this composition with local amplitude amplification, robust multiscale inference and matching adaptive-query lower bounds. [Attribution and closest comparison](references/related-work.md).

## Joint result: confidence across every refinement

For zero drift and $`m\ge2`$, put

```math
A_m(p_0)=\max\{\sqrt{p_0},1/m\}.
```

If one run reaches geometric errors $`\epsilon_k=c p_0 3^{-k}`$ at deterministic actual-call deadlines $`T_k`$, with all committed answers jointly correct with probability at least $`1-\alpha`$, then

```math
\sum_k \exp[-D T_k\epsilon_k/A_m(p_0)]\le B\alpha.
```

A matching geometric construction has $`T_k=O(A_m\epsilon_k^{-1}[\log(k+2)+\log(1/\alpha)])`$. Thus both branches of the replay frontier carry the all-time confidence price. In particular, $`m=2`$ still pays this price when $`p_0`$ is very small. The lower conclusion is multiscale/limsup: it does not penalize every individual time or force a $`\log K`$ factor onto a final tolerance known beforehand.

The new proof uses a fresh finite-phase hard family and polynomial quantum channels grouped by **calls actually executed**. It establishes replay-sensitive probability propagation directly. Every failed repeat-until-success attempt is charged. The [exact statement and proof](science/anytime-confidence.md) give the constants' scope, finite-horizon boundary and source assumptions.

## Read the science

- [Scientific route](science/README.md) — connected overview and proof dependencies.
- [Model and results](science/model-and-results.md) — exact quantifiers, frontier and interpretation.
- [Phase transduction](science/phase-transduction.md) — the exact success/failure instrument.
- [Replay algorithm](science/replay-algorithm.md) — amplification, explicit estimator and hard query budget.
- [Lower bounds](science/lower-bounds.md) — terminal converse and the fresh-phase strengthening.
- [All-time confidence](science/anytime-confidence.md) — canonical shared theorem, charged construction and replay-sensitive propagation proof.
- [Resources and robustness](science/resources-and-robustness.md) — inverse access, arithmetic, memory and coherence costs.
- [Related work](references/related-work.md) and [bibliography](references/bibliography.bib).

## Learn the result

The single educational anchor is Michael A. Nielsen and Isaac L. Chuang's *Quantum Computation and Quantum Information*, 10th Anniversary Edition (2010). The [learning route](learning/README.md) connects its foundations to the changing-source problem.

- [Thirty milestones](learning/milestones.md) organize the prerequisite concepts and the research argument into a common understanding map.
- [Anchor and bridge](learning/anchor-and-bridge.md) identify the relevant textbook sections, translate notation and access assumptions, and explain the steps supplied by this project.
- [Worked walkthrough](learning/walkthrough.md) follows a complete preparation/inverse attempt, its corrected failure and its accumulated phase, then connects that example to the full query law.

The milestone targets are defined by the project. The scientific pages above remain the authoritative home of the exact claims and proofs.

## Reproduce the numerical checks

```bash
python -m pip install -r verification/requirements.txt
python verification/run_validation.py --trials 64
python verification/check_twirl_degree.py --check verification/twirl-degree-results.json
```

The [verification guide](verification/README.md) describes the checks, recorded results and limits. They test arbitrary garbage and unitary completions, preservation of entangled reference states, the controlled forward/inverse twirl, amplification sensitivity and the actual-query ledger of the Ramsey estimator. The finite simulation uses the conservative proved schedule; it is not a hardware runtime benchmark or a substitute for the proofs.

## Consequential scope

The probability scale is known. The sampler's inverse must match its forward operation. The terminal theorem permits source means to drift within its stated tolerance; the indefinitely refining confidence theorem assumes exactly zero drift. A single probe remains coherent across many source windows, so small persistent memory does not mean constant global coherence depth. The result does not assume QRAM or free loading of classical data; local implementation costs are separate from the oracle-query law.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
