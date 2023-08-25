from py_dotenv import read_dotenv
import os
import booyah

os.environ["ROOT_PROJECT_PATH"] = os.getcwd()
read_dotenv('.env')
print('Spinning up environment [' + os.getenv('BOOYAH_ENV') + ']')

from booyah.router.application_router import ApplicationRouter
from booyah.config.routes import ApplicationRoutes


def application(environment, start_response):
    ApplicationRoutes.load_routes()
    router = ApplicationRouter.get_instance()
    response = router.respond(environment)
    response_body = response.response_body()

    start_response(response.status, response.response_headers())
    return iter([response_body])