from flask import Flask
app = Flask(__name__)
@app.route('/default/<int:name>')
def hello_world(name):
    return str(name * 4)

@app.route('/a')
def get_SB():
	return 5.670373e-8
	
@app.route('/appstuff')
def get_G():
	G = 6.6740e-11
	return G

def get_WC():
	WC = 2.828e-3
	return WC

@app.route('/return_tempS')
def return_tempS(lumi,radS): 
  tempS = (lumi/(4*(math.pi)*(radS**2)* get_WC()))**(1/4)
  return tempS

def return_tempP(dist,bAlb,lumi): 
  tempP = ((lumi*(1-bAlb))/((16*(math.pi))*(dist**2)*get_SB())) ** (1/4)
  return tempP

# lumi in relation to temp, dist, bAlbedo, (SB)

def return_lumi(tempP,dist,bAlb): 
  lumi = ((16*(math.pi))*(dist**2)*get_SB()*(tempP**4)) / (1-bAlb)
  return lumi

# bAlb in relation to temp, dist, lumi

def return_bAlb(tempP,dist,lumi):
  if ((((-16*(math.pi))*(dist**2)*get_SB()*(tempP**4))/(lumi))+1) < 0 or ((((-16*(math.pi))*(dist**2)*get_SB()*(tempP**4))/(lumi))+1) > 100:
    print("Error, impossi boule")
  else:
    bAlb = ((((-16*(math.pi))*(dist**2)*get_SB()*(tempP**4))/(lumi))+1)
    return bAlb

# dist in relation to temp, lumi, bAlb

def return_dist(tempP,lumi,bAlb):
  dist = ((lumi*(1-bAlb))/((16*(math.pi))*(tempP**4)*get_SB())) ** (1/2)
  return dist

# Calculating Radiation Energy of star

def return_Elambda(tempS):
  Elambda = get_SB()*(tempS**4)
  return Elambda

# Calculating Dominant Wavelength

def return_domLambda(tempS):
  # 2.898 x 10 -3 meter-kelvin
  
  domLambda = float(get_WC()/tempS)
  return domLambda

# Gravity on the planet

# massT = test mass
# massP = mass of the planet
# radP = radius of the planet

def return_gravity(massT,massP,radP):
  forceGrav = float((get_G() * massT * massP) / (radP**2))
  return forceGrav

# Gravitational Field

def return_gField(massP,radP):
  gField = float((get_G() * massP) / (radP**2))
  return gField

# Star Color

def return_colorS(tempS):
  
  if tempS <= 3000:
    colorS = 'Red'
  elif 3000 < tempS < 4000:
    colorS = 'Orange'
  elif 4000 < tempS < 6000:
    colorS = 'Yellow'
  elif 6000 < tempS < 10000:
    colorS = 'White'
  else:
    colorS = 'Blue'

# Inner habitable zone radius - function of lumi

def return_innerHab(lumi):
  innerHab = (lumi/1.1) ** 1/2
  return innerHab

# Outer habitable zone radius

def return_outerHab(lumi):
  outerHab = (lumi/0.53) ** 1/2
  
  return outerHab