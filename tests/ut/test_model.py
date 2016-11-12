import pytest

from jmodel.model import Model
from jmodel.field import Field


@pytest.fixture
def foo_model():
    class Foo(Model):
        a = Field()
        b = Field()

    return Foo


class TestModel:

    def test_fields(self, foo_model):
        assert foo_model.fields() == {'a': foo_model.a, 'b': foo_model.b}
