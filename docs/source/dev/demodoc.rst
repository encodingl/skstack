文档编写说明和示例
==============================

概述
----------------

 #. 文档使用sphinx生成，采用reStructuredText标记语言
 #. 开发人员，新增文档，请才有已有文档结构和文档工具书写
 #. `文档实例参考  <https://readthedocs.org/>`_
 #. `restructuredtext语法参考  <https://3vshej.cn/rstSyntax/index.html>`_
 #. `sphinx官方文档参考  <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_


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

`语法参考:  <https://3vshej.cn/rstSyntax/index.html>`_
 

关键字和代码段落
--------------------------

关键字标注

Words can have *emphasis in italics* or be **bold** and you can define
code samples with back quotes, like when you talk about a command: ``sudo``

代码段落空行分割且必须缩进"::"两个冒号开始

.. code-block:: python

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

.. image:: _images/demo.png
   :width: 700
   :height: 470
   :alt: image not found
   
提示

.. note::
	这是一个注意提示
..

.. warning::
	这是一个告警提示
..


