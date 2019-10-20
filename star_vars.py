from flask import Flask
import json
import math
import periodictable as ptable
app = Flask(__name__)

@app.route('/default/<float:name>')
def hello_world(name):
    response = {}
    response["ne"]="dsfsdfds"
    response["names"]="dsfsdfds"
    response["namesss"]="dsfsdfds"
    response["namessss"]="dsfsdfds"
    #dict = {"name":name*4};
    return response;
    ##return str(name * 4)

def get_SB():
    return 5.670373e-8
    
def get_G():
    G = 6.6740e-11
    return G

def get_WC():
    WC = 2.828e-3
    return WC

@app.route('/return_tempS/<float:lumi>/<float:radS>')
def return_tempS(lumi,radS):
  tempS = (lumi/(4*(math.pi)*(radS**2)* get_WC()))**(4)
  #return str(tempS)
  colorS = return_colorS(tempS)
  response = {}
  response["tempS"]=tempS
  response["colorS"]=colorS
  
  return response

@app.route('/return_tempP/<float:dist>/<float:bAlb>/<float:lumi>')
def return_tempP(dist,bAlb,lumi):
  tempP = ((lumi*(1-bAlb))/((16*(math.pi))*(dist**2)*get_SB())) ** (1/4)
  colorP = return_colorP(tempP)
  response = {}
  response["tempP"]=tempP
  response["colorP"]=colorP
  return response

# lumi in relation to temp, dist, bAlbedo, (SB)
@app.route('/return_lumi/<float:tempP>/<float:dist>/<float:bAlb>')
def return_lumi(tempP,dist,bAlb):
  lumi = ((16*(math.pi))*(dist**2)*get_SB()*(tempP**4)) / (1-bAlb)
  #return str(lumi)
  response = {}
  response["lumi"]=lumi
  return response

# bAlb in relation to temp, dist, lumi
@app.route('/return_bAlb/<float:tempP>/<float:dist>/<float:lumi>')
def return_bAlb(tempP,dist,lumi):
  if ((((-16*(math.pi))*(dist**2)*get_SB()*(tempP**4))/(lumi))+1) < 0 or ((((-16*(math.pi))*(dist**2)*get_SB()*(tempP**4))/(lumi))+1) > 100:
    return "Must be an element of [0,100]"
  else:
    bAlb = ((((-16*(math.pi))*(dist**2)*get_SB()*(tempP**4))/(lumi))+1)
    response = {}
    response["bAlb"]=bAlb
    return response

# dist in relation to temp, lumi, bAlb
@app.route('/return_dist/<float:tempP>/<float:lumi>/<float:bAlb>')
def return_dist(tempP,lumi,bAlb):
  dist = (((lumi*(1-bAlb))/((16*(math.pi))*(tempP**4)*get_SB())) ** (1/2)) / 1.496e11
  #return str(dist)
  response = {}
  response["dist"]=dist
  return response

# Calculating Radiation Energy of star
@app.route('/return_Elambda/<float:tempS>')
def return_Elambda(tempS):
  Elambda = get_SB()*(tempS**4)
  #return str(Elambda)
  response = {}
  response["Elambda"]=Elambda
  return response

# Calculating Dominant Wavelength (color)
@app.route('/return_domLambda/<float:tempS>')
def return_domLambda(tempS):
  # 2.898 x 10 -3 meter-kelvin
 
  domLambda = float(get_WC()/tempS)
  #return str(domLambda)
  response = {}
  response["domLambda"]=domLambda
  return response

# Gravity on the planet

# massT = test mass
# massP = mass of the planet
# radP = radius of the planet
@app.route('/return_gravity/<float:massT>/<float:massP>/<float:radP>')
def return_gravity(massT,massP,radP):
  forceGrav = float((get_G() * massT * massP) / (radP**2))
  #return str(forceGrav)
  response = {}
  response["forceGrav"]=forceGrav
  return response

# Gravitational Field

@app.route('/habitable/<float:massP>/<float:radP>/')
def return_gField(massP,radP):
  gField = float((get_G() * massP) / (radP**2))
  #return str(gField)
  response = {}
  response["gField"]=gField
  return response

# Planet Color
@app.route('/planetcolor/<float:tempP>')
def return_colorP(tempP):
  if tempP <= 200:
    colorP = 'Blue'
  elif 200 < tempP < 500:
    colorP = 'Brown'
  elif 500 < tempP < 1000:
    colorP = 'Red'
  elif 1000 < tempP < 10000:
    colorP = 'Yellow'
  else:
    colorP = 'White'
  return colorP


# Star Color

@app.route('/starcolor/<float:tempS>')
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
  #return colorS
  """
  response = {}
  response["colorS"]=colorS
  response["wlength"]=wlength
  return response
  """
  return colorS
# Habitable zone delimitations

@app.route('/habitable/<float:lumi>')
def return_habitable(lumi):
  innerHab = (lumi/1.1) ** 1/2
  outerHab = (lumi/0.53) ** 1/2
  #return 'The habitable zone is between ' + str(innerHab) + ' meters and ' + str(outerHab) + ' meters'
  response = {}
  response["innerHab"]=innerHab
  response["outerHab"]=outerHab
  return response
