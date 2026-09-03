import math
HBAR=1.054571817e-34
C=299792458.0
def casimir_force(area_m2,separation_m):
    if area_m2<=0 or separation_m<=0: raise ValueError("area and separation must be positive")
    f=(math.pi**2*HBAR*C/240.0)*area_m2/(separation_m**4)
    return {"value_N":f,"unit":"N","method":"Ideal parallel-plate Casimir model","evidence_status":"CALCULATED","warning":"Ideal model; not experimental proof."}
def radiation_force(power_w):
    return {"value_N":power_w/C,"unit":"N","method":"F=P/c","evidence_status":"CALCULATED","warning":"Directed radiation momentum, not reactionless thrust proof."}
def energy_balance(output_w,input_w,loss_w=0.0):
    return {"net_W":output_w-input_w-loss_w,"unit":"W","method":"Pnet=Pout-Pin-Ploss","evidence_status":"CALCULATED"}
