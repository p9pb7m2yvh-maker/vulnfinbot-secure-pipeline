"""Mini-VulnFinBot: простой финансовый помощник на Flask."""
import logging

from flask import Flask, jsonify

from .routes import bp


def create_app():
    app = Flask(__name__)
    app.logger.setLevel(logging.INFO)
    app.register_blueprint(bp)

    @app.after_request
    def add_security_headers(response):
        # заголовки, на которые ругается OWASP ZAP, если их нет
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Cache-Control"] = "no-store"
        response.headers["Content-Security-Policy"] = "default-src 'none'"
        response.headers["Referrer-Policy"] = "no-referrer"
        return response

    # Ошибки отдаём в JSON и без технических деталей
    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(413)
    def too_large(_error):
        return jsonify({"error": "Request is too large"}), 413

    @app.errorhandler(Exception)
    def internal_error(_error):
        # в лог пишем только тип события, без данных пользователя и stack trace в ответе
        app.logger.error("Unhandled error in request")
        return jsonify({"error": "Internal server error"}), 500

    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024  # 16 КБ на весь запрос
    return app
