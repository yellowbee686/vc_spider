# -*- coding: utf-8 -*-
import scrapy
import xlwt

class VCSpider(scrapy.Spider):
    name = "vcspider"

    def init_xl(self):
        self.xl_file = xlwt.Workbook()
        self.xl_table = self.xl_file.add_sheet('data')
        self.column_index = 0
        self.xl_file_name = 'data.xls'
        self.xl_file.save(self.xl_file_name)

    def start_requests(self):
        url = 'https://m.weiclicai.com/announcement-info/'
        start_page = getattr(self, 'start', 500)
        end_page = getattr(self, 'end', 959)
        self.init_xl()
        #print('start_page=%d end_page=%d'%(start_page, end_page))
        for i in range(start_page, end_page):
            complete_url = url + str(i)
            #print('parse_url=%s', url)
            yield scrapy.Request(complete_url, self.parse)


    def parse(self, response):
        # vc的网页中使用br来分隔每一行，这里extract返回一个list，每一项都是网页文本中的一行，同时接口中已经事先去除了空行
        # 由于逻辑需要，两行两行是一个整体
        contents = response.css('div.cont::text').extract()
        first = None
        for one_content in contents:
            if str.find(one_content, '第M') != -1:
                first = str.strip(one_content)
            elif str.find(one_content, '%') != -1:
                # 如果能配成一对 则log出来
                if first!=None:
                    #print('first=%s second=%s'%(first, one_content))
                    self.xl_table.write(self.column_index, 0, first)
                    self.xl_table.write(self.column_index, 1, one_content)
                    self.column_index = self.column_index + 1
                    first = None

        self.xl_file.save(self.xl_file_name)