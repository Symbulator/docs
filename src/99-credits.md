---
id: credits
kind: back
title: Roll the credits
updated: 2026-09-06
summary: >
  If you are interested in the people behind Symbulator, here's who made it and who helped, plus some acknowledgements. And some glowing reviews received over the decades.
---

## Who made Symbulator {#about-the-author}

Symbulator and its documentation, in all its versions up to this date, have been made by me, [**Roberto Perez-Franco**](http://roberto.perez-franco.com). I started coding it on 30 March 1999, when I was an engineering student at the Technological University of Panama (Universidad Tecnológica de Panamá) in [Azuero](https://ls.utp.ac.pa/). The first public release, version 0.92, went onto the Internet on 2 April 1999, three days after the first line of code, and version 0.994 — the equivalent of version 1 — came out on 29 May 1999. An early version won first place at the IEEE Student Paper Contest for Latin America in 2000, and version 5 (a.k.a. Q) served as my graduation thesis in July 2001. Version 6 came in 2013, while I was a researcher at MIT in the United States. Versions 7 and 8 came a decade later, in 2023, when I was in Melbourne Australia. This version 9 was made in 2026. 

::: figure assets/photo/roberto_2000_ti89.jpg
Roberto in 2000, with a TI-89
:::

### A timeline

| Date | Event |
|---|---|
| **30 March 1999** | The first line of code, at the Technological University of Panama in Azuero. |
| **2 April 1999** | Version 0.92, the first public release, goes onto the Internet. |
| **29 May 1999** | Version 0.994 — the equivalent of version 1. |
| **19 August 1999** | Version 2, presented in person for the first time, at UTP Azuero. |
| **October 1999** | The Elect SCS plug-in. The program is still called SCS. |
| **November 1999** | The paper is written. |
| **Late 1999 or early 2000** | Version 3. |
| **14 May 2000** | The Power Tools plug-in. The program is now called Symbulator. |
| **October 2000** | First place, IEEE Region 9 Student Paper Competition. |
| **December 2000** | The paper is published in Panama, in the bulletin of the IEEE section. |
| **9 January 2001** | Version 4. |
| **30 March 2001** | Version 5, called Q. |
| **9 July 2001** | The thesis is defended, and graded 100 out of 100. |
| **September 2001** | The paper is published in Barcelona, in the magazine of the IEEE student branch. |
| **June 2013** | Version 6, written at MIT. |
| **July 2023** | Versions 7 and 8, written in Melbourne. |
| **13 August 2026** | The symbulator package goes onto PyPI. |
| **28 August 2026** | Version 9, a public beta. |

### What Symbulator did for me

I've never made any money from Symbulator: it has always been and will remain free of charge. But I have benefited from Symbulator in other ways. Thanks in large part to Symbulator, I landed my first job, received a
Distinguished Alum award from UTP in 2008 and an Outstanding Young Person (TYOP) award from the Panamanian chapter of Junior Chamber International (JCI), and won a Fulbright Scholarship that
took me to a Master of Engineering and later a PhD in Engineering Systems at the Massachusetts Institute of Technology. MIT then hired me, and I lived in Boston for almost twelve years. I now live in Melbourne, Australia. You can say 
that writing Symbulator changed my life. Beyond my lifetime, Symbulator may preserve a part of my mind as it solves circuits for new generations, the same way a composer lives in the tunes or a writer in the words they conceived.

### Dedication

Two people made Symbulator possible, with their love and support.

The first is my wife **Monica**, who had the patience to live with a cyborg
for all the years my mind was focused on coding and documenting. *Mi reina*, my attention
was elsewhere, but my heart was always with you.

The second is my late father **Tito**, who invested time and money in my
education and bought me every gadget and every book I needed or wanted for my studies, 
with a blind faith that one day something good would come of it. I'm happy to know
that I made you proud, Dad, and I miss you every day.

### How to reach me

If you liked Symbulator, let me know. My email is my given name, then my last
name with a hyphen, as a dot-com address, like so: rxxxxxx@pxxxx-fxxxxx.cxx

## Acknowledgements {#acknowledgements}

### Human collaborators

Over the past decades, many people have made Symbulator better
through their suggestions and corrections, on both the software and the
documentation. Many were complete strangers at first and became dear friends
through our exchanges. Others were dear friends that became collaborators.

**Versions 1 through 6** received feedback and suggestions from José Vega
(Panama), Tim Hutcheson (USA), Lars Frederiksen (Denmark), Joe Riel (USA),
Arne Harstad (Norway), Erwin Baert (Belgium), Charles 'Chuck' Ware (USA),
Doug Burkett (USA), Reinhard Willinski (Germany), Kamil Malinski (Austria),
Jake Adams (USA), Daniele Martini (Italy), Rozgonyi Szabolcs (Hungary),
Michael Rans (UK), Alex Astashyn (Russia), Al Charpentier (USA), Nevin
McChesney (USA), Ivan Oro Yu (Panama), Pepe Iborra (Spain), and Dave Conklin
(USA). **Versions 7 and 8** received feedback and suggestions from Carlos
Perez Ortega (Chile) and Qifan Wang (China).

**Version 9** benefited from feedback and excellent suggestions from my dear
old friend Antony García (Panama), who is not only one hell of an engineer
and a consummate circuit theorist, but who also taught the same Circuits
class at UTP as Prof. Eliane Boulet for many years. I met Antony in May
2013, while he was a student at UTP Azuero in the same major that I had
completed more than a dozen years earlier. I was immediately struck by his
brilliance, and we became friends. In August 2026, I shared an early version
of Symbulator 9 with Antony while he was a PhD candidate in the ECE Department
at WPI (MA, USA).
Antony generously provided me with a series of fantastic recommendations —
from his vantage point as both a student and a teacher of circuit theory —
regarding features he would like to see in Symbulator. I worked with Claude
over a few weeks in September to turn them into reality.

My thanks to all of them. I truly am in their debt.

::: only 9
### AI collaborator

I also want to acknowledge that porting Symbulator to Python/SymPy, creating
its interface and websites and updating its documentation, would not have been possible without the coding prowess of Anthropic's
artificial intelligence assistant. Claude allowed me to do in two weeks something that 
I was unable to find the time to do in two decades: to port Symbulator to Python.

::: warning Use AI responsibly 
AI is not without risks, and needs careful policies and regulatory oversight on fronts like ethics, 
systemic biases, its impact on labour, and its voracious use of water and energy.
:::

I believe there is a right way to deploy this technology, and — after working
on Symbulator 9 with Claude — I am now convinced that AI will revolutionise the
way we work. We just need to do it the right way.
:::

### Software I relied on

::: only 7
Symbulator 7 relies on **DiffEq**, by Lars Frederiksen, for its Laplace
transforms. Lars is one of the most gifted TI-Basic programmers there has ever
been. For many years I hosted his programs exclusively on my website, at his
request, and had the honour of helping him beta-test them for the TI-89.
:::
::: only 8
Symbulator 8 relies on Lars Frederiksen's Laplace functions, adapted for the
TI-Nspire by Philippe Fortin. I have renamed that file **LF** here, in homage
to Lars.
:::
::: only 9
Symbulator 9 runs on **Python** and is powered by the algebraic capabilities
of **SymPy** and the numerical prowess of **NumPy**.
I am thankful to the creators of such wonderful open-source software, and to the 
maintainers who keep their development going. I am proud to honour the open-source
community by making Symbulator free and open-source software, from 2026.

Throughout its development, Symbulator 9's answers were checked
against **ahkab**, an independent circuit simulator written in Python by
Giuseppe Venturini. Every circuit that Symbulator's SPICE
translator exports is solved a second time by ahkab, and the two must agree
before a release goes out — a habit that has caught more than one convention I
had taken for granted. None of ahkab's code is part of Symbulator, and it is
not needed to run it: it is a second opinion, kept at arm's length, and a
valuable one. My thanks to Giuseppe for building such a tool and
sharing it freely.
:::

## Problem credits {#problem-credits}

To make this book useful to actual students, the problems were chosen from
widely used textbooks on electric circuit analysis, and their circuit diagrams
are reproduced here as they appear in the source.

| Code | Textbook |
|---|---|
| **AS2** | *Fundamentals of Electric Circuits* (2nd ed.), Charles K. Alexander and Matthew N. O. Sadiku, McGraw-Hill, 2004 |
| **AS5** | *Fundamentals of Electric Circuits* (5th ed.), Alexander and Sadiku, McGraw-Hill, 2013 |
| **AS7** | *Fundamentals of Electric Circuits* (7th international ed.), Alexander and Sadiku, McGraw-Hill, 2020 |
| **B11** | *Introductory Circuit Analysis* (11th ed.), Robert L. Boylestad, Pearson – Prentice Hall, 2007 |
| **Bo2** | *Elementary Linear Circuit Analysis* (2nd ed.), Leonard S. Bobrow, Oxford, 1987 |
| **HK5** | *Engineering Circuit Analysis* (5th ed.), William H. Hayt Jr. and Jack E. Kemmerly, McGraw-Hill, 1993 |
| **NR9** | *Electric Circuits* (9th ed.), James W. Nilsson and Susan A. Riedel, Prentice Hall, 2011 |
| **NR11** | *Electric Circuits* (11th ed.), Nilsson and Riedel, Pearson, 2020 |
| **NR12** | *Electric Circuits* (12th ed.), Nilsson and Riedel, Pearson, 2023 |
| **RM3** | *Circuit Analysis: Theory and Practice* (3rd ed.), Allan H. Robbins and Wilhelm C. Miller, Thomson – Delmar Learning, 2004 |
| **TR5** | *The Analysis and Design of Linear Circuits* (5th ed.), Roland E. Thomas and Albert J. Rosa, Wiley, 2006 |

For the purpose of teaching students how to use Symbulator, these diagrams are
reproduced under the principle of fair use. No copyright infringement is
intended.

## Praise received {#praise}

Over the past quarter of a century, the words of encouragement I received from
users of Symbulator were my incentive to keep working on it. Here is a little
of that precious collection.

> The masterpiece of TI-89 programming.
>
> — **Alex Astashyn**, EE+CoE+CoS major, Polytechnic University, Brooklyn, New York, USA

> Symbulator is and always will be the best program for TI-89/92/V200.
>
> — **Charles Ware**, EE major, Columbus, Ohio, USA

> Roberto, your program Symbulator is by itself a reason to buy the calc. It's
> a masterpiece of programming.
>
> — **Pepe Iborra**, Telecommunications, Spain

> The program is really a masterpiece. It gives you everything you need, very
> accurate, very fast. It's really what every Electrical Engineer dreams of.
> It's so easy to use and it does everything! DC, AC, Transient analysis,
> Thévenin, Bode plots… everything! I'm really amazed.
>
> — **Nikolaos Trichakis**, EE major, Aristotle University of Thessaloniki, Greece

> I wish I had it while going through school.
>
> — **Joe Riel**, BSEE, creator of Syrup (a symbolic circuit simulator for Maple V), University of California, Irvine, USA

> Congratulations for your program: it's simply fantastic. Symbulator is worth
> the cost of a TI-89!
>
> — **Pier Giorgio Raponi**, engineering student, Pisa, Italy

> You've made an excellent program. Symbulator is really the best circuit
> simulator ever made for a calculator.
>
> — **Rui Sebastião**, EE major, University of Coimbra, Portugal

> Symbulator is probably the most useful program ever made for a TI calculator.
> I am an electronics student and even paid for the EE*Pro software, yet I find
> myself using Symbulator more because it is much better at what it does.
>
> — **Josh Cunningham**, electronics major

> Symbulator, by far, has been the best tool for EE I have come across yet. […]
> It is truly an impressive piece of work. You should be proud. It certainly is
> helping me to focus on my studying of EE instead of trying to remember all
> the math.
>
> — **Jim Wachtel**, EE, Process Control & Electrical Co., St. Louis, Missouri, USA

## Licence {#licence}

From June 2013, Symbulator
was offered under a Creative Commons BY-NC-SA licence. Since 2026 it is open source
under the MIT licence, which supersedes it. If you want to port it to another
platform, you are free to do so, provided the copyright notice and the
attribution of authorship travel with it.