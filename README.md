# soriana_search_engine_AWS_API
#### Consumición de API REST a través de los servicios de AWS y FastAPI
#### Cliente: Soriana.
---
## Objetivo
Deployar la REST API creada en un entorno local para realizar queries sobre la base de Typesense en la nube. 
La API debe poder ser consumida tanto a nivel URL como UI (Swagger).

![Workflow](https://github.com/JuanMartinElorriaga/soriana_search_engine_AWS_API/blob/master/search_engine/references/serverless_soriana)

## Requisitos
- AWS Account (API Gateway, Lambda, S3)
- AWS CLI instalado en el entorno local para correr los comandos a través de la terminal
- Typesense Account & servidor corriendo (de preferencia, Sao Paulo)
- FastAPI; Uvicorn; Mangum (librerías de Python)

### FastAPI
- FastAPI es un framework de Python para construcción de API's, preparado para deployar directamente en producción.
- FastAPI utiliza de fondo Uvicorn, que es el servidor que por detrás corre la infra necesaria.
- Asimismo, se utiliza la librería Mangum como adaptador para usar aplicaciones ASGI con AWS Lambda y API Gateway. Dicho adaptador routea los request a la API Gateway y también los resultados de Lambda de vuelta a la API Gateway. Todo esto simplemente importando la librería y colocando la línea `handler = Mangum(app=app)`.

_Nota: ASGI (Asynchronous Server Gateway Interface) es el sucesor de WSGI, que provee una interfaz estándar entre web servers, frameworks y apps de Python en forma asíncrona._


### API Gateway
API Gateway representa el enrutador de peticiones por parte del usuario final, enviando las solicitudes para su procesamiento a través de las funciones Lambda.

### Lambda function
Lambda es un servicio serverless que permite correr código en diferentes runtimes (en este caso, Python). En este caso, sirve para ejecutar el código que interpreta, parsea y retorna el resultado de la query por parte del usuario sobre el servicio de Typesense.

### S3
S3 es un tipo de storage que permite almacenar diversos recursos. En este caso, se utiliza para almacenar la función Lambda en un archivo .zip, para promover escalabilidad y mayor facilidad en la actualización del código.

## Procedimiento
- Configurar cuenta en Typesense (alternativa open-source y typo-sensitive a ElasticSearch) y levantar un servidor. Es notable la diferencia de latencias cuando se usa el servidor de Sao Paulo en lugar de Estados Unidos. Tener en cuenta este detalle a la hora de deployar en producción.
- Verter contenido de testing sobre alguna base de Typesense. Esto puede hacerse tanto en forma manual mediante la interfaz o en forma de bulk mediante la API.
- Instalar las librerías FastAPI y Uvicorn en el entorno local.
- Testear la API en un entorno local: `uvicorn main:app --reload`. Si se conserva el puerto por default, revisar en: `http://localhost:8000/docs`.
- Crear un nuevo environment _(recomendación: usar virtualenv, ya que crea una carpeta de librerías dependientes que luego puede conservarse dentro del .zip de la función Lambda)_
- Empaquetar el código en formato .zip. Es importante que las dependencias de paquetes se encuentren dentro del .zip.
- Upload .zip a un S3, al cual luego Lambda se dirigirá para correr el código. La razón por la cual no se sube directamente a Lambda es porque hay un límite de almacenamiento de 10MB, con lo cual es mejor usar S3 como storage.
- Crear función Lambda con runtime Python. Es importante usar la opción _"Create a new role with basic Lambda permissions"_, para que la función tenga acceso suficiente al S3. Además, configurar el handler para que sea `main.handler`, ya que dicho handler se encuentra en el root y en el archivo `main`.
- Actualizar la función creada para que se dirija al S3 para buscar el código. Se puede realizar mediante CLI (o desde la Management Console): `aws lambda update-function-code --function-name medium-demo --s3-bucket $bucket_name --s3-key lambda.zip`.
- Crear la REST API con API Gateway _(la versión pública)_. Importante: la región debe ser la misma que la función Lambda para minimizar latencias.
- Chequear la opción de API Gateway proxy, para que el contenido de la HTTP request se transmita al parámetro `event` de la función Lambda. 
- En el caso de querer habilitar cualquier tipo de método, crear un Method con la opción `ANY` (incluye `GET, POST, PATCH, ...`), y un child Resource a partir de dicho método con el proxy integration, para routear todas las request por debajo del root `\` Dejar el resto de parámetros en default.
- Deployar API
- Testear el endpoint

---
### Notas 
- Para cambiar la url del endpoint, debe usar un Custom Domain Name.
- `{proxy+}` se usa para evitar escribir templates de mapeo entre las diferentes funciones Lambda. Acá, solo se una una única función para todos los endpoints. 
- Las request a la API Gateway pueden ser miles y procesadas en paralelo, garantizando escalabilidad.
- Para garantizar la seguridad de la API, es necesario integrar Cognito al sistema.
- Este sistema también puede ser adaptable al _Serverless Framework_ y a _AWS SAM_.

## Referencias
https://fastapi.tiangolo.com/

https://github.com/tiangolo/fastapi

https://www.youtube.com/watch?v=6fE31084Uks

https://towardsdatascience.com/fastapi-aws-robust-api-part-1-f67ae47390f9


## Resultado final
https://vb0wy8ppki.execute-api.us-east-2.amazonaws.com/dev/

Para ver en forma de UI (Swagger):

https://vb0wy8ppki.execute-api.us-east-2.amazonaws.com/dev/docs#/default/get_query__get
