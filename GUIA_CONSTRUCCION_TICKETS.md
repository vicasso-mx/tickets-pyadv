# Guía paso a paso: construir Tickets desde cero

Esta guía permite crear la aplicación de consola gradualmente en Python. Está pensada para una carpeta de proyecto vacía y sigue el paquete `tickets/`. En cada etapa se indica qué archivos crear, dónde añadir cada clase o método, qué comando ejecutar y qué resultado comprobar antes de continuar.

La aplicación mantiene los datos en memoria: al cerrar el programa, los tickets dejan de existir. No requiere paquetes externos.

## Requisitos y reglas del ejercicio

- Python 3.10 o posterior.
- Folios con el formato `TK-001` o `TK001` (tres dígitos; el guion es opcional).
- Tipos: `soporte`, `desarrollo` e `infraestructura`.
- Estados: `Abierto`, `En proceso` y `Cerrado`.
- Transiciones: `Abierto` puede pasar a `En proceso` o `Cerrado`; `En proceso` puede pasar a `Cerrado`; un ticket `Cerrado` no puede reabrirse.
- Título y descripción son obligatorios y no pueden consistir solo en espacios.
- No se admiten folios repetidos.

## 0. Preparar el proyecto

Abre PowerShell o una terminal y crea una carpeta vacía para el ejercicio. Por ejemplo:

```powershell
mkdir tickets-desde-cero
cd tickets-desde-cero
python --version
```

Comprueba que Python indique la versión instalada. En algunos equipos el comando puede ser `py --version`; en ese caso, sustituye `python` por `py` en los comandos de esta guía.

## 1. Crear la estructura de paquetes

Desde la raíz `tickets-desde-cero`, crea las carpetas:

```powershell
mkdir tickets
mkdir tickets\consola, tickets\dominio, tickets\servicios, tickets\almacenamiento, tickets\utilidades, tickets\pruebas
```

En `tickets/` y en cada subcarpeta crea un archivo vacío llamado `__init__.py`. Estos archivos marcan las carpetas como packages de Python.

Al final, la estructura será:

```text
tickets-desde-cero/
├── main.py
└── tickets/
    ├── __init__.py
    ├── __main__.py
    ├── consola/
    │   ├── __init__.py
    │   └── menu.py
    ├── dominio/
    │   ├── __init__.py
    │   ├── estados.py
    │   ├── ticket.py
    │   └── validaciones.py
    ├── servicios/
    │   ├── __init__.py
    │   └── servicio_tickets.py
    ├── almacenamiento/
    │   ├── __init__.py
    │   └── repositorio_memoria.py
    ├── utilidades/
    │   ├── __init__.py
    │   └── decoradores.py
    └── pruebas/
        ├── __init__.py
        ├── test_consola.py
        ├── test_dominio.py
        └── test_servicio.py
```

No es necesario crear todos los archivos de una sola vez; créalos en la etapa en que se describen.

## 2. Primera clase: Ticket

### 2.1 Crear el modelo inicial

En `tickets/dominio/ticket.py`, empieza con una clase `Ticket` y su constructor. El constructor recibe `folio`, `titulo` y `descripcion`. Guarda esos valores en atributos con guion bajo: `_folio`, `_titulo` y `_descripcion`. Agrega `_estado` con el valor inicial `Abierto`.

Debajo del constructor, añade una propiedad de solo lectura con `@property` para cada atributo. Las propiedades públicas se llamarán `folio`, `titulo`, `descripcion` y `estado`. No crees setters todavía: el objetivo inicial es que el código externo pueda consultar los valores, pero no asignarlos directamente.

Al final de la clase, añade `__str__` para producir una línea con nombre de clase, folio, título y estado.

En `tickets/__init__.py`, deja inicialmente un comentario de módulo. No importes todavía `Ticket`; primero se verificará el módulo directamente.

### 2.2 Crear las primeras pruebas

En `tickets/pruebas/test_dominio.py`, importa `unittest` y `Ticket`. Crea una clase de pruebas que herede de `unittest.TestCase` y agrega pruebas para:

1. Crear un ticket y comprobar que sus propiedades contienen los valores recibidos.
2. Comprobar que el estado inicial es `Abierto`.
3. Comprobar que convertir el ticket a texto incluye su folio.
4. Comprobar que asignar un valor a `ticket.estado` produce `AttributeError`, porque aún no tiene setter.

Incluye al final el bloque convencional de `unittest` que permite ejecutar el archivo directamente. Ejecuta desde la raíz del proyecto:

```powershell
python -m unittest tickets.pruebas.test_dominio -v
```

**Criterio para avanzar:** las pruebas de creación, estado, texto y encapsulamiento terminan en `OK`.

## 3. Tipos de ticket y herencia

En `tickets/dominio/ticket.py`, después del método `__str__` de `Ticket`, añade tres clases derivadas:

- `TicketSoporte`, cuyo constructor llama al constructor de `Ticket` con el tipo `soporte`.
- `TicketDesarrollo`, que usa el tipo `desarrollo`.
- `TicketInfraestructura`, que usa el tipo `infraestructura`.

Antes de la definición de `Ticket`, agrega el atributo de instancia `_tipo` en el constructor de `Ticket`. Para esta etapa, recibe el tipo como cuarto argumento opcional cuyo valor predeterminado es `soporte`. Añade también una propiedad pública de solo lectura llamada `tipo`.

En `tickets/pruebas/test_dominio.py`, agrega pruebas que creen cada clase derivada y comprueben su propiedad `tipo`. Vuelve a ejecutar:

```powershell
python -m unittest tickets.pruebas.test_dominio -v
```

**Criterio para avanzar:** la clase base sigue funcionando y las tres clases derivadas conservan sus tipos respectivos.

## 4. Validaciones y estados

### 4.1 Definir las reglas

En `tickets/dominio/estados.py`, define las tuplas `ESTADOS_VALIDOS` y `TIPOS_VALIDOS`. Después, define `TRANSICIONES_PERMITIDAS` como un diccionario cuyas claves son los estados y cuyos valores son las secuencias de estados destino admitidas.

En `tickets/dominio/validaciones.py`, importa `re` y define:

- `PATRON_FOLIO`, con el patrón `TK-?` seguido de exactamente tres dígitos.
- `folio_valido(folio)`, que solo acepta texto que coincida por completo con el patrón.
- `texto_requerido_valido(valor)`, que confirma que el valor es texto no vacío después de quitar espacios externos.

### 4.2 Validar la entidad y cambiar su estado

En `Ticket.__init__`, antes de asignar los atributos privados, valida el folio con `folio_valido`, el título, la descripción y el tipo. Lanza `ValueError` cuando un dato sea inválido. Guarda título y descripción después de quitar espacios externos. En la etapa siguiente, el decorador asumirá la validación del folio y podrás quitar esa comprobación directa del constructor.

Después de la propiedad `estado`, añade `cambiar_estado(nuevo_estado)`. En este orden, el método debe comprobar que el estado exista, tratar como operación sin cambio el caso en que sea igual al actual y verificar que la transición aparezca en `TRANSICIONES_PERMITIDAS`. Para una transición válida, actualiza `_estado` y devuelve `True`; para el mismo estado, devuelve `False`.

Añade `atender()` inmediatamente después de `cambiar_estado()`. Debe rechazar tickets cerrados y, en los demás casos, solicitar el cambio a `En proceso`.

En `tickets/pruebas/test_dominio.py`, agrega casos para folio inválido, texto vacío, estado desconocido, transición permitida, transición prohibida y atención de un ticket cerrado.

Ejecuta:

```powershell
python -m unittest tickets.pruebas.test_dominio -v
```

**Criterio para avanzar:** los datos incorrectos se rechazan con `ValueError`; una transición válida actualiza el estado, y una transición no permitida no altera el ticket.

## 5. Historial y contador de objetos

En `tickets/dominio/ticket.py`, agrega `from datetime import datetime` junto a los imports. Dentro de `Ticket`, pero fuera de sus métodos, declara `_contador_global = 0`.

En el constructor, después de asignar los atributos privados, inicializa `_historial` como lista, incrementa `Ticket._contador_global` y registra el evento inicial de creación.

Añade `_registrar_evento(accion, anterior, nuevo)` al final de la sección de métodos privados. Cada evento será un diccionario con fecha y hora, folio, acción y estados anterior y nuevo. Llama a este método desde `cambiar_estado` después de una transición válida.

Después de `_registrar_evento`, agrega la propiedad `historial`. Devuelve una tupla de copias de los diccionarios para que el código externo no pueda alterar la lista interna.

Agrega `total_tickets_creados()` como método de clase, usando `@classmethod`, debajo de `atender()`. Prueba que crear un ticket agregue un evento y que cambiar su estado agregue otro.

Ejecuta:

```powershell
python -m unittest tickets.pruebas.test_dominio -v
```

**Criterio para avanzar:** cada creación y cambio real de estado genera un evento; repetir el mismo estado no agrega evento duplicado.

## 6. Decorador de validación regex

En `tickets/utilidades/decoradores.py`, importa `wraps` desde `functools` y `folio_valido` desde `tickets.dominio.validaciones`. Añade `validar_folio(funcion)`. Su función envolvente recibe primero `self` y `folio`, valida el folio, lanza `ValueError` si no cumple y solo entonces invoca la función original. Usa `@wraps(funcion)` sobre la envolvente.

En `tickets/dominio/ticket.py`, agrega el import de `validar_folio` junto a los demás imports. Coloca `@validar_folio` inmediatamente encima de `def __init__(...)` en la clase `Ticket`. Esto valida el folio antes de construir la entidad y también se aplica cuando una clase derivada llama a `super().__init__`.

Añade una prueba que intente crear un folio inválido y comprueba que se recibe `ValueError`.

Ejecuta:

```powershell
python -m unittest tickets.pruebas.test_dominio -v
```

**Criterio para avanzar:** el constructor no acepta folios inválidos y el decorador conserva el nombre y documentación de la función original gracias a `wraps`.

## 7. Repositorio en memoria

En `tickets/almacenamiento/repositorio_memoria.py`, crea la clase `RepositorioMemoria`. En su constructor, inicializa `_tickets` como diccionario vacío. Usa el folio como clave.

Agrega estos métodos en este orden:

1. `agregar(ticket)`: rechaza folios ya existentes con `ValueError`, almacena y devuelve el ticket.
2. `buscar(folio)`: devuelve el ticket o `None` si no se encuentra.
3. `listar()`: devuelve una tupla con los tickets almacenados.
4. `__len__()`: devuelve la cantidad almacenada.

Todavía no existe el servicio, así que agrega temporalmente las pruebas del repositorio a `tickets/pruebas/test_dominio.py`. Crea una clase de prueba que instancie un ticket y un repositorio; comprueba inserción, búsqueda, ausencia y duplicados. Cuando llegues a la etapa del servicio, crea `test_servicio.py` y mueve allí esos casos del repositorio si quieres conservar separadas las responsabilidades de las pruebas.

Ejecuta la prueba del archivo que hayas elegido. Por ejemplo:

```powershell
python -m unittest tickets.pruebas.test_dominio -v
```

**Criterio para avanzar:** buscar un folio agregado devuelve el mismo objeto, buscar uno inexistente devuelve `None`, y los duplicados se rechazan.

## 8. Servicio de aplicación

En `tickets/servicios/servicio_tickets.py`, importa `Ticket`, las tres clases derivadas, `folio_valido` y `RepositorioMemoria`. Crea la clase `ServicioTickets`.

Antes de `__init__`, define el diccionario de clase `_clases_por_tipo`, que relaciona cada nombre de tipo con su clase derivada. En `__init__`, recibe opcionalmente un repositorio; si no recibe uno, construye `RepositorioMemoria`.

Agrega los métodos en este orden:

1. `crear_ticket(folio, titulo, descripcion, tipo)`: valida el folio, rechaza duplicados, busca la clase del tipo, crea el objeto y lo agrega al repositorio.
2. `consultar_ticket(folio)`: busca y devuelve el ticket; si no existe, lanza `LookupError`.
3. `listar_tickets(estado=None, tipo=None)`: obtiene los tickets y aplica los filtros. Usa comprensiones de listas, una por filtro.
4. `atender_ticket(folio)`: consulta el ticket y llama a su método `atender()`.
5. `actualizar_estado(folio, nuevo_estado)`: consulta y llama a `cambiar_estado()`.
6. `ordenar_por_folio()`: ordena la secuencia de tickets usando `sorted` y una `lambda` como clave.
7. `total_tickets_creados()`: método estático que delega al contador de `Ticket`.

En `tickets/pruebas/test_servicio.py`, prueba crear, consultar, filtrar por tipo y estado, detectar duplicados, manejar folio inexistente, atender y actualizar el estado.

Ejecuta:

```powershell
python -m unittest tickets.pruebas.test_servicio -v
```

**Criterio para avanzar:** los casos de uso pueden ejecutarse sin leer entradas de teclado; los errores de dominio se pueden probar directamente.

## 9. Menú de consola

En `tickets/consola/menu.py`, define `ejecutar_menu(servicio, entrada=input, salida=print)`. Los parámetros `entrada` y `salida` hacen posible sustituir teclado y pantalla durante las pruebas.

Dentro de la función, crea un ciclo que muestre las opciones para crear, consultar, listar, atender, actualizar estado y salir. Después de leer la opción:

- para crear, solicita folio, título, descripción y tipo;
- para consultar y atender, solicita folio;
- para listar, recorre los tickets ordenados por folio;
- para cambiar estado, solicita folio y estado destino;
- ante una opción desconocida, informa y vuelve a mostrar el menú;
- captura `ValueError` y `LookupError` y presenta su mensaje sin cerrar el programa.

En `tickets/pruebas/test_consola.py`, pasa una función `entrada` simulada que entregue primero una opción incorrecta y luego `0` para salir. Pasa una función `salida` que guarde los mensajes en una lista y comprueba que apareció el aviso de opción incorrecta.

Ejecuta:

```powershell
python -m unittest tickets.pruebas.test_consola -v
```

**Criterio para avanzar:** una entrada incorrecta no termina el menú y `0` sí permite salir limpiamente.

## 10. Puntos de entrada

En `tickets/__main__.py`, importa el menú y el servicio. Define `main()` para crear `ServicioTickets` y pasarlo a `ejecutar_menu`. Añade la condición de ejecución principal para que funcione `python -m tickets`.

En el archivo `main.py` de la raíz, importa `main` desde `tickets.__main__` y llama a la función bajo la condición `if __name__ == "__main__"`. Esto permite dos formas de inicio:

```powershell
python main.py
```

o:

```powershell
python -m tickets
```

Prueba ambas formas desde la raíz y elige la opción **0** para terminar.

## 11. Ejecutar todas las pruebas automatizadas

Desde la carpeta raíz del proyecto, ejecuta el descubrimiento de pruebas de la biblioteca estándar:

```powershell
python -m unittest discover -s tickets/pruebas -v
```

El comando debe terminar con `OK`. Si una prueba falla, revisa primero la etapa correspondiente: los nombres de los módulos y las rutas de importación deben coincidir con la estructura del proyecto.

También puedes ejecutar cada grupo por separado:

```powershell
python -m unittest tickets.pruebas.test_dominio -v
python -m unittest tickets.pruebas.test_servicio -v
python -m unittest tickets.pruebas.test_consola -v
```

## 12. Recorrido manual de aceptación

Inicia la aplicación y confirma este recorrido:

1. Crea el ticket `TK-001`, con título y descripción no vacíos, tipo `soporte`.
2. Intenta crear de nuevo `TK-001`; debe aparecer un error de folio duplicado.
3. Intenta crear `TK-1`; debe aparecer un error de formato.
4. Consulta `TK-001`; debe mostrarse en estado `Abierto`.
5. Atiéndelo; debe quedar `En proceso`.
6. Cámbialo a `Cerrado`.
7. Intenta atenderlo otra vez; debe aparecer un error y seguir cerrado.
8. Lista los tickets y confirma que el folio aparezca.
9. Sal con la opción `0`.

## 13. Qué se aprendió

- **Clases, atributos y métodos:** el modelo `Ticket` reúne datos y comportamiento relacionado.
- **Encapsulamiento:** los atributos con guion bajo se consultan mediante propiedades públicas.
- **Herencia:** las clases derivadas representan tipos concretos de ticket.
- **Decoradores:** `validar_folio` aplica la comprobación regex antes de ejecutar el constructor.
- **Comprensiones de listas:** el servicio filtra tickets de forma compacta y legible.
- **Funciones lambda:** el servicio define la clave de ordenamiento por folio.
- **Modularidad:** cada package separa dominio, interfaz, coordinación, almacenamiento y utilidades.
- **Pruebas automatizadas:** `unittest` verifica el comportamiento sin instalar dependencias.
