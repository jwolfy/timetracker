from app import create_app


def test_app_is_created(app):
    assert app.name == 'app'


def test_default_app_config_is_populated():
    app = create_app()
    assert app.config['SECRET_KEY'] == 'secretkey'
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] is False


def test_app_config_is_populated_from_config_file(app):
    from testing_config import Config as TestingConfig
    assert app.config['SECRET_KEY'] == TestingConfig.SECRET_KEY
    assert app.config['SQLALCHEMY_DATABASE_URI'] == TestingConfig.SQLALCHEMY_DATABASE_URI
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == TestingConfig.SQLALCHEMY_TRACK_MODIFICATIONS
