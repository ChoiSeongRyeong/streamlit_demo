from collections import namedtuple
import altair as alt
import os
import math
import yaml
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
from icecream import ic
from glob import glob

from src.util import getYearList, getYearDirectoryConfig

WORKDIR = "/app"

# make hashed passwords
# hashed_passwords = stauth.Hasher(['']).generate()

# read authentication configuration file
with open('./config.yaml') as file:
    config = yaml.safe_load(file)
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
#    config['preauthorized']
)

# login page
name, authentication_status, username = authenticator.login('Login', 'main')
# main page
if st.session_state["authentication_status"] == False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] == None:
    st.warning('Please enter your username and password')
elif st.session_state["authentication_status"]:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{st.session_state["name"]}*')
    
    # 연도 선택
    YEAR_LIST = getYearList()
    year =  st.selectbox(
        "choose year",
        YEAR_LIST
    )
    # 해당 연도 정보 처리
    assert glob(f"data/result/{year}")
    dir_config = getYearDirectoryConfig(year)

    if not dir_config:
        st.warning("No images. Choose an another year.")
    else:
        ic(dir_config["dir_children_names"])

        # 이벤트 다중선택
        choices = st.multiselect("choose events", dir_config["dir_children_names"], default=None)
        #st.write(f"choices: {choices}")
        # 해당 이벤트 정보 처리
        choices_with_index = dir_config["dir_children_names"][dir_config["dir_children_names"].isin(choices)]
        if len(choices_with_index) == 0:
            st.warning("No event selected. Choose events.")
        else:
            #st.write(f"choices_with_index: {choices_with_index}")
            for idx, choice in enumerate(choices_with_index):
                
                item_paths = glob(os.path.join(WORKDIR, f"data/result/{year}/{idx}/*.jpg"))
                n_items = len(item_paths)
                st.write(f"event: {choice}")
                st.write(f"number of items: {n_items}")
                k = 0
                for i, item_path in enumerate(item_paths):
                    if i % 3 == 0:
                        col_1, col_2, col_3 = st.columns(3)
                        try:
                            col_1.image(item_path)
                        except:
                            st.error(f"error raised when loading image from {item_path}")
                    elif i % 3 == 1:
                        try:
                            col_2.image(item_path)
                        except:
                            st.error(f"error raised when loading image from {item_path}")
                    else:
                        try:
                            col_3.image(item_path)
                        except:
                            st.error(f"error raised when loading image from {item_path}")
        
