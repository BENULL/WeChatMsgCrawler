# [python]微信公众号文章爬取

## 需求

爬取一些微信公众号的文章

## 数据来源

1.搜狗微信搜索，可以搜索微信公众号文章，但只能显示该公众号最近十篇的文章

2.通过个人微信公众号中的素材管理，查看其他微信公众号文章


## 步骤

1.手动从网站上获取cookie通过cookie登陆

2.从请求url中获取token

3.拼接参数请求`https://mp.weixin.qq.com/cgi-bin/searchbiz`获取公众号的fakeid也就是biz

4.拼接参数请求`https://mp.weixin.qq.com/cgi-bin/appmsg`获取文章列表信息

5.通过文章url爬取文章

**通过这种方式是没办法得到阅读量和点赞数的，因为网页打开公众号文章是没有阅读数和点赞数的**
