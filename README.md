# Instrucciones de uso
(Si no cacha na y es primera vez que usted ve esto, mire más abajo en la sección de información general).

Disclaimer: **Este servicio solo funciona en la máquina prime**
(esto debido a unas configuraciones con el login de Microsoft

### Instalación:
```
docker compose up
```
Esto crea dos contenedores, uno para la base de datos, llamado postgres, y otro para el backend.
Hecho eso estará todo instalado pero quizá no 100% funcional.

### Migraciones:
El backend se trabajó en Django, para los que cachan, aquí vuelve uno de sus enemigos, el makemigrations
- Primero deben identificar el contenedor del backend (no el de la bd, el del backend!!)
```
docker ps -a
```
- Copiar el container ID del contenedor del backend y luego ejecutar
```
docker exec -it <container_ID> bash
```
Esto les abrirá una consola dentro del contenedor
- Navegar hasta la carpeta que tenga el manage.py y ejecutar
```
python -m manage.py makemigrations
```
```
python -m manage.py migrate
```
Esto debería crear las migraciones en el backend, creando así también las tablas en la BD.
Para verificar que las tablas se hayan creado, les recomiendo utilizar el gestor de bases de datos DBeaver, tendrán que conectarse a través de un túnel SSH pasando por un jump server:
- Jump server: credenciales para APU
- SSH Tunnel: credenciales para prime


# Información general sobre servicios de primos

Todos los servicios que tiene Primos están o deberían estar alojados en prime.
Prime es una máquina dentro del departamento de infromática.

### Para acceder a prime desde la red de la U:
- Acceder a APU
- Desde APU ejecutar:
```
ssh primo@prime
```

Podrán ver el estado de los servicios (todos en Docker container) ejecutando:
```
docker ps -a
```
