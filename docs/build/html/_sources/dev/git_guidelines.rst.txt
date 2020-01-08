Git开发和版本管理指南
==============================

分支使用说明
--------------------------------

功能分支工作流包含分支： feature,master, hotfix

:feature分支:
	当有需求需要开发时，可以从master分支创建一个feature分支，在feature分支做开发测试，测试通过后可以结束feature开发分支，feature分支会被合并回master分支，并创建tag；

:master分支:
	master保存所有版本的信息，预发布和生产环境使用master分支tag发布。
	用来做hotfix分支和feature分支的创建。

:hotfix分支:
	如果线上版本出现问题，可以从master的tag创建hotfix分支做修复测试，然后部署，发布完成后，结束hotfix分支，合并回master分支。非紧急bug修复，可在feature分支处理



:分支命名规范:

 * 命名规范：分支类型.创建日期.自定义标注
 * 示例：feature.20191030.dashboad  hotfix.20191030.dashboad1



版本管理
--------------------------------

版本管理基于tag号版本命名：由tag号保证唯一性。具体规范如下：

命名规范：v发布日期年月.阶段版本号.修正版本号：示例1：v201910.alpha.01   示例2：v201910.release

* 发布日期年月：为版本正式发布日期，精确到月份
* 阶段版本号定义参考:alpha beta rc release/stable

	  #. alpha：内部测试版
	  #. beta：公开测试版
	  #. rc：Release Candidate（候选版本）
	  #. stable/release：稳定版。
	  
* 修正版本号：当月第一次发布为01 第二次发布为02 以此类推，主要用于bug修复 





