---
id: manual-credits
kind: manual-back
book: manual
title: Who made this
versions: [9]
updated: 2026-09-11
summary: >
  Symbulator is one person's work since 1999, improved by many others, MIT-licensed since 2026. The long version is in the Course.
---

## The author

Symbulator and its documentation are the work of
[**Roberto Perez-Franco**](http://roberto.perez-franco.com), begun on
**30 March 1999** as an engineering student at the Technological University
of Panama.

An early version won first place at the IEEE Student Paper Contest for Latin
America in 2000; version 5 was his graduation thesis in 2001. Version 6 came
in 2013 at MIT, versions 7 and 8 in 2023 in Melbourne, and this one in 2026.

## Acknowledgements

Many people have made Symbulator better over the decades, through their
suggestions and their corrections. Several were strangers who became friends
in the exchange.

**Versions 1 to 6** — José Vega (Panama), Tim Hutcheson (USA), Lars
Frederiksen (Denmark), Joe Riel (USA), Arne Harstad (Norway), Erwin Baert
(Belgium), Charles 'Chuck' Ware (USA), Doug Burkett (USA), Reinhard Willinski
(Germany), Kamil Malinski (Austria), Jake Adams (USA), Daniele Martini
(Italy), Rozgonyi Szabolcs (Hungary), Michael Rans (UK), Alex Astashyn
(Russia), Al Charpentier (USA), Nevin McChesney (USA), Ivan Oro Yu (Panama),
Pepe Iborra (Spain) and Dave Conklin (USA).

**Versions 7 and 8** — Carlos Perez Ortega (Chile) and Qifan Wang (China).

**Version 9** — Antony García (Panama), engineer, circuit theorist and a
teacher of the same Circuits class at UTP. He read an early version in August
2026 and sent back a series of recommendations, from his vantage point as
both student and teacher, which became features over the following weeks.

My thanks to all of them. I truly am in their debt.

### Claude

Porting Symbulator to Python and SymPy, building its interface and websites
and rewriting its documentation would not have happened without Anthropic's
AI assistant. Claude let me do in two weeks what I had not found time for in
two decades.

::: warning Use AI responsibly
AI is not without risks, and needs careful policies and regulatory oversight
on fronts like ethics, systemic biases, its impact on labour, and its
voracious use of water and energy.
:::

There is a right way to deploy this technology, and after working on
Symbulator 9 with Claude I am convinced it will change the way we work — if
we do it the right way.

### The software it stands on

**Python**, with **SymPy** for the algebra and **NumPy** for the numerics. My
thanks to their creators and maintainers, and it is why Symbulator is free
and open-source from 2026.

Answers are checked during development against **ahkab**, an independent
circuit simulator by Giuseppe Venturini. Every circuit the SPICE translator
exports is solved a second time by ahkab and the two must agree before a
release — a habit that has caught more than one convention taken for granted.
None of ahkab's code is part of Symbulator and it is not needed to run it: it
is a second opinion, kept at arm's length, and a valuable one.

## Licence

**MIT**, since 2026. Port it anywhere you like, provided the copyright notice
and the attribution travel with it.

## Getting in touch

The author can be reached at help@symbulator.com
