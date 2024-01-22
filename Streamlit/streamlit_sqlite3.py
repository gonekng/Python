import time, sys, os
import numpy as np
import pandas as pd

import sqlite3
import streamlit as st

# DB 연동
def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Exception as e:
        st.write(e)

    return conn

# DB 생성
def create_database():

    st.write("# PAGE1 : 데이터베이스 만들기")
    st.write("---")

    db_filename = st.text_input("데이터베이스 이름을 입력하세요.")
    create_db = st.button('데이터베이스 생성')

    if create_db:
        if db_filename.endswith('.db'):
            if db_filename not in [file for file in os.listdir(os.getcwd())]:
                conn = create_connection(db_filename)
                st.success('데이터베이스 생성 완료.')
            else:
                st.error('이미 존재하는 데이터베이스입니다. 다시 입력하세요.')
        else: 
            st.error('파일이름은 .db로 끝나야 합니다. 다시 입력하세요.')

# 데이터 업로드
def upload_data():

    st.write("# PAGE2 : 파일 업로드하기")
    st.write("---")

    sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
    db_filename = st.selectbox('데이터베이스를 선택하세요.', sqlite_dbs)
    if db_filename is not None:
        conn = create_connection(db_filename)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        tables = [table[0] for table in tables]
        table_name = st.text_input('테이블 이름을 입력하세요.')
        if len(table_name) > 0:
            if table_name not in tables:
                uploaded_file = st.file_uploader('업로드할 파일을 첨부하세요.')
                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file, encoding='cp949')
                        st.write('**Data loaded successfully. These are the first 3 rows.**')
                        st.dataframe(df.head(3), use_container_width=True)
                    
                        col1, col2 = st.columns([8,1])
                        is_apply = col2.button('Upload', use_container_width=True)
                        if is_apply:
                            pg_bar = col1.progress(0, text="⏩Progress")
                            for percent_complete in range(100):
                                time.sleep(0.01)
                                pg_bar.progress(percent_complete + 1, text="Progress")
                                df.to_sql(name=table_name, con=conn, if_exists='replace', index=False)
                            time.sleep(0.1)
                            st.success("업로드가 완료되었습니다.")
                    except Exception as e:
                        st.write(e)
            else:
                st.error("이미 존재하는 테이블입니다. 다시 입력하세요.")
    else:
        st.error('DB 파일이 존재하지 않습니다. DB 파일을 먼저 생성하세요.')

# 쿼리 실행
def run_query():

    st.write("# PAGE3 : SQL 쿼리로 데이터 조작하기")
    st.write("---")

    sqlite_dbs = [file for file in os.listdir('.') if file.endswith('.db')]
    db_filename = st.selectbox('DB Filename', sqlite_dbs)
    query = st.text_area('SQL Query', height=150)
    if db_filename is not None:
        if len(query) == 0:
            is_disabled = True
        else:
            is_disabled = False
        submitted = st.button('Run Query', disabled=is_disabled)

        if submitted:
            conn = create_connection(db_filename)
            query = conn.execute(query)
            cols = [column[0] for column in query.description]
            results_df= pd.DataFrame.from_records(
                data = query.fetchall(), 
                columns = cols
            )
            st.dataframe(results_df)
    else:
        st.error('DB 파일이 존재하지 않습니다. DB 파일을 먼저 생성하세요.')

def convert_df(df):
    return df.to_csv(index=False).encode('cp949')


# --------------------- 메인 함수 --------------------- #

def main():

  # Page Configuration
    st.set_page_config(
        page_title="Sqlite3 DB Connect with Streamlit",
        page_icon="⚒️",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={
            'Get Help': 'mailto:donumm64@gmail.com',
            'About': "*Made by gonekng*"
        }
    )

  # 사이드바 설정
    st.sidebar.subheader("🎈Streamlit으로 Sqlite3 DB 관리하기")
    st.sidebar.write("---")
    
    page_names_to_funcs = {
        "Create Database": create_database,
        "Upload Data": upload_data,
        "Run Query": run_query,
    }

    selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys(), label_visibility='collapsed')
    page_names_to_funcs[selected_page]()

if __name__ == "__main__":

    main()
