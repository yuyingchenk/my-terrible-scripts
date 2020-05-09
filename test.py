def OPEN_DEVICE_LIST():
    import xlrd
    location = r"C:\Users\Yingchen.Yu\Desktop\Ansible Campus Automation Project\Devices-Lists.xlsx"
    try:
        open_excel = xlrd.open_workbook(location)
        return open_excel
    except:
        return False

def READ_DEVICE_LIST(raw_excel_output):
    device_list = raw_excel_output.sheet_by_index(0)
    rows = device_list.nrows
    device_list.cell_value(0, 0)
    device_info = []
    for i in range(1, rows):
        device_info.append(device_list.row_values(i))
    return device_info

def CHECK_FILE_EXIST(device_info):
    import os.path
    os.chdir(r"C:\Users\Yingchen.Yu\Desktop\Ansible Campus Automation Project\inventory\host_vars\\")
    exist_file_name = device_info[0] + '.yaml'
    if os.path.isfile(exist_file_name):
        return True
    else:
        return False

def CREATE_DEVICE_FILE(device_info):
    exist_file_name = device_info[0] + '.yaml'
    device_ip = 'ansible_host=' + device_info[2] + '\n'
    device_location = '#location=' + device_info[1]
    device_ios = 'ansible_network_os=' + device_info[4] + '\n'
    with open(exist_file_name, 'w') as f:
            f.write(device_ip)
            f.write(device_ios)
            f.write(device_location)
    print('device {} has been added'.format(exist_file_name))

def DEVICE_FILE_LIST():
    import os.path
    os.chdir(r"C:\Users\Yingchen.Yu\Desktop\Ansible Campus Automation Project\inventory\host_vars\\")
    return os.listdir()

def DEVICE_FILE_DELETION(exist_file_name):
    import os
    os.unlink(exist_file_name)
    print('device {} has been removed'.format(exist_file_name))

if __name__== "__main__":
    checker_excel_file = OPEN_DEVICE_LIST()
    if checker_excel_file == False:
        print('excel file is not accessible')
    else:
        print('excel file is read successfully')
        device_name_iteration = []
        for device in READ_DEVICE_LIST(checker_excel_file):
            device_name_add = device[0] + '.yaml'
            device_name_iteration.append(device_name_add)
            checker_file_exist = CHECK_FILE_EXIST(device)
            if checker_file_exist == False:
                CREATE_DEVICE_FILE(device)

        checker_file_deletion = DEVICE_FILE_LIST()
        for exist_file_name in checker_file_deletion:
            if exist_file_name not in device_name_iteration:
                DEVICE_FILE_DELETION(exist_file_name)