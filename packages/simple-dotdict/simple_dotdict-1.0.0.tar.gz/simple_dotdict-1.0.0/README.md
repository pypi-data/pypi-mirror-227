# Simple Dotdict

The `dotdict` class is a dictionary that allows access to its elements using dot notation. It inherits from the built-in `dict` class in Python.

## Installation

To install [`simple-dotdict`](https://pypi.org/project/dotdict/), you can use pip:

```bash
pip install simple-dotdict
```

## Usage

Here is an example of how to use the `dotdict` class:

```python
from simple_dotdict import dotdict

d = dotdict({'key': 'value'})
print(d.key)  # Outputs: value
```

You can also set and delete keys using dot notation:

```python
d.new_key = 'new_value'  # Sets a new key-value pair
print(d.new_key)  # Outputs: new_value
del d.new_key  # Deletes the key-value pair
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.# simple-dotdict
