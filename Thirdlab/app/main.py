# dummy entrypoint for compatibility; web app lives in controllers

if __name__ == '__main__':
    from app import controllers
    controllers.app.run(debug=True)
