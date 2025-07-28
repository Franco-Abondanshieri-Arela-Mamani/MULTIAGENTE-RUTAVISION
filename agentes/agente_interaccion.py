from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import ast
import pyttsx3  # <--- para síntesis de voz

class AgenteInteraccion(Agent):
    class InstruccionBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.engine = pyttsx3.init()
            # Opcional: Cambiar voz a femenina/masculina si se desea
            # voices = self.engine.getProperty('voices')
            # self.engine.setProperty('voice', voices[1].id)  # 0: male, 1: female (depende del sistema)

        def frase_natural(self, datos):
            # Si es un diccionario con claves conocidas, formatea la frase
            if isinstance(datos, dict):
                if 'accion' in datos and datos['accion'] == 'girar':
                    direccion = datos.get('direccion', 'desconocida')
                    distancia = datos.get('distancia', None)
                    if distancia:
                        return f"Gira a la {direccion} en {distancia} metros."
                    else:
                        return f"Gira a la {direccion}."
                if 'alerta' in datos and datos['alerta'] == 'obstaculo':
                    tipo = datos.get('tipo', 'obstáculo')
                    distancia = datos.get('distancia', None)
                    if distancia:
                        return f"Cuidado, hay un {tipo} a {distancia} metros."
                    else:
                        return f"Cuidado, hay un {tipo} en el camino."
                if 'mensaje' in datos:
                    return str(datos['mensaje'])
                # Otros casos personalizados aquí
            # Si no es dict o no se reconoce, devuelve el texto plano
            return str(datos)

        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                try:
                    datos = ast.literal_eval(msg.body)
                    texto = self.frase_natural(datos)
                    print(f"Instrucción al usuario: {texto}")
                    self.engine.say(texto)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"Mensaje ignorado o inválido: {msg.body}")

    async def setup(self):
        print("Agente de Interacción iniciado")
        self.add_behaviour(self.InstruccionBehaviour()) 