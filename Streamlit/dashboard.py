import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import folium
import vworld_key


def get_df():
    df = pd.read_csv("place.csv", encoding='utf-8')
    return df

def main():
    
    # 페이지 설정
    st.set_page_config(page_title='Where to meet', layout="wide")
    
    # 사이드바
    st.sidebar.image(Image.open('streamlit_logo.png'))
    st.sidebar.write("---")
    
    rainbow = ['red', 'orange', 'yellow', 'green', 'blue', 'navy', 'purple']
    color = ['black', 'black', 'black', 'white', 'white', 'white', 'white']
    text = 'WELCOME'
    for r, c, t in zip(rainbow, color, text):
        st.sidebar.markdown(f"<h3 style='color:{c}; background-color:{r}'>__{t}:</h3>", unsafe_allow_html=True)
    st.sidebar.write("---")
    st.sidebar.text("This is Jiwon!\nNice to meet you!")
    
    # 메인 화면
    st.header("A Letter From Peter")
    st.subheader(':blue["Let me know where we will meet on Satuerday, with the dashboard made by streamlit."]')
    st.write("---")

    # 레이아웃(2분할)
    col1, col2 = st.columns([1,2])
    with col1:
        st.image(Image.open('question.jpg'))
        
    with col2:
        st.subheader(':blue["What about 홍대입구?"]')
        center = [37.5575,126.9245] # 홍대입구역 좌표
        
        # 데이터 불러오기
        df = get_df()
        df['to_홍대'] = np.round(np.sqrt(np.power((df['Lat']-center[0]),2) + np.power((df['Lon']-center[1]),2)),2)
        
        # 탭 만들기
        tab1, tab2 = st.tabs(['On Map', 'Raw Data'])

        with tab2:
            st.write(df)
            
        with tab1:
            # 지도 객체 만들기
            m = folium.Map(location=center, zoom_start=11)
            
            # 배경 레이어 삽입 (*vworld API)
            tiles = f"http://api.vworld.kr/req/wmts/1.0.0/{vworld_key.key}/Base/{{z}}/{{y}}/{{x}}.png"
            folium.TileLayer(
                tiles=tiles,
                attr="Vworld",
                overlay=True,
                control=True
            ).add_to(m)
            
            # 마커 및 직선 삽입
            for idx, row in df.iterrows():
                folium.Marker(location = [row['Lat'],row['Lon']], tooltip=row['Name'], icon=folium.Icon(color='gray')).add_to(m)
                folium.PolyLine(locations = [center, [row['Lat'],row['Lon']]], tooltip=row['to_홍대']).add_to(m)   
            folium.Marker(location = center, tooltip='홍대입구역', icon=folium.Icon(color='red')).add_to(m)
            
            # 경계선 맞추기
            m.fit_bounds(m.get_bounds())
            
            # 지도 저장 및 화면 출력
            m.save('map.html')
            st.components.v1.html(open("map.html", "rb").read(), height=600)
            
    st.write("---")
    
if __name__ == '__main__':
    
    main()
