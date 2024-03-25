from flask import Flask
app = Flask(__name__)

@app.route('/')
def inddex():
    return "Rushidhar1999"

if __name__ == "__main__":
    app.run()
