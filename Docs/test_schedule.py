from qiskit import circuit, pulse, transpile, QuantumCircuit, schedule, execute
from qiskit.providers.fake_provider import FakeAthens, FakeBelem, FakeQuito, FakeAlmaden
import numpy as np
import matplotlib.pyplot as plt
from qiskit import assemble
from qiskit.providers.aer import PulseSimulator
from qiskit.providers.aer.pulse import PulseSystemModel
#plt.switch_backend('agg')

backend = FakeAthens()
circ = circuit.QuantumCircuit(1)
circ.h(0)
circ.barrier()
circ.measure_all()
circ_t = transpile(circ, backend, optimization_level = 1)

## Without schedule
job = backend.run(circ_t,  meas_level=2,  meas_return='single',  shots=4096)
print("Without Schedule", job.result().get_counts())

## With schedule
circ_schedule = schedule(circ_t,backend)
#plt.close('all')
#plt.ion(), plt.show()
#circ_schedule.draw(backend = backend)
sched_results = backend.run(circ_schedule,shots = 4096).result()
sched_counts = sched_results.get_counts()
print("With Schedule",sched_counts)

backend_model= PulseSystemModel.from_backend(backend)
backend_sim = PulseSimulator()
qubit_lo_freq = backend_model.hamiltonian.get_qubit_lo_from_drift()
test_qobj = assemble(circ_schedule,
                        backend = backend_sim,
                        qubit_lo_freq = qubit_lo_freq,
                        meas_level = 2,
                        meas_return = 'single',
                        shots = 4096)

sim_result = backend_sim.run(test_qobj, system_model=backend_model).result()
print("With Schedule & Pulse Simulator",sim_result.get_counts())
