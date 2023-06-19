

def deploy():
    """Run deployment tasks."""
    from apps import create_app, db
    from flask_migrate import upgrade, migrate, init, stamp
    from apps.home.models import AText

    app = create_app()
    app.app_context().push()

    # create database and tables
    db.create_all()

    # migrate database to latest revision
    stamp()
    migrate()
    upgrade()


deploy()
