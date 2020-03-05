import simpy as sim
import random

env = sim.Environment()
procesador = sim.Resource(env, capacity=1)
ram = sim.Container(env, capacity=100, init=100)  # cant de ram
esperando = sim.Resource(env, capacity=1)

sumatiempo = 0


def proceso(env, ram, procesador, ram_nec, inst_nec, timeout):
    global sumatiempo
    yield env.timeout(timeout)
    t_i = env.now
    # Entra a RAM
    yield ram.get(ram_nec)
    # Pasa a cpu
    while inst_nec > 3:
        yield procesador.request()
        # simular proceso
        yield env.timeout(1)
        inst_nec -= 3
    # revisar si necesita esperar I/O
    wait = random.randint(1, 2)
    if wait == 2:
        yield env.timeout(1)
    # devolver memoria
    ram.put(ram_nec)
    tiempototal = env.now-t_i
    sumatiempo += tiempototal


procesos = 25
for i in range(procesos):
    ram_nec = random.randint(1, 10)
    inst_nec = random.randint(1, 10)
    timeout = random.expovariate(1/10)
    env.process(proceso(env, ram, procesador, ram_nec, inst_nec, timeout))


env.run()

tiempoPromedio = sumatiempo/procesos
print(tiempoPromedio)
