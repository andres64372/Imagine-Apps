# Aplicación CRUD con FastAPI

Esta es una aplicación de ejemplo creada con FastAPI, un moderno marco web para construir APIs rápidas en Python.

## Documentación de la API

Puede acceder a la documentación de la API generada automáticamente visitando la ruta `/docs` una vez que la aplicación esté en funcionamiento. Esta documentación interactiva proporcionada por Swagger UI le permite explorar y probar los puntos finales de la API de manera sencilla.

Para acceder a la documentación abra su navegador y vaya a:
http://imapp.azurefd.net/docs

## Infraestructura

- Esta aplicación fue desplegada en un cluster de kubernetes de azure
- La base de datos PostgreSQL está hosteada en NeonDB.
- Para acceder al recusro de kubernetes se creó un perfil de frontdoor el cual contiene la url imapp.azurefd.net apuntando al balanceador de cargas de kubernetes