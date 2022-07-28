# Liquidity Provision Delta Hedge
Includes emperical results and plots for paper on delta hedging LP positions.

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
│   └── v2_experiment_runner.py
└── utils
    └── image_creation.py
```