from os    import name
from flask import (
    Flask,
    render_template,
    send_file,
    request,
    Response
)

app = Flask(__name__, template_folder='assets/html')
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

class Website:
    def __init__(self) -> None:
        self.routes = {
            '/': {
                'function': self._index,
                'methods': ['GET', 'POST']
            },
            '/assets/<folder>/<file>': {
                'function': self._assets,
                'methods': ['GET', 'POST']           
            }
        }

        self.config = {
            'host': '0.0.0.0',
            'port': 1337 if name == 'nt' else 80,
            'debug': True
        }

    def _index(self) -> Response:
        return render_template('index.html')
        
    def _assets(self, folder: str, file: str) -> Response:
        try:
            return send_file(f"assets/{folder}/{file}", as_attachment=False)
        except:
            return "File not found", 404

    @staticmethod
    def page_not_found(e) -> Response:
        return render_template('404.html'), 404

if __name__ == '__main__':
    website = Website()
    
    app.register_error_handler(404, Website.page_not_found)
    for route in website.routes:
        app.add_url_rule(
            route,
            view_func = website.routes[route]['function'],
            methods   = website.routes[route]['methods']
        )

    app.run(**website.config)