import serial
import io
import time
import click

class YStage():
    def __init__(self, com_port, baudrate = 9600, logger = None):
        """The constructor for the ystage.

           **Parameters:**
            - com_port (str): Communication port for the ystage.
            - baudrate (int, optional): The communication speed in symbols per
              second.
            - logger (log, optional): The log file to write communication with the
              ystage to.

           **Returns:**
            - ystage object: A ystage object to control the ystage.

        """

        if isinstance(com_port, int):
            com_port = 'COM'+str(com_port)

        try:
            # Open Serial Port
            s  = serial.Serial(com_port, baudrate, timeout = 1)
            # Text wrapper around serial port
            self.serial_port = io.TextIOWrapper(io.BufferedRWPair(s,s,),
                                                encoding = 'ascii',
                                                errors = 'ignore')
        except:
            print('ERROR::Check Y Stage Port')
            self.serial_port = None

        self.move_aborted = False
        self.is_moving = False
        self.min_y = -7000000
        self.max_y = 7500000
        self.spum = 100     # steps per um
        #self.prefix = '1'
        self.suffix = '\r\n'
        self.on = False
        self.position = 0
        self.home = 0
        self.mode = None
        self.velocity = None
        self.gains = None
        self.configurations = {'imaging':{'g':'5,10,5,2,0'  ,'v':0.15400},
                               'moving': {'g':'5,10,7,1.5,0','v':1}
                               }
        self.logger = logger

    def initialize(self):
        """Initialize the ystage."""
        import pyseq
        hs = pyseq.HiSeq()
        hs.y.prefix = ''

        
        response = self.command('r')                                            # Initialize Stage
        time.sleep(2)
        #response = self.command('W(EX,0)')                                      # Turn off echo
        self.set_mode('moving')
        #response = self.command('MA')                                           # Set to absolute position mode
        #set programmed positional mode
        response = self.command('s r0x24 21')
        #set absolute move
        response = self.command('s r0xc8 0') 
        #sets max velocity to 4000 counts/sec
        self.command('s r0xcb 4000') 
        #sets max acceleration to 4000/sec^2
        self.command('s r0xcc 4000') 
        #sets max deceleration to 4000/sec^2
        self.command('s r0xcd 4000') 
        self.on = True
        #set position properties
        if click.confirm('Are all move parameters set?', default=True):
      		response = hs.y.command('t 1') 
            
        #homing
        #set home offset to 1000 counts
        self.command('s r0xc6 1000')
        #sets homing method to use next index pulse as home
        self.command('s r0xc2 544')
        if click.confirm('Are all home parameters set?', default=True):
         	response = self.command('t 2')


        

class YCmd():
    #function that parses commands from command line (“command”) 

    def command(self, text):
        """Send a serial command to the ystage and return the response.

           **Parameters:**
            - text (str): A command to send to the ystage.

           **Returns:**
            - str: The response from the ystage.
        """

        text = self.prefix + text + self.suffix
        self.serial_port.write(text)                                            # Write to serial port
        self.serial_port.flush()                                                # Flush serial port
        response = self.serial_port.readline()
        if self.logger is not None:
            self.logger.info('Ystage::txmt::'+text)
            self.logger.info('Ystage::rcvd::'+response)

        return  response
         

#open serial port
#Initialize com
#constructor for the YStage
    
#initialize(self)  #initialize YStage
    

    #dictionary for r0xa0
dict_r0xa0= {0:'Short circuit detected', 1:'Drive over temperature', 3: 'Under voltage', 4: ' Motor temperature sensor active', 5: ' Feedback error.', 6:' Motor phasing error.', 7: ' Current output limited.', 8: ' Voltage output limited.', 9: ' Positive limit switch active', 10: ' Negative limit switch active.', 11: ' Enable input not active.', 12: 'Drive is disabled by software', 13: ' Trying to stop motor', 14: 'Motor brake activated', 15: 'PWM outputs disabled.', 16: ' Positive software limit condition', 17: 'Negative software limit condition.', 18: 'Tracking error.', 19: 'Tracking warning', 20: ' Drive has been reset.', 21: ' Position has wrapped. The Position parameter cannot increase indefinitely. After reaching a certain value the parameter rolls back. This type of counting is called position wrapping or modulo count. Note that this bit is only active as the position wraps.', 22: ' Drive fault. A drive fault that was configured as latching has occurred. For information on latching faults, see the CME 2 User Guide.', 23: ' Velocity limit has been reached.', 24: ' Acceleration limit has been reached.', 25: 'Position outside of tracking window.', 26: ' Home switch is active', 27: 'Trajectory is stil running, motor has not yet settled into position.', 28: ' Velocity window. Set if the absolute velocity error exceeds the velocity window value.', 29: 'Phase not yet initialized. If the drive is phasing with no Halls, this bit is set until the drive has initialized its phase.', 30: ' Command fault. PWM or other command signal not present', 31: 'Error not defined'}

    #dictionary for r0xc9
dict_r0xc9 = {0: 'Reserved for future use.', 1: 'Reserved for future use.', 2: 'Reserved for future use.', 3: 'Reserved for future use.', 4: 'Reserved for future use.', 5: 'Reserved for future use.', 6:'Reserved for future use.', 7:'Reserved for future use.', 8:'Reserved for future use.', 9: 'Cam table underflow.', 10:'Reserved for future use', 11: 'Homing error. If set, an error occurred in the last home attempt. Cleared by a home command.', 12: 'Referenced. Set when a homing command has been successfully executed. Cleared by a home command.', 13: 'Homing. If set, the drive is running a home command', 14: 'Set when a move is aborted. Cleared at the start of the next move.', 15: 'In-Motion Bit. If set, the trajectory generator is presently generating a profile.'}

    #dictionary for r0xa4
dict_r0xa4: {0: 'Data flash CRC failure. This fault is considered fatal and cannot be cleared.', 1: 'Drive internal error. This fault is considered fatal and cannot be cleared.', 2: 'Short circuit.', 3: 'Drive over temperature.', 4: 'Motor over temperature.', 5: 'Over voltage.', 6: 'Under voltage. ', 7: 'Feedback fault.' , 8: 'Phasing error', 9: 'Following error', 10: 'Over Current (Latched)', 11: 'FPGA failure. This fault is considered fatal and cannot usually be cleared. If this fault occurred after a firmware download, repeating the download may clear this fault.', 12: 'Command input lost', 13: 'Reserved', 14: 'Safety circuit consistency check failure.', 15: 'Unable to control motor current', 16: 'Motor wiring disconnected', 17: 'Reserved.', 18: 'Safe torque off active.'}

    #dictionary for error codes
dict_error: {1: 'Too much data passed with command', 3: 'Unknown command code', 4: 'Not enough data was supplied with the command', 5: 'Too much data was supplied with the command', 9: 'Unknown parameter ID', 10: 'Data value out of range', 11: 'Attempt to modify read-only parameter', 14: 'Unknown axis state', 15: 'Parameter doesn’t exist on requested page', 16: 'Illegal serial port forwarding', 18: 'Illegal attempt to start a move while currently moving', 19: 'Illegal velocity limit for move', 20: 'Illegal acceleration limit for move', 21: 'Illegal deceleration limit for move', 22: 'Illegal jerk limit for move', 25: 'Invalid trajectory mode', 27: 'Command is not allowed while CVM is running', 31: 'Invalid node ID for serial port forwarding', 32: 'CAN Network communications failure', 33: 'ASCII command parsing error', 36: 'Bad axis letter specified', 46: 'Error sending command to encoder', 48: 'Unable to calculate filter'}


#Note that when a latching fault has occurred, bit 22 of the status register (0xa0) is set. To clear a fault condition, write a 1 to the associated bit of the fault register (0xa4).

#function called “remove chars”, removes excess characters in output string
    def remove_chars(text):
        bit_num = text
        #bit_num = 'v 268435456\n'
        extra_chars = ['v', '\n', ' ']
        bit_num_new = bit_num
        for i in extra_chars:
            bit_num_new = bit_num_new.replace(i, "")
        return bit_num_new
        
#function called “parse”, looks for bit value in error outputs for r0xa0, r0xc9, and r0xa4


    def parse_r0xa0(self, text):
        status_num = self.command(text)
        status_num_str = remove_chars(status_num)
        status_num_int= int(status_num_str) 
        bit_num=format(status_num_int, 'b')
        bit_num_len = len(status_num_str) 
        list(enumerate(bit_num))
        error_value = [i for i, value in enumerate(reversed(bit_num), 0) if value == '1'] #switched from (bit_num,0) -> (bit_num,1)
        print(error_value)
        for value in error_value:
            return dict_r0xa0.get(i, value) #return int
            if click.confirm('Do you want corresponding error?', default=True):
                return dict_r0xa0.get(value) #return string
            #return dict_r0xa0.get(value) #return string
            
    def parse_r0xa4(self, text):
        status_num = self.command(text)
        status_num_str = remove_chars(status_num)
        status_num_int= int(status_num_str) 
        bit_num=format(status_num_int, 'b')
        bit_num_len = len(status_num_str) 
        list(enumerate(bit_num))
        error_value = [i for i, value in enumerate(reversed(bit_num), 0) if value == '1'] #switched from (bit_num,0) -> (bit_num,1)
        print(error_value)
        for value in error_value:
            return dict_r0xa4.get(i, value) #return int
            if click.confirm('Do you want corresponding error?', default=True):
                return dict_r0xa4.get(value) #return string

    def parse_r0xc9(self, text):
        status_num = self.command(text)
        status_num_str = remove_chars(status_num)
        status_num_int= int(status_num_str) 
        bit_num=format(status_num_int, 'b')
        bit_num_len = len(status_num_str) 
        list(enumerate(bit_num))
        error_value = [i for i, value in enumerate(reversed(bit_num), 0) if value == '1'] #switched from (bit_num,0) -> (bit_num,1)
        print(error_value)
        for value in error_value:
            return dict_r0xc9.get(i, value) #return int
                if click.confirm('Do you want corresponding error?', default=True):
                    return dict_r0xc9.get(value) #return string
            #return dict_r0xa4.get(value) #return string     

    def move_aborted(self):
        if (parse_r0xc9(self.command('g r0xc9')) == 14):
            print('move was aborted')
            self.move_aborted = True

    def is_moving(self, text):
        self.is_moving = False
        if (parse_r0xa0(self.command('g r0xa0')) == 27):
            print('currently moving')
            self.is_moving = True
            
    def velocity_bounds(self): #check if velocity is in bounds
        self.velocity_in_bound = True
        if (parse_r0xa0(self.command('g r0xa0')) == 28):
            print('velocity out of bounds')
            self.is_moving = False
            
    def _init_(self, pos):
        self.position = pos

    @property
    def get_position(self):
        self.position = int(remove_chars(self.command('g r0x32')))
        return self.position

    @position.setter
    def set_position(self, pos):
        self.position = int(remove_chars(self.command('s r0x32' + str(pos))))
        
    def in_position(self, pos):
        self.in_position = False
        if self.min_y <= self.command('g r0xca') <= self.max_y:
            self.in_position = True
        
    def check_velocity(self):
        self.in_velocity = False
        if self.min_v <= self.command('g r0xcb') <= self.max_v:
            self.in_velocity = True

    def check_accel(self):
        self.in_accel = False
        if self.min_a <= self.command('g r0xcc') <= self.max_a:
            self.in_accel = True        
         
    def move(self, pos):
        #get max velocity 
        self.command('g r0xcb') 
        #get max acceleration 
        self.command('g r0xcc') 
        #get max deceleration 
        self.command('g r0xcd') 
        #set position

        
        if (self.in_position == True):
            while self.position != pos:
                self.command('s 0xca' + str(pos) )
                self.command('t 1')
            while not self.check_position():                                # Wait till y stage is in position
                    time.sleep(1)
                self.read_position()                                            # Update stage position
            return True                                                         # Return True that stage is in position
        else:
            print("YSTAGE can only between " + str(self.min_y) + ' and ' +
                str(self.max_y))
       
        
        #if mode is imaging, set mode to moving
        #else:
        self.command('s r0xca' + str(pos)) #sets position command to pos (units of pos = counts)
        self.command('t 1') #executes the move
        if (self.move_aborted == True): #check to see if move was aborted
            print("move aborted")
        parse_str('g r0xc9') #check bit 14
        self.command('t 0')
        self.command('s r0x24 0') #Disable the drive


        #is it moving?
        #self.is_moving = self.command('g r0xa0')
        #if specific put value from parse, it is moving. otherwise, it is not moving. 
            #https://stackoverflow.com/questions/71777411/get-a-dictionary-having-a-specific-key-value-pair-from-a-complex-dictionary
        if (parse_r0xa0(self.command('g r0xa0')) == 27):
            return True
			set_mode (imaging vs. moving)

gains = {1: PG, 2: VG, 3: AF, 4: GM, 5: VF}

    def set_mode(self, mode):
        """Change between imaging and moving configurations."""
        
        mode_changed = True 
        if self.mode != mode:
            if mode in self.configurations.keys():
                gains = str(self.configurations[mode]['g'])
                _gains = [float(g) for g in gains.split(',')]
                velocity = self.configurations[mode]['v']
                all_true = False
                while not all_true:
                    self.command('GAINS('+gains+')')
                    time.sleep(1)
                    try:
                        gains_ = self.command('GAINS').strip()[1:].split(' ')       # format reponse
                        all_true = all([float(g[2:]) == _gains[i] for i, g in enumerate(gains_)])
                    except:
                        all_true = False
                velocity_ = None
                while velocity_ != float(velocity):
                    self.command('V'+str(velocity)) #replace 'V' with 'g r0x18'
                    time.sleep(1)
                    try:
                        velocity_ = float(self.command('V').strip()[1:]) #Velocity command V sets or reports the programmed velocity of the motor.
                    except:
                        velocity_ = False
                self.mode = mode
                self.velocity = velocity_
                self.gains = gains
            else:
                mode_change = False
                message = 'Ystage::ERROR::Invalid configuration::'+str(mode)
                if self.logger is not None:
                    self.logger.info(message)
                else:
                    print(message)

        return mode_changed

#parsing output errors
def parse_error(text):
        status_num = self.command(text)
        status_num_str = remove_chars(status_num)
        status_num_int= int(status_num_str) 
        bit_num=format(status_num_int, 'b')
        bit_num_len = len(status_num_str) 
        list(enumerate(bit_num))
        error_value = [i for i, value in enumerate(reversed(bit_num), 0) if value == '1'] #switched from (bit_num,0) -> (bit_num,1)
        print(error_value)
        for value in error_value:
            return dict_error.get(i, value) #return int
            if click.confirm('Do you want corresponding error?', default=True):
                return dict_error.get(value) #return string
