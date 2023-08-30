class dotdict(dict):
    """
    Dot.notation access to dictionary elements

    This class allows dictionary attributes to be accessed using dot notation.
    It inherits from the built-in dict class.

    Example:
    d = dotdict({'key': 'value'})
    print(d.key)  # Outputs: value
    """

    # This method is used to access the value of a dictionary key using dot notation.
    __getattr__ = dict.get

    # This method is used to set the value of a dictionary key using dot notation.
    __setattr__ = dict.__setitem__

    # This method is used to delete a dictionary key using dot notation.
    __delattr__ = dict.__delitem__
