# spyral

An implementation of the Spiral vocoder in Python

Read a paper on Spiral here: https://doi.org/10.1121/1.5009602

## Installing

### Download:

```bash
git clone https://github.com/cbrown1/spyral.git
```

### Compile and install:

```bash
python setup.py build
sudo python setup.py install
```

## Usage
```python
n_electrodes = 20
n_carriers = 80
spread = -8
vocoded = spyral(input, fs, n_electrodes, n_carriers, spread)
```
