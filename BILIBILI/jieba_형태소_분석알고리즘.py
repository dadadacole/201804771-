# -*- coding: utf-8 -*-
"""jieba 형태소 분석

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/dadadacole/Comparing-BTS--BILIBILI-and-YOUTUBE--comments/blob/main/jieba_%ED%98%95%ED%83%9C%EC%86%8C_%EB%B6%84%EC%84%9D.ipynb

# 환경 준비
"""

# jieba 설치하기
!pip install jieba

# jieba 실행하기
import jieba
## pandas을 실행하기, 단 실행 별명을 pd로
import pandas as pd

"""# 데이터 불러오기"""

# 구글 드라이브 연결을 위한 기본 세팅 
!pip install -U -q PyDrive
 
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from google.colab import auth
from oauth2client.client import GoogleCredentials

auth.authenticate_user()
gauth = GoogleAuth()
gauth.credentials = GoogleCredentials.get_application_default()
drive = GoogleDrive(gauth)

## 문서 ID로 실제 파일 불러오기
# 실습을 위한 중국 역대 신년사 1992-2020
## https://drive.google.com/file/d/18TnFdgMoVVT5EIs7aAX1NYF7sNRIeRkN/view?usp=sharing

rawdata_downloaded = drive.CreateFile({'id': '18TnFdgMoVVT5EIs7aAX1NYF7sNRIeRkN'})
rawdata_downloaded.GetContentFile('rawdata.tsv')

# "rawdata.tsv" 파일의 내용을 "원본데이터" 변수로 불러오기
원본데이터 = pd.read_csv('rawdata.tsv' )

# "원본데이터" 변수 내용 확인하기
원본데이터

"""# 형태소 분석"""

# jieba(중국어형태소분석기) 중 품사태깅 요소를 pseg 별명으로 실행하기
import jieba
import jieba.posseg as pseg

# "원본데이터"를 대상으로 "jieba"를 사용해서 형태소 분석하기
저장공간  = [] ## 모든 결과를 저장할 빈 공간으로 "저장공간" 설정
for index, row in 원본데이터.iterrows():# 원본데이터의 컬럼(열)을 불러와서 반복할 준비!
    textdata = row[4]  # 분석에서 사용할 텍스트 정보가 있는 열을 지정해준다. 주의! python은 0부터 시작한다!
    type = row[0]  # 분석에서 사용할 분류 정보가 있는 열을 지정해준다. 주의! python은 0부터 시작한다!
    형태소 = pseg.cut(textdata)  # jieba의 pos 기능을 활용해서 대상 텍스트를 형태소 분리한다.
    for word in 형태소:  # jieba로 도출된 개별 형태소에 추가 정보를 기입하기 위해서 반복해준다.
      형태소종합 = [word.word,word.flag,type,1]  # 형태소종합에 분류정보와 카운트정보를 추가한다.
      저장공간.append(형태소종합) # 형태소종합의 내용을 종합하여 저장한다.

# "형태소" 변수의 저장 내용 확인
형태소

# "형태소종합" 변수의 저장 내용 확인
형태소종합

# "저장공간" 변수의 저장 내용 확인
저장공간

# 단일 데이터프레임 구조로 변환
분석통합 = pd.DataFrame(저장공간)

# "분석통합" 변수의 저장 내용 확인
분석통합

# "분석통합" 변수의 컬럼(열) 이름 변경
분석통합.columns = ["형태소", "품사", "분류", "카운트"]

# "분석통합" 변수의 저장 내용 확인
분석통합

# "분석통합" 변수의 내용을 형태소, 품사, 분류가 같은 것을 합치고, 카운트의 총합을 구해서 "그룹통합" 변수에 저장한다.
그룹통합 = 분석통합.groupby(['형태소', '품사', "분류"])['카운트'].sum()

# "그룹통합" 변수의 저장 내용 확인
그룹통합

# "그룹통합" 변수의 내용을 데이터프레임 형식으로 변환해서 "그룹통합" 변수에 저장한다.
그룹통합 = pd.DataFrame(그룹통합)

# "그룹통합" 변수의 저장 내용 확인
그룹통합

# "그룹통합" 변수의 내용을 "형태소분석결과.csv" 파일로 저장한다.
# header는 컬럼(열) 정보의 포함 여부이다.
# encoding은 문자코드를 선택하는 것이다. python에서는 기본적으로 utf-8(유니코드)를 사용한다.

그룹통합.to_csv('지에바.csv', header='true', encoding='utf-8-sig')