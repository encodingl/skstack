功能介绍
===============
That has a paragraph about a main subject and is set when the '='
is at least the same length of the title itself.

概述
----------------
Subtitles are set with '-' and are required to have the same length
of the subtitle itself, just like titles.


 

项目演示1
-------------
关键字标注

Words can have *emphasis in italics* or be **bold** and you can define
code samples with back quotes, like when you talk about a command: ``sudo``

代码段落空行分割且必须缩进"::"两个冒号开始
::

	from bs4 import BeautifulSoup
	    import scrapy
	
	
	    class ExampleSpider(scrapy.Spider):
	        name = "example"
	        allowed_domains = ["example.com"]
	        start_urls = (
	            'http://www.example.com/',
	        )
	
	        def parse(self, response):
	            # use lxml to get decent HTML parsing speed
	            soup = BeautifulSoup(response.text, 'lxml')
	            yield {
	                "url": response.url,
	                "title": soup.h1.string
	            }

项目演示2
-------------
图片

.. image:: _static/demo.png
   :width: 700
   :height: 470
   :alt: Scrapy architecture
   
提示


