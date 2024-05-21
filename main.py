
from typing import Union

from fastapi import FastAPI, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel


from lib.apis import methods
from lib.apis import request
from lib.apis import status
from lib.apis import redirect
from lib.apis import redirect_final
from lib.apis import anything
from lib.apis import response
from lib.apis import response_formats
from lib.apis import cookies
from lib.apis import images
from lib.apis import dynamic
from lib.apis import qrcode
from lib.apis import test_password_manager
from lib.apis import meta

from lib.fastapi import tags_metadata, description, app_version

import json


app = FastAPI(docs_url = "/", redoc_url = None,
    title = "FastAPI Httpbin",
    description = description,
    version = app_version,
    swagger_ui_parameters = {"docExpansion":"none"},
    openapi_tags = tags_metadata
    )

app.openapi_version = '3.0.2'
app.openapi_url = '/oas-httpbin/openapi.json'

# Assuming your JSON file is named 'schema.json'
json_file_path = './openapi_schema.json'

# Read content from the JSON file
with open(json_file_path, 'r') as file:
    json_content = file.read()

# Parse JSON content
try:
    openapi_schema = json.loads(json_content)

    openapi_schema["info"]["description"] = description
    # openapi_schema["info"]["version"] = app_version
    # openapi_schema["tags"] = tags_metadata

    app.openapi_schema = openapi_schema

    print("JSON content loaded successfully.")
except json.JSONDecodeError as e:
    print("Error decoding JSON:", e)

#
# Ordering of these in the Swagger docs is set in lib/fastapi.py
#
app.include_router(methods.router, tags = ["HTTP Methods"])
app.include_router(status.router, tags = ["Status Codes"])
app.include_router(request.router, tags = ["Request Inspection"])
app.include_router(response.router, tags = ["Responses"])
app.include_router(response_formats.router, tags = ["Response Formats"])
app.include_router(redirect_final.router, tags = ["Redirects"])
app.include_router(qrcode.router, tags = ["QR Codes"])
app.include_router(redirect.router, tags = ["Redirects"])
app.include_router(anything.router, tags = ["Anything"])
app.include_router(cookies.router, tags = ["Cookies"])
app.include_router(images.router, tags = ["Images"])
app.include_router(dynamic.router, tags = ["Dynamic Data"])
app.include_router(test_password_manager.router, tags = ["Forms"])
app.include_router(meta.router, tags = ["Meta"])

#
# Load some static resources
#
app.mount("/about", StaticFiles(directory = "static/about", html = True), name = "static")
app.mount("/roadmap", StaticFiles(directory = "static/roadmap", html = True), name = "static")
app.mount("/qrcode", StaticFiles(directory = "static/qrcode", html = True), name = "static")
app.mount("/test-password-manager-form", StaticFiles(directory = "static/password-manager", html = True), name = "static")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-FastAPI-Httpbin-version"] = app_version
    response.headers["X-Website"] = "https://httpbin.dmuth.org/"
    return response


favicon_path = "static/favicon.jpg"
@app.get('/favicon.ico', summary = "Favicon endpoint", tags = ["Images"],
    response_class = FileResponse,
    responses={
        200: {
            "content": {"image/jpeg": {}},
            "description": "Return a 32x32 favicon in JPG format.",
        }
    }
    )
async def favicon(response: Response):
    return FileResponse(favicon_path)

logo_path = "img/logo.png"
@app.get('/static/logo.png', summary = "Logo endpoint", tags = ["Images"],
    response_class = FileResponse,
    responses={
        200: {
            "content": {"image/jpeg": {}},
            "description": "Return the logo.",
        }
    }
    )
async def logo(response: Response):
    return FileResponse(logo_path)



