from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class AgenteRutas(Agent):
    class RutaBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"Mensaje recibido de {msg.sender}: {msg.body}")

    async def setup(self):
        print("Entrando a setup de Rutas")
        self.add_behaviour(self.RutaBehaviour())
        print("Agente de Rutas iniciado") 