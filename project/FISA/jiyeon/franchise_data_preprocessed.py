# -*- coding: utf-8 -*-
"""franchise_data_preprocessed.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lLdKxRNH8eAo7IRMoQUxZL5SfmXWAC6G
"""

import os
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

API_KEY = "easVaxWMuRqzcCLh4cFq/PRM2hfw5X0aZwlY1NazxySDTNLq9xl/FimQauHvNhDks8NN98AACE5pLsIq/2tlhQ=="

"""# 2. API에서 데이터 불러오기 함수 정의"""

# API 설정
BASE_URL = "http://apis.data.go.kr/1130000/FftcBrandFrcsStatsService/getBrandFrcsStats"

def fetch_franchise_data(year):
    """특정 연도의 가맹점 현황 데이터를 가져와서 DataFrame으로 반환하는 함수"""

    def fetch_page(page_no):
        """특정 페이지의 데이터를 가져오는 함수"""
        params = {
            'serviceKey': API_KEY,
            'pageNo': str(page_no),
            'numOfRows': '1000',
            'yr': str(year)
        }

        response = requests.get(BASE_URL, params=params, verify=False, headers={'accept': '*/*'})
        return response

    try:
        # 첫 페이지 호출하여 전체 데이터 수 확인
        first_response = fetch_page(1)
        root = ET.fromstring(first_response.content)

        # 결과 코드 확인
        result_code = root.find('.//resultCode')
        if result_code is not None and result_code.text != '00':
            print(f"Error in API response. Result code: {result_code.text}")
            result_msg = root.find('.//resultMsg')
            if result_msg is not None:
                print(f"Result message: {result_msg.text}")
            return None

        # 전체 데이터 수 확인
        total_count = int(root.find('.//totalCount').text)
        print(f"Total records for year {year}: {total_count}")

        # 필요한 총 페이지 수 계산
        page_size = 1000
        total_pages = (total_count + page_size - 1) // page_size
        print(f"Total pages to fetch: {total_pages}")

        # 모든 페이지의 데이터 수집
        all_data = []
        for page in range(1, total_pages + 1):
            print(f"Fetching page {page} of {total_pages} for year {year}")
            response = fetch_page(page)
            root = ET.fromstring(response.content)

            for item in root.findall('.//item'):
                data_dict = {}
                for child in item:
                    if child.tag in ['frcsCnt', 'newFrcsRgsCnt', 'ctrtEndCnt', 'ctrtCncltnCnt', 'nmChgCnt']:
                        try:
                            data_dict[child.tag] = int(child.text) if child.text else None
                        except (ValueError, TypeError):
                            data_dict[child.tag] = None
                    elif child.tag in ['avrgSlsAmt', 'arUnitAvrgSlsAmt']:
                        try:
                            data_dict[child.tag] = float(child.text) if child.text else None
                        except (ValueError, TypeError):
                            data_dict[child.tag] = None
                    else:
                        data_dict[child.tag] = child.text

                data_dict['timestamp'] = datetime.now().isoformat()
                all_data.append(data_dict)

        # DataFrame 생성
        df = pd.DataFrame(all_data)

        if df.empty:
            print(f"No data found for year {year}")
            return None

        print(f"Total records collected for year {year}: {len(df)}")

        return df  # DataFrame 반환

    except Exception as e:
        print(f"Error processing data for year {year}: {str(e)}")
        return None

"""# 3. 2023 데이터 가져오기 및 확인"""

# 데이터 가져오기 (예시: 2023년 데이터)
df = fetch_franchise_data(2023)
if df is not None:
    print("\nFetched Data:")
    display(df.head())  # DataFrame의 첫 몇 줄 출력
else:
    print("No data was fetched.")

df.tail()

import os
import requests
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime

# API 설정
BASE_URL = "http://apis.data.go.kr/1130000/FftcBrandFrcsStatsService/getBrandFrcsStats"

def fetch_franchise_data(year):
    """특정 연도의 가맹점 현황 데이터를 가져와서 DataFrame으로 반환하는 함수"""

    def fetch_page(page_no):
        """특정 페이지의 데이터를 가져오는 함수"""
        params = {
            'serviceKey': API_KEY,
            'pageNo': str(page_no),
            'numOfRows': '1000',
            'yr': str(year)
        }

        response = requests.get(BASE_URL, params=params, verify=False, headers={'accept': '*/*'})
        return response

    try:
        # 첫 페이지 호출하여 전체 데이터 수 확인
        first_response = fetch_page(1)
        root = ET.fromstring(first_response.content)

        # 결과 코드 확인
        result_code = root.find('.//resultCode')
        if result_code is not None and result_code.text != '00':
            return None  # 데이터가 없을 때

        # 전체 데이터 수 확인
        total_count = int(root.find('.//totalCount').text)
        print(f"Total records for year {year}: {total_count}")

        # 필요한 총 페이지 수 계산
        page_size = 1000
        total_pages = (total_count + page_size - 1) // page_size

        # 모든 페이지의 데이터 수집
        all_data = []
        for page in range(1, total_pages + 1):
            response = fetch_page(page)
            root = ET.fromstring(response.content)

            for item in root.findall('.//item'):
                data_dict = {}
                for child in item:
                    if child.tag in ['frcsCnt', 'newFrcsRgsCnt', 'ctrtEndCnt', 'ctrtCncltnCnt', 'nmChgCnt']:
                        try:
                            data_dict[child.tag] = int(child.text) if child.text else None
                        except (ValueError, TypeError):
                            data_dict[child.tag] = None
                    elif child.tag in ['avrgSlsAmt', 'arUnitAvrgSlsAmt']:
                        try:
                            data_dict[child.tag] = float(child.text) if child.text else None
                        except (ValueError, TypeError):
                            data_dict[child.tag] = None
                    else:
                        data_dict[child.tag] = child.text

                data_dict['timestamp'] = datetime.now().isoformat()
                all_data.append(data_dict)

        # DataFrame 생성
        df = pd.DataFrame(all_data)

        return df if not df.empty else None  # 데이터가 비어있지 않으면 반환

    except Exception as e:
        print(f"Error processing data for year {year}: {str(e)}")
        return None

# 모든 연도 데이터 가져오기
all_data_frames = []
year = 2017  # 시작 연도

while True:
    df = fetch_franchise_data(year)
    if df is not None:
        print(f"Data for year {year} fetched successfully with {len(df)} records.")
        all_data_frames.append(df)
    else:
        print(f"No data available for year {year}. Ending fetch process.")
        break
    year += 1  # 다음 연도로 이동

# 모든 연도 데이터를 하나의 DataFrame으로 합치기
if all_data_frames:
    full_data = pd.concat(all_data_frames, ignore_index=True)
    print(f"\nTotal records collected from all years: {len(full_data)}")
    display(full_data.head())
else:
    print("No data was fetched from any year.")

# 2017년부터 2023년까지 연도별 데이터 가져오기 및 저장
data_frames_by_year = {}
for year in range(2017, 2024):  # 2023까지 포함
    df = fetch_franchise_data(year)
    if df is not None:
        data_frames_by_year[year] = df
        print(f"Data for year {year} fetched successfully with {len(df)} records.")
    else:
        print(f"No data available for year {year}.")

# 연도별 DataFrame 확인
for year, df in data_frames_by_year.items():
    print(f"\nYear {year} Data:")
    display(df.head())

df_2023 = df

data_frames_by_year

# 연도별 고유 회사명과 브랜드명 리스트 확인
for year, df in data_frames_by_year.items():
    unique_corp_names = df['corpNm'].unique()  # 고유한 회사명 리스트
    unique_brand_names = df['brandNm'].unique()  # 고유한 브랜드명 리스트
    print(f"Year {year}:")
    print(f"  Unique Companies (corpNm): {unique_corp_names}")
    print(f"  Unique Brands (brandNm): {unique_brand_names}\n")

import pandas as pd

# 연도별 데이터프레임을 세로로 연결 (concat)하여 하나의 큰 데이터프레임으로 생성
franchise_data = pd.concat(data_frames_by_year.values(), ignore_index=True)

# 결합된 데이터의 확인
franchise_data.head()

# 'timestamp' 열의 형식을 '년-월-01' 형식으로 변환
# 각 연도의 첫 번째 날짜(1일)로 맞추기

# 'timestamp' 열의 형식을 'YYYY-MM-01'로 수정
franchise_data['timestamp'] = pd.to_datetime(franchise_data['timestamp']).dt.strftime('%Y-%m-01')

# 변환된 데이터 확인
franchise_data.head()

franchise_data = franchise_data.rename(columns={"timestamp": "date"})

franchise_data

