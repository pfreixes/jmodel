import pytest

from jmodel.model import Model
from jmodel.fields import Field
from jmodel.exceptions import DecodeError


@pytest.fixture
def foo_model():
    class Foo(Model):
        a = Field()
        b = Field()

    return Foo


class TestModel:

    @pytest.mark.xfail
    def test_loads(self):
        m = Model.loads("""{"a": 1}""")
        assert m.a == 1

    @pytest.mark.xfail
    def test_loads_many(self, foo_model):
        m1, m2 = Model.loads("""[{"a": 1}, {"a": 2}]""", many=True)
        assert m1.a == 1
        assert m2.b == 1

    @pytest.mark.parametrize("payload,kwargs", [
        (None, {}),
        ("", {}),
        ("!", {}),
        ("!", {"many": True}),
    ])
    def test_loads_invalid_payload(self, payload, kwargs):
        with pytest.raises(DecodeError):
            Model.loads(payload, **kwargs)

    def test_fields(self, foo_model):
        assert foo_model.fields() == {'a': foo_model.a, 'b': foo_model.b}
