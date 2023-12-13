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
    #Equation moustique
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
    
    st.graphviz_chart('''
    digraph {
        Homme_sain -> Homme_Malade
        Homme_Malade -> Homme_Mort
        Moustique_Sain -> Moustique_Malade
        Homme_Malade -> Moustique_Sain 
        Moustique_Malade -> Homme_sain
        
    }
''')
    
    
    
    
    
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
    


if __name__ == "__main__":
    run()
