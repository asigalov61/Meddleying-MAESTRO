from flask import Flask, send_file

app = Flask(__name__)


@app.route('/')
def file_downloads():
    return '''
        <html>
          <head>
            <meta charset="utf-8">
            <title>Meddleying-MAESTRO Music</title>
            <link href="https://fonts.googleapis.com/css?family=Open+Sans" rel="stylesheet" type="text/css">
            <link href="styles/style.css" rel="stylesheet" type="text/css">
          </head>
          <body>
            <center><p><br><br><br><br><br></p></center>
            <center><h1 style="color:Black;">Meddleying-MAESTRO Music</h1></center>
            <section id="section3">
            <center>
            <midi-player
              src="https://asigalov61.pythonanywhere.com/static/output.mid"
              sound-font visualizer="#section3 midi-visualizer">
            </midi-player>
            </center>
            </section>
            <center><a href="/file"><button>Download new sample MIDI file every 30 minutes</button></a></center>
            <script src="https://cdn.jsdelivr.net/combine/npm/tone@14.7.58,npm/@magenta/music@1.21.0/es6/core.js,npm/focus-visible@5,npm/html-midi-player@1.1.0"></script>
            <center><h1 style="color:Black;">Project Los Angeles</h1></center>
            <center><h1 style="color:Black;">Tegridy Code 2020</h1></center>
            <br><center><a href="https://github.com/asigalov61/Meddleying-MAESTRO">Meddleying MAESTRO GitHub Repo</a><br>
          </body>
        </html>
        '''


@app.route('/file')
def return_files():
    return send_file(
        'static/output.mid',
        mimetype='audio/mid',
        attachment_filename='Meddleying_Maestro_Composition.mid',
        as_attachment=True
    )


if __name__ == '__main__':
    app.run()
