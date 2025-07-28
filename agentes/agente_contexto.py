from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import requests  # <--- NUEVO: para hacer peticiones HTTP

class AgenteContexto(Agent):
    class UbicacionBehaviour(CyclicBehaviour):
        async def run(self):
            # Espera inicial para asegurar que el agente de rutas esté listo
            await asyncio.sleep(3)
            while True:
                ubicacion = {"usuario": "usuario1", "latitud": -15.84, "longitud": -70.02}
                # Enviar ubicación al agente de rutas
                msg = Message(to="agente_rutas@xmpp.jp")
                msg.body = str(ubicacion)
                await self.send(msg)
                print("Mensaje enviado a agente_rutas")
                # --- NUEVO: Registrar ubicación en la base de datos Django vía API ---
                try:
                    url = "http://localhost:8000/detection_simulator/ubicacion_api/"
                    response = requests.post(url, json=ubicacion)
                    if response.status_code in (200, 201) and response.json().get('ok'):
                        print("Ubicación registrada en la base de datos Django.")
                    else:
                        print(f"Error al registrar ubicación: {response.text}")
                except Exception as e:
                    print(f"Excepción al registrar ubicación: {e}")
                await asyncio.sleep(5)

    async def setup(self):
        print("Agente de Contexto iniciado")
        self.add_behaviour(self.UbicacionBehaviour()) 