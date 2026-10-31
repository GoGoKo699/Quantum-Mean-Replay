# Reproducible scientific validation

## What was run

The validation uses Python 3.12.14 and NumPy 2.3.5, with no other third-party dependency. The actual NumPy version is pinned in [requirements.txt](requirements.txt). The root seed is `20261031`; separate deterministic child generators drive the matrix, amplification, rare-event Ramsey, and global-corollary checks. [results.json](results.json) records the interpreter, dependency version, platform, source hashes, parameters, residuals, and query accounting.

From the repository root:

```bash
python verification/run_validation.py --trials 64
```

The script writes `verification/results.json` and prints a compact summary. A different `--output` path may be supplied. The numerical tolerances account for ordinary floating-point roundoff; exact last-bit agreement across different BLAS implementations is not assumed.

These checks address particular failure modes in the claimed construction. They do not prove the theorem, establish novelty, certify the adaptive lower bound, or predict performance on noisy hardware.

## Matrix circuit checks

The script constructs 96 sources across workspace dimensions 2, 4, 8, and 16, eight marked probabilities including both endpoints and rare events, and three independently random garbage/completion choices per case. It builds the full circuit matrix, extracts every measured-workspace Kraus operator, and checks the output on both an entangled pure probe/reference input and an entangled full-rank input.

| Quantity | Largest observed residual |
|---|---:|
| Source unitarity, operator norm | $`1.60\times10^{-15}`$ |
| Success Kraus operator, operator norm | $`7.86\times10^{-16}`$ |
| Failure Kraus operator, operator norm | $`6.08\times10^{-16}`$ |
| Branch probabilities | $`1.23\times10^{-15}`$ |
| Normalized success state, trace distance | $`4.52\times10^{-16}`$ |
| Normalized corrected failure state, trace distance | $`3.63\times10^{-13}`$ |
| Full corrected instrument, trace distance | $`7.67\times10^{-16}`$ |

The somewhat larger normalized-failure residual occurs when conditioning on a very small branch probability. The full unnormalized instrument remains at floating-point precision. The reference system is untouched; checking it addresses the possibility that an apparently correct probe marginal conceals lost entanglement.

The one-use hard-family check compares complete superoperators on a six-dimensional input: a route label selecting no query, forward, or inverse, tensored with a query qubit. Averaging the 16 left/right/global phase choices agrees with a parameter-independent channel driven by one Bernoulli-$`p`$ coin to operator-norm error at most $`2.23\times10^{-16}`$, across nine probabilities. Superoperator equality covers arbitrary ancillary references. The report also records that omitting the global-phase twirl leaves nonzero cross-route terms; the implementation does not silently omit that component of the hard family.

## Local amplification and excluded inverse errors

There are 144 independent matrix amplification checks spanning the supplied probability interval, replay caps from 2 to 1024, and the odd-integer choices of $`k`$. Their largest error against $`\sin^2(k\arcsin\sqrt p)`$ is $`1.05\times10^{-15}`$. For every selected schedule, a 257-point grid includes the boundaries of the derivative interval. The observed derivative ratios lie inside the proved bounds:

| Ratio | Observed range | Proved containing interval |
|---|---:|---:|
| $`q_k'(p)/k^2`$ | $`[0.8832,1]`$ | $`[2/\pi,1]`$ |
| Absolute phase derivative divided by $`k^2`$ | $`[2.0000,2.8765]`$ | $`[4/\pi,4]`$ |

A finite-difference derivative check has maximum relative discrepancy $`3.59\times10^{-8}`$. The grids are evidence about the implementation and selected edges, not a substitute for the analytic inequalities.

The perturbed-inverse example is expected to fail the exact correction identities. It reproduces a nonzero corrected-failure error and probe-dependent success probability while the preparation mean is unchanged. It therefore confirms an explicit limitation of the theorem rather than an unexpected failure of it. Details and the separate channel-error budget are in [resources-and-robustness.md](../science/resources-and-robustness.md).

## Exact conservative Ramsey simulation

The simulation implements the [proved schedule](../science/replay-algorithm.md), not a reduced-shot heuristic:

- $`k`$ is the largest positive odd integer at most $`\min\{m/2,1/(4\sqrt{p_0})\}`$.
- With $`a=4/\pi`$, $`\rho=\pi/8`$, and failure target $`\beta=0.05`$, set $`K=\lceil\log_2(\rho/(a k^2\epsilon))\rceil`$.
- At level $`j`$, each of the two quadratures uses $`r_j=\lceil128\log(4/\beta_j)\rceil`$ batches of $`L_j=2^j`$ accepted gates, where $`\beta_j=\beta 2^{j-K-2}`$.
- The attempt cap is $`\lceil4S+16\log(2/\beta)\rceil`$, where $`S=2\sum_j L_jr_j`$. Every attempt costs $`2k`$ physical primitive calls.
- The estimator uses nearest-lift phase unwrapping, clipping to $`f_k([p_0,2p_0])`$, and the exact monotone inverse map.

Two probability scales, four replay caps, and four source modes give 32 rare-event cases. Each case has 64 independent seeded trials. The modes are equal means, a fresh balanced two-point mean mixture, different mixtures by quadrature and scale, and mixtures chosen from earlier classical phase estimates. Drift cases use $`\delta=\epsilon/32`$. A fresh source type is drawn for every attempted source, including failed attempts.

The simulator uses the true $`p`$ only to generate sources, measurement outcomes, and the permitted history-dependent source adversary. The estimation schedule and final inversion use the supplied scale and observed quadratures; they are not supplied the true target.

### Why the large-call simulations can be compressed exactly

For source means $`p-\delta`$ and $`p+\delta`$, let their input mixture weights be $`1-w,w`$, their success probabilities be $`s_-,s_+`$, and their accepted phases be $`f_-,f_+`$. Then

```math
\bar s=(1-w)s_-+ws_+,\qquad
w_{\mathrm{accepted}}=\frac{ws_+}{\bar s}.
```

For a batch ending after $`L`$ successes, the number of failed attempts is negative-binomial with parameters $`(L,\bar s)`$, and the number of accepted plus-type sources is binomial with parameters $`(L,w_{\mathrm{accepted}})`$. These two quantities are independent for the independent marked-attempt process. The accumulated phase is $`Lf_-+N_+(f_+-f_-)`$. Sampling these exact distributions avoids allocating one array entry per physical oracle call while retaining the success-selection bias and the actual-call distribution.

This compression applies to the specific independently redrawn source mixtures being simulated. It is not an assumption used to prove the upper bound for arbitrary allowed source sequences. Within a trial, a mixture can be chosen from earlier classical results; the same conditional sampling identity then applies to that next group of batches.

### Results and costs

All 2048 rare-event trials returned an estimate within $`\epsilon`$, and none exhausted its attempt cap. The largest observed absolute error was $`0.109\epsilon`$. For 64 successes in 64 independent trials, the per-case one-sided exact 95% binomial lower bound is $`0.05^{1/64}\approx0.9543`$. These are per-case finite-sample statements, not simultaneous confidence bounds or a universal guarantee.

The following rows show the quadrature-dependent drift case at $`p_0=1/1024`$, $`p=1.4p_0`$, and $`\epsilon=p_0/64`$.

| Replay cap $`m`$ | Chosen $`k`$ | Uses per source | Median actual primitive calls | Hard primitive-call cap | Maximum error / $`\epsilon`$ |
|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 2 | 217,566,195 | 867,887,992 | 0.0733 |
| 8 | 3 | 6 | 83,362,542 | 325,376,712 | 0.0746 |
| 32 | 7 | 14 | 26,988,815 | 94,737,944 | 0.0830 |
| 128 | 7 | 14 | 26,989,788 | 94,737,944 | 0.1003 |

The repeated $`k=7`$ reflects the conservative first-lobe cap, rather than spending all available replay. These large call counts are an honest consequence of the explicit proof constants. The validation is not a claim that this schedule is practically optimized, that the calls were executed on quantum hardware, or that it beats a classical estimator at these finite numerical parameters.

The global $`k=1`$ corollary receives a separate targeted check for negative phases, $`p=0`$, $`p=1`$, and the $`K=0`$ branch at large tolerance. All 448 trials across seven cases returned an estimate within $`\epsilon`$, with no attempt-cap failures and maximum error below $`0.240\epsilon`$. Its source means are clipped to $`[0,1]`$, as required at the endpoints. The cases and coverage are recorded separately in the JSON report so these checks are not confused with the known-scale rare-event theorem.

## Verification limits

The checks cover matrix algebra, preservation of probe/reference correlations, the full one-use twirled channel, amplification boundaries, an explicit inverse-error counterexample, and the charged multiscale implementation under selected allowed drift sequences. They do not numerically test a large-query adversary lower bound or infer asymptotic optimality from a fit. The lower bound is an analytic claim requiring its separate proof review.
