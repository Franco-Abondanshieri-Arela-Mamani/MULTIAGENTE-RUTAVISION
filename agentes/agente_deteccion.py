from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import requests  # <--- NUEVO: para hacer peticiones HTTP

class AgenteDeteccion(Agent):
    class DeteccionBehaviour(CyclicBehaviour):
        async def run(self):
            # Aquí deberías integrar la detección real de obstáculos
            # Por ahora, ejemplo simulado (puedes reemplazarlo por datos reales)
            obstaculo = {
                "tipo": "bache",
                "latitud": -15.841,
                "longitud": -70.021,
                "descripcion": "Bache profundo en la vía"
            }
            # Reporta al agente de interacción
            msg_interaccion = Message(to="agente_interaccion@xmpp.jp")
            msg_interaccion.body = str(obstaculo)
            await self.send(msg_interaccion)
            # Reporta al agente colaborativo
            msg_colaborativo = Message(to="agente_colaborativo@xmpp.jp")
            msg_colaborativo.body = str(obstaculo)
            await self.send(msg_colaborativo)
            # --- NUEVO: Registrar obstáculo en la base de datos Django vía API ---
            try:
                url = "http://localhost:8000/detection_simulator/reportar_obstaculo/"
                response = requests.post(url, json=obstaculo)
                if response.status_code == 200 and response.json().get('ok'):
                    print("Obstáculo registrado en la base de datos Django.")
                else:
                    print(f"Error al registrar obstáculo: {response.text}")
            except Exception as e:
                print(f"Excepción al registrar obstáculo: {e}")
            await asyncio.sleep(15)

    async def setup(self):
        print("Entrando a setup de Detección")
        self.add_behaviour(self.DeteccionBehaviour())
        print("Agente de Detección iniciado") 