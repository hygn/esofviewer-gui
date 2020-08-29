def query(hoc):
    import platform
    import browser_cookie3
    if platform.system() == 'Linux':
        data = str(browser_cookie3.firefox(domain_name=hoc+".ebssw.kr")).replace('<CookieJar[','').replace('}>','').split(">, <")
    else:
        data = str(browser_cookie3.chrome(domain_name=hoc+".ebssw.kr")).replace('<CookieJar[','').replace('}>','').split(">, <")
    cookies = ''
    for i in data:
        if hoc+'.ebssw.kr' in i:
            cookies = cookies + i.replace('Cookie ','').split(' for')[0] + ', '
    return cookies
