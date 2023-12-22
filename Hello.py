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
import streamlit.components.v1 as components

#import numpy as np

#%matplotlib widget
#import matplotlib.pyplot as plt
#from matplotlib import cm

#from scipy.integrate import odeint

#import function as func



LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Modèle de MacDonald",
        page_icon=":mosquito:",
    )
    st.write("""
    ## Présentation du modèle de MacDonald:
    """)
 #   st.write("""
 #   Le modele de MacDonald...
 #  """)
    
    
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
    
    graphe = st.selectbox("Que voulez-vous tracer", ["Dynamique de population", "Incidence"])
    if (graphe == "Dynamique de population"):
        
    
        fig, ax1 = plt.subplots()
        ax2 = ax1.twinx()
        ax1.plot(t,sol[:,0],'g--',label="Moustiques sains")
        ax1.plot(t,sol[:,1],'r--',label="Moustiques infectieux")
        ax2.plot(t,sol[:,2],color = "forestgreen", label="Humain sains")
        ax2.plot(t,sol[:,3],color = "firebrick", label="Humain infectieux")
        ax2.plot(t,sol[:,4],color = "royalblue", label="Humain guéri")
        ax1.set_xlabel('Temps')
        ax1.set_ylabel('Nombre de moustiques')
        ax2.set_ylabel('Nombre d humains')
        
    #    col = ["springgreen", "lightcoral", "forestgreen","firebrick","royalblue" ]
     #   for i,c in zip([0,1,2,3,4],col) :
     #       ax.plot(t, sol[:, i], color = c,
     #                label='theta(t)')
     
        fig.legend(loc='upper center') 
        
        st.pyplot(fig)
    

    if (graphe == "Incidence"):
        n = len(sol)
        ih = np.zeros(n)
        #r*Thm*Sm*Ih
        #r*Tmh*Sh*Im
        ih[1:(n-1)] = (r*Thm*sol[0:(n-2),2]*sol[0:(n-2),1])/(sol[1:(n-1),3]+sol[1:(n-1),4]+sol[1:(n-1),2])
        im = np.zeros(n)
        im[1:(n-1)] = (r*Tmh*sol[0:(n-2),0]*sol[0:(n-2),3])/(sol[1:(n-1),1]+sol[1:(n-1),0])
        fig, ax = plt.subplots()
        ax.plot(t[1:(n-2)],ih[1:(n-2)],'b')
        ax.plot(t[1:(n-2)],im[1:(n-2)],'b--')
        ax.set_xlabel('Temps')
        ax.set_ylabel('Incidence')
        
        st.pyplot(fig)
        
    st.header("Visualisation 3D : plan de phase")
    st.subheader("Trajectoires")
    
    #####
    def gradient_couleurs_bleu_rouge(nombre_de_couleurs):
        # Créer un dégradé de couleur du bleu au rouge
        colormap = plt.cm.get_cmap('RdYlBu')  # Choisir une colormap allant du rouge au bleu
        couleurs = [colormap(i) for i in np.linspace(0, 1, nombre_de_couleurs)]

        return couleurs
    
    #number = st.number_input(value =10, min_value = 1, max_value = 100, label = 'Insert a number', step =1)
    #couleurs_gradient = gradient_couleurs_bleu_rouge(number)
    y0 = np.array([100, 1, 100, 0, 0])
    t = np.linspace(0, 2000, 2001)
    fig3d = plt.figure()
    ax3d = fig3d.add_subplot(projection='3d')
    
    ax3d.axes.set_xlim3d(left=0, right=150)
    ax3d.axes.set_ylim3d(bottom=0, top=100) 
    ax3d.axes.set_zlim3d(bottom=0, top=100) 
    
    on = st.selectbox("L'axe des x represent les :",("sains","guéris"))
    if on == "sain" :
        ID = 2
    else :
        ID = 4

    
    names_comp = ["_","_","sains","_", "guéris"]   
    
   
    option = st.selectbox(
        'Choisis une option :',
        ('Selection des conditions initials',
         'Conditions initials aléatoires'))
    
    if option == 'Selection des conditions initials' :
        st.subheader("Conditions initiales")
        l2col1 ,l2col2 ,l2col3, l2col4 ,l2col5 = st.columns(5)
        
        with l2col1:
            y0[0] = st.number_input('Moustiques sains ', min_value=0, max_value=100,step=1,
                                  value = 100)
        with l2col2:
            y0[1] = st.number_input('Moustiques infectés ', min_value=0, max_value=100,step=1,
                                  value =1)
          
        with l2col3:
            y0[2] = st.number_input('Humains sains', min_value =0, max_value=100,step=1,
                                  value =100)
        with l2col4:
            y0[3] = st.number_input('Humains infectés ', min_value = 0, max_value=100,step=1,
                                  value =0)
        with l2col5:
            y0[4] = st.number_input('Humains guéris ', min_value = 0, max_value=100,step=1,
                                  value =0)
            
        sol2 = odeint(func.ModelMalaria, y0, t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
        x = sol2[:, ID]
        y = sol2[:, 3]
        z = sol2[:, 1]
        
        ax3d.scatter(x[0], y[0], z[0], zdir='z')
        ax3d.plot(x, y, z, zdir='z')
    
    
    elif option == 'Conditions initials aléatoires':
        n_traj = st.number_input('Nombre de trajectoires', min_value=1, max_value=1000,step=1,
                              value = 1)
    
        Y0 = np.random.randint(100, size=(n_traj, 5))
        colors_line =  gradient_couleurs_bleu_rouge(n_traj)
    # Plot a sin curve using the x and y axes.
        for i in range(np.shape(Y0)[0]) :
            sol2 = odeint(func.ModelMalaria, Y0[i,:], t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
            x = sol2[:, ID]
            y = sol2[:, 3]
            z = sol2[:, 1]
            
            ax3d.scatter(x[0], y[0], z[0], zdir='z', color = colors_line[i])
            ax3d.plot(x, y, z, zdir='z', label='curve in (x, y)', color = colors_line[i])
        
    
        
    ax3d.set_xlabel(f'Humains {names_comp[ID]}')
    ax3d.set_ylabel('Humains infectés')
    ax3d.set_zlabel('Moustiques infectés')
    l3col1 ,l3col2  = st.columns(2)
    with l3col1:
        elev = st.slider('elevation', min_value=-90, max_value=90, value = 20)
    with l3col2:
        azim = st.slider('azimute', min_value=-90, max_value=90, value = -35)
    
    ax3d.view_init(elev=elev, azim=azim)
    st.pyplot(fig3d)
    

    #components.html(mpld3.fig_to_html(fig3d), height=600)
    l4col1 ,l4col2   = st.columns(2)
    with l4col1:
        max_hs= st.number_input('Borne sup. humains sains', min_value=0, max_value=100,step=1,
                              value =100)
    with l4col2:
        max_hi= st.number_input('Borne sup. humains infectés', min_value=0, max_value=100,step=1,
                              value =2)
    with l4col2:
        max_mi= st.number_input('Borne sup. moustiques infectés', min_value=0, max_value=100,step=1,
                              value =100)
    
    st.subheader("Surface de trajectoires")
    Y0 = np.zeros((101,5))
    Y0[:,1] = np.linspace(0,max_mi, 101)
    Y0[:,2] = np.linspace(0,max_hs, 101)
    Y0[:,3] = np.linspace(0,max_hi, 101)
    X = np.zeros((len(t),101))
    Y = np.zeros((len(t),101))
    Z = np.zeros((len(t),101))



    for i in range(np.shape(Y0)[0]) :
        sol2 = odeint(func.ModelMalaria, Y0[i,:], t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
        X[:,i] = sol2[:, 2]
        Y[:,i] = sol2[:, 3]
        Z[:,i] = sol2[:, 1]
        
    fig3d2 = plt.figure()
    
    ax3d2 = fig3d2.add_subplot(projection='3d')
   

        
    ax3d2.axes.set_xlim3d(left=0, right=150)
    ax3d2.axes.set_ylim3d(bottom=0, top=100) 
    ax3d2.axes.set_zlim3d(bottom=0, top=100) 
    
    ax3d2.set_xlabel('Humains sains')
    ax3d2.set_ylabel('Humains infectés')
    ax3d2.set_zlabel('Moustiques infectés')
    ax3d2.plot_wireframe(X, Y, Z)
    
    l5col1 ,l5col2   = st.columns(2)
    with l5col1:
        elev = st.slider('elevation ', min_value=-90, max_value=90, value = 20)
    with l5col2:
        azim = st.slider('azimute ', min_value=-90, max_value=90, value = -40)

    ax3d2.view_init(elev=elev, azim=azim)
    st.pyplot(fig3d2)
 
    # Plot scatterplot data (20 2D points per colour) on the x and z axes.
    
    # ax.scatter(x, y, zs=0, zdir='y', c=c_list, label='points in (x, z)')
    
    # Make legend, set axes limits and labels

    
    # Customize the view angle so it's easier to see that the scatter points lie
    # on the plane y=0
    #ax3d.view_init(elev=20., azim=-35, roll=0)
    
    


if __name__ == "__main__":
    run()

