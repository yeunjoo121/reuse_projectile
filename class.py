class data:
    transmitted = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    Roll = 0.0
    Pitch = 0.0
    Yaw = 0.0
    Gyro_X = 0.0
    Gyro_Y = 0.0
    Gyro_Z = 0.0
    X_acc = 0.0
    Y_acc = 0.0
    Z_acc = 0.0
    
    def str_to_float(self, splited_str):
        for j in range(0, 9):
            error = 0
            for i in range(0, len(splited_str[j])):
                if (not((splited_str[j][i] >= '0' and splited_str[j][i] <= '9') or (splited_str[j][i] == '.')
                      or (splited_str[j][i] == '-'))):
                    print("transformation error!\n")
                    error = 1
            if (error == 0):
                self.transmitted[j] = float(splited_str[j])
        """self.Roll = transmitted[0]
        self.Pitch = transmitted[1]
        self.Yaw = transmitted[2]
        self.Gyro_X = transmitted[3]
        self.Gyro_Y = transmitted[4]
        self.Gyro_Z = transmitted[5]
        self.acc_X = transmitted[6]
        self.acc_Y = transmitted[7]
        self.acc_Z = transmitted[8]"""
    
    def print_data(self):
        #print("Roll : {0}" .format(self.euler_angle[0]))
        print("Roll : {0} Pitch : {1} Yaw : {2}".format(self.Roll, self.Pitch, self.Yaw))
        print("Gyro_X : {0} Gyro_Y : {1} Gyro_Z : {2}".format(self.Gyro_X, self.Gyro_Y, self.Gyro_Z))
        print("X_acc : {0} Y_acc : {1} Z_acc : {2}".format(self.X_acc, self.Y_acc, self.Z_acc))
        print("\n")

transmitted_str = "-172.12,-79.86,74.4,0.0,0.0,0.0,-0.986,-0.022,-0.175"
splited_str = transmitted_str.split(',')
data1 = data()
data1.str_to_float(splited_str)
data1.print_data()

