import asyncio
from pymongo.errors import PyMongoError
from app.core.excepciones import PersistenciaNoDisponibleError

async def con_reintentos(coro_fn, *args, intentos=3, espera_segundos=0.5, **kwargs):
    """Reintentos con espera fija ante fallos temporales de MongoDB;
    agotados los intentos, se traduce a un error que la API mapea a 503."""
    ultimo_error = None
    for intento in range(1, intentos + 1):
        try:
            return await coro_fn(*args, **kwargs)
        except PyMongoError as e:
            ultimo_error = e
            if intento < intentos:
                await asyncio.sleep(espera_segundos)
    raise PersistenciaNoDisponibleError(str(ultimo_error))