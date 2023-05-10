import time


# 64位二进制中，最高位为符号位，固定为0，剩下63位分别为时间戳、数据中心id和机器id。
# 所以时间戳占用的位数为 63-10=53 位，数据中心id和机器id各占用5位。
# 最后一位为序列号，用于同一毫秒内生成不同的id。
# 所以每秒最多能生成 2^10 = 1024 个id。
# 时间戳初始值为 2014-09-01 00:00:00，即 1410000000000。
# 本实现中，数据中心id和机器id通过参数传入，序列号初始值为0。
# 数据中心id和机器id的取值范围都为 0~31，通过参数传入。

class SnowFlake:
    def __init__(self, datacenter_id, machine_id):
        self.datacenter_id = datacenter_id
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1

    def get_timestamp(self):
        return int(time.time() * 1000)

    def generate_id(self):
        timestamp = self.get_timestamp()

        if timestamp < self.last_timestamp:
            raise Exception("Clock moved backwards. Refusing to generate id.")

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 0x3ff
            if self.sequence == 0:
                timestamp = self.get_timestamp()
                while timestamp <= self.last_timestamp:
                    timestamp = self.get_timestamp()
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return ((timestamp - 1410000000000) << 22) | (self.datacenter_id << 17) | (
                self.machine_id << 12) | self.sequence


snowflake = SnowFlake(1, 1)
if __name__ == '__main__':
    snowflake = SnowFlake(1, 1)
    id = snowflake.generate_id()
    print(id)
    # 1147925725739880448

# 1147925752033972224
