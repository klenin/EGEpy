from ...GenBase import DirectInput, EGEError

class IpComputerNumber(DirectInput):

    def generate(self):
        subnet_bits = self.rnd.in_range(3, 12)
        comp_num = self.rnd.in_range(1, 2 ** subnet_bits - 1)
        masked = (self.rnd.in_range(1, 2 ** (16 - subnet_bits) - 1) << subnet_bits) + comp_num
        mask = 2 ** 16 - 2 ** subnet_bits
        mask_text = str(mask >> 8) + '.' + str(mask & 255)
        if not comp_num == (masked & ~mask):
            raise EGEError(f'{comp_num} != ({masked} & ~{mask})')

        dec_ip = '.'.join(
            map(str, [ self.rnd.in_range(128, 255), self.rnd.in_range(0, 255), masked >> 8, masked & 255 ])
        )
        self.text = f'''Если маска подсети 255.255.{mask_text} и IP-адрес компьютера в сети {dec_ip}, то номер 
компьютера в сети равен'''
        self.correct = comp_num
        self.accept_number()

        return self
