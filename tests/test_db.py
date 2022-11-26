def test_db(config):
    assert config['SQLALCHEMY_DATABASE_URI'] != 'sqlite:///tarefas.db'
