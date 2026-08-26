# decorators.py
from functools import wraps
from signnet.models.SignedNetwork import SignedNetwork

def require_edges(func):
    """Decorator ensuring that the provided SignedNetwork contains active structural elements (edges).
    
    Raises:
        ValueError: If the network contains zero edges.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        network = None
        
        if 'network' in kwargs:
            network = kwargs['network']
            for arg in args:
                if isinstance(arg, SignedNetwork):
                    network = arg
                    break

        if network is not None and network.number_of_edges == 0:
            raise ValueError(
                f"Execution blocked for '{func.__name__}': "
                f"The network topology contains no edges."
            )
            
        return func(*args, **kwargs)
    return wrapper
