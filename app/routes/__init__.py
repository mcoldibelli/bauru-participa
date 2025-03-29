from app.routes.poll_routes import poll_bp

def register_routes(app):
    app.register_blueprint(poll_bp, url_prefix="/api/enquetes")