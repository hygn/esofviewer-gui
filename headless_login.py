def login(hoc=None, id_=None, pw=None, type_='Normal'):
    from selenium import webdriver
    import platform
    os = platform.system()
    if os == 'Windows':
        try:
            driver = webdriver.Edge()
        except:
            driver = webdriver.Ie()
    elif os == 'Linux':
        try:
            driver = webdriver.Firefox()
        except:
            driver = webdriver.Chrome()
    else:
        try:
            driver = webdriver.Safari()
        except:
            driver = webdriver.Firefox()
    driver.get('https://'+hoc+'.ebssw.kr/sso/loginView.do?loginType=onlineClass')
    if type_ == 'normal':
        pass
    elif type_ == 'kakao':
        oauth = driver.find_element_by_class_name('lg_sns03')
        oauth.click()
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.support.ui import WebDriverWait
        wait = WebDriverWait(driver, 10)
        wait.until(EC.url_contains('https://accounts.kakao.com/'))
        input_id = driver.find_element_by_id('id_email_2')
        input_id.send_keys(id_)
        input_pw = driver.find_element_by_id('id_password_3')
        input_pw.send_keys(pw)
# suspend development due to technical issue