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
            <center><p><br><br><br><br><br><br><br><br><br><br><br><br><br><br></p></center>
            <center><h1 style="color:Black;">Meddleying-MAESTRO Music</h1></center>

            <center>
            <style>
            body {
              background-image: url('https://www.pythonanywhere.com/user/asigalov61/files/home/asigalov61/site/static/logo.jpeg');
              background-repeat: no-repeat;
              background-attachment: bottom;
              background-size: cover;
            }
            </style>
            </center>
            <center><a href="/file"><button>Download new sample MIDI file every 20 minutes</button></a></center>
            <center><h1 style="color:Black;">Project Los Angeles</h1></center>
            <center><h1 style="color:Black;">Tegridy Code 2020</h1></center>
            <br><center><a href="https://github.com/asigalov61/Meddleying-MAESTRO">Meddleying MAESTRO GitHub Repo</a><br>
          </body>
        </html>
        '''


@app.route('/file')
def return_files():
    return send_file(
        'output.mid',
        mimetype='audio/mid',
        attachment_filename='Meddleying_Maestro_Composition.mid',
        as_attachment=True
    )


if __name__ == '__main__':
    app.run()
