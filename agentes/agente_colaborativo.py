from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import requests
import ast

class AgenteColaborativo(Agent):
    class ColaborativoBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"[COLABORATIVO] Reporte recibido: {msg.body}")
                # Enviar el reporte a la API REST de Django
                try:
                    data = ast.literal_eval(msg.body)
                    url = "http://127.0.0.1:8000/deteccion/api/obstaculos/"
                    response = requests.post(url, json=data)
                    if response.status_code == 201:
                        print("[COLABORATIVO] Reporte guardado en Django API.")
                    else:
                        print(f"[COLABORATIVO] Error al guardar en API: {response.text}")
                except Exception as e:
                    print(f"[COLABORATIVO] Error enviando a API: {e}")

    async def setup(self):
        print("Agente Colaborativo iniciado")
        self.add_behaviour(self.ColaborativoBehaviour()) 