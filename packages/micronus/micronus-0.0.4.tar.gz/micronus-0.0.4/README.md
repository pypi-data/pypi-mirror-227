# Micronus
![example workflow](https://github.com/hastur66/Micronus/actions/workflows/pytest.yml/badge.svg)
[![codecov](https://codecov.io/gh/hastur66/Micronus/branch/master/graph/badge.svg?token=3YXM0OAJCG)](https://codecov.io/gh/hastur66/Micronus)

A light-weight transformer model.

#### Install
```
pip install micronus
```

#### Train
exampel
```
python -m micronus.train --dataset data/english-german-both.pkl 
```

#### Inference
example
```
python -m micronus.inference --sentence "Hello world!"
```