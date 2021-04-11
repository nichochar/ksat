from ksat import serialization


TEST_CASES = [
    # (args, kwargs)
    ([1, 2, "a string"],{"key1": True, "key2": 2}),
    ([1], {}),
    ([], {"key1": True, "key2": 2}),
]


def test_serialize_and_deserialize():
    for (args, kwargs) in TEST_CASES:
        pickled_string = serialization.serialize_args(*args, **kwargs)
        result_args, result_kwargs = serialization.deserialize_args(pickled_string)

        assert result_args == args
        assert result_kwargs == kwargs
