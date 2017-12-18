import math


def calcReqdYaw(airspeed, desiredBearing, windspeed, windDir):
    toRad = 0.0174533
    Va = airspeed
    Vw = windspeed
    Psi = windDir * toRad
    Theta = desiredBearing * toRad
    A = Va / math.cos(Theta)
    B = Va / math.sin(Theta)
    C = Vw * (math.sin(Psi) / math.sin(Theta)) - Vw * (math.cos(Psi) / math.cos(Theta))
    Phi = 2.0 * (math.atan((math.sqrt(A*A + B*B - C*C)-B) / (A + C)))
    Vr = (Va * math.cos(Phi) + Vw*math.cos(Psi))/math.cos(Theta)
    return {'yaw': Phi * 57.2958, 'speed': Vr}


print calcReqdYaw(100, 30.0, 25, 90)