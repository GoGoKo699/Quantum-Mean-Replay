# Learning route

The scientific question is how long a fresh quantum sampler must remain accessible to estimate a mean efficiently, and what changes when every committed refinement must remain trustworthy. A sampler can disappear after its local window while a separate probe retains phase information. Understanding that separation connects the circuit, the inference procedure and the lower bound.

The single educational anchor is **Michael A. Nielsen and Isaac L. Chuang, *Quantum Computation and Quantum Information*, 10th Anniversary Edition (Cambridge University Press, 2010)**, [book DOI](https://doi.org/10.1017/CBO9780511976667). The [anchor and bridge](anchor-and-bridge.md) give targeted sections and the missing steps to this project. Primary research references in the scientific account provide attribution for imported methods.

## Choose a reading route

| Purpose | Route |
|---|---|
| See the mechanism in a small complete example | Read the [worked walkthrough](walkthrough.md), then the [exact phase instrument](../science/phase-transduction.md). |
| Build a connected understanding of the full result | Follow [M01–M30](milestones.md), using the [anchor and bridge](anchor-and-bridge.md) and each milestone's source pointers. |
| Understand the joint confidence–replay result | Read [all-time confidence](../science/anytime-confidence.md), which owns the shared proof, then the final walkthrough section. |
| Inspect a particular theorem or proof | Start with the [model and results](../science/model-and-results.md), then follow the [scientific route](../science/README.md). |
| Reproduce the finite calculations | Use the [verification guide](../verification/README.md), its actual commands and recorded numerical outputs. |

## What the map covers

The [30-milestone map](milestones.md) has two phases: background/preliminaries and narrative/innovation. Each phase develops local objects and operations into a complete account of the problem. The targets and dependencies belong to the project and are common to every reader.

The background prepares states, measurements, inverse circuits, phase inference and distinguishability. The narrative joins the correctable instrument, local amplification, robust inference and converse arguments into the matching resource law. Its final steps introduce the continuous finite-phase twirl, blocks grouped by actual calls, and the first-error argument that makes the replay-limited branch pay the all-time confidence price. The synthesis retains the known probability scale, exact inverse requirement, hard physical-query budget and long probe coherence. The all-time extension assumes zero drift; a fixed positive drift tolerance cannot support indefinitely shrinking radii.

The walkthrough supplies an explanatory example; the source bridge identifies which steps go beyond the textbook. Full technical calculations and universal claims remain in their linked scientific proofs. The [related-work account](../references/related-work.md) distinguishes inherited methods from the resource statement established here.

[Repository overview](../README.md) · [Milestone map](milestones.md) · [Anchor and bridge](anchor-and-bridge.md) · [Worked walkthrough](walkthrough.md)
