import numpy as np
from sk8o_sim import FullInitialConditionsCfg, FullSimulation, FullSimulationCfg
from sk8o_sim.controllers import SK8OFullController

sim = FullSimulation(FullSimulationCfg())
sim.new_reference(reference=[0, 0, 0.3])
controller = SK8OFullController()
data = sim.reset()
for _ in range(10000):
    data = sim.run(controller.action(data), 0.4)
    sim.render()
    if sim.has_fallen():
        print("The robot has fallen! :(")
sim.close()
