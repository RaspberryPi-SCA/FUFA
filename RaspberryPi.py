import paramiko # ssh 통신
import numpy as np
import random # random
import time


class RaspberryPi:
    def __init__(self, HOST, ID, PW, PORT, AESFILENAME):
        self.AESFILENAME = AESFILENAME
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(hostname = HOST, port = PORT, username = ID, password = PW)
        except Exception as errorMessage:
            print("eror:", errorMessage)
    
    def sendPT(self, PT):
        self.stdin, self.stdout, self.stderr = self.ssh.exec_command(self.AESFILENAME)

        input = ' '.join([format(x, '02x') for x in PT]) + '\n'
        self.stdin.write(input)
        self.stdin.flush()
    
    def readCT(self, CT):
        stdout = self.stdout.readlines()[0]
        for byteIndex in range(16):
            CT[byteIndex] = int(stdout.strip().split(' ')[byteIndex], 16)

    def __del__(self):
        self.ssh.close()


if __name__ == '__main__':
    HOST = '192.168.137.157'
    ID = 'ckh'
    PW = '  '
    PORT = 22
    AESFILE = '/UROP/aes'

    encryptTimes = 2
    
    plaintexts  = np.empty((encryptTimes, 16), dtype=np.uint8)
    ciphertexts = np.empty((encryptTimes, 16), dtype=np.uint8)
    
    testAES = RaspberryPi(HOST = HOST, ID = ID, PW = PW, PORT = PORT, AESFILENAME = AESFILE)
    for times in range(encryptTimes):
        plaintexts[times] = np.random.randint(low=0, high=256, size=16, dtype=np.uint8)
        testAES.sendPT(plaintexts[times])
        testAES.readCT(ciphertexts[times])
    del testAES
    
    for times in range(encryptTimes):
        for index in range(16):
            print('0x{:02x}, '.format(plaintexts[times, index]), end='')
        print()
        for index in range(16):
            print('0x{:02x}, '.format(ciphertexts[times, index]), end='')
        print()
        print()