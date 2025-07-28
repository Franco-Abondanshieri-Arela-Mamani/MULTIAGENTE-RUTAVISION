from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import requests  # <--- NUEVO: para hacer peticiones HTTP

class AgenteSupervision(Agent):
    class SupervisionBehaviour(CyclicBehaviour):
        async def run(self):
            # Aquí podrías recibir mensajes de estado de los demás agentes
            msg = await self.receive(timeout=10)
            if msg:
                print(f"[SUPERVISIÓN] Estado recibido: {msg.body}")
                evento = {
                    "agente": str(msg.sender),
                    "evento": f"Estado recibido: {msg.body}"
                }
            else:
                print("[SUPERVISIÓN] Sin respuesta de algún agente, posible fallo.")
                evento = {
                    "agente": "desconocido",
                    "evento": "Sin respuesta de algún agente, posible fallo."
                }
            # --- NUEVO: Registrar evento en la base de datos Django vía API ---
            try:
                url = "http://localhost:8000/detection_simulator/evento_supervision_api/"
                response = requests.post(url, json=evento)
                if response.status_code in (200, 201) and response.json().get('ok'):
                    print("Evento de supervisión registrado en la base de datos Django.")
                else:
                    print(f"Error al registrar evento de supervisión: {response.text}")
            except Exception as e:
                print(f"Excepción al registrar evento de supervisión: {e}")

    async def setup(self):
        print("Agente de Supervisión iniciado")
        self.add_behaviour(self.SupervisionBehaviour()) 