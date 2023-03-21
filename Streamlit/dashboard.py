import os
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import st_folium


def get_df():
    df = pd.read_csv("C:/Users/user/Desktop/강지원/Github/Python_edu/Streamlit/place.csv", encoding='utf-8')
    return df

def main():
    
    st.set_page_config(page_title='Where to meet', layout="wide")
    st.header("A Letter From Mr.Jung")
    st.subheader(':blue["Let me know where we will meet on Satuerday, with the dashboard made by streamlit."]')
    st.write("---")

    col1, col2 = st.columns([1,2])
    with col1:
        st.image(Image.open('C:/Users/user/Desktop/강지원/Github/Python_edu/Streamlit/question.jpg'))
    with col2:
        center = [37.5575,126.9245]
        df = get_df()
        df['to_홍대'] = np.round(np.sqrt(np.power((df['출발지_x']-center[0]),2) + np.power((df['출발지_y']-center[1]),2)),2)
        tab1, tab2 = st.tabs(['On Map', 'Raw Data'])
        with tab2:
            st.write(df)
        with tab1:
            m = folium.Map(location=center, zoom_start=11)
            key = 'E00B11DC-0EA7-30F4-B7F6-0D5B4A4CDFA3'
            tiles = f"http://api.vworld.kr/req/wmts/1.0.0/{key}/Base/{{z}}/{{y}}/{{x}}.png"
            folium.TileLayer(
                tiles=tiles,
                attr="Vworld",
                overlay=True,
                control=True
            ).add_to(m)
            for idx, row in df.iterrows():
                folium.Marker(location = [row['출발지_x'],row['출발지_y']], tooltip=row['이름'], icon=folium.Icon(color='gray')).add_to(m)
                folium.PolyLine(locations = [center, [row['출발지_x'],row['출발지_y']]], tooltip=row['to_홍대']).add_to(m)   
            folium.Marker(location = center, tooltip='홍대입구역', icon=folium.Icon(color='red')).add_to(m)
            m.fit_bounds(m.get_bounds())
            m.save('C:/Users/user/Desktop/강지원/Github/Python_edu/Streamlit/map.html')
            st.components.v1.html(open("C:/Users/user/Desktop/강지원/Github/Python_edu/Streamlit/map.html", "rb").read(), height=600)
    st.write("---")

    st.sidebar.image(Image.open('C:/Users/user/Desktop/강지원/Github/Python_edu/Streamlit/h_logo.png'))
    st.sidebar.write("---")
    rainbow = ['red', 'orange', 'yellow', 'green', 'blue', 'navy', 'purple']
    color = ['black', 'black', 'black', 'white', 'white', 'white', 'white']
    text = 'WELCOME'
    for r, c, t in zip(rainbow, color, text):
        st.sidebar.markdown(f"<h3 style='color:{c}; background-color:{r}'>__{t}:</h3>", unsafe_allow_html=True)
    st.sidebar.write("---")
    st.sidebar.text("This is Jiwon!\nNice to meet you!")

    
if __name__ == '__main__':
    
    main()
