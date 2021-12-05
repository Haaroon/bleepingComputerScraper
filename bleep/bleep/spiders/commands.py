import logging
logging.getLogger().setLevel(logging.WARNING);

# for each row in table
# for tr in response.xpath('//*[@id="forum_table"]/tr'):
#     if tr.xpath('td[2]//text()').extract()[0] == 'Topic':
#         continue
#     url = tr.xpath('td[2]//h4//a/@href').extract()[0].strip()
#     pag = len(tr.xpath('td[2]//ul//li'))
#     if pag != 0:
#         url = tr.xpath('td[2]//ul//li['+str(pag)+']//a[1]/@href').extract()[0]
#     print(url)