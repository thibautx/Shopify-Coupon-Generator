from flask import Flask, render_template
from flask_admin import Admin
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['DATABASE_URI'] = 'sqlite:///app.db'

# Configurations
app.config.from_object('config')

db = SQLAlchemy(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)


# Admin
from flask_admin.contrib.sqla import ModelView
from api.models import Discount
admin = Admin(app, 'Admin', template_mode='bootstrap3')
admin.add_view(ModelView(Discount, db.session))

@app.errorhandler(404)
def not_found(error):
    return '404'


# Register blueprints
from app.api.controllers import api_module as mod_api
app.register_blueprint(mod_api)

db.create_all()

@app.route('/')
def landing_page():
    return render_template('index.html')