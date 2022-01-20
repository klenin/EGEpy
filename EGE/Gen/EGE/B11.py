# Copyright © 2010-2014 Alexander S. Klenin
# Copyright © 2012 V. Kevroletin
# Copytight © 2022 Vladimir K. Glushkov, glushkov.vk@students.dvfu.ru
# Licensed under GPL version 2 or later.
# http://github.com/klenin/EGEpy
import itertools

import EGE.Html as html

from EGE.Bits import Bits
from EGE.GenBase import DirectInput
from EGE.Utils import char_range, nrange, unique

class IpMask(DirectInput):
    """
    Генератор B11 ip_mask - указать адрес подсети по IP-адресу и маске подсети.
    """
    @staticmethod
    def _bits_to_mask(bits: int):
        mask = '1' * bits + '0' * (32 - bits)
        mask = [ mask[i:i + 8] for i in range(0, 32, 8) ]
        return [ int(byte, 2) for byte in mask ]

    @staticmethod
    def _prepare(header: list, parts: list, ip: list):
        def find_part(x: int):
            return parts.index(x)
        return (
            ''.join([ header[i] for i in map(find_part, ip) ]),
            html.table(html.row('th', header) + html.row('td', parts), border=1)
        )
    @staticmethod
    def sign(a, b):
        return bool(a > b) - bool(a < b)

    def generate(self):
        ip = []
        while not ip and all([ el == 0 for el in ip ]):
            ip = [ self.rnd.in_range(0, 255) for _ in range(0, 4) ]
        mask = self._bits_to_mask(self.rnd.in_range(1, 31))
        header = list(char_range('A', 'H'))
        masked_ip = [ ip[i] & mask[i] for i in range(len(ip)) ]
        parts = sorted(unique(list(itertools.chain(
            masked_ip,
            [ ip[i] & mask[i] for i in range(len(ip)) ],
            list(reversed(ip)),
            mask,
            [ ip[i] ^ mask[i] for i in range(len(ip)) ],
            self.rnd.pick_n(8, nrange(0, 255))
        )))[:len(header)])
        self.correct, table_text = self._prepare(header, parts, masked_ip)
        example_ip = [ 192, 168, 128, 0 ]
        example_parts = [ 128, 168, 255, 8, 127, 0, 17, 192 ]
        example_answer, example_table_text = self._prepare(header, example_parts, example_ip)
        self.text = f"""
В терминологии сетей TCP/IP маской сети называется двоичное число, определяющее,
какая часть IP-адреса узла сети относится к адресу сети, а какая — к адресу самого
узла в этой сети. Обычно маска записывается по тем же правилам, что и IP-адрес.
Адрес сети получается в результате применения поразрядной конъюнкции к заданному
IP-адресу узла и маске. <br/>
По заданным IP-адресу узла и маске определите адрес сети.
<table>
  <tr><td>IP-адрес узла:</td><td>{ip}</td></tr>
  <tr><td>Маска:</td><td>{mask}</td></tr>
</table>
При записи ответа выберите из приведенных в таблице чисел четыре элемента IP-адреса
и запишите в нужном порядке соответствующие им буквы. Точки писать не нужно.
{table_text}
<br/><i><strong>Пример</strong>.
Пусть искомый IP-адрес {example_ip}, и дана таблица</i>
{example_table_text}
<i>В этом случае правильный ответ будет записан в виде: {example_answer}</i>"""
        return self

class SubnetMask(DirectInput):
    """
    Генератор B11 subnet_mask - найти наибольший (или наименьший) возможный
        или конкретный третий байт маски по заданным адресам ip и сети
    """
    def generate(self):
        question, question_type = self.rnd.pick([
            ('Чему равно наибольшее возможное значение третьего слева байта маски?', 0),
            ('Чему равно наименьшее возможное значение третьего слева байта маски?', 1),
            ('Чему равен третий слева байт маски?', 2),
        ])
        subnet_network = [
            self.rnd.in_range(200, 255), self.rnd.in_range(30, 255), 0, 0
        ]

        ip_address = [
            subnet_network[0],
            subnet_network[1],
            0,
            self.rnd.pick([ 0, self.rnd.in_range(100, 255) ])
        ]

        ip = [ 0 ] * 8

        subnet_zeros = self.rnd.in_range(5, 7)
        ip[8 - subnet_zeros - 1] = 1
        for i in range(8 - subnet_zeros, len(ip)):
            ip[i] = int(self.rnd.coin())
        if question_type == 2:
            ip[8 - subnet_zeros] = 1

        ip_address[2] = Bits() \
            .set_bin(ip, True) \
            .get_dec()

        subnet = [0] * 8
        subnet[8 - subnet_zeros - 1] = 1
        subnet_network[2] = Bits() \
            .set_bin(subnet, True) \
            .get_dec()

        mask = [0] * 8
        for i in range(8):
            if question_type == 1:
                mask[i] = 1 if ip[i] == subnet[i] and i < 8 - subnet_zeros else 0
            else:
                mask[i] = 1 if ip[i] == subnet[i] else 0
            if mask[i] == 0:
                break

        answer = Bits() \
            .set_bin(mask, True) \
            .get_dec()

        self.text = f"""
В терминологии сетей TCP/IP маской сети называется 32-разрядная двоичная последовательность, определяющая, какая часть IP-адреса узла сети относится
к адресу сети, а какая – к адресу самого узла в этой сети. При этом в маске сначала (в старших разрядах) стоят единицы, а затем с некоторого места нули.
Адрес сети получается в результате применения поразрядной конъюнкции к заданному IP-адресу узла и маске. Обычно маска записывается по тем же правилам,
что и IP-адрес – в виде четырёх байтов, причём каждый байт записывается в виде десятичного числа.<br/>
Пример. Пусть IP-адрес узла равен 231.32.255.131, а маска равна 255.255.240.0. Тогда адрес сети равен 231.32.240.0.<br/>
Для узла с IP-адресом {ip_address} адрес сети равен {subnet_network} . {question} Ответ запишите в виде десятичного числа."""
        self.correct = answer
        return self


