# Artifact - Prototipo 2 - RacconAnalytics

## Grupo 2F

- Juan David Buitrago Salazar
- Juan David Serrano Ruiz
- Federico Hernández Montaño
- Johan Stiven Sarmiento Torres
- Daniela Ariadna Rueda Hernández
- Luis David Garzón Morales
- Miguel Angel Citarella Camargo
- David Felipe Chaparro Pérez
- Andrés Felipe León Sánchez

## Software system
### Name

Raccon Analytics

### Logo

![](./images/logo.jfif)

### Description

El proyecto consiste en el desarrollo de una aplicación web orientada al análisis de tendencias de contenido en plataformas digitales. El sistema permitirá a los usuarios realizar búsquedas sobre temas específicos y visualizar indicadores que reflejen el nivel de actividad, popularidad y relevancia del tema dentro de distintas plataformas sociales. En el primer prototipo del sistema, el análisis se enfocó principalmente en contenido proveniente de YouTube. Para este segundo prototipo, el sistema integra dos nuevos componentes lógicos: un componente de consulta de Google Trends y un componente de Procesamiento de lenguaje natural, para expandir semánticamente la búsqueda del usuario y mostrar tendencias de búsqueda, complementando así el análisis proveniente de Youtube.

El funcionamiento general de la aplicación se basa en que el usuario ingresa una consulta relacionada con un tema de interés. A partir de esta consulta, el sistema realizará solicitudes a las APIs disponibles de las plataformas objetivo y recopilará información sobre contenido relacionado con dicha búsqueda. Posteriormente, la aplicación procesará los resultados obtenidos para generar estadísticas básicas que permitan evaluar la relevancia del tema dentro de cada plataforma.

El propósito de la plataforma no es únicamente mostrar resultados de búsqueda, sino ofrecer una visión agregada del comportamiento del contenido asociado a un tema. Esto permitirá identificar tendencias, evaluar la popularidad de ciertos tópicos y detectar contenido relevante dentro de comunidades digitales.

El alcance de este segundo prototipo del sistema está limitado a la recopilación y análisis de métricas básicas disponibles a través de las APIs públicas de las plataformas seleccionadas: Youtube y Google trends, complementando la búsqueda del usuario con su expandimiento en búsuqedas relacionadas por el Procesamiento de lenguaje natural. Debido a las restricciones propias de estas APIs, tales como límites diarios de consultas o disponibilidad limitada de ciertos tipos de información, el sistema priorizará la obtención de datos esenciales que permitan generar indicadores representativos del comportamiento del contenido.

### **Lenguajes de propósito general:**
Para el desarrolllo del sistema se usaron los siguientes lenguajes de programación de propósito general:
- Python
- Typescript
- Java
- Go
- C#

## **Architectural Structures**

### **Component-and Connector (C&C) Structure**

#### C&C View:

![](./images/Vista-C&C.jpeg)

#### **Architectural styles**

La aplicación emplea un estilo arquitectónico de Microservicios, caracterizado por su naturaleza distribuida y el alto grado de autonomía de sus componentes. La comunicación externa se gestiona mediante el patrón API Gateway, que actúa como un punto de entrada único para los componentes de presentación (frontend Web y Desktop), desacoplando la capa de presentación de la lógica interna del sistema.

Este diseño permite la orquestación y el enrutamiento hacia servicios especializados que operan de manera independiente y poseen su propia persistencia de datos:

- *Servicio de Adquisición de Datos de YouTube:* Se encarga de capturar información en tiempo real (tendencias, videos registrados y mátricas de anaálisis de red socisal) mediante la integración con la API externa de YouTube V3. 

- *Servicio de Gestión de Usuarios:* Administra el ciclo de vida de las cuentas, permitiendo el registro y la autenticación de usuarios de forma aislada, garantizando que la lógica de identidad no interfiera con las funciones de búsqueda.

- *Servicio de Adquisión de Datos de Google Trends*: Captura información sobre la tendencia de la búsqueda del usuario, como el volumen de consulta de la temática a través del tiempo. 

- *Procesamiento de Lenguaje Natural*: Este componente se apoya sobre un servicio de API externo de Nvidia para realizar Procesamiento de Lenguaje Natural (NLP) sobre la búsqueda del usuario y expandir semánticamente la consulta hallando posibles búsquedas o entradas de usuario relacionadas. 

Los componentes son reutilizables, escalables independientemente y se comunican principalmente a través de protocolos ligeros (HTTP: REST y Streaming), lo que refuerza la agilidad y el bajo acoplamiento del sistema.

#### **Architectural elements and relations**

Nuestro sistema cuenta con:
- **2 Componentes de presentación: Presenta a través de KPIs, gráficos analíticos y métricas importantes, los datos retornados por los servicios lógicos.**
    - **Frontend web:** Desarrollado en Typescript usando el framework Next JS para implementar Server Side Rendering. Se limita a la interfaz web, cuya responsabilidad es renderizar la información suministrada por los servicios lógicos a través del API Gateway
    - **Frontend de escritorio:** Desarrollado en C#. Permite al usuario interactuar desde la app con interfaz de escritorio mostrando la infmración suministrada por los servicios lógicos a través del API-Gateway
    
- **5 Componentes lógicos:**   
   - **Orquestador (API Gateway):** Punto de entrada y enrutamiento. Actúa como mediador, manejando las peticiones hacia el servicio de adquisición de YouTube y el de gestión de usuarios. Provee una interfaz unificada para el frontend, ocultando la complejidad de la arquitectura distribuida. Desarrollado en el lenguaje de propósito general Go.
    - **Users Management Service**: Gestiona el ciclo de vida de los usuarios (registro e inicio de sesión), exponiendo recursos de autenticación. Desarrollado en TypeScript.
    - **Youtube Data Acquisition Service**: Orquesta la extracción de datos externos. Procesa la query del usuario, consulta la API de YouTube, cálcula métricas y estandarizada los datos para ser presentados en el front. Desarrollado en el lenguaje Python.
    - **Google Trends Data Acquisition Service**: Maneja la extracción de datos de tendecias de búsquedas, consultando la API externa de Google Trends, enriqueciendo la información retornada por el componente de Youtube. Desarrollado en lenguaje de propósito general Python.
    - **Natural Language Processing Service**:  Implementa la lógica de IA. Diseña prompts específicos para expandir la búsqueda del usuario a partir de hallazgo de posibles bbúsquedas relacionadas. Desarrollado en el lenguaje Java.
    
- **4 Componentes de Datos:**
    - *Base de datos relacional Users*: Repositorio centralizado para la información básica y credenciales de acceso de los usuarios.
    - 2 Bases de datos No SQL:
        - *Youtube Historical Search Keywords:* Almacenamiento persistente de los datos estandarizados y retornados por la API externa de Youtube.
        - *Google Trends Historical Search Keywords:* Almacena los datos retornador por la API externa de Google Trends
     - *Almacenamiento de datos Caché:* Componente de almacenamiento volátil que almacena los datos retornados por la API externa de Youtube para mejorar el rendimiento del componente lógico y el uso limitado de la API externa.
  
- **5 Componentes externos**
    - Web browser: Consume el contenido web para renderizar la interfaz web.
    - OAuth Google API
    - External Youtube API
    - External Google Trends API
    - Nvidia NIM API 

#### **Architectural pattern**
Se implementó un patrón arquitécnico con un componente orquestador que hace referencia al API-gateway, evitando que los componentes de presentación adquieran una responsabilidad de sincronización de lógica de negocio que no es responsabilidad natural en la capa de presentación. Este componente es el punto único de entrada el sistema de análisis de tendencias. Recibe las solicitudes del cliente, enruta las peticiones al microservicio correspondiente, gestionando autenticación, validación y contro de acceso. De esta manera, se desacopla al cliente de la arquitectura interna basada en microservicios y simplifica la comunicación.

---
### **Layered Structure**

#### **Logic layers**
Para complementar la vista por capas de todo el sistema, se establecieron de igual forma la estructura de capas lógicas o subarquitectura de los componentes lógicos a continuación:

![](./images/Layered-Architecture-view-Logic-layers.png)

---

##### YouTube Acquisition Data Service Sub-architecture

![](./images/youtube.png)

Este componente implementa la lógica de adquisición, procesamiento y almacenamiento de datos provenientes de la API de YouTube.

- *Controllers* (/analyze, /healthy):
  Actúan como punto de entrada HTTP. Delegan la lógica al Orchestrator-service y al Cache-service.

- *Cache-service*:
  Gestiona la verificación de resultados previamente calculados.  
  - Flechas verdes: puede ser invocado por los controllers y el orquestador para evitar llamadas redundantes.
  - Flechas rojas: persiste información auxiliar como Quota_log en el repositorio.

- *Orchestrator-service*:
  Coordina el flujo principal del análisis.
  - Flechas verdes: invoca servicios permitidos como Transformer-service.
  - Flechas rojas: invoca hacia abajo a Youtube_client-service para consumir la API externa.

- *Youtube_client-service*:
  Encapsula las llamadas a la API de YouTube. Solo es invocado por el orquestador (flecha roja).

- *Transformer-service*:
  Se encarga de mapear y normalizar la respuesta de la API hacia los modelos internos.
  - Flechas verdes: interactúa con Models / Schemas.

- *Repositories* (Quota_log, Analysis_repository):
  Persisten datos en MongoDB.
  - Flechas rojas: indican escritura desde servicios superiores.
  - Flechas verdes: permiten acceso controlado a los modelos.

- *Models / Schemas*:
  Definen la estructura tipada de los datos del sistema. Son utilizados por el transformer y los repositorios.

---

##### Google Trends Service Sub-architecture

![](./images/Google_Trends.png)

Este servicio obtiene y procesa tendencias desde Google Trends.

- *Controllers* (/interest_over_time, /bulk-interest, /related_queries):
  Exponen endpoints que delegan la lógica al Trends service.

- *Key build generator*:
  Genera claves normalizadas para consultas y almacenamiento.
  - Flechas verdes: puede ser invocado por controllers.
  - Flechas rojas: persiste información en Repositories.

- *Trends service*:
  Orquesta la lógica de negocio.
  - Flechas rojas: invoca a PyTrends client para consumir la API externa.

- *PyTrends client*:
  Cliente que encapsula la comunicación con Google Trends.
  - Flechas verdes: entrega datos hacia Models / Schemas.

- *Repositories*:
  Persisten resultados procesados.
  - Flechas verdes: interactúan con los modelos.

- *Models / Schemas*:
  Definen la estructura de datos utilizada en el servicio.

---

##### NLP Service Sub-architecture

![](./images/NLP_Service.png)

Este servicio se encarga del procesamiento de lenguaje natural para enriquecer las consultas.

- *Controllers* (/inference, /health):
  Exponen endpoints para inferencia y monitoreo.

- *Prompt Builder Service*:
  Construye prompts estructurados para el modelo NLP.
  - Flechas verdes: interactúa con Models / Schemas.

- *Nvidia Nim Service*:
  Ejecuta la inferencia usando modelos de IA.
  - Flechas verdes: también utiliza los modelos definidos.

- *Models / Schemas*:
  Representan la estructura de entrada/salida del procesamiento NLP.

---

##### Users Service Sub-architecture

![](./images/users_service.png)

Gestiona autenticación, usuarios y servicios relacionados.

- *Controllers*:
  Contienen endpoints de autenticación, OAuth, recuperación de cuenta y perfil de usuario.

- *AuthService*:
  Núcleo de la lógica de autenticación.
  - Flechas verdes: interactúa con otros servicios como RateLimitService y UsersService.

- *AuthAuditService*:
  Registra eventos de autenticación.
  - Flechas rojas: persiste logs en Repositories.

- *RecoveryMailService*:
  Gestiona recuperación de cuentas vía correo.
  - Flechas rojas: escribe en repositorios.

- *RateLimitService*:
  Controla la tasa de solicitudes hacia el sistema.

- *UsersService*:
  Gestiona información de usuarios.
  - Flechas verdes: interactúa con Models / Schemas.

- *Repositories* (PrismaService):
  Acceso a la base de datos relacional.
  - Flechas rojas: reciben escritura desde servicios.

- *Models / Schemas*:
  Definen estructuras de datos para usuarios y autenticación.

---

### Decomposition View

![](./images/Vista_Descomposicion.png)

---

### Deployment View

![](./images/Vista_Despliegue.png)
___
## **Prototype**
### Intructions

*Prerrequisitos:* 
- El despliegue de este sistema está orientado a contenedores, usando Docker y docker compose.
Por tanto, si se desea hacer el despliegue orientado a contenedores solo se necesita tener Docker en el equipo.

- Si se desea hacer el despliegue de forma local sin contenedroes, Se deben tener las siguientes aplicaciones instaladas en el sistema:
    - API Gateway (Go)
        - Go 1.22 (según api-gateway/go.mod)
        - Variables de entorno de servicios dependientes (URLs a users/youtube/etc.) en .env (api-gateway/README.md)
      
    - Google Trends Acquisition Service
        - Python 3.11+ y pip
        - FastAPI + Uvicorn + Pytrends + Motor/PyMongo (requirements en google-trends-acquisition-service/requirements.txt)
        - MongoDB (cache y TTL, ver app/db/cache_repository.py)
        - Variables de entorno .env (ver google-trends-acquisition-service/README.md)

    - YouTube Acquisition Service
        - Python 3.11+ y pip
        - FastAPI + Uvicorn + Motor/PyMongo + Redis client (ver youtube-acquisition-service/requirements.txt)
        - MongoDB (persistencia) y Redis (cache)
YouTube Data API v3 key (configuración en .env)

    - NLP Service (NVIDIA NIM)
        - Java 17 (maven compiler 17) + Maven (ver nlp-service-nvidia/pom.xml)
        - Spring Boot
        - API key de NVIDIA NIM (nvidia.nim.api.key) en variables de entorno o properties (application.properties)

     - Users Service
        - Node.js + npm
        - NestJS + TypeScript (ver users-service/package.json)
        - PostgreSQL (usado por Prisma)
        - Redis (sesiones/cache)
        - Variables de entorno .env (ver users-service/README.md)
Web Frontend (Next.js)

        - Node.js + npm/yarn/pnpm
        - Next.js + React (ver web-page/package.json)
        
    - Desktop Frontend (WPF)
        - Windows
        - .NET SDK 10 (target net10.0-windows) + WPF (ver desktop-frontend/desktop-frontend.csproj)

___
**Pasos para despliegue:**
El sistema se distribuye utilizando una estrategia de repositorio tipo umbrella, donde un repositorio principal actúa como orquestador y contiene referencias a los distintos microservicios mediante submódulos de Git.

Este enfoque permite mantener cada componente desacoplado, pero coordinado desde un único punto de entrada para facilitar el despliegue.

1. Clonar el repositorio principal: El repositorio prototype-2 actá como orquestador y punto de entrada para despliegue al tener punteros que referencian cada uno de los repositorios de cada componente del sistema. Se clonan de forma recursiva los repositorios apuntados desde prototype-2 con el comando a continuación.

```bash
git clone --recurse-submodules https://github.com/RacconAnalytics/prototype-2.git
```


*Notas:*
- *Si ya clonó antes el repositorio ejecute el siguiente comando para sincronizar todos los subrepositorios bajo prototype-2*
```bash
git submodule update --init --recursive
```

- *Para evitar problemas de despliegue por contenedores ya existentes en el equipo de despliegue que puedan tener el mismo nombre que los contenedores referenciacos aquí, o porqué ya hay contenedores corriendo en puertos a ser usados, se opta por ejecutar los siguiente comandos:*

```bash
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

2. Ejecutar el docker compose: Este comando permite levantar todos los contenedores por cada uno de los componentes del sistema a partir de un docker compose que actua como orquestador de despliegue desde el repositorio principal prototype-2.

```bash
docker compose up -d --build
```

Con todos los contenedores activos, teniendo los componentes en ejecución, ya es posible acceder y probar sistema desde la interfaz web, ingresando al puerto 3000 en localhost:
**http://localhost:3000**



