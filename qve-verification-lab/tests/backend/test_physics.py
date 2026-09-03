from backend.app.services.physics import casimir_force,radiation_force,energy_balance
def test_energy(): assert energy_balance(10,4,1)["net_W"]==5
def test_radiation(): assert radiation_force(299792458)["value_N"]==1
def test_casimir_positive(): assert casimir_force(1,1)["value_N"]>0
