from bs4 import BeautifulSoup
from urllib import request
from bs4.element import Tag
import pymysql

url = "http://gzjd.sipac.gov.cn/Web/BBS/MainList.aspx"
content = request.urlopen(url).read()
soup = BeautifulSoup(content, 'html5lib', from_encoding='GB2312')
# 根据id拿到table
table = soup.find(id="DataGrid1")
# 遍历tbody里面的tr
for tr in table.tbody.children:
    if (type(tr) == Tag):
        tds = tr.children
        td1 = next(tds)
        type_ = next(tds).string
        # 如果是第一行跳过
        if (type_ == "类 别"):
            continue
        status_ = next(tds).string
        if (status_ == None):
            status_ = "已回复"
        td_ = next(tds)
        href_ = td_.a["href"]
        href_ = "http://gzjd.sipac.gov.cn/Web/BBS/" + href_
        # content_=request.urlopen("http://gzjd.sipac.gov.cn/Web/BBS/"+href_).read()
        topic_ = td_.string
        date_ = next(tds).string
        click_ = next(tds).string
        deployment_ = next(tds).string
        # 存储到数据库
        try:
            conn = pymysql.connect(
                host='192.168.1.82', user='root', passwd='123456', db='bbs', charset='utf8')
            cur = conn.cursor()
            cur.execute('INSERT INTO bbs(type, status, topic,href, date, click, deployment)\
                            VALUES ("%s","%s","%s","%s","%s","%s","%s")'
                        % (
                            type_, status_, topic_, href_, date_, click_, deployment_
                        ))
            conn.commit()
        except Exception:
            print("MySQL Error")
