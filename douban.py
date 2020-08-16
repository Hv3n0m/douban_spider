from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3

#1.爬取网页
#2.逐一解析数据
#3.保持数据


findLink = re.compile(r'<a href="(.*?)">')  # 电影超链接
findImg = re.compile(r'<img.*src="(.*?)"')  # 电影图片
findTitle = re.compile(r'<span class="title">(.*?)</span>') # 电影标题
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')   # 电影评分
findJudge = re.compile(r'<span>(\d*)人评价</span>')  # 电影概述
findInq = re.compile(r'<span class="inq">(.*?)</span>')  # 电影评价
findBd = re.compile(r'<p class="">(.*?)</p>',re.S) # 电影相关内容 re.S 可以包含换行


def main():
    baseurl = 'https://movie.douban.com/top250?start='
    #baseurl = 'https://www.baidu.com'
    datalist = getDate(baseurl)
    savepath = '豆瓣Top250.xls'
    dbpath = 'movie250.db'
    #saveDate(datalist,savepath) # 保存在表格中
    saveData2DB(datalist,dbpath)


def getDate(baseurl):
    datalist = []
    for i in range(0,10):
        url = baseurl + str(i*25)
        html = askURL(url)

        soup = BeautifulSoup(html,"html.parser")
        for item in soup.find_all('div',class_="item"):
            data = [] # 保存一部电影的所有信息
            item =str(item)
            
            link = re.findall(findLink,item)[0]
            data.append(link)
            imgSrc = re.findall(findImg,item)[0]
            data.append(imgSrc)
            titles = re.findall(findTitle,item)
            if len(titles) == 2:
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(' ')
            rating = re.findall(findRating,item)[0]
            data.append(rating)
            judeNum = re.findall(findJudge,item)[0]
            data.append(judeNum)
            inq = re.findall(findInq,item)
            if len(inq) !=0:
                inq = inq[0].replace('。','')
                data.append(inq)
            else:
                data.append(' ')
            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/(\s+)?'," ",bd)
            bd = re.sub('/'," ", bd)
            data.append(bd.strip())

            datalist.append(data) # 把信息放入datalist中
    return datalist
          

#获取指定网站的网页内容
def askURL(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
}
    request = urllib.request.Request(url=url,headers=headers)
    html =''
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def saveDate(datalist,savepath):
    book = xlwt.Workbook(encoding="utf-8",style_compression=0)
    sheet = book.add_sheet('豆瓣Top250', cell_overwrite_ok=True)
    col = ("电影连接", "图片连接", "影片中文名", "影片外文名", "评分", "评价数", "概述", "相关信息")
    for i in range(0,8):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalist[i]
        for j in range(0,8):
            sheet.write(i+1,j,data[j])
    book.save('sss.xls')

def init_db(dbpath):
    sql = '''
        create table movie250
        (
            id integer primary key autoincrement,
            info_link text,
            pic_link text,
            cname varchar,
            ename varchar,
            score numeric,
            rated numeric,
            instroduction text,
            info text
        )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

def saveData2DB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250(info_link,pic_link,cname,ename,score,rated,instroduction,info)
            values(%s)''' % ",".join(data)
        print(sql)
        cursor.execute(sql)
        conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    #askURL()
    #init_db('movie250.db')
    main()