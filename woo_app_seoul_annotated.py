import streamlit as st
import pandas as pd
import plotly.express as px


#bar chart는 geo라는 이름의 list를 인자로 받아서 안에있는 파라미터에 대해 함수를 반복수행
#그리고 bar_df는 edited_df를 사용한다는것에 주의
@st.cache_data
def bar_chart(*geo):
    bar_df = edited_df[edited_df["선택"]]
    fig = px.bar(bar_df,
                 title="서울시 구별 미세먼지",
                 y='미세먼지',
                 color='지역구',
                 hover_data='미세먼지')
    return fig

#line chart는 geo라는 이름의 list를 인자로 받아서 안에있는 파라미터에 대해 함수를 반복수행
#여기서 line_df는 pivot이 진행되지않은 original df를 사용한다
@st.cache_data
def line_chart(*geo):
    line_df = df[df["구분"].apply(lambda x: x in geo)]
    fig = px.line(line_df,
                 x="일시",y='초미세먼지(PM2.5)',
                 title="서울시 구별 미세먼지",
                 color="구분",
                 line_group='구분',
                 hover_name='구분'
                 )
    return fig

#geo는 그래프를 그릴 '선택된' '지역구' 들의 리스트이다, 이는 col1과 col2 사이에서 작업했다


#불러오기
df = pd.read_csv("seoul_filtered.csv")
#pivot table로 dataframe의 구조를 바꾼다
pivottable = pd.pivot_table(df, index="구분",
                            values=["미세먼지(PM10)","초미세먼지(PM2.5)"],
                            aggfunc='mean',)
pivottable['선택'] = pivottable["미세먼지(PM10)"].apply(lambda x: False)
pivottable[["미세먼지","초미세먼지"]] = pivottable[["미세먼지(PM10)","초미세먼지(PM2.5)"]]
del pivottable["미세먼지(PM10)"]
del pivottable["초미세먼지(PM2.5)"]

#구조를 어떻게 바꾸었는지 출력
print("ㅡㅡㅡㅡㅡㅡㅡpivot table--------------")
print(pivottable)

#간단한 streamlit 구성
col1, col2 = st.columns(2)
with col1:
    edited_df = st.data_editor(pivottable)

#index를 지역구 column으로 추가함, 프린트에서 확인
edited_df["지역구"] = edited_df.index
print("ㅡㅡㅡㅡㅡㅡㅡeditted DF--------------")
print(edited_df)
#이 select list를 밑에 함수에 파라미터로 전달함
select = list(edited_df[edited_df["선택"]]["지역구"])

with col2:
    tab1, tab2 = st.tabs(["Barchart","LineChart"])
    with tab1:
        st.title("bar")
        st.plotly_chart(bar_chart(*select))
    
    with tab2:
        st.title("Line")
        st.plotly_chart(line_chart(*select))
