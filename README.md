# Liquidity Provision Delta Hedge
Includes emperical results and plots for paper on delta hedging LP positions.

## Codebase Structure
```
.
├── LICENSE
├── README.md
├── configs
│   └── config.json
├── results
│   ├── IL.png
│   ├── LPPNL.png
│   ├── concentrated_liquidity.png
│   ├── pool_assets_v3.png
│   └── uniform_liquidity.png
├── src
│   ├── delta_hedge
│   │   └── Derivative.py
│   ├── deribit
│   │   └── retrieve_instruments.py
│   └── images
│       └── plot_runner.py
└── utils
    └── image_creation.py
```