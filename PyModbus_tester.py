
from pymodbus.client import ModbusTcpClient #get the pyModbus library from pip if this causes a problem
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.constants import Endian
import time


'''
README: To use this, set the server_ip and server_port in the section: if __name__ == "__main__":
For Omron robots, the standard port for Modbus is 502. The IP depends on the socket the computer connects to.

'''

class OmronRobotConnection():
    def __init__(self, in_server_IP, in_server_port):
        self.server_IP = in_server_IP
        self.server_port = in_server_port
        self.client = None
        self.angles_degrees = Array("d", [0, 0, 0, 0, 0, 0])


    def connect_to_robot(self):
        try:
            print("Attempting to connect with Omron robot over ModBus", self.server_IP)
            self.client = ModbusTcpClient(self.server_IP, self.server_port)
            connection = self.client.connect()
            
        except Exception as err:
            print("Error when trying to connect to Omron robot via Modbus: ", err)


    def receive_data(self):
        while True:
            try:
                result = self.client.read_input_registers(7013, 4, unit=1)
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
                self.angles_degrees[0] = decoder.decode_32bit_float()
                
                result = self.client.read_input_registers(7015, 4, unit=1)
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
                self.angles_degrees[1] = decoder.decode_32bit_float()

                result = self.client.read_input_registers(7017, 4, unit=1)
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
                self.angles_degrees[2] = decoder.decode_32bit_float()

                result = self.client.read_input_registers(7019, 4, unit=1)
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
                self.angles_degrees[3] = decoder.decode_32bit_float()

                result = self.client.read_input_registers(7021, 4, unit=1)
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
                self.angles_degrees[4] = decoder.decode_32bit_float()

                result = self.client.read_input_registers(7023, 4, unit=1)
                decoder = BinaryPayloadDecoder.fromRegisters(result.registers, Endian.Big, wordorder=Endian.Big)
                self.angles_degrees[5] = decoder.decode_32bit_float()

                print("received these angles: ", self.angles_degrees[:])
                time.sleep(0.03)

            except Exception as err:
                time.sleep(0.2)
                print("Error handling data received from Omron robot: ", err)


if __name__ == "__main__":
    server_ip = "192.168.250.66"
    server_port = "502"
    robot_connection = OmronRobotConnection(server_ip, server_port)

    robot_connection.connect_to_robot()
    robot_connection.receive_data()
    
