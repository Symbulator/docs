Five problems are in the $s$ domain. FD returns every answer as a
function of $s$, initial conditions included, so a transfer function is nothing
more than the answer with the source left as a symbol, and two of these are
exactly that. Two others ask for a function of time, and are worked the way the
book works them: the circuit is solved in the $s$ domain and the answer inverted
afterwards, which is what `s2t` does in the {{card:Evaluate}} card. Nothing on
this page is labelled *filter* or *transfer function*, because nothing needs to
be. The book's other Laplace-chapter examples are in the TR section above, where
the solver transforms and inverts out of sight.
