[![Build Status](https://travis-ci.org/cbrown1/spyral.svg?branch=master)](https://travis-ci.org/cbrown1/spyral)

# spyral

A Python implementation of the Spiral vocoder

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

## Authors

### Original spiral matlab code

- **Jacques Grange**

- **John Culling**

### Python port

- **Christopher Brown**

- **Kutay Sezginel**

## License

This project is licensed under the GPLv3 - see the [LICENSE.md](LICENSE.md) file for details.
