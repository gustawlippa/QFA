# Quantum Finite Automata

This library provides implementations of multiple quantum finite automata 
models.

## Implemented automata models

* **PFA** - Probabilistic Finite Automaton
* **MO1QFA** - Measure-Once Quantum Finite Automaton
* **MM1QFA** - Measure-Many Quantum Finite Automaton
* **GQFA** - General Quantum Finite Automaton

Each module contains a usage example.

### Helper modules

* **LanguageChecker** - used to check a language against an automaton using 
multiple acceptance conditions
* **LanguageGenerator** - generates language samples from regular expressions
* **Plotter** - plots the results obtained from running a LanguageChecker

[Here](./doc/pl/README.md) is the modules' overview in polish.

## Citation

If you have used our library and and would like to cite its usage, we please use the following BibTeX entry. Thanks!

```
@article{lippa2020simulations,
  title={Simulations of Quantum Finite Automata.},
  author={Lippa, G and Makie{\l}a, K and Kuta, M},
  journal={Computational Science--ICCS 2020},
  volume={12142},
  pages={441--450},
  year={2020}
}
```
