import requests
from bs4 import BeautifulSoup as beaf
import random
import time
def get_zlzp(keyword,cot=1,salaryl=None,salaryh=None,city='全国'):
    city_dct = {'全国': '489', '北京': '530', '上海': '538', '深圳': '765', '广州': '763', '天津': '531', '成都': '801', '杭州': '653',
                '武汉': '736', '大连': '600', '长春': '613', '南京': '635', '济南': '702', '青岛': '703', '苏州': '639', '沈阳': '599',
                '西安': '854', '郑州': '719', '长沙': '749', '重庆': '551', '哈尔滨': '622', '无锡': '636', '宁波': '654', '福州': '681',
                '厦门': '682', '石家庄': '565', '合肥': '664', '惠州': '773'}

    header = {
        'Host': 'fe-api.zhaopin.com',
        'Origin': 'https://sou.zhaopin.com',
        'Referer': 'https://sou.zhaopin.com/?p=4&jl=489&in=10100&kw=%E9%BB%91%E7%9B%92%E6%B5%8B%E8%AF%95&kt=3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER'
    }
    cot=int(cot)
    if salaryl==None or salaryh==None:
        url='https://fe-api.zhaopin.com/c/i/sou?start={num}&pageSize=60&cityId={city1}&industry=10100&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={name1}&kt=3&lastUrlQuery=%7B%22p%22:{p1},%22jl%22:%22{city2}%22,%22in%22:%2210100%22,%22kw%22:{name2},%22kt%22:%223%22%7D'.\
            format(name1=keyword,name2=keyword,p1=cot,num=60*(cot-1),city1=city_dct[city],city2=city_dct[city])
        rep=requests.get(url,headers=header)
        rep.encoding='utf-8'
        lst=[]
        for i in rep.json()['data']['results']:
            dct={}
            dct['name']=i['jobName']
            dct['url']=i['positionURL'].replace('/','|')
            dct['exp']=i['workingExp']['name']
            dct['edu']=i['eduLevel']['name']
            dct['salary']=i['salary']
            dct['city']=i['city']['display']
            lst.append(dct)
        return lst
    else:
        url='https://fe-api.zhaopin.com/c/i/sou?start={num}&pageSize=60&cityId={city1}&salary={low1},{high1}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={name1}&kt=3&lastUrlQuery=%7B%22p%22:{p1},%22jl%22:%22{city2}%22,%22sf%22:%22{low2}%22,%22st%22:%22{high2}%22,%22kw%22:%22{name2}%22,%22kt%22:%223%22%7D'.\
            format(num=60*(cot-1),city1=city_dct[city],low1=int(salaryl),high1=int(salaryh),name1=keyword,p1=cot,city2=city_dct[city],low2=int(salaryl),high2=int(salaryh),name2=keyword)
        rep=requests.get(url,headers=header)
        rep.encoding='utf-8'
        lst=[]
        for i in rep.json()['data']['results']:
            dct={}
            dct['name']=i['jobName']
            dct['url']=i['positionURL'].replace('/','|')
            dct['exp']=i['workingExp']['name']
            dct['edu']=i['eduLevel']['name']
            dct['salary']=i['salary']
            dct['city']=i['city']['display']
            lst.append(dct)
        return lst

def get_lgzp(keyword,cot=1,salaryl=None,salaryh=None,city='全国'):
    agent_lst = [
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER ',
        ]
    if city=='全国':
        str_city=''
    else:
        str_city='&city={city}'.format(city=city)
    if salaryl==None or salaryh==None:
        str_salary=''
    elif int(salaryh)<2000:
        str_salary='&yx=2K以下'
    else:
        salaryl=int(salaryl)//1000
        salaryh=int(salaryh)//1000
        salary=str(salaryl)+'k'+'-'+str(salaryh)+'k'
        str_salary='&yx={yx}'.format(yx=salary)
    form_data = {
        'first': 'false',
        'pn': '%s' % cot,
        'kd': '%s' % keyword
    }
    url='https://www.lagou.com/jobs/positionAjax.json?px=default{yx}{city}&needAddtionalResult=false'.format(yx=str_salary,city=str_city)
    headers = {
        'Host': 'www.lagou.com',
        'Origin': 'https://www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?xl=%E6%9C%AC%E7%A7%91&px=default&city=%E5%85%A8%E5%9B%BD',
        'User-Agent': random.choice(agent_lst)
    }
    rep=requests.post(url,headers=headers,data=form_data)
    rep.encoding='utf-8'

    lst=[]
    for i in rep.json()['content']['positionResult']['result']:
        dct={}
        dct['name']=i['positionName']
        dct['exp']=i['workYear']
        dct['edu']=i['education']
        dct['url']=('https://www.lagou.com/jobs/%s.html' % i['positionId']).replace('/','|')
        dct['salary']=i['salary']
        dct['city']=i['city']
        lst.append(dct)
    return lst

def get_qtzp(keyword,cot=1,salaryl=None,salaryh=None,city='全国'):
    city_dct={'北京': '010000', '上海': '020000', '深圳': '040000', '武汉': '180200',
              '西安': '200200', '杭州': '080200', '南京': '070200', '成都': '090200',
              '重庆': '060000', '东莞': '030800', '大连': '230300', '沈阳': '230200',
              '苏州': '070300', '昆明': '250200', '长沙': '190200', '合肥': '150200',
              '宁波': '080300', '郑州': '170200', '天津': '050000', '青岛': '120300',
              '济南': '120200', '哈尔滨': '220200', '长春': '240200', '福州': '110200'}
    header = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36',
        'Host': 'search.51job.com',
        'Referer': 'https://search.51job.com/list/000000,000000,0000,00,9,99,java,2,1997.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=',
        'Cookie': 'guid=15288956658212670080; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttps%253A%252F%252Fwww.baidu.com%252Fs%253Ftn%253D97931839_hao_pg%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526usm%253D1%2526ie%253Dutf-8%2526rsv_cq%253D%2525E9%2525BD%252590%2525E9%2525B2%252581%2525E4%2525BA%2525BA%2525E6%252589%25258D%2525E7%2525BD%252591%2526rsv_dl%253D0_right_recommends_merge_21102%2526cq%253D%2525E9%2525BD%252590%2525E9%2525B2%252581%2525E4%2525BA%2525BA%2525E6%252589%25258D%2525E7%2525BD%252591%2526srcid%253D28310%2526rt%253D%2525E8%2525B5%252584%2525E8%2525AE%2525AF%2525E7%2525B1%2525BB%2525E7%2525BD%252591%2525E7%2525AB%252599%2526recid%253D21102%2526euri%253D6f4d7746fc104cfaad99e4672164935e%26%7C%26adsnum%3D2004282; partner=baidupz; 51job=cenglish%3D0%26%7C%26; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA000000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FAjava%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1532315011%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA000000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FApython%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1532315106%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch2%7E%601%A1%FB%A1%FA000000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FAFPGA%BF%AA%B7%A2%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1532317700%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch3%7E%601%A1%FB%A1%FA000000%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FAFPGA%BF%AA%B7%A291%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1532317804%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch4%7E%601%A1%FB%A1%FA121800%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FAjava%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1532315030%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21collapse_expansion%7E%601%7C%21; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D',

    }


    bc_url = '?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    if city=='全国':
        city_str=000000
    else:
        city_str=city_dct[city]

    if salaryl==None or salaryh==None:
        salary_str=99
    elif int(salaryh)<=2000:
        salary_str='01'
    elif int(salaryh)<=3000:
        salary_str='02'
    elif int(salaryh)<=5000:
        salary_str='03'
    elif int(salaryh)<=6000:
        salary_str='04'
    elif int(salaryh)<=8000:
        salary_str='05'
    elif int(salaryh)<=10000:
        salary_str='06'
    elif int(salaryh)<=15000:
        salary_str='07'
    elif int(salaryh)<=20000:
        salary_str='08'
    elif int(salaryh)<=30000:
        salary_str='09'
    else:
        salary_str='10'
    url = 'https://search.51job.com/list/{city},000000,0000,00,9,{salary},{keyword},2,{num}.html'.\
        format(city=city_str,salary=salary_str,keyword=keyword,num=cot)
    url=url+bc_url
    rep=requests.get(url,headers=header)
    rep.encoding='GB2312'
    bs=beaf(rep.text,'lxml')
    dw_table=bs.find('div',attrs={'class':'dw_table'})
    bs=beaf(str(dw_table),'lxml')
    result=bs.find_all('div',attrs={'class':'el'})
    result=result[1:]
    lst=[]
    edu_lst=['大专','本科','研究生','硕士','博士','中专','高中']
    exp_lst=['无工作经验','1年经验','3-4年经验','5-7年经验','2年经验']
    for i in result:
        dct={}
        # print(i.find_all('span'))
        dct['name']=str(i.p.span.text).replace(' ','').replace('\n','')
        dct['url']=i.p.span.a.get('href').replace('/','|')
        dct['city']=i.find_all('span')[2].text
        dct['salary']=i.find_all('span')[3].text
        rep=requests.get(url=i.p.span.a.get('href'),headers=header)
        rep.encoding='GB2312'
        bs=beaf(rep.text,'lxml')
        lst1=[]
        for i in bs.find_all('p', attrs={'class': 'msg ltype'}):
            for j in i.text.split('|'):
                lst1.append(j.replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0', ''))
        for i in lst1:
            if i in edu_lst:
                dct['edu']=i
            if i in exp_lst:
                dct['exp']=i
        try:
            dct['edu']
        except:
            dct['edu']='无要求'
        lst.append(dct)
    # print(lst)
    return lst

def zl_info(url):
    header={
        'Host':'jobs.zhaopin.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    # url='https://jobs.zhaopin.com/153424414250576.htm'
    rep=requests.get(url,headers=header)
    # print(rep.text)
    bs=beaf(rep.text,'lxml')
    name=bs.find('div',attrs={'class':'inner-left fl'})
    name=name.h1.text
    li=bs.find('ul',attrs={'class':'terminal-ul clearfix'}).find_all('li')
    salary=li[0].strong.text
    exp=li[4].strong.text
    edu=li[5].strong.text
    desp=bs.find('div',attrs={'class':'tab-inner-cont'}).text.replace('查看职位地图','')
    city=bs.find('div',attrs={'class':'tab-inner-cont'}).h2.text
    print(desp)
    dct={}
    dct['name']=name
    dct['salary']=salary
    dct['exp']=exp
    dct['edu']=edu
    dct['desp']=desp
    dct['city']=city
    return dct

def qt_info(url):
    # url='https://jobs.51job.com/guangzhou-thq/104566036.html?s=01&t=0'
    print('开始获取页面信息')
    header={
        'Host':'jobs.51job.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    edu_lst = ['大专', '本科', '研究生', '硕士', '博士', '中专', '高中']
    exp_lst = ['无工作经验', '1年经验', '3-4年经验', '5-7年经验', '2年经验']
    rep=requests.get(url=url,headers=header)
    bs=beaf(rep.text,'lxml')
    name=bs.find('h1').get('title')
    salary=bs.find('div',attrs={'class':'cn'}).strong.text
    lst1 = []
    edu=''
    exp=''
    for i in bs.find_all('p', attrs={'class': 'msg ltype'}):
        for j in i.text.split('|'):
            lst1.append(j.replace('\r', '').replace('\n', '').replace('\t', '').replace('\xa0', ''))
    for i in lst1:
        if i in edu_lst:
            edu=i
        if i in exp_lst:
            exp=i
    if exp=='':
        exp='无工作经验'
    if edu=='':
        edu='无要求'
    desp=bs.find('div',attrs={'class':'bmsg job_msg inbox'}).text
    desp=desp.replace('微信分享','')
    city=lst1[0].split('-')[0]
    dct={}
    dct['name']=name
    dct['salary']=salary
    dct['exp']=exp
    dct['edu']=edu
    dct['desp']=desp
    dct['city']=city
    print('页面信息获取完成')
    return dct


def lg_info(url):
    agent_lst = [
        'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER ',
        ]
    header = {
        'Host': 'www.lagou.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(agent_lst)}
    rep=requests.get(url=url,headers=header)
    bs=beaf(rep.text,'lxml')
    name=bs.find('span',attrs={'class':'name'}).text
    dd=bs.find('dd',attrs={'class':'job_request'})
    span=dd.find_all('span')
    salary=span[0].text
    exp=span[2].text
    edu=span[3].text
    city=span[1].text
    desp=bs.find('dd',attrs={'class':'job_bt'}).div.text
    dct={}
    dct['name']=name
    dct['salary']=salary
    dct['exp']=exp
    dct['edu']=edu
    dct['desp']=desp
    dct['city']=city
    return dct

def page(i):
    i=int(i)
    if i <= 3:
        return [1,2,3,4,5]
    else:
        return [i-2,i-1,i,i+1,i+2]


if __name__=='__main__':
    city_dct1={'北京': '010000', '上海': '020000', '深圳': '040000', '武汉': '180200',
              '西安': '200200', '杭州': '080200', '南京': '070200', '成都': '090200',
              '重庆': '060000', '东莞': '030800', '大连': '230300', '沈阳': '230200',
              '苏州': '070300', '昆明': '250200', '长沙': '190200', '合肥': '150200',
              '宁波': '080300', '郑州': '170200', '天津': '050000', '青岛': '120300',
              '济南': '120200', '哈尔滨': '220200', '长春': '240200', '福州': '110200'}
    city_dct2 = {
                '全国': '489', '北京': '530', '上海': '538', '深圳': '765', '广州': '763', '天津': '531', '成都': '801', '杭州': '653',
                '武汉': '736', '大连': '600', '长春': '613', '南京': '635', '济南': '702', '青岛': '703', '苏州': '639', '沈阳': '599',
                '西安': '854', '郑州': '719', '长沙': '749', '重庆': '551', '哈尔滨': '622', '无锡': '636', '宁波': '654', '福州': '681',
                '厦门': '682', '石家庄': '565', '合肥': '664', '惠州': '773'
                 }
    lst=[]
    for i in range(24):
        if list(city_dct1.keys())[i] in list(city_dct2.keys()):
            lst.append(list(city_dct1.keys())[i])

    print(lst)