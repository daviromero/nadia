# Natural Deduction Proof Assistant (NADIA)

The NADIA is a tool written in Python that can be used as a desktop application, or in a [web platform](https://sistemas.quixada.ufc.br/nadia/). The main idea is that the students can write their proofs as similar as possible to what is available in the textbooks and to what the students would usually write on paper. NADIA allows the students to automatically check whether a proof in the natural deduction is valid. If the proof is not correct, NADIA will display the errors of the proof. So, the students may make mistakes and learn from the errors. The web interface is very easy-to-use and has: 
- An area for editing the proof in plain text. The students should write a proof in Fitch-style (see [ND Rules](https://raw.githubusercontent.com/daviromero/nadia/main/ND-Rules.pdf)).
- A message area to display whether the proof is valid, the countermodel, or the errors on the proof.
- And the following links: 
  - Check, to check the correctness of the proof; 
  - Manual, to view a document with the inference rules and examples; 
  - Fitch, to generate the LaTeX code in a Fitch-style of a valid proof. Use the `logicproof` package in your LaTeX code; 
  - Gentzen, to generate the LaTeX code in a Gentzen-style of a valid proof. Use the `proof` package in your LaTeX code; 
  - Fitch LaTeX in Overleaf, to open the proof source code directly in [Overleaf](http://overleaf.com/) that is a collaborative platform for editing LaTeX

To facilitate the writing of the proofs, we made the following conventions in NADIA:
- The Atoms are written in capital letters (e.g. `A, B,  H(x)`);
- Variables are written with the first letter in lowercase, followed by letters and numbers (e.g. `x, x0, xP0`);
- Formulas with $\forall x$ and $\exists x$ are represented by $Ax$ and $Ex$ ('A' and 'E' followed by the variable x). For instance, `Ax(H(x)->M(x))` represents $\forall x~(H(x)\rightarrow M(x))$.
- Table below shows the equivalence of logic symbols and those used in NADIA.
- The order of precedence of quantifiers and logical connectives is defined by $\lnot,\forall,\exists,\wedge,\vee,\rightarrow$ with right alignment. For example:
  - Formula `~A&B -> C` represents formula $(((\lnot A)\land B)\rightarrow C)$;
  - The theorem `~A|B |- A->C` represents $((\lnot A)\vee B)\vdash (A\rightarrow B)$.
- Each inference rule will be named by its respective connective and `i` (introduction) or `e` (elimination). For example, `->e` represents the elemination and rule. 
- The justifications for the premises  use the reserved word `pre`.

| Symbol |  $\lnot$ | $\land$ | $\lor$ | $\rightarrow$ | $\forall x$ | $\exists x$ | $\bot$ | box | $\vdash$ |
| :---:  |  :---:  | :---: | :---:  | :---:  | :---:  | :---:  | :---:  | :---:  | :---: |
| LaTeX  |  $\backslash\textrm{lnot}$ | $\backslash\textrm{land}$ | $\backslash\textrm{lor}$ | $\backslash\textrm{rightarrow}$ | $\backslash\textrm{forall x}$ | $\backslash\textrm{exists x}$ | $\backslash\textrm{bot}$ | $[.~]$ | $\backslash\textrm{vdash}$ |
| NADIA |  ~  | \& | $\mid$ | -> | Ax | Ex | @  | { } | \|- |

![](https://raw.githubusercontent.com/daviromero/nadia/main/NADIA-EXAMPLE.png)

## License
NADIA is available by [**MIT License**](https://raw.githubusercontent.com/daviromero/nadia/main/license.txt).

## Requirements:
You must install 
- [rply 0.7.8 package](https://pypi.org/project/rply/)
- ipywidgets

## Install

To install NADIA from Github, run the following command:
```bash
pip install git+https://github.com/daviromero/nadia.git
```

To install NADIA from PyPi repository, run the following command:
```bash
pip install nadia-proof
```

## NADIA
You can run NADIA with the command line: 
```bash
nadia -i [input_proof_file] [-t input_theorem]
```
## NADIA in Voila
You can run NADIA in Jupyter Nootebook or in a [Voilà](https://voila.readthedocs.io/) 
```bash
voila nadia_pt.ipynb
```
## NADIA in your code
You can import NADIA in your code (basic usage)
```bash
from nadia.nadia_pt_fo import check_proof

print(check_proof('''1. A|B              pre
2. A->C             pre
3. B->C             pre
4. {    A           hip
5.      C           ->e 4,2
   } 
6. {    B           hip
7.      C           ->e 6,3
   }
8. C                |e 1, 4-5, 6-7'''))```
