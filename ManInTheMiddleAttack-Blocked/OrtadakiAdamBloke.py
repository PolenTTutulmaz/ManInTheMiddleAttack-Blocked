import socket
import subprocess
import re
import random
import platform
import wmi


def get_arp_table():
    try:
        result = subprocess.check_output(["arp", "-a"]).decode("utf-8")
        lines = result.split("\n")[3:-1]
        arp_table = [re.split(r"\s+", line.strip()) for line in lines]

        return arp_table
    except Exception as e:
        print(f"Hata: {e}")
        return None


# ARP tablosunu al
arp_table = get_arp_table()
if arp_table:
    # print("ARP Tablosu:")
    for entry in arp_table:
        IP_Adres = entry[0]
        MAC_Adres = entry[1]
else:
    print("ARP Tablosu alınamadı.")


def get_default_gateway():
    try:
        result = subprocess.check_output(["ipconfig"]).decode("utf-8")
        gateway_match = re.search(r"Default Gateway.*?: ([\d\.]+)", result)

        if gateway_match:
            gateway_ip = gateway_match.group(1)

            # Default gateway MAC adresini al
            arp_table = get_arp_table()
            gateway_mac = None
            for entry in arp_table:
                if entry[0] == gateway_ip:
                    gateway_mac = entry[1]
                    break

            if gateway_mac:
                return gateway_ip, gateway_mac
            else:
                print("Default Gateway MAC adresi bulunamadı.")
                return None
        else:
            print("Default Gateway adresi bulunamadı.")
            return None
    except Exception as e:
        print(f"Hata: {e}")
        return None


# Default gateway adresini al
default_gateway_info = get_default_gateway()
if default_gateway_info:
        Default_Gateway_IP_Adres = default_gateway_info[0]
        Default_Gateway_Mac_Adres = default_gateway_info[1]

arp_table_tuples = [tuple(entry) for entry in arp_table]
#print(arp_table_tuples)
gateway_mac = list(default_gateway_info[1])
result = ''.join(gateway_mac)

sayac = sum(1 for eleman in arp_table_tuples if result in eleman)

if sayac == 1:
    print("Saldırı altında değilsiniz")
    input()
else:
    print("Saldırı altındasınız!")

    deger = input("Saldırıyı bloke etmek ister misiniz?  Y/N")
    if deger == "y" or deger == "Y":
        def dhcp_ip_changer():
            nic_configs = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=True)

            # First network adaptor
            nic = nic_configs[0]

            # Enable DHCP
            nic.EnableDHCP()
            return True


        def static_ip_changer(ip, subnetmask, gateway, dns1, dns2):
            nic_configs = wmi.WMI('').Win32_NetworkAdapterConfiguration(IPEnabled=True)

            # First network adaptor
            nic = nic_configs[0]

            # Set IP address, subnetmask, default gateway, and DNS
            a = nic.EnableStatic(IPAddress=[ip], SubnetMask=[subnetmask])
            b = nic.SetGateways(DefaultIPGateway=[gateway])
            c = nic.SetDNSServerSearchOrder([dns1, dns2])
            d = nic.SetDynamicDNSRegistration(FullDNSRegistrationEnabled=1)

            if [a[0], b[0], c[0], d[0]] == [0, 0, 0, 0]:
                return True
            else:
                return False


        # DHCP'ye geçiş
        #print("DHCP'ye geçiş yapıldı:", dhcp_ip_changer())


        def get_local_ip():
            try:
                # Windows sistemlerinde hostname ile IP alınabilir
                if platform.system() == "Windows":
                    host_ip = socket.gethostbyname(socket.gethostname())
                else:
                    # Diğer sistemlerde socket modülü kullanılır
                    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    s.connect(("8.8.8.8", 80))  # Google'ın DNS sunucusuna geçici bir bağlantı
                    host_ip = s.getsockname()[0]
                    s.close()
                return host_ip
            except Exception as e:
                print("IP adresi alınamadı:", str(e))
                return None


        # IP adresini al ve ekrana yazdır
        ip_address = get_local_ip()
        #if ip_address:
            #print("Cihazın IP Adresi:", ip_address)


        def generate_random_ip(base_ip):
            # Ayıracı kullanarak IP'yi böl
            base_ip_parts = base_ip.split('.')

            # İlk üç hane
            first_three_parts = base_ip_parts[:3]

            # Rastgele son hane seç
            last_part = str(random.randint(2, 254))  # 0,1 ve 255 olmamalı, bu yüzden 2-254 arası seçiyoruz

            # Yeni IP'yi birleştir
            new_ip = '.'.join(first_three_parts + [last_part])

            return new_ip


        # Örnek kullanım
        base_ip_address = ip_address
        random_ip_address = generate_random_ip(base_ip_address)

        #print("Eski IP Adresi:", base_ip_address)
        #print("Yeni Rastgele IP Adresi:", random_ip_address)

        # Statik IP ayarı
        ip_address = random_ip_address
        subnet_mask = "255.255.255.0"
        default_gateway = default_gateway_info[0]
        dns_server1 = "8.8.8.8"
        dns_server2 = "8.8.4.4"

        #print("Statik IP ayarı yapıldı:",
        static_ip_changer(ip_address, subnet_mask, default_gateway, dns_server1, dns_server2)

        print("Saldırı başarıyla bloke edildi!")
        input()

    if deger == "n" or deger == "N":
        print("""
        Saldırıyı bloke edemedik. 
        Bulunduğunuz ağdaki biri tarafından saldırıya uğruyorsunuz!
        Ortak ağdan çıkıp güvenilir bir ağa bağlanmanızı tavsiye ederiz!""")

        input()





