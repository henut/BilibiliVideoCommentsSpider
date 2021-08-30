if __name__ == '__main__':
    e=0
    page=1
    while e == 0 :
        url = "https://api.bilibili.com/x/v2/reply?pn="+ str(page)+"&type=1&oid=17784172&sort=2"
        try:
            print()
            content=get_content(url)
            print("page:",page)
            Out2File(content)
            page=page+1
            # 为了降低被封ip的风险，每爬20页便歇5秒。
            if page%10 == 0:
                time.sleep(5)
        except:
            e=1