

from typing import Any
from scipy.integrate import odeint
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import streamlit as st
import function as func
from streamlit.hello.utils import show_code


st.title("Prévisions du futur")
st.write("Dans cette selection nous allons tester différents scénarios pour lutter contre notre maladie")


option = st.selectbox(
    'Quelle scéanrio veux tu tester ?',
    ( 'Réduction population de moustique', 'Développement antibiotique'))
st.write('You selected:', option)

if st.button("Affichage paramètre"):
    data ={
        "Paramètres":  ["r", "am", "bm", "ah", "bh", "mu", "nu",  "Tmh","Thm" ,"Sm", "Im", "Sh", "Ih", "Rh"],
        "Valeurs" : [0.01, 0.01,0.01, 0.03, 0.02, 0.01,0.01, 0.1,0.02,100, 2, 100, 0, 0]
    }
    df = pd.DataFrame(data)
    st.table(df)



r, am, bm, ah, bh, mu, nu,  Tmh,Thm  = 0.01, 0.01,0.01, 0.03, 0.02, 0.01,0.01, 0.1,0.02
Sm, Im, Sh, Ih, Rh =  100, 2, 100, 0, 0
Nm = Im +Sm
Nh = Ih + Sh + Rh
m = r/Nh



if option == 'Réduction population de moustique':
    
    par1=np.linspace(start= 0,stop=  1000 ,num = 1000)
   
    R0 = np.zeros(1000)
    
    for i in range(1000): 
        R0[i] = (par1[i]*Thm*Tmh*m*m)/(Nh*bm*(bh+mu+nu))
        
    fig, ax = plt.subplots()    
    ax.plot(par1 , R0, c = 'black')

    st.pyplot(fig)
    
    

if option == 'Développement antibiotique':
    
    
    par1=np.linspace(start= 0,stop=  1.00 ,num = 1000)
    R0 = np.zeros(1000)
    
    for i in range(1000): 
        R0[i] = (Nm*Thm*Tmh*m*m)/(Nh*bm*(bh+mu+par1[i]))
        
    fig, ax = plt.subplots()    
    ax.plot(par1 , R0, c = 'black')
    #tracer ligne 1 pointillé
    st.pyplot(fig)
    
    
#t = np.linspace(0, 100, 1001)
    

#sol = odeint(func.ModelMalaria, y0, t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))


   




#Ajout des valeurs à partir duquel R0 <1    
#Buton edit paramètres
# Ajout de l'évolution du système


st.subheader("Source")
st.write("https://malariajournal.biomedcentral.com/articles/10.1186/1475-2875-10-202")
st.write("https://www.who.int/fr/teams/global-malaria-programme/prevention/vector-control")
