from src.app import app

import src.api.routes
import src.api.error
import src.api.sockets
import src.threads


if __name__ == '__main__':	
	app.run(port=app.config['PORT'])