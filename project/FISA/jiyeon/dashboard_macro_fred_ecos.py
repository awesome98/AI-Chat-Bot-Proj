# -*- coding: utf-8 -*-
"""국내외거시경제지표_FRED_ECOS.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1VAuQz6HwdGnT43lG9bRIQpyDwIUOgrlN
"""

# 라이브러리 임포트
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from fredapi import Fred
import requests
import matplotlib.font_manager as fm

# 한글 폰트 경로 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 나눔고딕 폰트 사용
font_prop = fm.FontProperties(fname=font_path)

# API 키 설정
FRED_API_KEY = '5cafaa9a5f90981d7a9c005ea24ba83a'
ECOS_API_KEY = '2IJKJSOY6OFOQZ28900C'

# FRED 인스턴스 생성
fred = Fred(api_key=FRED_API_KEY)

# 미국 정책금리 데이터 가져오기
us_policy_rate = fred.get_series('FEDFUNDS')  # 'FEDFUNDS'는 FRED의 미국 연방기금금리 데이터 시리즈 ID입니다
us_policy_rate = us_policy_rate[us_policy_rate.index >= '2000-01-29']


url = f"https://ecos.bok.or.kr/api/StatisticSearch/{ECOS_API_KEY}/json/kr/1/100000/722Y001/M/200001/202409/0101000"


# 한국 정책금리 데이터 가져오기
response = requests.get(url)
data = response.json()

# 데이터 확인 및 처리
if 'StatisticSearch' in data and 'row' in data['StatisticSearch']:
    kr_policy_rate = pd.DataFrame(data['StatisticSearch']['row'])
    kr_policy_rate = kr_policy_rate[['TIME', 'DATA_VALUE']]
    kr_policy_rate.columns = ['TIME', '한국 정책금리']
    kr_policy_rate['TIME'] = pd.to_datetime(kr_policy_rate['TIME'], format='%Y%m')
    kr_policy_rate['한국 정책금리'] = kr_policy_rate['한국 정책금리'].astype(float)

    # 그래프 그리기
    plt.figure(figsize=(12, 6))
    plt.plot(kr_policy_rate['TIME'], kr_policy_rate['한국 정책금리'], label='한국 정책금리', color='blue')
    plt.plot(us_policy_rate.index, us_policy_rate.values, label='미국 정책금리', color='brown')

    # 제목, 축 레이블 및 범례에 한글 폰트 설정
    plt.title('한미 정책금리 비교', fontproperties=font_prop)
    plt.xlabel('날짜', fontproperties=font_prop)
    plt.ylabel('금리 (%)', fontproperties=font_prop)
    plt.legend(prop=font_prop)

    plt.grid(True)
    plt.show()
else:
    print("한국 정책금리 데이터를 가져오는 데 실패했습니다.")

