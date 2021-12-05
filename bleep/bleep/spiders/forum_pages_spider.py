import scrapy
from datetime import datetime

class ForumPagesSpider(scrapy.Spider):
    name = "ForumPages"

    def start_requests(self):
        urls = [
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-2?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-3?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-4?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-5?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-6?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-7?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-8?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-9?sort_key=last_post&topicfilter=all',
            'https://www.bleepingcomputer.com/forums/f/239/ransomware-help-tech-support/page-10?sort_key=last_post&topicfilter=all',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for tr in response.xpath('//*[@id="forum_table"]/tr'):
            if tr.xpath('td[2]//text()').extract()[0] == 'Topic':
                continue
            url = tr.xpath('td[2]//h4//a/@href').extract()[0].strip()
            pag = len(tr.xpath('td[2]//ul//li'))
            if pag != 0:
                url = tr.xpath('td[2]//ul//li[' + str(pag) + ']//a[1]/@href').extract()[0]
            yield response.follow(url, callback=self.postPage)

    def postPage(self, response):
        # get the pages
        all_posts = response.xpath('//*[contains(@id, "post_id_")]')
        for post in all_posts:
            try:
                raw_content = post.xpath('.//div//div[@class="post_body"]//div[contains(@class, "post entry-content")]//p//text()').extract()
                cleaned_post = ''.join(raw_content).replace('\xa0', ' ').replace('\n', '')
                username = post.xpath('.//div//h3//span[contains(@class, "author")]//text()').extract()[0]
                time = post.xpath('.//div//div[@class="post_body"]//abbr[contains(@class, "published")]/@title').extract()[0]
                post_unqiue_id = post.xpath('./@id').extract()[0].split('_')[-1]
                thread_title  = post.xpath('.//div//h3//span//a/@title').extract()[0]
                source_url = response.url
                yield {
                    'post_content': cleaned_post,
                    'username': username,
                    'time': time,
                    'post_unique_id': post_unqiue_id,
                    'thread_title': thread_title,
                    'source_url': source_url,
                }
            except Exception as e:
                print("Error")
                print(e)
                continue
        # if more within time then push previous page
        if len(all_posts):
            post = all_posts[0]
            time = post.xpath('.//div//div[@class="post_body"]//abbr[contains(@class, "published")]/@title').extract()[0]
            date = datetime.strptime(time[:-6], "%Y-%m-%dT%H:%M:%S")
            if 'page-' in response.url and date >= datetime(2021, 6, 1, 0, 0, 0):
                # get next page
                prev_page = int(response.url.split("page-")[1]) - 1
                new_url = response.url.split("page-")[0]+'page-'+str(prev_page)
                if prev_page >= 1:
                    yield response.follow(new_url, callback=self.postPage)

