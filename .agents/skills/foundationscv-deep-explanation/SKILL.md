---
name: foundationscv-deep-explanation
description: Teach or re-explain unfamiliar Foundations of Computer Vision chapter concepts in the postgraduate Vault at the user's confirmed high-detail level. Use for chapter summaries, formula explanations, screenshots, or follow-ups such as “没看懂”、“详细解释”、“这是像素还是频率”. Focus on conceptual teaching; use the chapter-study workflow for file creation or completion synchronization.
---

# FoundationsCV Deep Explanation

Teach until the user can track what each quantity is, where it lives, how it is computed, and what practical question it answers. A polished chapter outline is not sufficient evidence of understanding.

## Start from the lowest concrete carrier

Before introducing an unfamiliar abstraction, choose the smallest carrier that preserves it:

- spatial signal: four to eight pixel values;
- image filter: a small patch and kernel;
- frequency: sampled cosine values before Fourier coefficients;
- direction: a two-component vector and projection;
- video: a short frame stack or an $x$-$t$ slice.

State explicitly whether each displayed array or symbol is a pixel value, normalized signal, filter weight, convolution response, frequency coordinate, transform coefficient, amplitude, phase, or velocity. Never silently cross from the spatial domain to the frequency domain.

## Explanation ladder

Use the following layers in order when the concept is new. Compress only layers the user already demonstrates.

1. **Purpose:** explain in plain Chinese what problem this concept solves and why the previous tool is insufficient.
2. **Concrete construction:** build one hand-calculable example from raw numbers, a small matrix, an ASCII diagram, or consecutive frames.
3. **Object and domain map:** name every quantity, its role, its units when meaningful, and whether it belongs to the input, filter, response, spatial domain, frequency domain, or time domain.
4. **Formula derivation:** write the starting formula, substitute definitions, expand sums or algebra without hidden steps, and interpret the result after each stage.
5. **Contrast cases:** include at least one matched case and one non-matched, shifted, reversed, constant, or otherwise diagnostic case. Explain response sign, zero, and magnitude when relevant.
6. **Integration:** reconnect the result to the chapter chain and separate `必须掌握` from `暂时了解即可`.

Do not lead with a long formal definition. Intuition comes first, but do not stop at analogy: show the exact mapping from the analogy to the symbols and computation.

## Formula protocol

For each unfamiliar formula:

1. Say what the whole formula computes in one sentence.
2. Define every symbol before manipulating it.
3. State shapes or units when they resolve ambiguity, such as pixels, cycles per pixel, radians per frame, or pixels per frame.
4. Expand the operation using finite indices or a small numerical instance.
5. Show why each equality is legal, such as convolution linearity, the chain rule, or a trigonometric identity.
6. Interpret positive, negative, zero, magnitude, direction, and phase where applicable.
7. State what the formula does **not** prove or measure.

Use only `$...$` and `$$...$$` math delimiters. Use `\\` for matrix row breaks.

## Repair protocol after “没懂”

Do not restate the same explanation more verbosely.

1. Identify the first broken link: object identity, domain change, operation, equality, geometry, or purpose.
2. State the correction immediately, for example: `Gaussian 本身只平滑；Gaussian 导数的正负两瓣才比较两侧亮度。`
3. Restart one abstraction level lower.
4. Change representation: formula to numbers, numbers to ASCII geometry, spatial image to frequency-domain table, or video to an $x$-$t$ timeline.
5. Use a counterexample to expose the misconception.
6. Return to the original formula only after the concrete mechanism is visible.

Answer the user's local confusion first; do not repeat the entire chapter unless the missing link affects the whole chain.

## Chapter-specific invariants

- Distinguish raw pixels, normalized samples, spatial kernels, filter responses, and Fourier coefficients.
- For Gabor filters, separate Gaussian localization from sinusoidal frequency/orientation selection.
- For quadrature pairs, separate signed phase-specific responses from local amplitude.
- For frequency planes, derive DC and radius from the Fourier basis rather than using the center-map metaphor alone.
- For Gaussian derivatives, state that Gaussian smooths; its derivative detects change by weighted side comparison.
- For steerability, connect basis responses to vector projection and distinguish change direction from edge orientation.
- For spatiotemporal filters, begin with stacked frames, derive the motion constraint, and distinguish one-channel normal-velocity evidence from full 2D velocity.

## Hard pre-send gate

Treat the following as acceptance criteria, not style suggestions. Do not send a chapter summary or unfamiliar formula explanation until every relevant item passes:

- [ ] The explanation begins from the smallest concrete carrier that preserves the mechanism.
- [ ] Every key quantity is labeled by object type, representation domain, and any useful shape or unit.
- [ ] At least one example is calculated through the complete mechanism; an isolated scalar identity does not qualify.
- [ ] At least one numeric contrast or counterexample exposes a likely misconception.
- [ ] Each unfamiliar formula is mapped back to the concrete example, with key equalities expanded and interpreted.
- [ ] Positive, negative, zero, magnitude, direction, or phase is interpreted wherever the concept produces those outcomes.
- [ ] The causal chain, `必须掌握`, `暂时了解即可`, and transfer self-check are present.
- [ ] `Content read once` is not treated as demonstrated understanding and does not authorize compression.
- [ ] If all required layers would make the response too long, split the teaching into explicit modules rather than omitting layers.

When the user identifies a still-unknown subset, answer that local subset first and rebuild it one abstraction level lower; do not repeat the entire polished outline.

## Mastery and stopping

Treat `content covered`, `main chain understood`, `can calculate`, and `can independently explain` as different levels. For a first reading, stop when the user can explain the causal chain and interpret the core formulas; do not require advanced proofs or implementation details.

End a chapter explanation with:

- a short causal-chain recap;
- a `必须掌握` list;
- a `暂时了解即可` list;
- a small self-check using transfer questions rather than wording recall.

Do not change `study_status`, Canvas, index, or task archive merely because the material was covered. Require the user's explicit confirmation of chapter completion.

## Avoid

- presenting transformed quantities without saying that a transform occurred;
- saying only that a formula follows from `线性` or `定理` without showing the relevant step;
- using a new technical term to define another unfamiliar term;
- interpreting zero response as absence of structure before checking phase or orientation mismatch;
- treating one successful numerical substitution as general understanding;
- declaring mastery because the explanation was long.
