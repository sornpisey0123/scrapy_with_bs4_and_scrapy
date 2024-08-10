import scrapy

class ProductSpider(scrapy.Spider):
    name = 'goldone_product_spider'
    allowed_domains = ['goldonecomputer.com']
    start_urls = ['https://www.goldonecomputer.com']

    def parse(self, response):
        # Scrape all category links
        category_links = response.css('ul.dropmenu li a::attr(href)').getall()
        for link in category_links:
            yield response.follow(link, self.parse_category)

    def parse_category(self, response):
        # Scrape product links in the category
        product_links = response.css('div.product-thumb a::attr(href)').getall()
        for product_link in product_links:
            yield response.follow(product_link, self.parse_product)

        # Follow pagination links if available
        next_page = response.css('ul.pagination li.next a::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse_category)

    def parse_product(self, response):
        # Extract product details
        product_name = response.css('h3.product-title::text').get(default='Unknown Product').strip()
        final_price = response.css('ul.price h3.special-price::text').get(default='Unknown Price').strip()
        old_price = response.css('ul.price span.price-old::text').get(default='').strip()
        brand = response.css('ul.list-unstyled li:nth-of-type(1) a::text').get(default='Unknown Brand').strip()
        product_code = response.css('ul.list-unstyled li:nth-of-type(2)::text').get(default='Unknown Code').strip()
        image = response.css('div.image img::attr(src)').get(default='No Image').strip()
        review_count = response.css('a.review-count::text').get(default='0').strip()

        # Extract category and its link if available
        category = response.css('ul.breadcrumb li:nth-last-child(2) a::text').get(default='Unknown Category').strip()
        category_link = response.css('ul.breadcrumb li:nth-last-child(2) a::attr(href)').get(default='').strip()

        # Ensure final price is not 'Unknown Price' and category is not 'Unknown Category'
        if final_price and final_price != 'Unknown Price' and category != 'Unknown Category':
            yield {
                'category': {
                    'name': category,
                    'link': response.urljoin(category_link)
                },
                'product': {
                    'Product Name': product_name,
                    'Final Price': final_price,
                    'Old Price': old_price,
                    'Brand': brand,
                    'Product Code': product_code,
                    'Image': response.urljoin(image),
                    'Review Count': review_count
                }
            }
