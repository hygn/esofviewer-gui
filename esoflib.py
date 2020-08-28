def work(url=None,jsessionid=None,khanuser=None,playbackspeed="1",download=False,checkonly=False):
    import pycurl
    import time
    import wget
    from urllib.parse import urlencode
    from io import BytesIO
    import random
    import browser_cookie3
    import platform
    import youtube_dl
    buffer = BytesIO()
    def curl(url, postfields, cookie, posten, os, browser):
        curl = pycurl.Curl()
        curl.setopt(curl.URL, url)
        if posten:
            curl.setopt(curl.POSTFIELDS, postfields)
        else:
            pass
        curl.setopt(pycurl.COOKIE, cookie)
        if os == "windows":
            if browser == "chrome":
                curl.setopt(pycurl.USERAGENT,
                   "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36")
            if browser== "firefox":
                curl.setopt(pycurl.USERAGENT,
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0")
        if os == "linux":
            if browser == "chrome":
                curl.setopt(pycurl.USERAGENT,
                       "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36")
            if browser== "firefox":
                curl.setopt(pycurl.USERAGENT,
                        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0")
        curl.setopt(pycurl.WRITEDATA, buffer)
        curl.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl.setopt(pycurl.SSL_VERIFYHOST, 0)
        curl.perform()
        curl.close()
        dat = buffer.getvalue().decode('UTF-8')
        return dat
    if platform.system() == 'Linux':
        OS = "linux"
        browser = "firefox"
    else:
        OS = "windows"
        browser = "chrome"
    hoc = url.split("//")[1].split(".")[0]
    get = url.strip("https://"+hoc+".ebssw.kr/mypage/userlrn/userLrnView.do?")
    params = get.split("&")
    cookie = 'JSESSIONID='+str(jsessionid)+", KHANUSER="+str(khanuser)
    dat = curl(url, "", cookie, False , OS, browser)
    print(url)
    cnts = dat.split('if( headerCntntsTyCode === "')[1].split('"')[0]
    # next load
    post_data = {
        'stepSn': params[1].split("=")[1],
        'sessSn': '',
        'atnlcNo': params[0].split("=")[1],
        'lctreSn': params[2].split("=")[1],
        'cntntsTyCode': cnts}
    postfields = urlencode(post_data)
    dat = curl("https://"+hoc+".ebssw.kr/mypage/userlrn/userLrnMvpView.do",postfields, cookie, True, OS, browser)
    try:
        video = dat.split('src":"')[1].split('"')[0]
        vidtype = "ebs"
    except IndexError:
        video = dat.split('<iframe id="iframeYoutube" src="')[1].split('"')[0]
        vidtype = "yt"
        pass
    except Exception:
        return "error not supported data type"
    revtime = dat.split('var revivTime = Number( "')[1].split('"')[0]
    name = dat.split('<strong class="content_tit">')[1].split("<")[0]
    print(name)
    # getjs
    get_data = {
        '_': str(time.time()).split(".")[0]}
    getfields = urlencode(get_data)
    curl("https://"+hoc+".ebssw.kr/js/require.js?"+getfields, "", cookie, False, OS, browser)
    curl("https://"+hoc+".ebssw.kr/js/egovframework/com/ebs/cmmn/common.js?" +
         getfields, "", cookie, False, OS, browser)
    # startsig
    post_data = {
        'lctreSn': params[2].split("=")[1],
        'cntntsUseTyCode': cnts}
    postfields = urlencode(post_data)
    curl("https://"+hoc+".ebssw.kr/esof/cmmn/cntntsUseInsert.do",
         postfields, cookie, True, OS, browser)
    if vidtype == 'ebs' and download:
        wget.download(video.replace("\\", ""), name+'.mp4')
        print("video downloaded")
    if vidtype == 'yt' and download:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video])
    i = 0
    if int(revtime) < 120:
        lrntime = int(int(revtime)/2)
    else: 
        lrntime = 120
    rep = int((int(revtime) - int(revtime)%lrntime)/lrntime)
    rem = int(revtime) % lrntime
    if checkonly == True:
        time_min = str(int((int(revtime) - int(revtime) % 60)/60)) 
        time_sec = str(int(revtime) % 60)
        return [name,time_min,time_sec,revtime]
    while checkonly == False:
        if i == 0:
            lrnmux = 0
        else:
            lrnmux = 1
        post_data = {
            'stepSn': params[1].split("=")[1],
            'lrnAt': '0',
            'atnlcNo': params[0].split("=")[1],
            'lctreSn': params[2].split("=")[1],
            'cntntsTyCode': cnts,
            'lctreSeCode': 'LCTRE',
            'revivTime': revtime,
            'lrnTime': str(lrntime*lrnmux)}
        post_data.update({'lastRevivLc': str(int(lrntime * i))})
        postfields = urlencode(post_data)
        if playbackspeed != "inf":
            curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do",
                 postfields, cookie, True, OS, browser)
            print('checkpacket')
        if i != rep:
            if playbackspeed == "1":
                time.sleep(lrntime)
            elif playbackspeed == "20":
                time.sleep(10)
            elif playbackspeed == "inf":
                pass
            elif playbackspeed == "1.5":
                time.sleep(lrntime/1.5)
            else:
                return "error invalid playbackspeed"
        if i == rep:
            if playbackspeed == '1':
                time.sleep(rem)
            elif playbackspeed == '20':
                time.sleep(10)
            elif playbackspeed == 'inf':
                pass
            elif playbackspeed == "1.5":
                time.sleep(lrntime/1.5)
            else:
                return "error invalid playbackspeed"
            post_data.update({'endButtonYn':  'Y', 'lastRevivLc': str(int(revtime)), 'lrnTime': str(rem)})
            postfields = urlencode(post_data)
            curl("https://"+hoc+".ebssw.kr/mypage/userlrn/lctreLrnSave.do",
                 postfields, cookie, True, OS, browser)
            print('complete!')
            return 'complete!'
            break
        i = i + 1
