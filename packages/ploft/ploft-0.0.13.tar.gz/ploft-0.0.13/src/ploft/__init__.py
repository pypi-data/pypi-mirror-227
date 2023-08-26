import pkg_resources

#from pkg_resources import resource_stream


import sys
if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

data_path = pkg_resources.resource_filename('ploft', 'jsc/main2.js')

f = importlib_resources.files('ploft')



__all__ = ["__version__"]
