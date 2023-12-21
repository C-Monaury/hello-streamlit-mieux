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
      \frac{S_H}{dt}  & = & a_H\cdot N_H - b_H\cdot S_H - r\cdot t_{MH}\cdot S_H\cdot I_M \\
      \frac{I_H}{dt}   & = & r\cdot t_{MH}\cdot S_H\cdot I_M - (b + \mu + \nu)\cdot I_H \\
      \frac{R_H}{dt} & = & \nu\cdot I_H-b_H\cdot R_H
   \end{array}
   \right.
             ''' 
    )
    #Equation moustique
    st.latex(r'''
             Moustique
    \left  \{
    \begin{array}{r c l}
      \frac{S_M}{dt} & = & a_M\cdot N_M - b_M\cdot S_M - r\cdot t_{HM}\cdot S_M\cdot I_H \\
      \frac{I_M}{dt} & = & r\cdot t_{HM}\cdot S_M\cdot I_H - b_M\cdot I_M \\
   \end{array}
   \right.
             ''' 
    )
    
    st.image('./Schema.png')

    #Presentation des parametres
    st.write("""
    ## Présentation des parametres:
    """)
    
    st.latex(r'''
             Homme
    \left  \{
    \begin{array}{r c l}&
      &a_H : taux\ de\ natalité\ de\ l'homme \\&
      &b_H : taux\ de\ mortalité\ naturelle\ de\ l'homme \\&
      &a_H = b_H \\
   \end{array}
   \right.
             ''' 
    )
    
    st.latex(r'''
          Moustique
 \left  \{
 \begin{array}{r c l}&
   &a_M : taux\ de\ natalité\ du\ moustique \\&
   &b_M : taux\ de\ mortalité\ naturelle\ du\ moustique \\&
   &a_M = b_M \\
\end{array}
\right.
          ''' 
 )
         
    st.latex(r'''
                  Malaria
         \left  \{
         \begin{array}{r c l}&
           &t_{HM} : taux\ de\ transmission\ de\ l'homme\ vers\ le\ moustique \\&
           &t_{MH} : taux\ de\ transmission\ du\ moustique\ vers\ l'homme \\&
           &r = \frac{m}{N_H} : avec\ m\ le\ "bitting\ rate" \\&
           &\mu : taux\ de\ mortalité\ humaine\ de\ la\ Malaria \\&
           &\nu : taux\ de\ guérison\ humain\ de\ la\ Malaria \\ 
        \end{array}
        \right.
                  ''' 
         )
    
    
    
    r, am, bm, ah, bh, mu, nu, Thm, Tmh  = 0.01, 0.1,0.1, 0.002, 0.002, 0.01,0.01, 0.2,0.1
    
    st.subheader("Paramètres Homme")
    l1col1 ,l1col2 ,l1col3 = st.columns(3)
    
    with l1col1:
      Thm =st.slider('Transmision Homme moustique', min_value=0.01, max_value=0.99)
      
    with l1col2:
      Tmh =st.slider('Transmission Moustique Homme', min_value=0.01, max_value=0.99)
      
    with l1col3:
      mu =st.slider('Mortalité de la malaria ', min_value=0.01, max_value=0.99)
    
    
    y0 = [1000, 10, 100, 0, 0]
    t = np.linspace(0, 100, 1001)
    

    sol = odeint(func.ModelMalaria, y0, t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(t,sol[:,0],'g--',label="Moustiques sains")
    ax1.plot(t,sol[:,1],'r--',label="Moustiques infectieux")
    ax2.plot(t,sol[:,2],color = "forestgreen")
    ax2.plot(t,sol[:,3],color = "firebrick")
    ax2.plot(t,sol[:,4],color = "royalblue")
    ax1.set_xlabel('Temps')
    ax1.set_ylabel('Nombre de moustiques')
    ax2.set_ylabel('Nombre d humains')
    
#    col = ["springgreen", "lightcoral", "forestgreen","firebrick","royalblue" ]
 #   for i,c in zip([0,1,2,3,4],col) :
 #       ax.plot(t, sol[:, i], color = c,
 #                label='theta(t)')
    
    st.pyplot(fig)
    


if __name__ == "__main__":
    run()

