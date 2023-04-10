import scrapy

class ShowbagsSpider(scrapy.Spider):
    name = 'showbags'
    start_urls = [f'https://www.eastershow.com.au/explore/showbags/?page={page}' for page in range(1, 53)]

    def parse(self, response):
        # page = response.url.split("=")[-1]
        for showbag in response.css('div.showbagsCard-content'):
            name = showbag.css('h3.showbagsCard-product--name::text').get().strip()
            price = showbag.css('span.showbagsCard-product--price::text').get().strip()[1:]
            price = float(price.replace(',', ''))
            total_price_string = showbag.css('strong:contains("Total Retail Value:")::text').get()
            try:
                total_price = float(total_price_string.replace("Total Retail Value: $", "").strip())
            except (ValueError, AttributeError):
                continue
            distributor = showbag.css('div.showbagsCard-description-copy--distributor p::text').get()
            distributor_text = distributor.strip().split("The content of ")[0].strip() if distributor else None
            has_voucher = 'voucher' in showbag.get().lower() or 'discount offer' in showbag.get().lower()

            if total_price:
                result = {"name": name, "price": price, "total_price": total_price, "distributor": distributor_text, "has_voucher": has_voucher}
                yield result
