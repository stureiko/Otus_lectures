resource "yandex_vpc_network" "network-1" {
	name = "network-1"
}

resource "yandex_vpc_subnet" "subnet-1" {
	name           = "subnet-1"
  zone           = "ru-central1-b"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}
