from dataclasses import fields
from typing import Dict, Any

def validate_kwargs(cls, /, **kwargs) -> Dict:
        expected = [f.name for f in fields(cls)]        
        params = {k: kwargs[k] for k in kwargs if k in expected}
        
        return params

def save_init_kwargs(cls, /, **kwargs) -> Any:
    params = validate_kwargs(cls, **kwargs)
    
    return cls(**params)