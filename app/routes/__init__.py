from app.routes.poll_routes import poll_bp
from app.routes.user_routes import user_bp

def register_routes(app):
    app.register_blueprint(poll_bp, url_prefix="/api/enquetes")
    app.register_blueprint(user_bp, url_prefix="/api/usuarios")