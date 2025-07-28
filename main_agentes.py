from agentes.agente_contexto import AgenteContexto
from agentes.agente_interaccion import AgenteInteraccion
from agentes.agente_supervision import AgenteSupervision
from agentes.agente_colaborativo import AgenteColaborativo
from agentes.agente_deteccion import AgenteDeteccion
from agentes.agente_simulacion import AgenteSimulacion
from agentes.agente_rutas import AgenteRutas
import asyncio

JIDS = {
    'contexto':      ("agente_contexto@xmpp.jp", "123456"),
    'interaccion':   ("agente_interaccion@xmpp.jp", "123456"),
    'supervision':   ("agente_supervision@xmpp.jp", "123456"),
    'colaborativo':  ("agente_colaborativo@xmpp.jp", "123456"),
    'deteccion':     ("agente_deteccion@xmpp.jp", "123456"),
    'simulacion':    ("agente_simulacion@xmpp.jp", "123456"),
    'rutas':         ("agente_rutas@xmpp.jp", "123456"),
}

async def main():
    print("Iniciando agente de interacción...")
    interaccion = AgenteInteraccion(*JIDS['interaccion'])
    print("Iniciando agente de supervisión...")
    supervision = AgenteSupervision(*JIDS['supervision'])
    print("Iniciando agente colaborativo...")
    colaborativo = AgenteColaborativo(*JIDS['colaborativo'])
    print("Iniciando agente de detección...")
    deteccion = AgenteDeteccion(*JIDS['deteccion'])
    print("Iniciando agente de simulación...")
    simulacion = AgenteSimulacion(*JIDS['simulacion'])
    print("Iniciando agente de rutas...")
    rutas = AgenteRutas(*JIDS['rutas'])
    print("Iniciando agente de contexto...")
    contexto = AgenteContexto(*JIDS['contexto'])

    await interaccion.start()
    await supervision.start()
    await colaborativo.start()
    await deteccion.start()
    await simulacion.start()
    await rutas.start()
    await asyncio.sleep(2)  # Espera a que los receptores estén listos
    await contexto.start()

    print("Agentes lanzados. Pulsa Ctrl+C para detener.")
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await contexto.stop()
        await interaccion.stop()
        await supervision.stop()
        await colaborativo.stop()

if __name__ == "__main__":
    asyncio.run(main()) 