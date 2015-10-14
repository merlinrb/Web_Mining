# encoding=utf-8
import requests
from bs4 import BeautifulSoup
# import random
# from multiprocessing import Pool
from multiprocessing.dummy import Pool

def is_existing(book_id):
    response = requests.get('http://taebc.ebook.hyread.com.tw/bookDetail.jsp?id=' + book_id)
    if '未購買此電子書' in response.text:
        return False
    else:
        return True


# for i in range(10000, 22222):
#     print(is_existing(str(i)), i)
# exit()
# 对同一本书自动借和还n次
def auto_lend(user_name, password, book_id):
    # 网站主页
    home_page = 'http://taebc.ebook.hyread.com.tw/'
    # 登录接口
    login_url = 'http://taebc.ebook.hyread.com.tw/SSO/stdLogin.jsp'
    # 书籍列表
    book_list_url = 'http://taebc.ebook.hyread.com.tw/Template/standard/more_recommendBooks.jsp'
    # 有些网站反爬虫，这里用headers把程序伪装成浏览器
    header = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
    }
    # 登录需要提交的表单
    login_data = {'account2': user_name,  # 填入网站的上网帐号
                  'passwd2': password,  # 未加密
                  'subcode': 'yzu',
                  }
    # 书籍详细页面
    book_detail_url = 'http://taebc.ebook.hyread.com.tw/bookDetail.jsp?id=' + book_id
    # 借书接口
    borrow_url = 'http://taebc.ebook.hyread.com.tw/service/authCenter.jsp'
    # 还书接口
    return_url = 'http://taebc.ebook.hyread.com.tw/group/encryptReturnEbook.jsp'
    # 我的书籍列表
    my_book_list = 'http://taebc.ebook.hyread.com.tw/Template/standard/member/MyEbook.jsp'

    global s
    # 登录
    s.post(login_url, data=login_data, headers=header)
    # 打开书籍目录
    s.get(book_list_url)
    print('成功登录')
    # 打开书籍详细页
    r = s.get(book_detail_url)
    soup = BeautifulSoup(r.text.encode('utf-8'))
    # <div class="school_library" >
    key_both = soup.body.find_all('form', {'action': '/service/authCenter.jsp'})
    # print(key_both[0].prettify())

    key = key_both[0].find('input', {'name': 'data'})['value']
    book_info = {
        'data': key,
        'rdurl': "/Template/standard/member/MyEbook.jsp",
    }
    # 借书
    s.post(borrow_url, data=book_info, headers=header)
    print('成功借阅')
    # 获取我的书架页面
    r = s.get(my_book_list)
    sp = BeautifulSoup(r.text.encode('utf-8')).find_all('div', {'class': 'lendbook'})[0]
    return_key = sp.find_all('a', {'class': 'btn'})[2]['href'].split('=')[1]
    # 归还
    s.get(return_url + '?data=' + return_key)
    print('成功归还')


def multiprocess(book_id):
    book_id = str(book_id)
    if is_existing(book_id):
        print('正在处理第%s本书'%book_id)
        auto_lend('s1026069', '243190', book_id)


if __name__ == "__main__":
    book_id = range(10000, 100000)
    s = requests.session()
    pool = Pool()
    pool.map(multiprocess, book_id)
    pool.close()
    pool.join()