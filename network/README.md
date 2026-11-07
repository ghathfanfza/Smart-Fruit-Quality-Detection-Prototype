# Perancangan Jaringan

Topologi hierarkis di Cisco Packet Tracer untuk mendukung sistem Smart Fruit Quality Sorter.

**Perangkat:** 1 Router Cisco 2911 (DHCP server dan jalur ke ISP), 1 Multilayer Switch Cisco 3560 (core, Inter-VLAN routing lewat SVI), 3 Access Switch Cisco 2960 (IoT, Admin/Server, Security).

| VLAN | Nama | Fungsi | Subnet | Gateway |
|---|---|---|---|---|
| 10 | IoT | Perangkat IoT dan komputer operasional | 192.168.10.0/24 | 192.168.10.1 |
| 20 | Server | Smart Agriculture Server | 192.168.20.0/24 | 192.168.20.1 |
| 30 | Admin | Komputer administrator | 192.168.30.0/24 | 192.168.30.1 |
| 40 | Security | CCTV dan komputer keamanan | 192.168.40.0/24 | 192.168.40.1 |
| 99 | Management | Manajemen perangkat jaringan | - | - |

**Fitur:** VLAN 802.1Q (trunk antar switch), Inter-VLAN routing (SVI dan `ip routing`), DHCP di router dengan DHCP relay (`ip helper-address`) pada tiap interface VLAN, dan ACL.

**Hasil uji:** DHCP memberi IP otomatis sesuai VLAN. Ping antar VLAN berhasil lewat multilayer switch. Admin dan perangkat IoT dapat mengakses server, sedangkan Security PC diblokir oleh ACL.

**Uplink:** multilayer switch terhubung ke router lewat port routed Fa0/4 (10.10.10.2/30, router 10.10.10.1), dengan default route ke router dan `ip helper-address 10.10.10.1` di tiap SVI.

**ACL:** `SECURITY-TO-SERVER` menolak trafik VLAN 40 (Security) ke VLAN 20 (Server) dan mengizinkan sisanya, dipasang di SVI VLAN 40 arah masuk.

**Berkas:**
- `OrangeField.pkt`: file topologi Packet Tracer
