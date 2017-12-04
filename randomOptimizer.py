import csv, math, random


def calcCL(m, v, s, rho):
    # L = 1/2 rho v^2 S cl
    # mg = 1/2 rho v^2 S cl
    # 2 mg / rho v^2 S = cl
    return (2.0 * m * 9.81) / (rho * v * v * s)


def calcCD(cd0, cl, k):
    return cd0 + k * cl * cl


def calcK(eff, AR):
    return 1.0 / (3.14159 * eff * AR)


def calcDrag(cd, v, s, rho):
    return 0.5 * cd * v * v * s * rho


def calcStallSpeed(clmax, s, m, rho):
    return math.sqrt((2 * m * 9.81) / (rho * s * clmax))


def flyMission(_m, _AR, _S, _cd0, _fuelFraction):
    m = _m
    m0 = m
    v = 35
    AR = _AR
    s = _S
    rho = 1.22
    cd0 = _cd0
    eff = 0.9
    b = math.sqrt(AR * s)

    clmax = 1.1

    fuelFraction = _fuelFraction
    mFuel = m0 * fuelFraction

    fuelBurn = (0.35 * 0.7) / 3600  # kg / sec

    dist = 0.0

    k = calcK(eff, AR)

    t = 0
    while m > (m0 - mFuel):

        v = math.sqrt(((2.0 / rho) * (m * 9.81 / s)) * math.sqrt(k / cd0))
        if v < 40 and v > 20:

            dist += v

            cl = calcCL(m, v, s, rho)
            cd = calcCD(cd0, cl, k)
            drag = calcDrag(cd, v, s, rho)
            power = drag * v
            ld = cl / cd

            if t == 0:
                initPower = power
                initLD = ld
                initCL = cl
                initCD = cd

            m = m - fuelBurn
            t += 1

        else:
            return {"range": 0, "power": 0, "LD": 0, "CL": 0, "CD": 0, "v": 0, "fuelWeight": 0, "fuelFraction": 0,
                    "span": 0, "AR": 0}
    return {"range": dist / 1000.0, "power": initPower, "LD": initLD, "CL": initCL, "CD": initCD, "v": v,
            "fuelWeight": mFuel, "fuelFraction": fuelFraction, "span": b, "AR": AR}


def optimize(n):
    failures = 0
    bestRange = 0.0
    for i in range(0, n):
        m = 15 + random.random() * 10.0
        AR = 10 + random.random() * 5.0
        s = 2.0 * random.random()
        cd0 = 0.06 + random.random() * 0.005
        fuelFraction = 0.4 + random.random() * 0.25
        results = flyMission(m, AR, s, cd0, fuelFraction)
        rangeFlown = results["range"]

        if rangeFlown > bestRange:
            print "new best range: " + str(rangeFlown)
            bestRange = rangeFlown
            print "initial mass: " + str(m)
            print "wing area: " + str(s)
            print "wing span: " + str(results["span"])
            print "wing chord: " + str(s / results["span"])
            print "wing AR: " + str(results["AR"])
            print "initial CL: " + str(results["CL"])
            print "initial CD: " + str(results["CD"])
            print "initial L/D: " + str(results["LD"])
            print "initial power: " + str(results["power"])
            print "initial cruise speed: " + str(results["v"])
            print "initial fuel weight: " + str(results["fuelWeight"])
            print "initial fuel fraction: " + str(results["fuelFraction"])
            print "time to fly (still air): " + str((4578000 / results["v"]) / 3600) + " hrs"

            print "---------------------------------------------"


optimize(1000)



















