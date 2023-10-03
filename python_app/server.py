from py_overdrive_sdk.py_overdrive import Overdrive
import socketio
from flask import Flask



sio = socketio.Server(cors_allowed_origins="*",async_mode='threading', allowEIO3 = True, allowedHeaders='*')

app = Flask(__name__)
app.wsgi_app = socketio.WSGIApp(sio, app.wsgi_app)
CAR_COLOR = {
    '07ad9c444182bd10091ea55cf738d2d6':'red',
    '8a38a5c780bf6e846ce80a7dedf881db':'blue',
    '96e2237b2f36e0f8a2220f5ecf640495':'black',
    '66b9133f75973861d43c8ca3eb2605ee':'green'
}
offset = {'LANE1':-68,'LANE2':-23,'LANE3':23,'LANE4':68}

def my_driving_policy_stop(self, **kwargs):
  self.change_speed(0,1000)

def my_driving_policy_start(self, **kwargs):
  if (kwargs['piece'] == 36 and (kwargs['location']%3 == 1)) or kwargs['location'] == 33:
        self.change_speed(500,1000)
  elif kwargs['piece'] in [20, 18] and ((kwargs['location'] in [0,1]) or (20 <= kwargs['location'] <= 25 and kwargs['location']%2 == 1) or (26 <= kwargs['location'] <= 37 and kwargs['location']%3 == 1)):
        self.change_speed(800,1000)

red_car = Overdrive("127.0.0.1", 4001, '07ad9c444182bd10091ea55cf738d2d6',my_driving_policy_start)
blue_car = Overdrive("127.0.0.1", 4002, '8a38a5c780bf6e846ce80a7dedf881db',my_driving_policy_start)
black_car = Overdrive("127.0.0.1", 4003, '96e2237b2f36e0f8a2220f5ecf640495',my_driving_policy_start)

@sio.event
def connect(sid, environ):
    print(f"Connected: {sid}")

@sio.event
def disconnect(sid):
    print(f"Disconnected: {sid}")

@sio.on("red_receive")
def red_receive(sid, data):
    red_car._driving_policy = my_driving_policy_start
    if(data['isEnable']==True):
        if(data['changeLane'] is None):
            red_car.change_speed(500, 2000)
        elif(data['changeLane'] is not None):
            red_car.change_lane(500,500,offset[data['changeLane']])
    elif(data['isEnable']==False):
        red_car._driving_policy = my_driving_policy_stop

@sio.on("blue_receive")
def blue_receive(sid, data):
    blue_car._driving_policy = my_driving_policy_start
    if(data['isEnable']==True):
        if(data['changeLane'] is None):
            blue_car.change_speed(500, 2000)
        elif(data['changeLane'] is not None):
            blue_car.change_lane(500,500,offset[data['changeLane']])
    elif(data['isEnable']==False):
        blue_car._driving_policy = my_driving_policy_stop


@sio.on("black_receive")
def black_receive(sid, data):
    black_car._driving_policy = my_driving_policy_start
    if(data['isEnable']==True):
        if(data['changeLane'] is None):
            black_car.change_speed(500, 2000)
        elif(data['changeLane'] is not None):
            black_car.change_lane(500,500,offset[data['changeLane']])
    elif(data['isEnable']==False):
        black_car._driving_policy = my_driving_policy_stop


if __name__ == "__main__":
    app.run(port=8000)
