from fastapi import FastAPI, Request
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
import json
import os
import logging


app = FastAPI()

# Set up the logger
logging.basicConfig(filename='logs.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger('__api__')


@app.get("/", response_class=HTMLResponse)
async def custom_api_homepage():
    """
    Welcome to Free Proxy API.

    Returns:
        str: HTML response with a welcome message and a link to the API documentation.
    """
    return """
    <h1>Welcome to Free Proxy API</h1>
    <p>API documentation is available at <a href="/docs">/docs</a>.</p>
    """


@app.get("/live-proxy-list", name="Get newest free proxies (refreshes every 5 minutes)")
async def get_newest_proxies(request: Request):
    """
    Get the newest proxies from the data file.

    Args:
        request (Request): The incoming request object.

    Returns:
        list: The newest proxies from the data file.
    """
    logger.info(f"Request received from {request.client.host} to get the newest proxies")

    with open(os.path.abspath('http-proxy-list/proxy-list/data-with-geolocation.json'), "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            # Find the newest timestamp in the data
            newest_timestamp = max(d.get("timestamp", 0) for d in data)

            # Filter out dictionaries that have an old timestamp
            filtered_data = [d for d in data if d.get("timestamp", 0) == newest_timestamp]

            logger.info(f"{len(filtered_data)} newest proxies returned to {request.client.host}")
            return filtered_data
        else:
            logger.error(f"Error: data is not a list. Request received from {request.client.host}")
            return data


@app.get("/proxy-list", name="Get free proxies from last 24 hours")
async def get_proxy_list(request: Request):
    """
    Get the proxy list from the data file.

    Args:
        request (Request): The incoming request object.

    Returns:
        list: The free proxies from the data file from the last 24 hours.
    """
    logger.info(f"Request received from {request.client.host} to get the proxy list")

    with open(os.path.abspath('http-proxy-list/proxy-list/dumped_data.json'), 'r') as f:
        json_data = json.load(f)

    logger.info(f"{len(json_data)} proxies returned to {request.client.host}")
    return json_data


# Generate OpenAPI schema with proper tags and descriptions
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Free Proxy API",
        version="1.0.0",
        description="Providing free proxies for any use",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)