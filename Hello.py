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

#%matplotlib widget
import matplotlib.pyplot as plt
from matplotlib import cm
import streamlit.components.v1 as components
from scipy.integrate import odeint
import mpld3

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
    
    st.graphviz_chart('''
    digraph {
        Homme_sain -> Homme_Malade
        Homme_Malade -> Homme_Mort
        Moustique_Sain -> Moustique_Malade
        Homme_Malade -> Moustique_Sain 
        Moustique_Malade -> Homme_sain
        
    }
''')
    #Presentation des parametres
    st.write("""
    ## Présentation des parametres:
    """)
    
    st.latex(r'''
             Moustique
    \left  \{
    \begin{array}{r c l}
      &a_M : taux\ de\ natalité\ du\ moustique \\
      &b_M : taux\ de\ mortalité\ naturelle\ du\ moustique \\
      &t_{HM} : taux\ de\ transmission\ de\ l'homme\ vers\ le\ moustique \\
      &a_H : taux\ de\ natalité\ de\ l'homme \\
      &b_H : taux\ de\ mortalité\ naturelle\ de\ l'homme \\
      &t_{MH} : taux\ de\ transmission\ du\ moustique\ vers\ l'homme \\
      &r & = & \frac{m}{N_H} : avec\ m\ le\ "bitting\ rate" \\
      &\mu : taux\ de\ mortalité\ humaine\ de\ la\ Malaria \\
      &\nu : taux\ de\ guérison\ humain\ de\ la\ Malaria \\ 
   \end{array}
   \right.
             ''' 
    )
    
    
    
    
    
    r, am, bm, ah, bh, mu, nu, Thm, Tmh  = 0.01, 0.01,0.01, 0.03, 0.02, 0.01,0.01, 0.2,0.1
    
    st.subheader("Paramètres Homme")
    l1col1 ,l1col2 ,l1col3 = st.columns(3)
    
    with l1col1:
      Thm =st.slider('Transmision Homme moustique', min_value=0.01, max_value=0.99)
      
    with l1col2:
      ah =st.slider('Taux de croissance Homme', min_value=0.01, max_value=0.99)
      
    with l1col3:
      bh =st.slider('Taux de mortalité ', min_value=0.01, max_value=0.99)
    
    
    y0 = [2, 100, 100, 0, 0]
    t = np.linspace(0, 1000, 2001)
    

    sol = odeint(func.ModelMalaria, y0, t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
    fig, ax = plt.subplots()
    col = ["cornflowerblue", "crimson", "royalblue","firebrick","gray" ]
    names_compart = ["Sm", "Im", "Sh", "Ih", "Rh"]
    for i,c in zip([0,1,2,3,4],col) :
      
        ax.plot(t, sol[:, i], color = c,
                 label= names_compart[i])
    
    ax .legend(loc = 0)
    
    st.pyplot(fig)
    
    #####
    def gradient_couleurs_bleu_rouge(nombre_de_couleurs):
        # Créer un dégradé de couleur du bleu au rouge
        colormap = plt.cm.get_cmap('RdYlBu')  # Choisir une colormap allant du rouge au bleu
        couleurs = [colormap(i) for i in np.linspace(0, 1, nombre_de_couleurs)]

        return couleurs
    
    #number = st.number_input(value =10, min_value = 1, max_value = 100, label = 'Insert a number', step =1)
    #couleurs_gradient = gradient_couleurs_bleu_rouge(number)
    y0 = np.array([100, 1, 100, 0, 0])

    fig3d = plt.figure()
    ax3d = fig3d.add_subplot(projection='3d')
    
    ax3d.axes.set_xlim3d(left=0, right=100)
    ax3d.axes.set_ylim3d(bottom=0, top=100) 
    ax3d.axes.set_zlim3d(bottom=0, top=100) 

    st.subheader("Paramètres Homme")
    option = st.selectbox(
        'Test',
        ('Selection des condition initial',
         'Conditions initials aléatoire'))
    if option == 'Selection des condition initial' :
        l2col1 ,l2col2 ,l2col3, l2col4 ,l2col5 = st.columns(5)
        
        with l2col1:
            y0[0] = st.number_input('Moustique sain ', min_value=0, max_value=100,step=1,
                                  value = 100)
        with l2col2:
            y0[1] = st.number_input('Moustique infecté ', min_value=0, max_value=100,step=1,
                                  value =1)
          
        with l2col3:
            y0[2] = st.number_input('Humain sain', min_value =0, max_value=100,step=1,
                                  value =100)
        with l2col4:
            y0[3] = st.number_input('Humain infecté ', min_value = 0, max_value=100,step=1,
                                  value =0)
        with l2col5:
            y0[4] = st.number_input('Humain guéri ', min_value = 0, max_value=100,step=1,
                                  value =0)
            
        sol2 = odeint(func.ModelMalaria, y0, t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
        x = sol2[:, 2]
        y = sol2[:, 4]
        z = sol2[:, 1]
        
        ax3d.scatter(x[0], y[0], z[0], zdir='z')
        ax3d.plot(x, y, z, zdir='z', label='curve in (x, y)')
    
    
    elif option == 'Conditions initials aléatoire':
        n_traj = st.number_input('Nombre de trajectoires', min_value=1, max_value=1000,step=1,
                              value = 1)
    
        Y0 = np.random.randint(100, size=(n_traj, 5))
        colors_line =  gradient_couleurs_bleu_rouge(n_traj)
    # Plot a sin curve using the x and y axes.
        for i in range(np.shape(Y0)[0]) :
            sol2 = odeint(func.ModelMalaria, Y0[i,:], t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
            x = sol2[:, 2]
            y = sol2[:, 4]
            z = sol2[:, 1]
            
            ax3d.scatter(x[0], y[0], z[0], zdir='z', color = colors_line[i])
            ax3d.plot(x, y, z, zdir='z', label='curve in (x, y)', color = colors_line[i])
        
    
        
    ax3d.set_xlabel('Humain sain')
    ax3d.set_ylabel('Humain infecter')
    ax3d.set_zlabel('Moustique infecter')
    
    elev = st.slider('elevation', min_value=-90, max_value=90, value = 20)
    azim = st.slider('azimute', min_value=-90, max_value=90, value = -35)
    
    ax3d.view_init(elev=elev, azim=azim)
    st.pyplot(fig3d)
    #components.html(mpld3.fig_to_html(fig3d), height=600)



 
    # Plot scatterplot data (20 2D points per colour) on the x and z axes.
    
    # ax.scatter(x, y, zs=0, zdir='y', c=c_list, label='points in (x, z)')
    
    # Make legend, set axes limits and labels

    
    # Customize the view angle so it's easier to see that the scatter points lie
    # on the plane y=0
    #ax3d.view_init(elev=20., azim=-35, roll=0)
    
    

if __name__ == "__main__":
    run()

