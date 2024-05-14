from app import app, db # type: ignore
from app.models import User # type: ignore

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}