import json
import timeit

from marshmallow import Schema, fields, post_load


def marshmallow_countries(s):

    class Country:
        def __init__(self, name, code):
            self.name = name
            self.code = code

    class CountrySchema(Schema):
        name = fields.String(required=True)
        code = fields.String(required=True)

        @post_load
        def make_object(self, data):
            return Country(data['name'], data['code'])

    schema = CountrySchema(many=True)
    data, error = schema.load(json.loads(s))
    assert len(data) == 243


def marshmallow_medium(s):

    class Offer:
        def __init__(
                self,
                partner_id=None,
                price=None,
                cancellation=None,
                room_type=None,
                meal_plan=None,
                deeplink=None):

            self.partner_id = partner_id
            self.price = price
            self.cancellation = cancellation
            self.room_type = room_type
            self.meal_plan = meal_plan
            self.deeplink = deeplink

    class OfferSchema(Schema):
        partner_id = fields.String()
        price = fields.Float()
        cancellation = fields.String()
        room_type = fields.List(fields.String)
        meal_plan = fields.String()
        deeplink = fields.String()

        @post_load
        def make_object(self, data):
            return Offer(**data)

    class Image:
        def __init__(
                self,
                url=None,
                provider=None):

            self.url = url
            self.provider = provider

    class ImageSchema(Schema):
        url = fields.String()
        provider = fields.Integer()

        @post_load
        def make_object(self, data):
            return Image(**data)

    class Hotel:
        def __init__(
                self,
                rating=None,
                distance=None,
                property_type=None,
                stars=None,
                district=None,
                city=None,
                coordinates=None,
                chain=None,
                amenities=None,
                relevance=None,
                name_en=None,
                hotel_id=None,
                name=None,
                images=None,
                offers=None):

            self.rating = rating
            self.distance = distance
            self.property_type = property_type
            self.stars = stars
            self.district = district
            self.city = city
            self.coordinates = coordinates
            self.chain = chain
            self.amenities = amenities
            self.offers = offers
            self.relevance = relevance
            self.name_en = name_en
            self.hotel_id = hotel_id
            self.name = name
            self.images = images

    class HotelSchema(Schema):
        rating = fields.Float()
        distance = fields.Float()
        property_type = fields.String()
        stars = fields.Float()
        district = fields.String()
        city = fields.String()
        coordinates = fields.List(fields.Float)
        amenities = fields.List(fields.String)
        images = fields.Nested(ImageSchema, many=True)
        offers = fields.Nested(OfferSchema, many=True)
        chain = fields.String(required=False, allow_none=True)
        hotel_id = fields.String()
        name = fields.String()

        @post_load
        def make_object(self, data):
            return Hotel(**data)

    class Partner:
        def __init__(
                self,
                website_id=None,
                image=None,
                official=None,
                name=None):

            self.website_id = website_id
            self.image = image
            self.official = official
            self.name = name

    class PartnerSchema(Schema):
        website_id = fields.String()
        image = fields.String()
        official = fields.Boolean()
        name = fields.String()

        @post_load
        def make_object(self, data):
            return Partner(**data)

    class ResultsSchema(Schema):
        partners = fields.Nested(PartnerSchema, many=True)
        hotels = fields.Nested(HotelSchema, many=True)

    schema = ResultsSchema()
    results, error = schema.load(json.loads(s)['results'])
    assert len(results['hotels']) == 30
    assert len(results['partners']) == 148


if __name__ == "__main__":
    with open('./benchmark/data/countries.json') as fd:
        s = fd.read()

    print("Testing with countries.json")
    print("---------------------------")
    print("JSON loads took: {}".format(
        timeit.timeit("json.loads(s)", number=1, setup="from __main__ import json, s")
    ))

    print("Marshmallow took loading countries to models: {}".format(
        timeit.timeit("marshmallow_countries(s)", number=1, setup="from __main__ import marshmallow_countries, s")
    ))

    print("")

    with open('./benchmark/data/medium.json') as fd:
        s = fd.read()

    print("Testing with medium.json")
    print("------------------------")
    print("JSON loads took: {}".format(
        timeit.timeit("json.loads(s)", number=1, setup="from __main__ import json, s")
    ))

    print("Marshmallow took loading medium to models: {}".format(
        timeit.timeit("marshmallow_medium(s)", number=1, setup="from __main__ import marshmallow_medium, s")
    ))
