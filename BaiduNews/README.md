
## 爬新闻：
采用第一个函数```crawl()```
返回4个列表

|列表|内容|
|---|:---|
|instant_news_list|即时新闻|
|focal_news_list|焦点新闻|
|hot_news_list|热点新闻|
|latest_news_list|最新新闻|

这里我在爬的时候，**最新新闻**是包含**即时新闻**的，考虑到我们的需求，我在**最新新闻**里，通过筛选时间，把在今天发生的放在**即时新闻**里；

返回的所有```list```的元素都是一个```tuple```,包含url和新闻标题

---

## 提取热搜词：
采用第二个函数```get_keywords()```
返回值为6个中文热搜词的列表

从所有标题组成的字符串里提取
考虑到一些停用词，或者一些类似‘中国’等tf-idf值比较低的词，词频又较高，不合适作为热搜词，所以该函数直接调用了```jieba.analyse.extract_tags()```，再通过处理一些格式，得到tf-idf值最高的6个词


---

## 第二个任务：

感觉要把每个功能都封装进具体的函数，这样思路比较直接

### 基本任务：
- 先定义一个通用函数，传入url就下载网页内容`crawl(url)`,返回一个**Beautifulsoup**的`soup`对象
- 默认`parse(soup)`是用来解析直接查询词语返回的网页
- 按照需求还需要有一个解析相同新闻的网页，如果结构相同的话，就不需要重新写一个`parse`函数了
- 搜索，通过`search(query_word)`来实现，这个函数构造一个url，然后传给`crawl(url)`就好了

### 懒加载：
先呈现第一个页面的，总共要爬10页，这样其实第2到10页也是链接，我只要把链接传到`crawl(url)`就好了，解析应该还是用`parse`函数，这样的思路就比较清晰了。

每次返回的新闻列表中，每一条也是一个`list`
内容也在注释里写清楚了~

|index|内容|含义|
|---|:---|:---|
|0|title |新闻标题|
|1|title_url |新闻链接|
|2|source_and_time |作者/时间|
|3|summary |摘要|
|4|simi_words |相同新闻|
|5|simi_words_url |相同新闻查询的url|

具体测试在test.ipynb里
接口算是提供完善了，但是后台的逻辑组织需要你加油了~~


## 4/21 更新

更新了`spider_1.py`的`parse()`
修复了有些新闻内容不全导致的索引缺失问题

## 4/22 更新

更新了时间筛选函数`date_filter(begin_date, end_date, query_word)`
参数是起始日期和返回日期的str格式，和下表定义的格式相同，关键字
返回一个请求的get请求的url

还是调用百度的接口再封装
主要工作是解析get参数，然后自己构造参数

|参数|含义|
|---|:---|
|bt|(begin_time)起始日期）0：0：0的unix时间戳|
|et|(end_time)结束日期）23：59：59的unix时间戳|
|y0,m0,d0|起始日期的年，月，日|
|y1,m1,d1|结束日期的年，月，日|
|begin_time|起始日期的字符串形式，example:'2017-4-22'|
|end_time|结束日期的字符串形式|
|query_word|查询关键字|


- 其他参数照抄
- 这些参数在构造请求url的时候要转换成`str`形式
- `query_word`需要用`urllib.qoute()`处理一下
```python
import datetime
from urllib import quote
def date_filter(begin_date, end_date, query_word):
    date0 = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    date1 = datetime.datetime.strptime(end_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
    y0, m0, d0 = str(date0.year), str(date0.month), str(date0.day)
    y1, m1, d1 = str(date1.year), str(date1.month), str(date1.day)
    query_word = quote(query_word)
    bt = str(int(time.mktime(date0.timetuple())))
    et = str(int(time.mktime(date1.timetuple())))
    url = 'http://news.baidu.com/ns?from=news&cl=2&bt='+ bt + '&y0='+ y0 +'&m0=' + m0 + '&d0=' + d0 + '&y1=' + y1 + '&m1=' + m1 + '&d1=' + d1 + '&et=' + et + '&q1=' + query_word + '&submit=%B0%D9%B6%C8%D2%BB%CF%C2&q3=&q4=&mt=0&lm=&s=2&begin_date=' + begin_date + '&end_date=' + end_date + '&tn=newsdy&ct1=1&ct=1'
    return url
```

## 4/23 更新

增加分页
首先简单分析了一下url的参数：

- `pn`是起始的新闻条目的index
- `rn`是每页显示的新闻条目的index

如果是简单的search,那么重新构造url很简单
但是新实现的date_filter，我测试了一下，也是可以用这两个参数构造的

这样我就需要想一个统一的url构造规则

如果这样的话，`search`函数生成一个url,同样`date_filter`也是生成一个url
我可以定义一个`page_filter`函数来统一处理这些url
默认每页显示20条

这样的话，所有的请求url构造都要经过这一个`page_filter`函数了。
我把`page`默认设置为0,然后`rn`设置为20

```python
def page_filter(url, page=0):# append url with pn and rn params
    # rn are set to be 20
    rn = 20
    pn = page * rn
    rn = str(rn)
    pn = str(pn)
    url = url + '&pn=' + pn
    url = url + '&rn=' + rn
    return url
```

考虑一个异常：最后一页，应该不用管，因为总归是遍历的

这样，原来的`search`函数需要改变为只返回url：
```python
def search(query_word):
    word = urllib.quote(query_word)
    url  = 'http://news.baidu.com/ns?cl=2&tn=news&word=' + word
    return url
```

然后做一个高一点的封装：

```
def search_with_page(query_word, page=0):
    url = search(query_word)
    url = page_filter(url, page)
    return url

def date_filter_with_page(begin_date, end_date, query_word, page=0):
    url = date_filter(begin_date, end_date, query_word)
    url = page_filter(url, page)
    return url
```
测试可以这样
```
print search_with_page('军民融合', 3)
print 
print date_filter_with_page('2017-1-1', '2017-1-2', '军民融合', 2)
```

`parse`的架构也变得简单点，删去`is_homepage`参数

有点乱，现在理一下各个函数的功能，低耦合

构造请求url:
- `search_with_page(query_word, page=0)`
- `date_filter_with_page(begin_date, end_date, query_word, page=0)`
爬url:
- `crawl(url)`
解析生成新闻list
- `parse(soup)`




