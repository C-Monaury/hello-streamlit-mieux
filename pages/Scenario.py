

#from typing import Any
#from scipy.integrate import odeint
#import numpy as np
#import pandas as pd
#import matplotlib.pyplot as plt

#import streamlit as st
#import function as func
from streamlit.hello.utils import show_code


st.title("Prévisions du futur")
st.write("Dans cette selection nous allons tester différents scénarios pour lutter contre notre maladie")

st.write(range(2))
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



r, am, bm, ah, bh, mu, nu,  Tmh,Thm  = 0.01, 0.02,0.01, 0.03, 0.02, 0.01,0.01, 0.1,0.02
Sm, Im, Sh, Ih, Rh =  100, 2, 100, 0, 0
Nm = Im +Sm
Nh = Ih + Sh + Rh
m = r/Nh
y0 = [Sm, Im, Sh, Ih, Rh]


if option == 'Réduction population de moustique':
    
    par1=np.linspace(start= 0,stop=  1000 ,num = 1000)
   
    R0 = np.zeros(1000)
    
    for i in range(1000): 
        R0[i] = (par1[i]*Thm*Tmh*m*m)/(Nh*bm*(bh+mu+nu))
     #Plot du R0   
    fig, ax = plt.subplots()    
    ax.plot(par1 , R0, c = 'black')
    st.pyplot(fig)
    
    #Plot de la simualtion en 
    eff =st.slider("Pourcentage d'efficacité du traitement",min_value=0, max_value=100, step=1)
    eff = 1 - eff/100
    
    nbr = st.slider("Nombre de traitement", min_value=1, max_value=10, step=1)
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



if option == 'Développement antibiotique':
    
    
    par1=np.linspace(start= 0,stop=  1.00 ,num = 1000)
    R0 = np.zeros(1000)
    
    for i in range(1000): 
        R0[i] = (Nm*Thm*Tmh*m*m)/(Nh*bm*(bh+mu+par1[i]))
        
    fig, ax = plt.subplots()    
    ax.plot(par1 , R0, c = 'black')
    #tracer ligne 1 pointillé
    st.pyplot(fig)
    
    
    eff =st.slider("",min_value=0, max_value=100, step=1)
    eff = 1 - eff/100
    
    nbr = st.slider("Nombre de traitement", min_value=1, max_value=10, step=1)
    nbrpas =1000
    t = np.linspace(0, 1000, nbrpas)
    
    timesim =  np.linspace(0, nbrpas, nbr+2)
    timesim = np.ceil(timesim)
    
    
    
    dtemps = nbrpas/(nbr+1)
    
    
    solnew =np.zeros((1001, 5))
    
    t = np.linspace(0, 1000, nbrpas+1)
        
    tpartiel = np.linspace(0,dtemps,int(dtemps))
    
    sol = odeint(func.ModelMalaria, y0, t, args=(r, am, bm, ah, bh, mu, nu, Thm, Tmh))
        
        
    
    
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
    
    
    

   




#Ajout des valeurs à partir duquel R0 <1    
#Buton edit paramètres
# Ajout de l'évolution du système


st.subheader("Source")
st.write("https://malariajournal.biomedcentral.com/articles/10.1186/1475-2875-10-202")
st.write("https://www.who.int/fr/teams/global-malaria-programme/prevention/vector-control")
