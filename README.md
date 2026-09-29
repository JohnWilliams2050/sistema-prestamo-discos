# Sistema de Renta de Discos Musicales

Aplicación para gestionar el préstamo de discos musicales a clientes, con control de inventario y validaciones de negocio (disponibilidad de stock y estado del cliente). El sistema está construido siguiendo el estilo arquitectónico de **Arquitectura en Capas (Layered Architecture)**, separando la presentación, la lógica de negocio, el acceso a datos y la persistencia en componentes independientes.

## Descripción del sistema

El sistema permite:

- Registrar discos en el catálogo, indicando título, artista, género y cantidad de copias disponibles.
- Registrar clientes mediante nombre, correo electrónico y teléfono.
- Consultar si un correo ya pertenece a un cliente existente, evitando exponer un listado completo de clientes por razones de privacidad.
- Crear una renta asociando un cliente activo a un disco con stock disponible.
- Rechazar una renta de forma controlada cuando el disco no tiene copias disponibles (409) o cuando el cliente está inactivo (403).
- Activar o desactivar clientes como una operación administrativa independiente del flujo de renta.

El flujo principal —seleccionar un disco, confirmar la renta y recibir una confirmación con la fecha límite de devolución— está implementado de extremo a extremo: desde el formulario en Angular hasta el documento persistido en MongoDB.

## Tecnologías usadas

| Componente | Tecnología |
|---|---|
| Frontend | Angular (TypeScript) |
| Backend | FastAPI (Python) |
| Base de datos | MongoDB |
| Protocolo de integración | REST sobre JSON, siguiendo la convención JSON:API |
| Contenerización | Docker y Docker Compose |
| Servidor del frontend | Nginx (sirviendo el build de producción de Angular) |

La arquitectura organiza estas tecnologías en cuatro capas: presentación (Angular), API (controladores FastAPI), negocio (servicios con las reglas de renta) y persistencia (repositorios sobre MongoDB). Cada capa se comunica únicamente con la inmediatamente inferior, y el acceso a MongoDB está aislado dentro de la capa de persistencia.

## Pasos para despliegue

### Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado, con virtualización habilitada en el sistema.
- Git (opcional, solo para clonar el repositorio).

No es necesario instalar Python, Node.js o MongoDB de forma local: todo se ejecuta dentro de los contenedores.

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd sistema-prestamo-discos
```

### 2. Levantar el sistema completo

```bash
docker compose up --build
```

Este comando construye las imágenes del backend y el frontend, descarga la imagen de MongoDB, y levanta los tres servicios conectados en una misma red interna de Docker.

### 3. Acceder a la aplicación

- **Frontend:** [http://localhost:4200](http://localhost:4200)
- **Backend (documentación interactiva de la API):** [http://localhost:8000/docs](http://localhost:8000/docs)

MongoDB no expone ningún puerto hacia el host por diseño: solo es accesible desde el contenedor del backend, como parte de la estrategia de aislamiento de la capa de datos.

### 4. (Opcional) Cargar datos de ejemplo

El repositorio incluye un script en `scripts/seed_data.py` que crea discos y clientes de ejemplo a través de la API, útil para probar el sistema sin llenar los formularios manualmente.

```bash
pip install requests
python scripts/seed_data.py
```

### Detener el sistema

```bash
docker compose down
```

Para eliminar también los datos almacenados en MongoDB:

```bash
docker compose down -v
```
