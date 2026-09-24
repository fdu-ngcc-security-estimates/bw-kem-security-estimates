# BW-KEM Security Estimator

This repository contains tools for evaluating BW-KEM parameter sets. It estimates the cost of lattice attacks, communication sizes, and decryption-failure probabilities for the parameter sets defined in the project.

## Features

- Estimates primal and dual attacks against the underlying Module-LWE instance.
- Reports classical, quantum, and plausible SVP cost estimates.
- Computes public-key and ciphertext sizes.
- Evaluates an upper bound on the decryption-failure probability using a Chernoff bound.
- Includes standard and strengthened BW-KEM parameter sets.

## Requirements

- Python 3
- NumPy
- SciPy

Install the Python dependencies with:

```bash
python3 -m pip install numpy scipy
```

## Usage

Run the estimator from its source directory:

```bash
cd BW-KEM-security-estimator
python3 BWKEM.py
```

For each built-in parameter set, the script prints:

- the selected parameters;
- estimated primal and dual attack costs;
- key and ciphertext sizes; and
- an upper bound on the decryption-failure probability.

To evaluate a custom parameter set, create a `BWKEM_ParameterSet` in `BWKEM.py` and pass it to `summarize()`.

## Project Structure

```text
BW-KEM-security-estimator/
├── BWKEM.py          # Parameter sets and main entry point
├── BWKEM_failure.py  # Decryption-failure analysis
├── MLWE_security.py  # Primal and dual attack estimation
├── model_BKZ.py      # BKZ and SVP cost models
└── proba_util.py     # Probability-distribution utilities
```

## Acknowledgements

Parts of the security-estimation code are adapted from the [pq-crystals/security-estimates](https://github.com/pq-crystals/security-estimates) project.

---

# BW-KEM 安全性估算工具

本项目用于评估 BW-KEM 参数集，可计算格攻击成本、通信开销以及解密失败概率。

## 主要功能

- 估算底层 Module-LWE 实例所面临的 primal 和 dual 攻击成本；
- 给出经典、量子以及 plausible 三种 SVP 成本估算；
- 计算公钥和密文大小；
- 使用 Chernoff 界估算解密失败概率的上界；
- 提供标准参数集和增强参数集，可直接运行测试。

## 环境要求

- Python 3
- NumPy
- SciPy

可以使用以下命令安装依赖：

```bash
python3 -m pip install numpy scipy
```

## 使用方法

进入估算工具目录并运行主程序：

```bash
cd BW-KEM-security-estimator
python3 BWKEM.py
```

程序会依次测试内置参数集，并输出：

- 当前使用的参数；
- primal 和 dual 攻击的安全成本；
- 公钥及密文大小；
- 解密失败概率的上界。

如需测试自定义参数，可在 `BWKEM.py` 中创建 `BWKEM_ParameterSet`，然后将其传入 `summarize()`。

## 项目结构

```text
BW-KEM-security-estimator/
├── BWKEM.py          # 参数集定义和程序入口
├── BWKEM_failure.py  # 解密失败概率分析
├── MLWE_security.py  # Primal 和 dual 攻击估算
├── model_BKZ.py      # BKZ 与 SVP 成本模型
└── proba_util.py     # 概率分布工具函数
```

## 致谢

本项目的部分安全性估算代码基于 [pq-crystals/security-estimates](https://github.com/pq-crystals/security-estimates) 项目进行了适配。
