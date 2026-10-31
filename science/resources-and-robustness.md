# Resources, robustness, and limits of the replay theorem

## Scope

The resource law concerns a sequential supply of unitary samplers. The known probability scale is $`p_0\in(0,1/16]`$, the common target is $`p\in[p_0,2p_0]`$, and $`0<\epsilon\le p_0/64`$. The integrated upper bound allows each source mean to satisfy

```math
|p_i-p|\le\delta,\qquad \delta\le\epsilon/32.
```

Each current source $`U_i`$ is an honest unitary on a workspace initialized in a known zero state. Its marked probability is

```math
p_i=\langle0|U_i^\dagger\Pi U_i|0\rangle
```

for a known marked projector $`\Pi`$. Its output garbage and unitary completion may differ arbitrarily from those of every other source. The same $`U_i`$ and its exact inverse must remain available throughout that source's window. After leaving a window, the algorithm does not return to it. No coherent selection across source identities is assumed.

The minimax statement charges primitive source invocations. It does not equate an unknown unitary oracle with a free state preparation, a classical random-number generator, or an experimental device that only produces irreversible samples. Hu et al. provide the nonidentical-source problem and the relevant forward, inverse, and controlled-call convention; the present theorem should retain that operational distinction. [Hu et al., TQC 2024](https://arxiv.org/abs/2405.12838)

## Explicit cost ledger

For the achieved upper bound, choose

```math
k=\text{largest positive odd integer at most }
\min\{m/2,\;1/(4\sqrt{p_0})\}.
```

One amplified preparation $`A_{i,k}`$ uses exactly $`k`$ calls to $`U_i`$ or $`U_i^\dagger`$. One complete phase-transfer attempt applies $`A_{i,k}`$, the known marked-projector/probe operation, and $`A_{i,k}^\dagger`$, then measures the workspace's return to zero. It therefore costs exactly $`2k`$ primitive source calls, including a failed attempt. The implementation uses a new source on every attempt, so each used source receives exactly $`2k\le m`$ calls.

This upper construction uses uncontrolled source calls. Coherent control is needed only for known marking/probe operations. Controlled source calls are included in the stronger allowed model of the converse and are charged as ordinary physical invocations there.

| Resource | Accounting and assumption |
|---|---|
| Primitive source invocation | Every physical invocation of $`U_i`$, $`U_i^\dagger`$, or a permitted controlled form counts once. |
| Controlled invocation | A physical controlled-oracle gate counts once even if its coherent control has zero or small amplitude on the use branch. Query cost is not multiplied by a control probability. |
| Local amplification | $`k`$ primitive calls in $`A_{i,k}`$, another $`k`$ in its inverse; both directions are charged. |
| Marking and zero reflections | Each $`A_{i,k}`$ contains $`(k-1)/2`$ marking reflections and the same number of known zero-state reflections. The inverse contributes the same counts. |
| Middle probe operation | One exact $`\exp(i\pi (I-2\Pi)\otimes Z/4)`$ per attempt. A known success flag makes this a constant-size controlled rotation; a general predicate requires its coherent evaluation and uncomputation. |
| Workspace readout | A binary test of the entire zero state is required. Measuring all workspace bits and taking their classical OR is sufficient. Measuring only the output flag is generally insufficient. |
| Failure correction | One known Pauli $`Z`$ on the probe, or its correctly tracked Pauli-frame equivalent, after a nonzero-workspace result. |
| Workspace | The current source's full workspace, amplification ancillas, and one probe qubit. Source workspace is discarded/reset between windows; it is not assumed small. |
| Persistent quantum memory | One probe qubit persists across the sources in a Ramsey batch. It is measured and reset between Ramsey experiments. No quantum history of all sources is retained by the upper algorithm. |
| Classical information | Scale index, successful-transfer count, source-use count, measurement totals, and phase-unwrapping data. Classical bits may persist without keeping the source workspace coherent. |
| Distinct sources | One per attempted transfer in this construction. No optimality claim is made for the number of distinct sources separately from primitive queries. |
| Oracle implementation | Gate cost and physical duration of every actual sampler and inverse must be supplied by an application. A query theorem does not make these costs independent of workspace size. |

For example, if $`C_U`$ bounds the implementation cost of a primitive source call, $`C_0`$ that of a zero reflection, $`C_\Pi`$ that of a marking reflection, $`C_{\mathrm{mid}}`$ that of the middle operation, and $`C_{\mathrm{read}}`$ that of readout/reset, a complete attempt has cost at most

```math
2k C_U+(k-1)(C_0+C_\Pi)
+C_{\mathrm{mid}}+C_{\mathrm{read}}+O(1).
```

If these costs vary with $`i`$, the corresponding costs must be summed over actual attempts. The theorem's query count does not replace that sum by its smallest constituent cost.

At constant confidence, the explicit schedule requires

```math
S=O((k^2\epsilon)^{-1})
```

accepted transfers and caps attempted transfers at $`O(S)`$. Thus the primitive-call count is $`O((k\epsilon)^{-1})`$. A logarithmic factor in inverse failure probability is present when confidence is not fixed. The longest Ramsey batch contains $`\Theta((k^2\epsilon)^{-1})`$ accepted transfers; the proof also caps the total number of attempts. These are substantial coherence requirements. The conclusion concerns how long each transient sampler must remain usable, while the probe carries phase across many such samplers.

## Bounded values do not provide a free input oracle

A finite-precision value register encoding $`x\in[0,1]`$ can be converted coherently into a coin by a controlled rotation

```math
|x\rangle|0\rangle
\longmapsto
|x\rangle\bigl(\sqrt{1-x}|0\rangle+\sqrt{x}|1\rangle\bigr).
```

Applying this to a source distribution gives marked probability $`\mathbb E[x]`$. The effective sampler includes the value-to-coin circuit; its inverse includes the exact reverse circuit. The original source is still queried once per effective sampler call, while reversible arithmetic, angle synthesis, ancillas, and their inverses must be charged as additional gates.

The theorem does not supply QRAM, a loaded amplitude vector, a coherent lookup into an arbitrary classical data set, or an efficient dilation of an arbitrary observable. An application with such input requirements must provide and charge them. The lower bound uses a known unitary $`W_n`$ preparing the exact uniform state over $`n`$ index labels. This unitary depends only on the known integer $`n`$, carries no hidden input information, and does not assume that $`n`$ is a power of two. Its known-gate implementation cost is separate from the primitive-query lower bound; no QRAM is assumed.

If the implemented coin circuit consistently uses rounded values $`\widetilde x`$, with $`|\widetilde x-x|\le\nu`$, the induced mean changes by at most $`\nu`$. This can be included in the mean-drift budget **provided that the inverse is the exact inverse of the actual implemented circuit**. Unmatched forward and inverse synthesis errors are a different error model.

## What the drift guarantee covers

Within the monotone amplification interval $`r\in[p_0/2,3p_0]`$, write

```math
q_k(r)=\sin^2(k\arcsin\sqrt r),\qquad
f_k(r)=2\arctan(1-2q_k(r)).
```

The chosen $`k`$ keeps the amplification angle below $`\pi/4`$, and

```math
\frac{2}{\pi}k^2\le q_k'(r)\le k^2,\qquad
\frac{4}{\pi}k^2\le |f_k'(r)|\le4k^2.
```

Every accepted transfer therefore contributes a phase within $`4k^2\delta`$ of the target phase. A batch of $`L`$ accepted transfers has total phase deviation at most $`4Lk^2\delta`$, independently of which attempts succeeded. This is a pointwise bound; it does not require the success-conditioned source means to average to $`p`$.

The success probability

```math
s_i=\frac{1+(1-2q_k(p_i))^2}{2}\ge\frac12
```

can depend on the source mean. Consequently, accepting successful attempts generally biases the source mixture. The proof retains this selection effect rather than assuming unbiased accepted sources.

The source sequence may be fixed in advance or chosen using earlier classical records, as long as every current source satisfies the same pointwise mean promise and remains a unitary with the required inverse throughout its window. Conditional bounded-variable concentration then applies to the Ramsey outcomes, and a conditional success lower bound controls the attempt cap. These arguments do not include an uncontrolled quantum environment shared with the probe or an oracle that changes during its own amplification/inversion sequence.

The robustness theorem uses the explicit drift ratio $`\delta\le\epsilon/32`$.

The global $`k=1`$ corollary in [replay-algorithm.md](replay-algorithm.md) separately covers $`p\in[0,1]`$, including the endpoints, with the same small drift ratio. It uses no supplied rare-event scale and asserts the uniform $`O(\epsilon^{-1})`$ precision law, rather than the sharper scale-dependent rare-event rate.

## Exact inverse access is not a generic noise guarantee

Bounded mean drift allows large changes in output garbage and unitary completion across windows because each individual attempt cancels its own current source exactly. An approximate inverse need not preserve this cancellation.

The validation includes an explicit qubit example. Take a source of marked probability $`p=1/4`$, leave that source unchanged, and replace its inverse by

```math
\widetilde U^\dagger=e^{i\eta X}U^\dagger.
```

The preparation mean has zero drift. Nevertheless, after a failure, the prescribed Pauli correction does not restore an entangled probe/reference state. At $`\eta=10^{-3}`$, the normalized corrected failure has trace distance approximately $`1.155\times10^{-3}`$ from the input. The success probabilities for the two probe $`Z`$ eigenstates differ by approximately $`1.732\times10^{-3}`$. Thus both exact failure correction and outcome-independence from the probe can fail while the mean promise remains perfectly satisfied. These numbers are reproduced by the matrix circuit in [the validation script](../verification/run_validation.py) and recorded in [the results](../verification/results.json).

A separately specified channel-error budget can still be handled by an ordinary circuit hybrid bound. If the diamond-norm errors of all implemented primitive operations sum to at most $`\zeta`$, the final output distributions differ from the ideal ones by at most the corresponding trace-distance bound, and the success probability degrades by at most that amount. Such a budget must cover every actual call, including failed attempts and repeated uses within amplification. A fixed arbitrary per-call error is not covered uniformly as the required query count grows. More favorable noise dependence would require a stated structure or a separate error-correction argument.

## Boundaries of the lower bound and interpretation

The one-use obstruction is minimax over the full arbitrary-garbage model. The hard family changes the phases of the prepared output components, so it violates the stronger promise that every source shares one known clean first column. This lower bound therefore does not apply to that subclass. The finite-twirl validation checks the actual broader hard family, including its independent input/output and global phases.

Likewise, the adaptive replay converse concerns sequential source windows. It does not establish the same law when old sources may be revisited in arbitrary order, source identity is coherently selected, or a different physical access mechanism supplies extra correlations. The supplied constant-factor scale $`p_0`$ is also part of the theorem; scale-free estimation is not an achieved corollary here.

The central operational conclusion survives these qualifications: in the stated transient-source model, local replay and total estimation precision are distinct resources. The established construction transfers the usable scalar information to a small persistent probe, and the converse quantifies the local replay needed to reach the rare-event amplitude-estimation rate. The construction inherits the gearbox/RUS phase map and ordinary amplitude amplification; the resource theorem is the contribution under investigation. [Wiebe–Kliuchnikov, 2013](https://arxiv.org/abs/1305.5528); [Wiebe–Roetteler, 2014/2016](https://arxiv.org/abs/1406.2040)
