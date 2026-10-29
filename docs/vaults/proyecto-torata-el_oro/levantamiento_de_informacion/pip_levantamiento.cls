% --- PIP_LEVANTAMIENTO CLASS ---
% Clase de LaTeX para Informes de Levantamiento de Información Territorial
% Asignatura: Proyectos de Inversión Pública - Carrera de Economía (UNL)
% Basada en la arquitectura del TIC de la carrera, adaptada para trabajo en equipo y sin marco box.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{pip_levantamiento}[2026/10/20 Clase de Levantamiento Territorial UNL - Proyectos de Inversion Publica]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass[11pt]{article}

% --- Paquetes requeridos ---
\RequirePackage{graphicx}
\RequirePackage{geometry}
\RequirePackage{indentfirst}
\RequirePackage{caption}
\RequirePackage{floatrow}
\RequirePackage{booktabs}
\RequirePackage{float}
\RequirePackage{longtable}
\RequirePackage{threeparttable}
\RequirePackage{array}
\RequirePackage{multirow}
\RequirePackage{calc}
\RequirePackage{amsmath,amssymb}
\RequirePackage{fancyhdr}
\RequirePackage{setspace}
\RequirePackage{ragged2e}
\RequirePackage{titlesec}
\RequirePackage{url}
\RequirePackage{eso-pic}
\RequirePackage{etoolbox}
\RequirePackage{pdflscape}
\RequirePackage{rotating}
\RequirePackage{xcolor}
\RequirePackage[hidelinks,breaklinks]{hyperref}

% Enlaces
\definecolor{WordBlue}{HTML}{0563C1}
\AtBeginDocument{%
  \hypersetup{%
    colorlinks=true,
    linkcolor=WordBlue,
    citecolor=WordBlue,
    urlcolor=WordBlue,
    breaklinks=true,
    pdfborder={0 0 0}%
  }%
  \urlstyle{same}%
}

% --- Variables y metadatos institucionales ---
\newcommand{\university}[1]{\gdef\@university{#1}}
\newcommand{\faculty}[1]{\gdef\@faculty{#1}}
\newcommand{\school}[1]{\gdef\@school{#1}}
\newcommand{\course}[1]{\gdef\@course{#1}}
\newcommand{\assignment}[1]{\gdef\@assignment{#1}}
\newcommand{\subtitle}[1]{\gdef\@subtitle{#1}}
\newcommand{\professor}[1]{\gdef\@professor{#1}}
\newcommand{\advisorrole}[1]{\gdef\@advisorrole{#1}}
\newcommand{\city}[1]{\gdef\@city{#1}}
\renewcommand{\year}[1]{\gdef\@year{#1}}

% Valores por defecto
\university{UNIVERSIDAD NACIONAL DE LOJA}
\faculty{FACULTAD JURÍDICA, SOCIAL Y ADMINISTRATIVA}
\school{CARRERA DE ECONOMÍA}
\course{PROYECTOS DE INVERSIÓN PÚBLICA}
\assignment{LEVANTAMIENTO DE INFORMACIÓN Y LÍNEA BASE TERRITORIAL}
\professor{Econ. José Job Chamba Tandazo}
\advisorrole{DOCENTE:}
\city{LOJA -- ECUADOR}
\year{2026}

% Geometría APA 7
\geometry{%
  a4paper,
  top=2.54cm,
  bottom=2.54cm,
  left=2.54cm,
  right=2.54cm
}

% Estilo de párrafo
\AtBeginDocument{%
  \onehalfspacing
  \justifying
  \setlength{\parindent}{1.27cm}
  \setlength{\parskip}{0pt}
}

% Captions y leyendas APA 7
\DeclareCaptionLabelSeparator{newline}{\\ \vspace{2pt}}

\captionsetup{%
  justification=raggedright,
  singlelinecheck=false,
  labelfont=bf,
  textfont={it,singlespacing},
  labelsep=newline,
  font={small,singlespacing},
  skip=6pt
}

\captionsetup[table]{%
  labelsep=newline,
  justification=raggedright,
  singlelinecheck=false,
  font={small,singlespacing},
  labelfont=bf,
  textfont={it,singlespacing},
  skip=6pt
}

\captionsetup[figure]{%
  labelsep=newline,
  justification=raggedright,
  singlelinecheck=false,
  font={small,singlespacing},
  labelfont=bf,
  textfont={it,singlespacing},
  skip=6pt
}

\captionsetup[longtable]{%
  labelsep=newline,
  justification=raggedright,
  singlelinecheck=false,
  font={small,singlespacing},
  labelfont=bf,
  textfont={it,singlespacing},
  skip=6pt
}

\floatsetup[table]{capposition=top}
\floatsetup[figure]{capposition=bottom}

\AtBeginEnvironment{longtable}{%
  \singlespacing
  \setlength{\parindent}{0pt}%
  \RaggedRight
  \fontsize{8.5}{10.5}\selectfont
}
\AtBeginEnvironment{tabular}{%
  \singlespacing
  \setlength{\parindent}{0pt}%
  \RaggedRight
  \fontsize{8.5}{10.5}\selectfont
}
\setlength{\tabcolsep}{4pt}
\renewcommand{\arraystretch}{1.15}

% Comando institucional para notas
\newcommand{\fuente}[1]{%
  \vspace{4pt}%
  {\raggedright\singlespacing\footnotesize \textit{Nota.} #1\par}%
}

% Encabezados
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\small Carrera de Economía}
\fancyhead[R]{\small Parroquia Torata}
\fancyfoot[R]{\thepage}
\renewcommand{\headrulewidth}{0.5pt}

\fancypagestyle{plain}{%
  \fancyhf{}%
  \fancyhead[L]{\small Carrera de Economía}%
  \fancyhead[R]{\small Parroquia Torata}%
  \fancyfoot[R]{\thepage}%
  \renewcommand{\headrulewidth}{0.5pt}%
}

% Títulos APA 7 (Estándar unlthesis.cls)
\titleformat{\section}{\normalfont\normalsize\bfseries\centering}{\thesection}{1em}{}
\titleformat{\subsection}{\normalfont\normalsize\bfseries}{\thesubsection}{1em}{}
\titleformat{\subsubsection}{\normalfont\normalsize\bfseries\itshape}{\thesubsubsection}{1em}{}
\titleformat{\paragraph}[runin]{\normalfont\normalsize\bfseries}{\theparagraph}{1em}{}[.]
\titleformat{\subparagraph}[runin]{\normalfont\normalsize\bfseries\itshape}{\thesubparagraph}{1em}{}[.]

\titlespacing*{\section}{0pt}{18pt}{12pt}
\titlespacing*{\subsection}{0pt}{12pt}{6pt}
\titlespacing*{\subsubsection}{0pt}{12pt}{6pt}
\titlespacing*{\paragraph}{1.27cm}{12pt}{0.5em}
\titlespacing*{\subparagraph}{1.27cm}{12pt}{0.5em}

\setcounter{secnumdepth}{5}
\setcounter{tocdepth}{5}

\def\UrlBreaks{\do\/\do-\do\.\do\_\do\?\do\=\do\&\do\%}

% --- DEFINICIÓN DE PORTADA INSTITUCIONAL (Estilo TIC UNL sin cuadro fbox) ---
\renewcommand{\maketitle}{%
  \begin{titlepage}
    \thispagestyle{empty}
    \vspace*{\fill}
    
    \begin{center}
      % Logotipo oficial UNL
      \IfFileExists{asset/logo_unl.png}{%
        \includegraphics[height=2.2cm]{asset/logo_unl.png}\\[0.4cm]
      }{}%

      {\bfseries\large \@university}\\[0.25cm]
      {\bfseries\normalsize \@faculty}\\[0.2cm]
      {\bfseries\normalsize \@school}\\[1.0cm]

      {\bfseries\normalsize ASIGNATURA:}\\[0.15cm]
      {\bfseries\normalsize \@course}\\[1.2cm]

      \setstretch{1.3}
      {\bfseries\Large \@title}\\[0.4cm]
      \ifdefined\@subtitle
        {\bfseries\normalsize \@subtitle}\\[1.0cm]
      \else
        \vspace{0.8cm}
      \fi
    \end{center}

    \vspace{0.8cm}

    \begin{center}
      \setstretch{1.15}
      {\bfseries\normalsize AUTORES:}\\[0.2cm]
      {\normalsize \@author}\\[0.8cm]

      \ifx\@professor\empty
      \else
        {\bfseries\normalsize \@advisorrole}\\[0.15cm]
        {\normalsize \@professor}\\[0.8cm]
      \fi
    \end{center}

    \vspace{0.8cm}

    \begin{center}
      \setstretch{1.0}
      {\bfseries\normalsize \@city}\\[0.15cm]
      {\bfseries\normalsize \@year}
    \end{center}

    \vspace*{\fill}
  \end{titlepage}
  \clearpage
  \pagenumbering{arabic}
  \setcounter{page}{1}
}
