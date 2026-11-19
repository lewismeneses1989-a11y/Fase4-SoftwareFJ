# Fase4-SoftwareFJ

Sistema de gestión de **clientes, servicios y reservas** de la empresa ficticia Software FJ, desarrollado en Python con Programación Orientada a Objetos y **manejo avanzado de excepciones**. El sistema no usa bases de datos: todo se gestiona en memoria con listas y cada evento o error queda registrado en un archivo de logs.

- **Curso:** Programación (213023) - Universidad Nacional Abierta y a Distancia (UNAD)
- **Grupo:** 213023_386
- **Tutor:** Ermes Guarnizo Motta
- **Fase:** 4 - Componente práctico, trabajo colaborativo

## Integrantes y aportes

| Integrante | Usuario de GitHub | Parte | Archivo(s) |
|---|---|---|---|
| Luis Alfredo Adrada Meneses | lewismeneses1989-a11y | 1. Excepciones personalizadas y logs | `excepciones.py`, `registro_logs.py` |
| Luisa Fernanda Triana Cabezas | trianaluisafernanda2-ui | 2. Clase abstracta y clase Cliente | `entidad_base.py`, `cliente.py` |
| Luis Alfredo Adrada Meneses | lewismeneses1989-a11y | 3. Clase Servicio y servicios especializados | `servicios.py` |
| Jhoan Sebastián Guzmán Barreto | Guzman-10 | 4. Clase Reserva | `reservas.py` |
| Valentina Jaramillo Trujillo | jaramillovalentina1907-lgtm | 5. Simulación de 10 operaciones | `main.py` |
| Luis Alfredo Adrada Meneses | lewismeneses1989-a11y | Documentación | `README.md` |

## Estructura del proyecto

```
Fase4-SoftwareFJ/
├── excepciones.py      # Jerarquía de excepciones propias y encadenamiento
├── registro_logs.py    # Registro de eventos y errores en software_fj.log
├── entidad_base.py     # Clase abstracta EntidadSistema
├── cliente.py          # Clase Cliente con validaciones y encapsulación
├── servicios.py        # Clase abstracta Servicio y sus 3 servicios
├── reservas.py         # Clase Reserva: confirmar, cancelar y procesar
├── main.py             # Simulación integral de 10 operaciones
└── README.md
```

## Requisitos y ejecución

- Python 3 (probado con Python 3.13 y 3.14).
- Solo usa la biblioteca estándar (`abc`, `datetime`), no requiere instalar paquetes.

```
git clone https://github.com/lewismeneses1989-a11y/Fase4-SoftwareFJ.git
cd Fase4-SoftwareFJ
py main.py
```

En Linux o macOS se usa `python3 main.py`.

## Conceptos aplicados

- **Abstracción:** clases abstractas `EntidadSistema` y `Servicio` con `ABC` y `@abstractmethod`.
- **Herencia y polimorfismo:** `ReservaSala`, `AlquilerEquipo` y `Asesoria` sobrescriben `describir()`, `validar_parametros()` y `calcular_costo()`.
- **Encapsulación:** atributos protegidos y propiedades (`@property`) con validación.
- **Sobrecarga simulada:** `calcular_costo(horas, con_iva=False, descuento=0)` con parámetros opcionales.
- **Manejo de excepciones:** bloques `try/except`, `try/except/else` y `try/except/finally`.
- **Excepciones personalizadas:** jerarquía propia que hereda de `SoftwareFJError`.
- **Encadenamiento de excepciones:** `raise ... from error`, consultable con `__cause__`.
- **Registro de logs:** cada evento y error se guarda con fecha y nivel.

## Excepciones del sistema

| Excepción | Cuándo se lanza |
|---|---|
| `SoftwareFJError` | Clase base de todas las excepciones del sistema |
| `DatoInvalidoError` | Un dato tiene formato o valor incorrecto |
| `ParametroFaltanteError` | Falta un dato obligatorio |
| `OperacionNoPermitidaError` | Se intenta una acción no válida para el estado actual |
| `ReservaInvalidaError` | Una reserva no se puede crear o procesar |
| `ServicioNoDisponibleError` | El servicio solicitado no está disponible |
| `CalculoInconsistenteError` | Un cálculo de costo da un resultado imposible |

## Simulación de operaciones

| # | Operación | Tipo | Resultado esperado |
|---|---|---|---|
| 1 | Registrar cliente válido | Válida | Cliente creado |
| 2 | Registrar cliente con correo inválido | Inválida | `DatoInvalidoError` controlada |
| 3 | Registrar segundo cliente válido | Válida | Cliente creado |
| 4 | Crear catálogo de servicios | Válida | 4 servicios creados |
| 5 | Crear servicio con tarifa negativa | Inválida | `DatoInvalidoError` controlada |
| 6 | Crear, confirmar y procesar reserva | Válida | Total con descuento e IVA |
| 7 | Crear reserva con duración 0 | Inválida | `DatoInvalidoError` controlada |
| 8 | Cancelar dos veces una reserva | Inválida | `OperacionNoPermitidaError` controlada |
| 9 | Procesar reserva sin confirmar | Inválida | `ReservaInvalidaError` con causa encadenada |
| 10 | Procesar reserva de servicio no disponible | Inválida | `ReservaInvalidaError` con causa encadenada |

El sistema continúa funcionando después de cada error.

## Archivo de logs

Al ejecutar, se crea `software_fj.log` con el formato:

```
fecha | nivel | mensaje
```

Este archivo se genera en cada ejecución y está excluido del repositorio mediante `.gitignore`.

## Flujo de trabajo colaborativo

- Cada parte se registró como un **issue** con su responsable.
- Cada integrante trabajó en su propia **rama** y entregó su aporte mediante un **Pull Request** hacia `main`.
- El historial de aportes puede consultarse en la pestaña **Insights > Contributors**.