import pytest

from jmodel.model import Model
from jmodel.field import Integer, String
from jmodel.exception import Unknown


class TestModel:

    @pytest.fixture
    def payload(self):
        return """{"id": "1", "name": "foo"}"""

    def test_loads(self, payload):

        class Foo(Model):
            id = Integer()
            name = String()

        f = Foo.loads(payload)
        assert f.id == 1
        assert f.name == "foo"

    def test_unknown_field(self, payload):

        class Foo(Model):
            pass

        with pytest.assertRaises(Unkown):
            f = Foo.loads(payload)

    def test_allow_unknown_fields(self, payload):

        class Foo(Model):
            class Meta:
                unknown_fields = True

        f = Foo.loads(payload)
        assert f.id == 1
        assert f.name == "foo"

    def test_loads_many(self, payload):

        class Foo(Model):
            class Meta:
                unknown_fields = True

        foos = Foo.loads(
            """[%s,%s]""".format(payload, payload), 
            many=True
        )

        assert len(foos) == 2
        assert foos[0].id == 1
        assert foos[0].name == "foo"
        assert foos[1].id == 1
        assert foos[1].name == "foo"
