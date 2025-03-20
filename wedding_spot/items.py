import scrapy

class VenueItem(scrapy.Item):
    # Define the fields for your item
    url = scrapy.Field()
    venue_name = scrapy.Field()
    phone = scrapy.Field()
    venue_highlights = scrapy.Field()
    guest_capacity = scrapy.Field()  # Only the numeric part
    address = scrapy.Field()

    # Specify the order of fields
    fields = {
        'url': {'order': 1},
        'venue_name': {'order': 2},
        'phone': {'order': 3},
        'venue_highlights': {'order': 4},
        'guest_capacity': {'order': 5},
        'address': {'order': 6},
    }