import azure.functions as func
import logging
import httpx
#import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
@app.route(route="ejecutar/{id}")
def ejecutar(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Function ejecutar se ejecutó con un ID.')
    # Obtiene el id de la URL
    id_value = req.route_params.get("id")

    url = "https://adb-1489268997299702.2.azuredatabricks.net/api/2.0/jobs/run-now"
    headers = {
        "Authorization": "Bearer dapi5bbfa9ac673d27b9987df217e913827a-3",
        "Content-Type": "application/json"
    }
    data = {
        "job_id": id_value,
    
    }
    try:
        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            result = response.json()
            return func.HttpResponse(
                f"✅ Job {id_value} ejecutado correctamente. Respuesta: {result}",
                status_code=200
            )
        else:
            return func.HttpResponse(
                f"❌ Error al ejecutar el job {id_value}. "
                f"Status: {response.status_code}, Respuesta: {response.text}",
                status_code=response.status_code
            )
    except Exception as e:
        logging.error(f"Error en la petición: {e}")
        return func.HttpResponse(
            f"⚠️ Ocurrió un error al enviar el POST: {str(e)}",
            status_code=500
        )
@app.route(route="http_freddy")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        r = httpx.get("https://api.github.com")
        return func.HttpResponse(
            f"Llamada exitosa, código: {r.status_code}",
            status_code=200
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        return func.HttpResponse(
            "Error al procesar la solicitud.",
            status_code=500
        )
