---
id: lesson-fd
kind: lesson
title: The complex frequency domain
updated: 2023-07-08
summary: >
  Learn to solve *complex-frequency domain* problems using **fd**. Move between
  time- and s-domain using the **t2f** and **f2t** shortcuts. Learn to solve
  transfer function problems.
---

TODO: convert this lesson from docs-page7.

## s-domain analysis {#s-domain}

TODO. The **fd** {{v7,8|program}}{{v9|function}} solves a circuit in the complex
frequency domain.{{i:frequency domain}}

## t2f and f2t shortcuts {#t2f-f2t}

::: only 7,8
TODO. These are shortcuts to {{t:laplace}}'s Laplace and inverse Laplace
transforms.
:::
::: only 9
TODO. Symbulator 9 does export them, as `t2s` (time to s-domain) and `s2t`
(s-domain to time), wrapping SymPy's `laplace_transform` and
`inverse_laplace_transform`. `t2s("5")` gives `5/s`, the s-domain form of a
5 V step, which is what an `fd` or `tr` source value wants.

::: warning Use the package's own t
Both functions take `t` and `s` as arguments, defaulting to symbols declared
`positive=True`. Handing them an expression written in a bare `Symbol("t")`
does not fail — it treats that `t` as a constant and quietly returns the wrong
transform. Declare your own as `Symbol("t", positive=True)`, or pass the
symbol you used: `t2s(expr, t=my_t)`.
:::
:::

## Instructive FD problems {#practice-fd}

TODO.

## Transfer function problems {#transfer-functions}

TODO.
