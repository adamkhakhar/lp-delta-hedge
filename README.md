# Liquidity Provision Delta Hedge
Includes code to find options portfolio to Delta-Hedge both Uniswap v2 and Uniswap v3, emperical results, and plots. [INSERT PAPER URL].

# Getting Started
1. Update config in `/configs`. (`uniform_liquidity_config.json` for Uniswap v2 and `concentrated_liquidity_config.json` for Uniswap v3).
2. run `python3 src/v2_experiment_runner.py` for Uniswap v2 or `python3 src/v3_experiment_runner.py` for Uniswap v3.

## Codebase Structure
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