import threading

class Device:
    #This is the constructor
    def __init__(self, device_name, ip, loopback_ip, connection=None, command_list=None, backup_file_name=None, config_file=None):
        self.device_name = device_name
        self.ip = ip
        self.connection = connection
        self.command_list = command_list
        self.loopback_ip = loopback_ip
        self.backup_file_name = backup_file_name
        self.config_file = config_file

    #Connects to the device
    def connect(self):
        from netmiko import ConnectHandler
        self.connection = ConnectHandler(**self.device_name)

    #Get the commands from file
    def Get_commands(self):
        with open('commands_list.txt', 'r') as f:
          self.command_list = f.read().splitlines()
          self.command_list.append('int loop 0')
          self.command_list.append('ip add ' + str(self.loopback_ip) + ' 255.255.255.255')

    #Execute the configuration
    def execute(self):
        output = self.connection.send_config_set(self.command_list)
        print(output)

    #Get device config backup file name
    def Get_backup_file_name(self):
        import datetime
        now = datetime.datetime.now()
        today = str(now.year) + '-' + str(now.month) + '-' + str(now.day)
        self.backup_file_name = today + '-' + str(self.ip) + '.txt'

    #Use 'show run' to get the device config
    def Get_config_file(self):
        self.config_file = self.connection.send_command('show run')

    #Backup the device config
    def backup(self):
        with open(self.backup_file_name, 'w') as f:
            f.write(self.config_file)
            print('Successfully backup the configuration for: ' + str(self.ip))

def run(input):
    while True:
        device_info_dictionary = {
            'device_type': input[0],
            'ip': input[1],
            'username': input[3],
            'password': input[4]
        }

        #Connect to devices
        Device_configuration = Device(device_info_dictionary, input[1], input[2])
        try:
            Device_configuration.connect()
            print('Successfully connect to device: ' + str(input[1]))

        except:
            print('Connection failed! ' + str(input[1]))
            break

        #Config devices
        Device_configuration.Get_commands()
        Device_configuration.execute()

        #Back the device config
        Device_configuration.Get_backup_file_name()
        Device_configuration.Get_config_file()
        Device_configuration.backup()
        break

# Open and process the device list that contains all info
if __name__ == '__main__':
    with open('devices_list_netmiko.txt', 'r') as f:
        device = f.read().splitlines()

    #Defines a empty list to store the device info
    device_info = []
    for info in device:
        info_item = info.split(':')
        device_info.append(info_item)

    for element in device_info:
        my_thread = threading.Thread(target = run, args=(element, ))
        my_thread.start()

    main_thread = threading.current_thread()
    for my_thread in threading.enumerate():
        if my_thread != main_thread:
            my_thread.join()