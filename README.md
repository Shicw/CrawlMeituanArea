### 获取各个城市的商圈数据
*需要使用如下URL:*

+ https://www.meituan.com/changecity/
+ https://apimobile.meituan.com/group/v1/area/search/
+ https://hz.meituan.com/meishi/

*第一个链接是美团网用于选择切换城市时的页面,get_city.py脚本运行后会从该页面爬取全部城市的name和href*

*第二个链接就是美团网用于城市搜索的API,后面跟上城市名即可获得该城市的简写字母*

*第三个链接是某城市美团美食频道页面,其html源码中包含了该城市所有区县下的商圈数据,该链接的获得方法有两种:*

1.从URL①中获得的href,拼接上 '/meishi/'

2.从URL②中获取城市简写字母,拼接上'.meituan.conm/meishi/'

<u>请求https://hz.meituan.com/meishi/时,需在请求头上加入User-Agent信息,否则会默认跳转到"北京美团网"页面</u>