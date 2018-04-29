##########################
# Subroutines
##########################

__version__ = '0.0.2'

def Calc_Temp(centicelcius):
  Correct_Temp=centicelcius/100
  #Correct_Temp=float("%1.f" % Correct_Temp)
  Correct_Temp=float(round(Correct_Temp,1))
  return Correct_Temp

