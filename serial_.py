import binascii
import time
import serial
import struct
import structlog


log = structlog.get_logger()


class Communication:

    # 初始化
    def __init__(self, com, bps, timeout, DEBUG=False):
        self.port = com
        self.bps = bps
        self.timeout = timeout
        self.DEBUG = DEBUG
        global Ret
        try:
            # 打开串口，并得到串口对象
            self.main_engine = serial.Serial(self.port, self.bps, timeout=self.timeout)
            # 判断是否打开成功
            if self.main_engine.is_open:
                Ret = True
        except Exception as e:
            log.info(f"---异常---：{e}")

    # 打印设备基本信息
    def Print_Name(self):
        log.info(self.main_engine.name)  # 设备名字
        log.info(self.main_engine.port)  # 读或者写端口
        log.info(self.main_engine.baudrate)  # 波特率
        log.info(self.main_engine.bytesize)  # 字节大小
        log.info(self.main_engine.parity)  # 校验位
        log.info(self.main_engine.stopbits)  # 停止位
        log.info(self.main_engine.timeout)  # 读超时设置
        log.info(self.main_engine.writeTimeout)  # 写超时
        log.info(self.main_engine.xonxoff)  # 软件流控
        log.info(self.main_engine.rtscts)  # 软件流控
        log.info(self.main_engine.dsrdtr)  # 硬件流控
        log.info(self.main_engine.interCharTimeout)  # 字符间隔超时

    # 打开串口
    def Open_Engine(self):
        self.main_engine.open()

    # 关闭串口
    def Close_Engine(self):
        self.main_engine.close()
        log.info("Serial status: %s", self.main_engine.is_open)

    # 打印可用串口列表
    @staticmethod
    def Print_Used_Com():
        port_list = list(serial.tools.list_ports.comports())
        log.info(port_list)

    # 接收指定大小的数据
    # 从串口读size个字节。如果指定超时，则可能在超时后返回较少的字节；如果没有指定超时，则会一直等到收完指定的字节数。
    def Read_Size(self, size):
        return self.main_engine.read(size=size)

    # 接收一行数据
    # 使用readline()时应该注意：打开串口时应该指定超时，否则如果串口没有收到新行，则会一直等待。
    # 如果没有超时，readline会报异常。
    def Read_Line(self):
        return self.main_engine.readline()

    # 发数据
    def Send_data(self, data):
        self.main_engine.write(data)

    def Recive_data(self, way=1):
        # 循环接收数据，此为死循环，可用线程实现
        log.info("Start listening data from serial.")
        while True:
            try:
                # 一个字节一个字节的接收
                if self.main_engine.in_waiting:
                    if way == 0:
                        for i in range(self.main_engine.in_waiting):
                            log.info("接收ascii数据：" + str(self.Read_Size(1)))
                            data1 = self.Read_Size(1).hex()  # 转为十六进制
                            data2 = int(
                                data1, 16
                            )  # 转为十进制print("收到数据十六进制："+data1+"  收到数据十进制："+str(data2))
                    if way == 1:
                        # 整体接收
                        # data = self.main_engine.read(self.main_engine.in_waiting).decode("utf-8")#方式一
                        data = self.main_engine.read_all()  # 方式二
                        log.info(f"Receive data from serial: {data}.")
            except Exception as e:
                log.error("异常报错：%s", e)

    def send_servo_command(self, angle, servo_id=1):
        angle = int(angle)
        if not (0 <= servo_id <= 10) or not (0 <= angle <= 180):
            log.info("Invalid servo_id or angle.")
            return
        checksum = (0xAA + servo_id + angle) & 0xFF
        packet = struct.pack("BBBB", 0xAA, servo_id, angle, checksum)
        if self.DEBUG:
            log.info(f"发送的角度： {checksum}. servo_id: {servo_id}, angle: {angle}.")
        self.main_engine.write(packet)


# 食指 1 95-180
# 食指 2 110-180
if __name__ == "__main__":
    Communication.Print_Used_Com()
    Ret = False  # 是否创建成功标志

    Engine1 = Communication("/dev/cu.usbserial-111420", 9600, 0.5)
    if Ret:
        # Engine1.Recive_data(1)
        Engine1.Print_Used_Com()
        while True:
            Engine1.Recive_data(way=1)

    # 更多示例
    # self.main_engine.write(chr(0x06).encode("utf-8"))  # 十六制发送一个数据
    # print(self.main_engine.read().hex())  #  # 十六进制的读取读一个字节
    # print(self.main_engine.read())#读一个字节
    # print(self.main_engine.read(10).decode("gbk"))#读十个字节
    # print(self.main_engine.readline().decode("gbk"))#读一行
    # print(self.main_engine.readlines())#读取多行，返回列表，必须匹配超时（timeout)使用
    # print(self.main_engine.in_waiting)#获取输入缓冲区的剩余字节数
    # print(self.main_engine.out_waiting)#获取输出缓冲区的字节数
    # print(self.main_engine.readall())#读取全部字符。

    # 接收数据
    # 一个整型数据占两个字节
    # 一个字符占一个字节
