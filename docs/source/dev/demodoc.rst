文档编写示例
===============
That has a paragraph about a main subject and is set when the '='
is at least the same length of the title itself.

序号和超链接
----------------
Subtitles are set with '-' and are required to have the same length
of the subtitle itself, just like titles.

序号
~~~~~~~~~~~~~~~~~~~~~~
点号list:

 * Item Foo
 * Item Bar

序号list:

 #. Item 1
 #. Item 2
 
超链接
~~~~~~~~~~~~~~~~~~~~~~
语法`链接文字 <URL>`_

`spninx语法参考:  <https://www.cnblogs.com/zzqcn/p/5096876.html>`_
 

关键字和代码段落
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

图片和提示
-------------
图片

.. image:: _static/demo.png
   :width: 700
   :height: 470
   :alt: Scrapy architecture
   
提示


