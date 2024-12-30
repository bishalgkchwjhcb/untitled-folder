from flask import Flask, render_template
from config import Config
from models import db, login_manager, User, Attendance

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    with app.app_context():
        db.create_all()

        # Import routes
        from routes import auth, student, admin

        # Register blueprints
        app.register_blueprint(auth.bp)
        app.register_blueprint(student.bp)
        app.register_blueprint(admin.bp)

        # Home route
        @app.route('/')
        def home():
            return render_template('home.html')

        return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5002)
