from .app.server import server_run

__init__ = ["server_run"]

def app_run():
    server_run()

if __name__ == "__main__":
    app_run()
