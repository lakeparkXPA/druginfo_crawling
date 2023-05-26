from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
import os
import json

# 엑셀 로드
df = pd.read_excel('/Users/KimJunha/Desktop/smart_pv_drug.xlsx')
df = df.replace(np.nan,'')

# Chorme 연결
driver = webdriver.Chrome('/Users/KimJunha/chromedriver')
driver.implicitly_wait(3)
dr = 'https://www.druginfo.co.kr'
driver.get(dr)

# 로그인
key_file = os.path.join('', 'key.json')

with open(key_file) as f:
    key = json.loads(f.read())
id = key['id']
pw = key['pw']

driver.find_element_by_name('id').send_keys(id);time.sleep(1)
driver.find_element_by_name('t_passwd').send_keys(pw);time.sleep(1)
driver.find_element_by_xpath('//form[@name="loginForm"]/table/tbody/tr/td/table/tbody/tr/td/input').click()
time.sleep(3)

atc_name = [];atc_code = []
basis_code = []
rep_code = [];stand_code = []
charge_code = [];kd_code = []
mohw_name = [];mohw_code = []

for index, row in df.iterrows():
    atc = ''
    try:
        # 검색
        driver.find_element_by_name('tofind').clear();time.sleep(1)
        driver.find_element_by_name('tofind').send_keys(row['edi']);time.sleep(1)
        driver.find_element_by_xpath('//form[@name="searchForm"]/table/tbody/tr/td/input').click();time.sleep(2)

        # 검색 후 해당 약 url 이동
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            atc_url = soup.find("a", class_='product-link preview-product')['href'];time.sleep(2)
        except:
            atc_url = soup.find("a", class_='product-link')['href'];time.sleep(2)
        driver.get(dr + atc_url)

        # 주성분 코드 추출
        try:
            base_raw = driver.find_element_by_xpath('//td[text()="주성분코드"]//following-sibling::td')
            basis_code.append(base_raw.text.split('[')[0].strip())
        except:
            basis_code.append('')

        # 대표코드, 표준코드 추출
        try:
            stand_raw = driver.find_element_by_xpath('//tr[@id="pb0"]')
            stand_text = stand_raw.text.split(' ')
            rep_code.append(stand_text[4])
            stand_code.append(stand_text[5])
        except:
            rep_code.append('')
            stand_code.append('')

        # 청구코드[KD코드]
        try:
            kd_raw = driver.find_element_by_xpath('//td[text()="청구코드(KD코드)"]//following-sibling::td')
            kd_text = kd_raw.text.split(' ')[0]
            if '[' in kd_text:
                kd_text = kd_text.split('[')
                charge_code.append(kd_text[0])
                kd_code.append(kd_text[1].replace(']',''))
            else:
                charge_code.append(kd_text)
                kd_code.append('')
        except:
            charge_code.append('')
            kd_code.append('')

        # 복지부분류
        try:
            mohw_raw = driver.find_element_by_xpath('//td[text()="복지부분류"]//following-sibling::td')
            mohw_text = mohw_raw.text.split('[')
            mohw_code.append(mohw_text[0])
            mohw_name.append(mohw_text[1].replace(']','').strip())
        except:
            mohw_code.append('')
            mohw_name.append('')

        # ATC코드
        try:
            atc_raw = driver.find_element_by_xpath('//td[text()="ATC코드"]//following-sibling::td')
            atc_text = atc_raw.text.split('/')
            if len(atc_text) > 2:
                atc_name.append(','.join(atc_text[:-1]))
                atc_code.append(atc_text[-1])
            else:
                atc_name.append(atc_text[0].strip())
                atc_code.append(atc_text[-1].strip())
        except:
            atc_name.append('')
            atc_code.append('')

        time.sleep(2)

    # EDI 코드가 없는 경우
    except:
        atc_name.append('')
        atc_code.append('')
        charge_code.append('')
        kd_code.append('')
        basis_code.append('')
        rep_code.append('')
        stand_code.append('')
        mohw_code.append('')
        mohw_name.append('')

        time.sleep(2)

driver.close()

#엑셀로 저장
df['atc_name'] = atc_name;df['atc_code'] = atc_code
df['청구코드'] = charge_code;df['KD코드'] = kd_code
df['주성분코드'] = basis_code
df['대표코드'] = rep_code;df['표준코드'] = stand_code
df['복지부분류'] = mohw_code;df['복지부분류_코드명'] = mohw_name

writer = pd.ExcelWriter('/Users/KimJunha/Desktop/smart_pv_drug_atc_2.xlsx')
df.to_excel(writer, sheet_name='Sheet')
writer.save()