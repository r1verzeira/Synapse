import struct
import random
import socket

class PacketFactory:
    
    @staticmethod
    def generate_random_ip():
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    @classmethod
    def create_syn_packet(cls, source_ip, target_ip, target_port):
        # --- IP HEADER ---
        version_ihl = (4 << 4) + 5
        tos = 0
        tot_len = 20 + 20  # IP + TCP
        id = random.randint(1000, 50000)
        frag_off = 0
        ttl = 64
        protocol = socket.IPPROTO_TCP
        check = 0 
        saddr = socket.inet_aton(source_ip)
        daddr = socket.inet_aton(target_ip)

        ip_header = struct.pack('!BBHHHBBH4s4s', 
            version_ihl, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)

        # --- TCP HEADER ---
        sport = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)
        ack_seq = 0
        doff = 5
        flags = 2 # SYN Flag
        window = socket.htons(5840)
        check = 0
        urg_ptr = 0
        offset_res = (doff << 4) + 0

        tcp_header = struct.pack('!HHLLBBHHH', 
            sport, target_port, seq, ack_seq, offset_res, flags, window, check, urg_ptr)

        return ip_header + tcp_header