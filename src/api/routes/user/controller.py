from flask import jsonify

from src.app import app
from src.usecase.user.usecase import UserUsecase
from src.repository.user.sqla_repo import UserRepo
from src.repository.driver.postgres import postgresql_engine


@app.route('/user', methods=['GET'])
def register_n_get():
	repo = UserRepo(postgresql_engine)
	service = UserUsecase(repo)

	# service.register('nick', 'pwdhash!')

	created_user = service.get_by_id('1')

	return jsonify(created_user.to_dict()), 200