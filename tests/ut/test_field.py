from jmodel.field import Field


class TestField:

    def test_default_values(self):
        f = Field()
        assert f.required

    def test_not_required(self):
        f = Field(required=False)
        assert not f.required
