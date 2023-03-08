import signal

from app import app
if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8989,debug=True)

def handler(signal, frame):
  app.config['shutdown'] = True
  print('CTRL-C pressed!')
  app.stop()  # type: ignore
signal.signal(signal.SIGINT, handler)
