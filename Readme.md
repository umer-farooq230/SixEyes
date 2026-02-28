# Volatility Regime Detection Library

## Overview

This library is designed to help analyze financial time series by answering a core question:

> **“Given historical returns, what volatility regime are we in right now?”**

It focuses on **volatility state detection** using multiple volatility measures and unsupervised models, with a clean separation between computation and modeling layers.

---

## Project Structure

The project is structured into modular components to ensure clarity, extensibility, and maintainability:

├── Volatility/ # Volatility feature computation
├── RegimeModel/ # Unsupervised regime detection models


### Volatility/

Contains implementations of various volatility estimators:

- Rolling / realized volatility  
- EWMA volatility  
- Range-based volatility (planned)  
- Downside / asymmetric volatility (planned)  

### RegimeModel/

Contains unsupervised models for detecting latent volatility regimes:

- Hidden Markov Models (HMM)  
- Clustering-based approaches  
- Configurable number of regimes  

---

## Current Progress (Release 0.1)

### Implemented

- ✅ Rolling standard deviation (stateless)  
- ✅ EWMA volatility with span / alpha support  
- ✅ Structured modular project layout  

### Design Principles

- Clear separation between **feature computation** and **regime modeling**  
- Extensible architecture  
- Clean and simple interfaces  
- Model-agnostic feature pipeline  

---

## Features Planned for Release 1

### Volatility Feature Extraction

- Realized volatility (rolling standard deviation)  
- EWMA volatility (span / half-life support)  
- Range-based volatility:
  - Parkinson estimator  
  - Garman–Klass estimator  
- Downside / asymmetric volatility measures  

### Regime Detection

- HMM-based volatility state modeling  
- Clustering-based regime detection  
- Configurable number of volatility regimes  
- Standardized model interface  

### Pipeline

- Integrated feature extractor + regime model  
- Clean input / output structure  
- Unified API for:
  - `fit()`  
  - `predict()`  
  - `transform()`  
  - Regime probability outputs  

---

## Future Enhancements

### Forecasting

- GARCH-based forecasting  
- Regime-conditioned volatility prediction  

### Stress Testing & Simulation

- Volatility scenario simulation  
- Regime-switching stress testing tools  

### Diagnostics

- Regime entropy  
- Persistence metrics  
- Stability analysis  

### Advanced Capabilities

- Streaming support for high-frequency data  
- Integration with financial data sources:
  - OHLC data  
  - Returns  
  - Cryptocurrency data  
  - Other asset classes  

---

## Vision

This library aims to become a lightweight but extensible framework for:

- Volatility analytics  
- Regime detection  
- Risk modeling research  
- Quantitative finance experimentation  

---

## Status

🚧 Active development  
📦 Current Version: `0.1`  
🎯 Target: Robust volatility regime detection framework  

---

## Contributing

Contributions, suggestions, and discussions are welcome.  
Please open an issue or submit a pull request.

---

## License

_To be determined._