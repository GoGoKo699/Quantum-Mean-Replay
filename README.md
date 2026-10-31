# Quantum Mean Replay

**How many times must each fresh quantum sampler remain available to estimate a mean efficiently?**

This repository develops a matching query law for sequential samplers whose output states and unitary completions may change arbitrarily. Each source is available for one window, with a cap on its total forward and inverse calls. A correctable phase-transduction circuit transfers the source's mean information to one persistent probe qubit.

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

The theorem assumes $`0<p_0\le1/16`$, $`0<\epsilon\le p_0/64`$, exact inverse access within each window, and source means satisfying $`|p_i-p|\le\epsilon/32`$. A controlled physical invocation costs one query. Sources cannot be revisited or coherently selected across identities. The lower bound allows unrestricted persistent quantum memory and takes a worst case over local workspace dimensions. See the [complete model and theorem](science/model-and-results.md).

| Resource regime | Consequence |
|---|---|
| One use per source | The worst-case query cost is classical. |
| Two uses per source | A preparation/inverse pair suffices for order $`1/\epsilon`$ bounded-mean estimation. |
| More local replay | Local amplification improves rare-event sensitivity, with cost of order $`1/(m\epsilon)`$ before saturation. |
| Replay of order $`p_0^{-1/2}`$ | The usual rare-event amplitude-estimation order $`\sqrt{p_0}/\epsilon`$ is reached. |

The mechanism uses an established gearbox/repeat-until-success circuit. On success it adds a useful probe phase; on failure a known Pauli correction restores the probe. Each attempt can therefore use a different source. The new resource statement combines this composition with local amplitude amplification, robust multiscale inference and matching adaptive-query lower bounds. [Attribution and closest comparison](references/related-work.md).

## Read the science

- [Scientific route](science/README.md) — connected overview and proof dependencies.
- [Model and results](science/model-and-results.md) — exact quantifiers, frontier and interpretation.
- [Phase transduction](science/phase-transduction.md) — the exact success/failure instrument.
- [Replay algorithm](science/replay-algorithm.md) — amplification, explicit estimator and hard query budget.
- [Lower bounds](science/lower-bounds.md) — finite-twirl simulation and the adaptive fresh-source adversary.
- [Resources and robustness](science/resources-and-robustness.md) — inverse access, arithmetic, memory and coherence costs.
- [Related work](references/related-work.md) and [bibliography](references/bibliography.bib).

## Reproduce the numerical checks

```bash
python -m pip install -r verification/requirements.txt
python verification/run_validation.py --trials 64
```

The [verification guide](verification/README.md) describes the checks, recorded results and limits. They test arbitrary garbage and unitary completions, preservation of entangled reference states, the controlled forward/inverse twirl, amplification sensitivity and the actual-query ledger of the Ramsey estimator. The finite simulation uses the conservative proved schedule; it is not a hardware runtime benchmark or a substitute for the proofs.

## Consequential scope

The probability scale is known. The sampler's inverse must match its forward operation. Source means may drift only within the stated uniform tolerance. A single probe remains coherent across many source windows, so small persistent memory does not mean constant global coherence depth. The result does not assume QRAM or free loading of classical data; local implementation costs are separate from the oracle-query law.

## Purpose and contact

This repository serves as a record of the work and a guide for the author’s self-directed learning. For discussion or potential collaboration, please contact Ruge Lin at [gogoko699@gmail.com](mailto:gogoko699@gmail.com).
