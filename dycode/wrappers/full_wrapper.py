from dycode.wrappers.field_wrapper import dynamize_fields
from dycode.wrappers.method_wrapper import dynamize_methods
from ..functions import eval_function
import inspect

# TODO: check this later on

# Merge the signature of all the wrappers into one signature that acts upon the class

all_wrappers = [dynamize_fields, dynamize_methods]


def sigless_wrapper(cls, *args, **kwargs):
    ret_cls = cls
    for wrapper in all_wrappers:
        ret_cls = eval_function(wrapper, dynamic_args=True)(ret_cls, *args, **kwargs)
    return ret_cls


# merge the signature of the wrappers
sigless_wrapper.__signature__ = inspect.Signature.from_callable(all_wrappers[0])
for wrapper in all_wrappers[1:]:
    # get all the parameters until now
    params = list(sigless_wrapper.__signature__.parameters.values())

    # add in the new parameters
    new_sig = inspect.Signature.from_callable(wrapper)
    for item, value in new_sig.parameters.items():
        if value not in params:
            params.append(value)

    # assign a new signature which contains the new parameters and has the return annotation updated
    sigless_wrapper.__signature__ = inspect.Signature(
        params, return_annotation=new_sig.return_annotation
    )