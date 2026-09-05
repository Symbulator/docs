% symbulator.cls -- look of the Symbulator documentation PDFs
% Compile with xelatex.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{symbulator}[2026/08/20 Symbulator documentation]
\LoadClass[11pt,twoside,openany]{report}

\RequirePackage{geometry}
\RequirePackage{fontspec}
\RequirePackage{xcolor}
\RequirePackage{titlesec}
\RequirePackage{enumitem}
\RequirePackage{graphicx}
\RequirePackage{tcolorbox}
\RequirePackage{microtype}
\RequirePackage{fancyhdr}
\RequirePackage{amsmath}
\RequirePackage{tabularx}
\RequirePackage{booktabs}
\RequirePackage{imakeidx}
\RequirePackage{etoolbox}
\RequirePackage{needspace}
\RequirePackage[hidelinks]{hyperref}

\tcbuselibrary{skins,breakable}

% ---------------------------------------------------------------- page ----
% A4 since 29 Aug 2026 (Roberto), replacing the 170mm x 240mm trade size.
% The margin scheme is unchanged, so the text block grows with the page;
% the resulting 156mm measure sits within a couple of mm of the monograph
% and the Book, which have been A4 with 2.8cm margins all along.
\geometry{papersize={210mm,297mm},
          inner=24mm, outer=30mm, top=22mm, bottom=24mm,
          marginparwidth=0mm, footskip=12mm}

% --------------------------------------------------------------- colour ---
% Sampled from the Symbulator Py interface, so the documentation and the
% software it documents read as one product. Amber survives from the TI-89
% keypad as the single warm signal, reserved for warnings.
\definecolor{navy}{HTML}{203864}
\definecolor{accent}{HTML}{2F5FA8}
\definecolor{accentbg}{HTML}{E9EFF8}
\definecolor{sky}{HTML}{8EC7F5}
\definecolor{ink}{HTML}{1C2330}
\definecolor{slate}{HTML}{545D6D}
\definecolor{rule}{HTML}{E2E5EA}
\definecolor{amber}{HTML}{B7791F}
\definecolor{amberbg}{HTML}{FBF3E2}
\definecolor{green}{HTML}{2F7D4F}
\definecolor{greenbg}{HTML}{ECF5EF}
\definecolor{danger}{HTML}{A13030}
\definecolor{dangerbg}{HTML}{FDF1F1}
\definecolor{answer}{HTML}{A13030}
\definecolor{lcd}{HTML}{F2F6FC}
\definecolor{panel}{HTML}{F4F6FA}

% ----------------------------------------------------------------- type ---
% IBM Plex throughout, the same family the website loads, so the two outputs
% are typographically the same document. If Plex is not installed the build
% falls back to the TeX Gyre clones rather than failing.
\IfFontExistsTF{IBM Plex Serif}{
  \setmainfont{IBM Plex Serif}[Ligatures=TeX]
  \setsansfont{IBM Plex Sans}[Ligatures=TeX]
  \setmonofont{IBM Plex Mono}[Scale=0.86]
  % The face of a marked variable (#271, Roberto, 6 Sep 2026): the
  % family's SemiBold Italic, weight 600, not the Bold Italic that
  % \textbf{\textit{}} gives. He found the 700 cut "chubby" at body
  % size; a strip of five weights was set and 600 chosen -- a third
  % lighter in the stroke, the subscripts still open, still a mark.
  \newfontfamily\symvarfont{IBM Plex Serif SemiBold}[Ligatures=TeX,
    ItalicFont=IBM Plex Serif SemiBold Italic]
}{
  % Latin Modern, not TeX Gyre. The fallback used to name TeX Gyre
  % Schola/Heros and DejaVu Sans Mono, none of which can be loaded by
  % name on a stock MiKTeX -- so on a machine without Plex the build did
  % not fall back, it failed outright with "No pages of output". Latin
  % Modern ships with every TeX distribution and is registered for
  % by-name loading, so this branch works anywhere xelatex does.
  %
  % The PDF then differs typographically from the websites, which serve
  % Plex from Google Fonts to every reader. That is the point of the
  % warning: the book still builds, and you can see that it is not the
  % intended type.
  \ClassWarning{symbulator}{IBM Plex not found; falling back to Latin
    Modern. The PDF will not match the websites, which use Plex}
  \setmainfont{Latin Modern Roman}[Ligatures=TeX]
  \setsansfont{Latin Modern Sans}[Ligatures=TeX]
  \setmonofont{Latin Modern Mono}[Scale=MatchLowercase]
  \newcommand{\symvarfont}{\bfseries}   % no semibold in the fallback
}
% A problem's own variable -- the print side of {{var:I_s}} (#261): the
% mark's face, italic. build.py emits \symvar{I\textsubscript{s}}.
\newcommand{\symvar}[1]{{\symvarfont\itshape #1}}
\color{ink}
\linespread{1.06}
\setlength{\parskip}{0.55\baselineskip}
\setlength{\parindent}{0pt}
\setlength{\emergencystretch}{2em}
\newlength{\figwidth}\setlength{\figwidth}{0.72\linewidth}
% #153: build.py sizes each figure from the measured height of the label
% text inside the scan (tools/figure_sizes.json), so labels print at body
% text size everywhere. The width arrives in millimetres; the cap keeps a
% wide crop inside whatever line it lands on -- problem boxes are ~9mm
% narrower than the page's. \figwidth above survives only as the fallback
% for a figure the manifest has not measured yet.
\newcommand{\symfig}[2]{%
  \setlength{\@tempdima}{#1mm}%
  \ifdim\@tempdima>\linewidth\setlength{\@tempdima}{\linewidth}\fi
  \includegraphics[width=\@tempdima]{#2}}

% ------------------------------------------------------------- metadata ---
\newcommand{\@booktitle}{}\newcommand{\booktitle}[1]{\renewcommand{\@booktitle}{#1}}
\newcommand{\@booksubtitle}{}\newcommand{\booksubtitle}[1]{\renewcommand{\@booksubtitle}{#1}}
\newcommand{\@bookversion}{}\newcommand{\bookversion}[1]{\renewcommand{\@bookversion}{#1}}
\newcommand{\@bookplatform}{}\newcommand{\bookplatform}[1]{\renewcommand{\@bookplatform}{#1}}
\newcommand{\@bookauthor}{}\newcommand{\bookauthor}[1]{\renewcommand{\@bookauthor}{#1}}

\makeindex[intoc=true,title=Index,columns=2]

% ------------------------------------------------------------ title page --
\newcommand{\maketitlepage}{%
  \thispagestyle{empty}
  \vspace*{22mm}
  {\sffamily\bfseries\fontsize{38}{40}\selectfont\color{navy} \@booktitle\par}
  \vspace{2mm}
  {\color{accent}\rule{34mm}{2.2pt}\par}
  \vspace{5mm}
  {\sffamily\fontsize{13}{17}\selectfont\color{slate}\@booksubtitle\par}
  \vfill
  {\sffamily\fontsize{20}{24}\selectfont\color{accent}\@bookversion\par}
  {\sffamily\fontsize{12}{16}\selectfont\color{slate}\@bookplatform\par}
  \vspace{9mm}
  {\sffamily\fontsize{11}{14}\selectfont \@bookauthor\par}
  \clearpage}

% ------------------------------------------------------------- headings --
\titleformat{\chapter}[display]
  {\sffamily}
  {\color{accent}\bfseries\fontsize{11}{13}\selectfont\MakeUppercase{\chaptertitlename\ \thechapter}}
  {2mm}
  % \raggedright so a long title wraps instead of running off the page --
  % Lesson 4's "Shorts, equivalent resistance and Thévenin/Norton" was
  % 162pt overfull and clipped at the page edge until 29 Aug 2026.
  {\bfseries\fontsize{26}{30}\selectfont\raggedright}
  [\vspace{1mm}{\color{rule}\titlerule[0.8pt]}]
\titlespacing*{\chapter}{0pt}{0pt}{7mm}

\titleformat{\section}
  {\sffamily\bfseries\fontsize{15}{18}\selectfont}{\color{accent}\thesection}{3mm}{}
\titlespacing*{\section}{0pt}{7mm}{2mm}

\titleformat{\subsection}
  {\sffamily\bfseries\fontsize{11.2}{14}\selectfont\color{slate}}{}{0pt}{}
\titlespacing*{\subsection}{0pt}{5mm}{1mm}

\setcounter{secnumdepth}{1}
\setcounter{tocdepth}{1}

% The contents is navigation, not prose, so it is set in the sans — matching
% the sidebar on the website and the running feet here.
\RequirePackage{titletoc}
\renewcommand{\tableofcontents}{%
  \setcounter{secnumdepth}{0}%
  \chapter*{Contents}\markboth{Contents}{Contents}%
  \begingroup\sffamily
  \@starttoc{toc}%
  \endgroup}
\titlecontents{chapter}[0pt]
  {\addvspace{3.2mm}\sffamily\bfseries}
  {}{}
  {\hfill\normalfont\sffamily\bfseries\contentspage}
\titlecontents{section}[6mm]
  {\addvspace{0.6mm}\sffamily\fontsize{10}{13}\selectfont\color{slate}}
  {\contentslabel{8mm}}{}
  {\titlerule*[0.7pc]{\color{rule}.}\normalfont\sffamily
   \fontsize{10}{13}\selectfont\contentspage}
\renewcommand{\chaptername}{Lesson}

% Lessons carry numbered sections; front and back matter do not.
% Both open with \color{ink}: the second line of defence against the
% colour leak described at the problem box below -- a chapter must never
% inherit whatever colour the previous page's last box left behind.
\newcommand{\lesson}[2]{\color{ink}\setcounter{secnumdepth}{1}\chapter{#2}}
\newcommand{\frontchapter}[1]{%
  \color{ink}\setcounter{secnumdepth}{0}%
  \chapter*{#1}\addcontentsline{toc}{chapter}{#1}%
  \markboth{#1}{#1}}
% standfirst: the "what to expect" paragraph that opens a chapter
\newcommand{\chaptersummary}[1]{%
  {\sffamily\fontsize{12.8}{17}\selectfont\color{slate}#1\par}\vspace{3mm}}
% -------------------------------------------------------------- table ----
% Emitted by build.py for a pipe table. booktabs rules only: the web side
% is one rule under the header and a hairline between rows, and print
% should read the same way rather than becoming a grid of boxes.
\setlength{\tabcolsep}{0.6em}   % between columns; the emitter closes the ends with @{}
\renewcommand{\arraystretch}{1.25}

% ---------------------------------------------------------- quotation ----
% A quotation and its attribution. The words are italic and the
% attribution returns to the upright text face a size down, so the name
% inside it -- which the source sets bold -- is the thing the eye finds.
\newenvironment{symquote}
  {\begin{quote}\itshape}
  {\end{quote}}
\newcommand{\quoteby}[1]{%
  \par\smallskip{\normalfont\footnotesize #1}}

\newcommand{\practicerule}{%
  \vspace{3mm}{\color{rule}\hrule height 0.8pt}\vspace{2mm}}
\newcommand{\practiceheading}[1]{%
  \vspace{4mm}{\color{rule}\hrule height 0.8pt}\vspace{2mm}
  {\sffamily\bfseries\fontsize{13}{16}\selectfont #1\par}}

% -------------------------------------------------------------- running --
\pagestyle{fancy}\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\fancyfoot[LE,RO]{\sffamily\small\thepage}
\fancyfoot[RE]{\sffamily\footnotesize\color{slate}\@bookversion}
\fancyfoot[LO]{\sffamily\footnotesize\color{slate}\nouppercase{\leftmark}}

% ----------------------------------------------------------------- code ---
\newcommand{\symcode}[1]{{\ttfamily\small #1}}
% a value the software gave back, as distinct from one you typed
\newcommand{\ans}[1]{{\bfseries\color{answer}#1}}
% An answer that is a symbolic expression: same answer colour, but set as
% mathematics rather than bold text (build.py's answer_math decides which).
\newcommand{\ansmath}[1]{{\color{answer}\(\displaystyle #1\)}}

\newenvironment{symtype}
  {\par\vspace{1mm}\begin{tcolorbox}[breakable,enhanced,boxrule=0pt,
     frame empty, colback=lcd, left=3mm,right=3mm,top=1.6mm,bottom=1.6mm,
     borderline west={2.2pt}{0pt}{accent}, sharp corners]
   \ttfamily\small\raggedright\setlength{\parskip}{0pt}}
  {\end{tcolorbox}\color{ink}\vspace{1mm}}

% An address to share (#259): a URL on a line of its own, centred, on the
% input panel's tint -- the print side of the ::: address directive.
% #1 is the link target, #2 the text as printed (already escaped).
\newcommand{\symaddress}[2]{\par\vspace{1mm}%
  \begin{tcolorbox}[enhanced,boxrule=0pt,frame empty,colback=lcd,
     left=3mm,right=3mm,top=1.6mm,bottom=1.6mm,sharp corners,halign=center]
  \ttfamily\small\href{#1}{\textcolor{accent}{#2}}%
  \end{tcolorbox}\color{ink}\vspace{1mm}}

\newenvironment{symout}
  {\par\vspace{1mm}\begin{tcolorbox}[breakable,enhanced,boxrule=0pt,
     frame empty, colback=panel, left=3mm,right=3mm,top=1.6mm,bottom=1.6mm,
     borderline west={2.2pt}{0pt}{slate}, sharp corners]
   \ttfamily\small\raggedright\setlength{\parskip}{0pt}}
  {\end{tcolorbox}\color{ink}\vspace{1mm}}

% ------------------------------------------------------------- callouts ---
% Every callout carries an icon and a word, so the four kinds remain
% distinguishable in greyscale and on a black-and-white printout. The icons are
% drawn in TikZ, in ex units, so they scale with the surrounding type.

\newcommand{\@icotip}{%                                            lightbulb
  \tikz[baseline=-0.45ex,x=1ex,y=1ex,line width=0.5pt,line join=round]{
    \draw (0,0.35) circle (0.62);
    \draw (-0.30,-0.42) -- (0.30,-0.42);
    \draw (-0.20,-0.78) -- (0.20,-0.78);}}

\newcommand{\@iconote}{%                                            circled i
  \tikz[baseline=-0.45ex,x=1ex,y=1ex,line width=0.5pt]{
    \draw (0,0) circle (0.82);
    \draw (0,-0.42) -- (0,0.18);
    \fill (0,0.46) circle (0.10);}}

\newcommand{\@icowarning}{%                                  triangle and bang
  \tikz[baseline=-0.45ex,x=1ex,y=1ex,line width=0.5pt,line join=round]{
    \draw (0,0.92) -- (0.88,-0.62) -- (-0.88,-0.62) -- cycle;
    \draw (0,0.42) -- (0,-0.08);
    \fill (0,-0.34) circle (0.09);}}

\newcommand{\@icodanger}{%                                    octagon and bang
  \tikz[baseline=-0.45ex,x=1ex,y=1ex,line width=0.5pt,line join=round]{
    \draw (22.5:0.92) \foreach \a in {67.5,112.5,157.5,202.5,247.5,292.5,337.5}
      {-- (\a:0.92)} -- cycle;
    \draw (0,0.40) -- (0,-0.12);
    \fill (0,-0.40) circle (0.09);}}

% #1 accent colour, #2 background, #3 icon, #4 word, #5 the author's title
\newtcolorbox{@callout}[5]{breakable,enhanced,boxrule=0pt,frame empty,
  colback=#2, left=4mm,right=4mm,top=2.5mm,bottom=2.5mm, sharp corners,
  borderline west={2.6pt}{0pt}{#1},
  title={},
  before upper={%
    {\sffamily\color{#1}#3\hspace{0.45em}%
     \fontsize{7.6}{9}\selectfont\bfseries\MakeUppercase{#4}\par}%
    \vspace{0.8mm}%
    \ifstrempty{#5}{}{{\sffamily\bfseries\fontsize{10.6}{13}\selectfont
                       #5\par}\vspace{0.6mm}}}}

% Each wrapper re-asserts ink after its box: the colour-leak guard (see
% the problem box below). The installed tcolorbox has no `after app`
% key, so the guard lives in the wrappers instead of the box options.
\newenvironment{callouttip}[1]
  {\begin{@callout}{green}{greenbg}{\@icotip}{Tip}{#1}}
  {\end{@callout}\color{ink}}
% #188: accent, not slate -- note read grey beside the other three, which
% each have a hue of their own. Same token the screen side uses, so the
% two outputs are the same blue.
\newenvironment{calloutnote}[1]
  {\begin{@callout}{accent}{accentbg}{\@iconote}{Note}{#1}}
  {\end{@callout}\color{ink}}
\newenvironment{calloutwarning}[1]
  {\begin{@callout}{amber}{amberbg}{\@icowarning}{Warning}{#1}}
  {\end{@callout}\color{ink}}
\newenvironment{calloutdanger}[1]
  {\begin{@callout}{danger}{dangerbg}{\@icodanger}{Caution}{#1}}
  {\end{@callout}\color{ink}}

% ------------------------------------------------------ problems/figures --
% #172: a worked problem is a rule and a title, not a frame. It was a
% breakable tcolorbox until 30 Aug 2026, and the frame was what stranded
% the circuits: LaTeX refuses \begin{figure} inside any box ("Not in
% outer par mode"), so every one of the 280 circuits inside a problem had
% to sit exactly where it was written. A circuit that did not fit in what
% was left of the page took the rest of the page with it -- measured at
% sixteen pages of holes in the middle of v9's 259. Frameless, the same
% circuits are floats, and the text closes up behind them.
%
% What keeps a circuit with its problem is the placement build.py asks for:
% [!ht], never [b] or [p]. A circuit may stay where it was written or rise
% to the top of the page it lands on; it can never sink to the foot of a
% page or take a page of its own, either of which would put it after the
% words that introduce it. Measured over all 284 circuits in v9, none is
% printed before its own title and only two land more than a page after it.
% \FloatBarrier at the head of each problem was tried and dropped: it
% changed neither of those numbers, and it flushed the page it fired on,
% putting back the mid-page holes this whole change exists to remove.
%
% The old frame's \color{ink} guard is gone with the frame. It was there
% because a breakable box whose end met a page break leaked its white
% fill into the ambient colour of every page after it (Lessons 9 and 10
% opened with invisible titles in the 29 Aug 2026 A4 build). The callouts
% above are still boxes and still carry the guard, and
% tools/check_white_text.py still renders every page to prove it held.
\newenvironment{problem}[1]
  {\par\addvspace{4mm}{\color{rule}\hrule height 0.8pt}%
   \vspace{1.5mm}%
   {\sffamily\bfseries\fontsize{11.5}{14}\selectfont #1\par}\vspace{0.5mm}}
  {\par\addvspace{3mm}}

\newenvironment{solution}
  {\par\vspace{1.5mm}{\sffamily\bfseries\footnotesize\color{accent}%
   \MakeUppercase{Solution}\par}\vspace{-1mm}}
  {\par}

\newenvironment{symfigure}
  {\par\vspace{2mm}\begin{center}\captionsetup{}}
  {\end{center}\vspace{1mm}}
\newcommand{\caption@sym}[1]{}
\renewcommand{\caption}[1]{\par\vspace{1mm}%
  {\sffamily\footnotesize\color{slate}#1\par}}
\newcommand{\captionsetup}[1]{}

% lists
% parskip is generous for paragraphs; lists need their own, tighter, spacing
\setlist{parsep=0pt, partopsep=0pt}
\setlist[itemize]{leftmargin=5mm, itemsep=0.35\baselineskip,
                  topsep=0.35\baselineskip}
\setlist[enumerate]{leftmargin=6mm, itemsep=0.35\baselineskip,
                    topsep=0.35\baselineskip}

\newcommand{\printtheindex}{\clearpage\printindex}
