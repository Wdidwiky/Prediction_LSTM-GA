from flask import Flask, render_template
from config import Config
from extensions import cache


from routes.dashboard import dashboard_bp
from routes.history import history_bp
from routes.forecast import forecast_bp
from routes.model import model_bp

app = Flask(__name__)
app.config.from_object(Config)
cache.init_app(app)

app.register_blueprint(dashboard_bp)
app.register_blueprint(history_bp)
app.register_blueprint(forecast_bp)
app.register_blueprint(model_bp)

@app.errorhandler(404)
def page_not_found(e):
    return render_template(
        "404.html"
    ),404

@app.errorhandler(500)
def internal_error(e):
    return render_template(
        "500.html"
    ),500

if __name__ == '__main__':
    app.run()