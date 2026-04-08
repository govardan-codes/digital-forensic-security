from flask import Flask, render_template
from config import Config
from extensions import db, migrate, login_manager
import json

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize shared extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

     # ✅ Register Jinja filter for JSON loading
    app.jinja_env.filters['loads'] = json.loads

    login_manager.login_view = "auth_bp.login"
    login_manager.login_message_category = "warning"


    # Import models AFTER db.init_app
    from models import user, sbvm, evidence, key, verification, blockchain, audit

    # Register blueprints
    from routes.main import main_bp
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.investigator import investigator_bp
    from routes.verifier import verifier_bp
    from routes.evidence import evidence_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(investigator_bp)
    app.register_blueprint(verifier_bp)
    app.register_blueprint(evidence_bp)

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
