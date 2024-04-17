from flask_socketio import SocketIO
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flasgger import Swagger


jwt = JWTManager()
cors = CORS(supports_credentials=True)
socketio = SocketIO()

swagger_config = Swagger.DEFAULT_CONFIG
swagger_config['swagger_ui_bundle_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js'
swagger_config['swagger_ui_standalone_preset_js'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js'
swagger_config['jquery_js'] = '//unpkg.com/jquery@2.2.4/dist/jquery.min.js'
swagger_config['swagger_ui_css'] = '//unpkg.com/swagger-ui-dist@3/swagger-ui.css'

swagger = Swagger(template_file='swagger/api_docs.yaml', config=swagger_config)