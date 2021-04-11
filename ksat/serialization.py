import pickle


def serialize_args(*args, **kwargs):
    result = {"args": [], "kwargs": {}}
    for arg in args:
        result["args"].append(arg)

    for key, val in kwargs.items():
        result["kwargs"][key] = val

    return pickle.dumps(result)


def deserialize_args(serialized_args):
    container = pickle.loads(serialized_args)
    return container["args"], container["kwargs"]
