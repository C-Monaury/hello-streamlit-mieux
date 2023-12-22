

from typing import Any
from scipy.integrate import odeint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import function as func
from streamlit.hello.utils import show_code
import time




st.title("Modélisations scénarios")
st.write("Dans cette section nous allons tester différents scénarios pour lutter contre la malaria")


option = st.selectbox(
    'Quel scénario veux tu tester ?',
    ( 'Réduction population de moustique', 'Améliorations des soins et prévention'))
st.write('You selected:', option)

if st.button("Affichage paramètre"):
    data ={
        "Paramètres":  ["r", "am", "bm", "ah", "bh", "mu", "nu",  "Tmh","Thm" ,"Sm", "Im", "Sh", "Ih", "Rh"],
        "Valeurs" : [0.01, 0.015,0.015, 0.03, 0.03, 0.008,0.01, 0.1,0.02,100, 2, 100, 0, 0]
    }
    df = pd.DataFrame(data)
    st.table(df)



r, am, bm, ah, bh, mu, nu,  Tmh,Thm  = 0.01, 0.1,0.1, 0.003, 0.002, 0.001,0.001, 0.2,0.1
Sm, Im, Sh, Ih, Rh =  1000, 10, 100, 0, 0
Nm = Im +Sm
Nh = Ih + Sh + Rh
m = r/Nh
y0 = [Sm, Im, Sh, Ih, Rh]


if option == 'Réduction population de moustique':
    
    par1=np.linspace(start= 0,stop=  1000 ,num = 1000)
   
    R0 = np.zeros(1000)
    droite = np.zeros(1000)
    for i in range(1000): 
        R0[i] = (par1[i]*Thm*Tmh*m*m)/(Nh*bm*(bh+mu+nu))
        droite[i] = 1
     #Plot du R0  
    
     
     
    fig, ax = plt.subplots()    
    ax.plot(par1 , R0, c = 'black')
    ax.set_xlabel('Nombre de moustiques')
    ax.set_ylabel('R0')
    st.pyplot(fig)
    
    calc=st.button("Population de moustique au R0 = 1")
    if calc == True:
        with st.spinner('Wait for it...'):
            time.sleep(0.5)
            st.success('200')
    
    
    #Plot de la simualtion 
    st.subheader("Paramètres Traitements")
    l1col1 ,l1col2 = st.columns(2)
    
    with l1col1:
      eff =st.slider("Pourcentage d'efficacité du traitement",min_value=0, max_value=100, step=1)
      
    with l1col2:
      nbr = st.slider("Nombre de traitements", min_value=1, max_value=10, step=1)
    
    eff = 1 - eff/100
    
    
    
    
    
    nbrpas =1000
    t = np.linspace(0, 1000, nbrpas)
    
    timesim =  np.linspace(0, nbrpas, nbr+2)
    timesim = np.ceil(timesim)
    
    
    
    dtemps = nbrpas/(nbr+1)
    
    
    solnew =np.zeros((1001, 5))
    
    for i in range(nbr+1):
        dtemps = int(timesim[i+1]) -int(timesim[i])
        
        tpartiel = np.linspace(0,dtemps,int(dtemps))
        sol = odeint(func.ModelMalaria, y0, tpartiel, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
        
        for y in range(5):
            
            solnew[int(timesim[i]):int(timesim[i+1]),y] = sol[:,y]
        
        y0 = [sol[int(dtemps-1),0]*eff , sol[int(dtemps-1),1]*eff , sol[int(dtemps-1),2] , sol[int(dtemps-1),3] , sol[int(dtemps-1),4] ]
    
    
    t = np.linspace(0, 1000, nbrpas+1)
    
    fig2, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(t,solnew[:,0],'g--',label="Moustiques sains")
    ax1.plot(t,solnew[:,1],'r--',label="Moustiques infectieux")
    ax2.plot(t,solnew[:,2],color = "forestgreen")
    ax2.plot(t,solnew[:,3],color = "firebrick")
    ax2.plot(t,solnew[:,4],color = "royalblue")
    ax1.set_xlabel('Temps')
    ax1.set_ylabel('Nombre de moustiques')
    ax2.set_ylabel('Nombre d humains')
    st.pyplot(fig2)


    
    
    
##########################################################  
######################ANTIBIOTIQUE########################  
##########################################################  



if option == 'Améliorations des soins et prévention':
    
    
    par1=np.linspace(start= 0,stop=  1.00 ,num = 1000)
    R0 = np.zeros(1000)
    
    for i in range(1000): 
        R0[i] = (Nm*Thm*Tmh*m*m)/(Nh*bm*(bh+mu+par1[i]))
        
    fig, ax = plt.subplots()    
    ax.plot(par1 , R0, c = 'black')
    ax.set_xlabel('mu')
    ax.set_ylabel('R0')
    st.pyplot(fig)
    
    st.subheader("Paramètres Traitements")
    l2col1 ,l2col2 = st.columns(2)
    
    with l2col1:
      mu =st.slider("Améliorations des soins aux malades ",min_value=0, max_value=100, step=1)
    mu = 0.01 - mu/10000
    with l2col2:
      r = st.slider("Diminution du taux de piqure", min_value=1, max_value=100, step=1)
    r = 0.01 - r/10000
    
    
    

    
    
   
    
    t = np.linspace(0, 100, 1001)
   
    y0 = [1000, 10, 100, 0, 0]
    #Sm, Im, Sh, Ih, Rh
    sol4 = odeint(func.ModelMalaria, y0, t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
        
    
    fig3, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    ax1.plot(t,sol4[:,0],'g--',label="Moustiques sains")
    ax1.plot(t,sol4[:,1],'r--',label="Moustiques infectieux")
    ax2.plot(t,sol4[:,2],color = "forestgreen")
    ax2.plot(t,sol4[:,3],color = "firebrick")
    ax2.plot(t,sol4[:,4],color = "royalblue")
    ax1.set_xlabel('Temps')
    ax1.set_ylabel('Nombre de moustiques')
    ax2.set_ylabel('Nombre d humains')
    st.pyplot(fig3)
    
    
    

   




#Ajout des valeurs à partir duquel R0 <1    
#Buton edit paramètres
# Ajout de l'évolution du système


st.subheader("Source")
st.write("https://malariajournal.biomedcentral.com/articles/10.1186/1475-2875-10-202")
st.write("https://www.who.int/fr/teams/global-malaria-programme/prevention/vector-control")
st.write('https://doi.org/10.1016/S0140-6736(03)15267-1 ')



