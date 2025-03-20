import scrapy
import re
from urllib.parse import urlparse, parse_qs, urlencode
from wedding_spot.items import VenueItem  # Import the VenueItem


class VenuesSpider(scrapy.Spider):
    name = "venues"
    allowed_domains = ["www.wedding-spot.com"]
    start_urls = [
        "https://www.wedding-spot.com/wedding-venues/?pr=new%20jersey&r=new%20jersey%3anorth%20jersey&r=new%20jersey%3aatlantic%20city&r=new%20jersey%3ajersey%20shore&r=new%20jersey%3asouth%20jersey&r=new%20jersey%3acentral%20jersey&r=new%20york%3along%20island&r=new%20york%3amanhattan&r=new%20york%3abrooklyn&r=pennsylvania%3aphiladelphia&sr=1"
    ]


    page_count = 0

    def parse(self, response):
        self.logger.info(f"Scraping listing page: {response.url}")
        self.page_count += 1  
        self.logger.info(f"Scraped {self.page_count} pages so far.")

        venue_cards = response.css('div.venueCard--wrapper')
        for card in venue_cards:
            relative_url = card.css('a::attr(href)').get()
            if relative_url:
                yield response.follow(relative_url, callback=self.parse_venue)

        current_page_button = response.css('button[aria-current="true"]')
        if current_page_button:
            current_page = current_page_button.css('::text').get(default='1').strip()
            try:
                current_page = int(current_page)
            except ValueError:
                current_page = 1
                
            next_page_button = response.css('button[aria-label="Next Page"]:not([disabled])')
            if next_page_button:
                
                next_page = current_page + 1
                parsed_url = urlparse(response.url)
                query_params = parse_qs(parsed_url.query)
                query_params['page'] = [str(next_page)]
                next_page_url = parsed_url._replace(query=urlencode(query_params, doseq=True)).geturl()

                self.logger.info(f"Moving to next page: {next_page_url}")
                yield response.follow(next_page_url, callback=self.parse)

    def parse_venue(self, response):
        self.logger.info(f"Scraping venue detail page: {response.url}")

        item = VenueItem()

        seen = set()  
        venue_highlights = []
        for highlight in response.css('div.VenueHighlights--highlight div.VenueHighlights--label::text').getall():
            if highlight not in seen:  
                venue_highlights.append(highlight)
                seen.add(highlight)
        item['venue_highlights'] = ', '.join(venue_highlights)  

        details = {}
        for detail in response.css('div.VenuePage--detail'):
            headline = detail.css('h3.VenuePage--detail-headline::text').get(default='').strip()
            description = detail.css('p.VenuePage--detail-description::text').get(default='').strip()
            if headline and description:
                details[headline] = description

        guest_capacity = details.get('Guest capacity:', '')
        if guest_capacity:
            guest_capacity = re.search(r'\d+', guest_capacity) 
            guest_capacity = guest_capacity.group(0) if guest_capacity else ''  
        item['guest_capacity'] = guest_capacity

        item['url'] = response.url
        item['venue_name'] = response.css('h1.SecondaryCTA--venueName::text').get(default='').strip()
        
        phone = response.css('span.SecondaryCTA--hidden::text').get(default='').strip()
        if phone:
            phone = phone.replace('-', '')  # Remove hyphens
        item['phone'] = phone
        
        item['address'] = details.get('Location:', '')

        yield item