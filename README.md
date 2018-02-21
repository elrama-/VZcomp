# VZcomp [![Build Status](https://travis-ci.org/elrama-/VZcomp.svg?branch=master)](https://travis-ci.org/elrama-/VZcomp) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/f0392f5ac26d440bb7329a3bbc52f3a4)](https://www.codacy.com/app/elrama-/VZcomp?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=elrama-/VZcomp&amp;utm_campaign=Badge_Grade)
[![Coverage Status](https://coveralls.io/repos/github/elrama-/VZcomp/badge.svg?branch=master)](https://coveralls.io/github/elrama-/VZcomp?branch=master)
Quantu compiler based on Virtual-Z gates technique

This software is licensed under the MIT License. See LICENSE.txt for full disclaimer.


## Installation

Since the code is still under development, installation is done in developer mode. To do so, clone this repository and (in its root) run:

```python
pip install -e .
```

## Usage

The compiler is command-line-based. It can be called by:

```
python VZcomp\compiler.py path_to_qasm\qasm_file_exclude_extension
```

## About the compiler
This compiler is based on the phase-update+euler-decomposition technique described in https://arxiv.org/abs/1612.00858.

The compilation flow is composed of 4 steps:
0. Raw code.
1. Structured code.
2. code in terms of SU2 rotations.
3. code in terms of euler angles.
4. code in terms of XY rotations.

## Improvements to go:
1. Between steps 3 and 4, a flag should allow to only use pi/2 gates. KNOWN TO WORK
2. Between steps 3 and 4, we could use another euler angles step to ONLY use x' or y' angles(see PR for this). NOT SURE WHETHER IT WORKS.
