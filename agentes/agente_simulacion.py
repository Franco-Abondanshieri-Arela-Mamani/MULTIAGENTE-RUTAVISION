from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio

class AgenteSimulacion(Agent):
    class SimulacionBehaviour(CyclicBehaviour):
        async def run(self):
            # Simula una ubicación en un recorrido
            ubicacion_simulada = {"lat": -15.842, "lon": -70.023}
            msg = Message(to="agente_rutas@xmpp.jp")
            msg.body = str(ubicacion_simulada)
            await self.send(msg)
            await asyncio.sleep(10)

    async def setup(self):
        print("Entrando a setup de Simulación")
        self.add_behaviour(self.SimulacionBehaviour())
        print("Agente de Simulación iniciado") 