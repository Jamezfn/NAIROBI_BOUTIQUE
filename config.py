import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'my_password')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Development configuration with SQLite."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI', 'sqlite:///dev_app.db')
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration with SQLite."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI', 'sqlite:///test_app.db')
    TESTING = True

class ProductionConfig(Config):
    """Production configuration with SQLite."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('PROD_DATABASE_URI', 'sqlite:///prod_app.db')
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
