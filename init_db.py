from app import db, app, User

def init_db():
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                user_type='admin'
            )
            admin.set_password('admin123')  # Change this password in production
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
        print("Database initialized")

if __name__ == '__main__':
    init_db()
