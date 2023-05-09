from application import application, db

application.app_context().push()
db.create_all()
