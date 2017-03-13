def hasmethod(obj, name):
    return (
        hasattr(obj, name) and
        callable(getattr(obj, name))
    )
