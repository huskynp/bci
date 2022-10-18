# from ADCDifferentialPi import ADCDifferentialPi
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# adc = ADCDifferentialPi(0x68, 0x68, 16)
# adc.set_pga(8)
# adc.set_conversion_mode(1)

y_values = []


def get_voltage():

    # # y1 = adc.read_voltage(1)  # actual electrode
    # # y2 = adc.read_voltage(2)  # control electrode (ear)
    # # y3 = adc.read_voltage(3)  # 2nd control electrode (other ear)
    # control_avg = (y2+y3)/2
    # # y4 = adc.read_voltage(4)  # ground (anywhere)

    # y = (y1 - y4) - (control_avg - y4)
    # print(y)
    return 0


class handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        voltage = get_voltage()
        self.wfile.write(json.dumps({'voltage': voltage}).encode())


with HTTPServer(('', 8000), handler) as server:
    print("server running")
    server.serve_forever()
