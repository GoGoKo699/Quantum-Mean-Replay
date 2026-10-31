# An exact probe rotation from a reversible sampler

The construction in this file extracts a scalar success probability from an otherwise arbitrary sampler. It uses the sampler and its inverse, measures the sampler workspace, and either applies an exact rotation to a retained probe or returns that probe unchanged after a known correction. The workspace may then be discarded. In particular, the next attempt may use a different sampler with different output garbage.

The rotation mechanism is the **gearbox / repeat-until-success construction** of Wiebe and Kliuchnikov, subsequently developed by Wiebe and Roetteler. The contribution studied here concerns the resulting resource bounds for a sequence of expiring sampler oracles. We do not claim a new gearbox primitive. The connection to the original formulation is made explicit below. [1,2]

## 1. Access and notation

Let $A$ be a unitary on a workspace $W$, initialized in a specified computational basis state $|0\rangle_W$. Let $\Pi$ be a known success projector and define

$$
q=\langle0|A^\dagger\Pi A|0\rangle,
\qquad
S=I-2\Pi,
\qquad
R=A^\dagger S A.
\tag{1}
$$

Thus $S$ and $R$ are Hermitian involutions, and

$$
z=\langle0|R|0\rangle=1-2q\in[-1,1].
\tag{2}
$$

The retained probe $B$ is a qubit, with Pauli operator $Z_B$. An untouched reference system $E$ may be entangled with the probe. No assumption is made about that entanglement or the dimension of $E$.

The available operations are $A$, its exact inverse, and the known coupling

$$
\exp\!\left(\frac{i\pi}{4}S\otimes Z_B\right).
\tag{3}
$$

For a Bernoulli output flag, $S$ is the Pauli $Z$ of that flag, so (3) is a Clifford gate. For a more general supplied projector, implementing (3) is a separate resource that must be charged. A description of $A$ or of its unknown output garbage is not required.

## 2. The instrument identity

**Proposition 1 — exact rotation and correctable failure.** Apply

$$
V=(A^\dagger\otimes I_B)
\exp\!\left(\frac{i\pi}{4}S\otimes Z_B\right)
(A\otimes I_B)
\tag{4}
$$

to $|0\rangle_W$ and the probe. Measure $W$ in the computational basis. The all-zero outcome has probability

$$
s(q)=\frac{1+z^2}{2}=(1-q)^2+q^2\ge\frac12,
\tag{5}
$$

independent of the probe and reference state. Conditioned on this outcome, the probe undergoes

$$
T(q)=\exp\!\bigl(i\arctan(1-2q)Z_B\bigr).
\tag{6}
$$

Every other measurement outcome applies $Z_B$, up to a scalar depending only on the sampler and the recorded outcome. Applying the known correction $Z_B$ restores the incoming probe and its reference entanglement exactly.

**Proof.** Since $(S\otimes Z_B)^2=I$,

$$
V=\frac{I+iR\otimes Z_B}{\sqrt2}.
\tag{7}
$$

Decompose

$$
R|0\rangle=z|0\rangle+|w\rangle,
\qquad
\langle0|w\rangle=0,
\qquad
\|w\|^2=1-z^2.
\tag{8}
$$

The last identity follows from $R^\dagger R=I$. For every pure probe-reference state $|\Psi\rangle_{BE}$,

$$
\begin{aligned}
(V\otimes I_E)|0\rangle_W|\Psi\rangle_{BE}
={}&|0\rangle_W
\left(\frac{I+i zZ_B}{\sqrt2}\otimes I_E\right)
|\Psi\rangle_{BE}\\
&+\frac{i}{\sqrt2}|w\rangle_W
(Z_B\otimes I_E)|\Psi\rangle_{BE}.
\end{aligned}
\tag{9}
$$

Consequently, the probe Kraus operators for the workspace measurement are

$$
K_0=\frac{I+i zZ_B}{\sqrt2},
\qquad
K_j=\frac{i\langle j|w\rangle}{\sqrt2}Z_B
\quad(j\ne0).
\tag{10}
$$

They obey

$$
K_0^\dagger K_0=s(q)I_B,
\qquad
K_j^\dagger K_j=\frac{|\langle j|w\rangle|^2}{2}I_B.
\tag{11}
$$

The complete outcome distribution is therefore independent of the input on $BE$. For the all-zero outcome,

$$
\frac{K_0}{\sqrt{s(q)}}
=\frac{I+i zZ_B}{\sqrt{1+z^2}}
=\exp\!\bigl(i\arctan(z)Z_B\bigr).
\tag{12}
$$

For every nonzero outcome, normalizing removes the scalar in (10); the remaining operation is $Z_B$, up to an irrelevant global phase. Its correction acts only on $B$ and restores $|\Psi\rangle_{BE}$. The mixed-state statement follows by purification or linearity. $\square$

Equivalently, for every density operator $\rho_{BE}$, the two coarse-grained branches are

$$
\begin{aligned}
\mathcal I_{\rm success}(\rho_{BE})
&=s(q)(T(q)\otimes I_E)\rho_{BE}(T(q)^\dagger\otimes I_E),\\
\mathcal I_{\rm failure}(\rho_{BE})
&=(1-s(q))(Z_B\otimes I_E)\rho_{BE}(Z_B\otimes I_E).
\end{aligned}
\tag{13}
$$

After the failure correction, the second branch is simply $(1-s(q))\rho_{BE}$. Measuring every workspace qubit and checking whether the classical string is zero is a harmless refinement of this two-outcome instrument. No coherent approximate zero-test is needed.

The endpoint cases are included. At $q=0$ or $q=1$, success is certain and the rotation angle is respectively $\pi/4$ or $-\pi/4$. At $q=1/2$, success has probability $1/2$ and applies the identity; a failure applies the correctable Pauli $Z_B$.

## 3. Why a fresh source can replace a failed source

Suppose the current sampler is $A_i$, with success probability $q_i$. Once its workspace is measured, either its desired rotation has been added to the probe or the incoming probe has been restored. The previous sampler workspace need not remain coherent or be available again.

If $q_i=q$ for every source, every accepted rotation is exactly $T(q)$, even when the samplers have unrelated garbage states and unrelated unitary completions. After $L$ successes, the retained probe has undergone $T(q)^L$.

If the probabilities differ, a probe initialized in $|+\rangle$ instead accumulates the relative phase

$$
\Phi=\sum_{a=1}^{L}\varphi(q_{i_a}),
\qquad
\varphi(q)=2\arctan(1-2q),
\tag{14}
$$

where $i_1,\ldots,i_L$ are the accepted sources. The measured expectations are

$$
\langle X_B\rangle=\cos\Phi,
\qquad
\langle -Y_B\rangle=\sin\Phi.
\tag{15}
$$

The minus sign in the second observable follows from the convention $T(q)=e^{+i\varphi(q)Z_B/2}$. The companion [estimation algorithm](replay-algorithm.md) uses these direct Ramsey measurements.

A source may be selected using earlier **classical** outcomes. Proposition 1 then applies conditional on that history. It requires that the current operation really be a unitary on the initialized sampler workspace, with its matching inverse available during the same window. A device sharing an uncontrolled quantum environment with the retained probe is a different access model.

We do not use a coherently controlled accepted RUS gate. Coherently choosing between running this instrument and bypassing it can reveal that choice through the success record. The proved identity concerns an unconditionally executed attempt whose target probe may already be entangled with a reference. That is exactly the interface needed for the Ramsey algorithm.

## 4. Primitive calls and local amplification

If $A_i$ is a circuit using $k$ primitive calls to the current $U_i$ and $U_i^\dagger$, its inverse uses another $k$ calls. One complete attempt (4) therefore costs **$2k$ primitive calls**, whether it succeeds or fails. Both directions count against the same per-source budget.

For the unamplified sampler, $A_i=U_i$: one forward call and one matching inverse call suffice. For the rare-event algorithm, $A_i$ is an odd-length Grover preparation using the same source throughout. Its construction and its full $2k$-call accounting appear in [replay-algorithm.md](replay-algorithm.md).

The required persistent quantum memory is one probe qubit in addition to the workspace of the current sampler and any known reversible arithmetic. The sampler workspace is measured and reset, or replaced by fresh initialized workspace, after every attempt. Long probe coherence is still necessary: the finest Ramsey experiment retains the probe across many accepted rotations and the intervening failures. This construction reduces the required persistence of an individual sampler; it does not reduce the whole computation to short coherent experiments.

## 5. Relation to the original gearbox

The original gearbox uses a controlled $-iX_B$ on the marked subspace between preparation and unpreparation. Its zero-workspace Kraus operator is

$$
(1-q)I_B-iqX_B.
\tag{16}
$$

After normalization, this is an $X$ rotation of angle

$$
\alpha(q)=\arctan\frac{q}{1-q},
\tag{17}
$$

with the same success probability $(1-q)^2+q^2$ and known correctable failure operations. For a single-qubit input rotation with $q=\sin^2\theta$, the angle is $\arctan(\tan^2\theta)$, the usual gearbox formula. [1,2]

The identity

$$
\arctan(1-2q)=\frac\pi4-\alpha(q)
\tag{18}
$$

relates (6) to that formulation by a fixed known rotation and a change of probe basis. The endpoint $q=1$ is understood by continuity. Extending the proof from a prescribed product of input rotations to an arbitrary preparation $A$ and known projector $\Pi$ gives (9); the subsequent fresh-source estimation theorem is the resource question studied here.

## 6. Bounded values and compiled arithmetic

A reversible sampler with a value register can encode an expectation in a Bernoulli flag. For a known function $f(x)\in[0,1]$, append the known rotation

$$
C_f|x\rangle|0\rangle
=|x\rangle\left(\sqrt{1-f(x)}|0\rangle+\sqrt{f(x)}|1\rangle\right).
\tag{19}
$$

Then $A=C_f(U\otimes I)$ has marked probability $q=\mathbb E[f(X)]$. Its preparation contains one primitive call to $U$; its inverse contains one call to $U^\dagger$. The arithmetic and rotation synthesis implementing $C_f$ must also be charged. This is the usual coherent bounded-value conversion used in quantum mean estimation. [3,4]

Finite precision in that known conversion need not become an unstructured error on every retained probe gate. Use a compiled unitary $\widetilde C_f$ and its **exact compiled inverse** in the two halves of (4). The resulting $\widetilde A^\dagger S\widetilde A$ is still an exact Hermitian involution, so Proposition 1 remains exact for the probability actually encoded. If the compiled flag probability $\widetilde f(x)$ obeys

$$
\sup_x|\widetilde f(x)-f(x)|\le\tau,
\tag{20}
$$

the encoded mean changes by at most $\tau$. It can therefore be included in the allowed mean drift. This argument does not cover an inaccurate physical inverse of the unknown sampler or general gate noise. The full resource distinctions are discussed in [resources-and-robustness.md](resources-and-robustness.md).

## References

1. N. Wiebe and V. Kliuchnikov, *Floating Point Representations in Quantum Circuit Synthesis*, New Journal of Physics **15**, 093041 (2013), Theorem 1 and its proof. [arXiv:1305.5528v3](https://arxiv.org/abs/1305.5528v3).
2. N. Wiebe and M. Roetteler, *Quantum arithmetic and numerical analysis using Repeat-Until-Success circuits*, Quantum Information and Computation **16**, 134–178 (2016), Section II.B, Theorem 3. [arXiv:1406.2040v2](https://arxiv.org/abs/1406.2040v2).
3. G. Brassard, P. Høyer, M. Mosca and A. Tapp, *Quantum Amplitude Amplification and Estimation* (2002). [arXiv:quant-ph/0005055](https://arxiv.org/abs/quant-ph/0005055).
4. J. Hu, T. Li, X. Wang, Y. Xue, C. Zhang and H. Zhong, *Quantum Non-Identical Mean Estimation: Efficient Algorithms and Fundamental Limits*, TQC 2024, LIPIcs **310**, article 9, Definitions 6–7, Task 8 and Theorem 12. [Published primary source](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.TQC.2024.9); [full version, arXiv:2405.12838v1](https://arxiv.org/abs/2405.12838v1).
