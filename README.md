# Hannibal Barca Optimizer (HBO)

> A population-based metaheuristic inspired by Hannibal’s **Pincer Movement** and an auxiliary **parallax learning** mechanism for robust global optimization.

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Language: MATLAB](https://img.shields.io/badge/Languages-MATLAB-blue.svg)]()
[![Language: Python](https://img.shields.io/badge/Language-Python-yellow.svg)]()
[![Benchmarks: CEC’22](https://img.shields.io/badge/Benchmarks-CEC'22-orange.svg)]()
[![Status: Active](https://img.shields.io/badge/Status-Active-success.svg)]()

HBO addresses difficult, high-dimensional, nonconvex problems by fusing:
1) **Pincer-envelopment search** (coordinated flanking of the search region),
2) **Parallax learning** (multi-view evaluation to stabilize moves and avoid premature convergence),
3) **Tripartite progression** (exploration → tactical tightening → decisive exploitation).

The algorithm has been assessed on **CEC’22** functions, **classical engineering designs**, and **image multi-thresholding** tasks, showing competitive performance against recent metaheuristics.

---

## Highlights

- **Exploration with intent**: directional encirclement maintains diversity while steering toward promising basins.
- **Parallax evaluations**: candidate solutions are tested under slight geometric/perturbation “views,” improving selection reliability.
- **Low parameter burden**: defaults work well; parameters remain interpretable.
- **Reproducible MATLAB reference**: self-contained implementation in `Matlab/`.


---

## Citation


@article{ouertani2025hannibal,
  title={Hannibal Barca optimizer: the power of the pincer movement for global optimization and multilevel image thresholding},
  author={Ouertani, Mohamed Wajdi and Manita, Ghaith and Korbaa, Ouajdi},
  journal={Cluster Computing},
  volume={28},
  number={7},
  pages={482},
  year={2025},
  publisher={Springer}
}





