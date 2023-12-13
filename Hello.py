# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

import function as func



LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Modèle de MacDonald",
        page_icon=":mosquito:",
    )
    st.write("""
    ## Présentation du modèle de MacDonald:
    """)
    #équation Homme 
    st.latex(r'''
             Homme
    \left  \{
    \begin{array}{r c l}
      S_H  & = & a_H*N_H - b_H*S_H - r*T_H*S_H*I_M \\
      I_H   & = & r*T_H*S_H*I_M - (b + \mu + \nu)*I_H \\
      R_H & = & \nu*I_H-b_H*R_H
   \end{array}
   \right.
             ''' 
    )
    st.latex(r'''
             Moustique
    \left  \{
    \begin{array}{r c l}
      S_M  & = & a_M*N_M - b_M*S_M - r*T_M*S_M*I_H \\
      I_M   & = & r*T_M*S_M*I_H - b_M*I_M \\
   \end{array}
   \right.
             ''' 
    )
    
    
    
    
    
    
    
    r, am, bm, ah, bh, mu, nu, Thm, Tmh  = 0.01, 0.01,0.02, 0.03, 0.02, 0.01,0.01, 0.2,0.1
    
    st.subheader("Paramètres Homme")
    l1col1 ,l1col2 ,l1col3 = st.columns(3)
    
    with l1col1:
      Thm =st.slider('Transmision Homme moustique', min_value=0.01, max_value=0.99)
      
    with l1col2:
      ah =st.slider('Taux de croissance Homme', min_value=0.01, max_value=0.99)
      
    with l1col3:
      bh =st.slider('Taux de mortalité ', min_value=0.01, max_value=0.99)
    
    
    y0 = [2, 100, 100, 0, 0]
    t = np.linspace(0, 100, 1001)
    

    sol = odeint(func.ModelMalaria, y0, t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
    fig, ax = plt.subplots()
    col = ["cornflowerblue", "crimson", "royalblue","firebrick","gray" ]
    for i,c in zip([0,1,2,3,4],col) :
        ax.plot(t, sol[:, i], color = c,
                 label='theta(t)')
    
    st.pyplot(fig)
    st.write("# Welcome to Streamlit! 👋")

    st.sidebar.success("Select a demo above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.
        **👈 Select a demo from the sidebar** to see some examples
        of what Streamlit can do!
        ### Want to learn more?
        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)
        ### See more complex demos
        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


if __name__ == "__main__":
    run()
