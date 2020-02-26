from flask import jsonify

def register_error_handlers(app):
    def generic_handler(e):
        '''
        This generic handler will handle any errors registered and will return a JSON
        response instead of dumb html lol
        '''
        response = e.get_response()
        data = { "error": e.name, "description": e.description }
        return jsonify(data), e.code

    app.register_error_handler(400, generic_handler)
    app.register_error_handler(404, generic_handler)
    app.register_error_handler(500, generic_handler)
