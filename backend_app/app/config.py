import os


def configure_app(app):
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = 'MadHut'
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/swagger'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/'
    app.config['OPENAPI_SWAGGER_UI_URL'] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'

    app.config['API_SPEC_OPTIONS'] = {
        "components": {
            "securitySchemes": {
                "bearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        },
        "security": [{"bearerAuth": []}]
    }
