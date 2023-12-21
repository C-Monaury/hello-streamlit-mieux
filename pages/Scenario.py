

from typing import Any

import numpy as np

import streamlit as st
from streamlit.hello.utils import show_code


st.title("Prévisions du futur")
st.write("Dans cette selection nous allons tester différents scénarios pour lutter contre notre maladie")

st.link_button("Aide visuelle","https://docs.streamlit.io/library/api-reference")


option = st.selectbox(
    'Quelle scéanrio veux tu tester ?',
    ('Quarantaine', 'Réduction population de moustique', 'Développement antibiotique'))

st.write('You selected:', option)

st.subheader("Source")
st.write("https://malariajournal.biomedcentral.com/articles/10.1186/1475-2875-10-202")
st.write("https://www.who.int/fr/teams/global-malaria-programme/prevention/vector-control")
