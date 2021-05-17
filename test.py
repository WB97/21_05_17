from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class TableRead:
    def __init__(self,url):
        self.table1_tr_list = list()
        self.table1_tr_list2 = list()
        self.url = urlopen(url) #주소
        self.soup = BeautifulSoup(self.url, "html.parser")  #html코드 저장

    def tables_read(self,class_name):
        self.tables = self.soup.find_all('table',{'class':class_name}) #테이블태그 클래스이름으로 전부 찾기

    def trs_read(self,num):
        self.trs = self.tables[num].find_all('tr')  #몇번째(찾는) 테이블에서 tr코드 전부 찾기
        for i in range(len(self.trs)):  #html코드 버리고 텍스트 부분만 추출
            self.table1_tr_list.append(self.trs[i].text.strip())

    def mk_df(self,start,colname):  #행의 시작지점과 열의 이름위치를 인자로 받기
        for i in range(len(self.table1_tr_list)):   #df에 들어갈 값들을 임시리스트로 정리, 최종 리스트에 2차원으로 저장
            if i >= start:
                self.tr_list_value = self.table1_tr_list[i].split('\n')

                for j in range(len(self.tr_list_value)-1):  #누적사망자수열을 제외한 총 열의 길이만큼 반복
                    for k in range(len(self.tr_list_value[j])): #문자열의 크기만큼 반복
                        if self.tr_list_value[j][k] == '(':
                            self.tr_list_value[j] = int(self.tr_list_value[j][k+1:-1].replace(',',''))
                            break
                # print(self.tr_list_value)
                self.table1_tr_list2.append(self.tr_list_value)
        self.df = pd.DataFrame(self.table1_tr_list2)    #데이터프레임 생성
        self.df.columns = self.table1_tr_list[colname].split('\n')  #columns에 들어갈 행 추출 및 정리
        self.df = self.df.drop('누적사망자수', axis=1)    #누적사망자수 열 삭제

    def show_df(self):
        print(self.df)

    def graph(self,day):
        plt.rc('font', family='Malgun Gothic', size=6.5)
        sns.barplot(data=self.df, x=day, y='국가/일').set_title(f'{day} 당일 코로나 확진자 수')
        plt.show()

if __name__ == '__main__':

    covid_df = TableRead("http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=14&ncvContSeq=&contSeq=&board_id=&gubun=")
    covid_df.tables_read('num')
    covid_df.trs_read(1)
    covid_df.mk_df(1,0)
    covid_df.graph('05.15')
    # covid_df.test()