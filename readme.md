# MatchStatus service

## Introducción
Este microservicio es parte de la aplicación [Footmatch](https://github.com/orgs/Football-FIS/repositories), proyecto para la asignatura "*Fundamentos de Ingeniería Software para Cloud*" del "*Máster en Ingeniería del Software: Cloud, Datos y Gestión TI*" en la *Universidad de Sevilla*.

La función de este microservicio es la creación de eventos asociados a un partido. Además, proveerá al microservicio "*match-service*" del marcador del partido y diferentes eventos, con el tiempo en que ocurrieron.

### Autores
- Diego Monsalves Vázquez
- Víctor Manuel Vázquez García


## Tecnologías
Para el desarrollo de este microservicio se han usado las siguientes tecnologías:

 - **Django** (backend)
 - **MongoDB** (BBDD NoSQL)
 - **Swagger** (documentación API)
 - **Djongo** (conector MongoDB - Django)
 - **Docker** (gestor de contenedores)
 - **Okteto** (despliegue en cloud)


## APIs relacionadas
Se ha usado la API Rest **Tweepy** para la publicación de tweets con los estados que se van generando a lo largo de un partido. Este tweet mostrará el marcador, los equipos que estan jugando, un campo de descripcion del evento y la hora donde ocurre ese evento.
Este envío de tweets se hará siempre que se cree un estado para cualquier partido, y obtendrá la información del mismo.

Un ejemplo sería: 

09:24' | Mures CF 1-2 UD Pilas
Final del partido

Para poder consultar la creación de dicho tweet, debemos irnos hasta el perfil de Diego Monsalves Vázquez (@demvazquez), destacar que este perfil es privado, y cuando se requiera el uso para poder puntuar este proyecto, deberán avisar vía mail a diegomonsalvesvazquez@gmail.com o por teams para poder abrirlo, y así ser puntuado.

## Requisitos de proyecto
Comenzamos aspirando a una calificación de 9, pero por falta de tiempo, pese a tener algunos requisitos de 9, tanto la aplicación cumplen los requisitos para una **calificación de 7+**. A continuación se listarán los requisitos, así como las distintas evidencias:

### Microservicio avanzado

 - **Rutas y navegación**: se ha implementado el control de rutas y navegación con respecto al frontend. Además, se ha controlado el uso de componentes tal y como se explica en la documentación de la asignatura, perteneciendo cada uno de los componentes a un microservicio diferente. Puede apreciarse en el fichero de configuración de rutas de Angular [app-routing.module.ts](https://github.com/Football-FIS/footmatch-frontend/blob/develop/src/app/app-routing.module.ts).
 - **Caché frontend**: se implementa una caché de tipo localStorage para listar "mis partidos", para agilizar la carga de esta. Puede apreciarse en las funciones "*getMyMatchesInCache*" y " *setMyMatchesInCache*" dentro de los ficheros [match.service.ts](https://github.com/Football-FIS/footmatch-frontend/blob/develop/src/app/services/matchStatus.service.ts) y [my-matches.component.ts](https://github.com/Football-FIS/footmatch-frontend/blob/develop/src/app/my-matches/match.component.ts).
 - **Consumir API externa**: se consume la API Rest Tweepy. Puede apreciarse en la función "*post*" de *SendTweet* del fichero [views.py](https://github.com/Football-FIS/match-status-service/blob/main/matchStatus/matchStatus_API/views.py).
 - **Autenticación JWT**: permite realizar operaciones en función de los permisos del usuario y de si los partidos son de su propiedad. Se redirecciona la cabecera "*Bearer*" al microservicio "*team-service*". Puede apreciarse en la función "*validate_token*" del fichero [views.py](https://github.com/Football-FIS/match-status-service/blob/main/matchStatus/matchStatus_API/views.py).
 - **Tests backend**: estos comenzaron a realizarse, pero por falta de tiempo tuvieron que quedarse en 'stand by'. Pese a ello se adjunta 1 funcional en tests.py.
 - **Git flow**: pese a la escasez de tests, se implementa el recorrido de GitFlow, visual desde la pestaña de [Actions](https://github.com/Football-FIS/match-status-service/actions) en GitHub.


### Aplicación basada en microservicios avanzados

 - **Frontend común que integra otros frontends**: han colaborado todos los equipos con sus correspondientes componentes en el servicio [footmatch-frontend](https://github.com/Football-FIS/footmatch-frontend).
 - **Mecanismo de autenticación común (JWT)**: todos los microservicios validan el token JWT para obtener el usuario y validar si puede realizar dicha operación.
 - **ElectronJS**: permite compilar la aplicación como aplicación de escritorio. Puede observarse en el servicio [footmatch-frontend](https://github.com/Football-FIS/footmatch-frontend) en los ficheros [package.json](https://github.com/Football-FIS/footmatch-frontend/blob/develop/package.json) y [main.js](https://github.com/Football-FIS/footmatch-frontend/blob/develop/main.js).

### Otros requisitos

 - Determinar el coste de cada plan del customer agreement
 - API Rest documentado con Swagger
 - 4 características de microservicio avanzado
 - 3 características de aplicación basada en microservicios avanzados


## Lanzar aplicación

### Local
Opción recomendable para depuración. Requiere tener instalado python así como las librerías contenidas dentro del "*requirements.txt*".

    python ./matchStatus/manage.py runserver

### Docker
Opción recomendable para iniciar el servicio sin tener en cuenta las dependencias. Requiere tener habilitada la virtualización en el sistema operativo (en Windows el WSL2) y Docker instalado.

    docker -> docker compose up

### Docker-service
Opción para desplegar todos los microservicios al completo. Requiere los mismos requisitos que Docker. Para más información mirar: https://github.com/Football-FIS/match-status-service


## SWAGGER
Documenta las posibles peticiones así como los modelos y posibles respuestas de la API Rest de este microservicio.
**Local**: http://localhost:8000/api/v1/docs/
**Producción**: https://match-status-service-danaremar.cloud.okteto.net/api/v1/docs/
