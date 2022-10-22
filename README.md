# Liquidity Provision Delta Hedge Via Options
Includes code to find an options portfolio to delta hedge both Uniswap v2 and Uniswap v3, emperical results, and plots. [Paper](https://arxiv.org/abs/2208.03318).

Adam Khakhar and Xi Chen. 2022. Delta Hedging Liquidity Positions on Automated Market Makers. [https://arxiv.org/abs/2208.03318](https://arxiv.org/abs/2208.03318).

![Poster](results/Delta_Hedging_Liquidity_Positions_Poster.png)

If you use this code/research, please cite:
```
@misc{https://doi.org/10.48550/arxiv.2208.03318,
  doi = {10.48550/ARXIV.2208.03318},
  
  url = {https://arxiv.org/abs/2208.03318},
  
  author = {Khakhar, Adam and Chen, Xi},
  
  keywords = {Computational Engineering, Finance, and Science (cs.CE), Machine Learning (cs.LG), Trading and Market Microstructure (q-fin.TR), FOS: Computer and information sciences, FOS: Computer and information sciences, FOS: Economics and business, FOS: Economics and business, F.m},
  
  title = {Delta Hedging Liquidity Positions on Automated Market Makers},
  
  publisher = {arXiv},
  
  year = {2022},
  
  copyright = {arXiv.org perpetual, non-exclusive license}
}
```

# Getting Started
1. Update config in `/configs`. (`uniform_liquidity_config.json` for Uniswap v2 and `concentrated_liquidity_config.json` for Uniswap v3).
2. Run `python3 src/v2_experiment_runner.py` for Uniswap v2 or `python3 src/v3_experiment_runner.py` for Uniswap v3.

# Codebase Structure
```
.
├── LICENSE
├── README.md
├── configs
│   ├── concentrated_liquidity_config.json
│   └── uniform_liquidity_config.json
├── results
│   ├── IL.png
│   ├── LPPNL.png
│   ├── concentrated_liquidity.png
│   ├── experiment_v2_lppnl.png
│   ├── experiment_v2_options_target_pnl.png
│   ├── pool_assets_v3.png
│   └── uniform_liquidity.png
├── src
│   ├── delta_hedge
│   │   ├── AlgorithmicDataSet.py
│   │   ├── Derivative.py
│   │   ├── OptimizationRunner.py
│   │   ├── OptionsOptimizer.py
│   │   └── Train.py
│   ├── deribit
│   │   └── retrieve_instruments.py
│   ├── image_creation
│   │   └── plot_runner.py
│   ├── v2_experiment_runner.py
│   └── v3_experiment_runner.py
└── utils
    └── image_creation.py
```
