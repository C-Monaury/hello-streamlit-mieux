

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint


def ModelMalaria(y,t, r, am, bm, ah, bh, mu, nu,Thm, Tmh): 
  Sm, Im, Sh, Ih, Rh = y
  Nm = Sm + Im
  Nh = Sh + Ih + Rh
  dydt = [am*Nm - bm*Sm-r*Thm*Sm*Im,
          r*Thm*Sm*Ih -bm*Im,
          ah*Nh-bh*Sh-r*Tmh*Sh*Im,
          r*Tmh*Sh*Im-(bh+mu+nu)*Ih,
          nu*Ih-bh*Rh]
  return dydt

