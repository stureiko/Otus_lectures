resource "yandex_vpc_network" "network-1" {
	name = "network-1"
}

resource "yandex_vpc_subnet" "subnet-1" {
	name           = "subnet-1"
  zone           = "ru-central1-b"
  network_id     = yandex_vpc_network.network-1.id
  v4_cidr_blocks = ["192.168.10.0/24"]
}

resource "yandex_vpc_security_group" "mlflow-sg" {
  name        = "mlflow-security-group" # Choose a descriptive name
  network_id  = yandex_vpc_network.network-1.id # Replace with your network's ID
  description = "Allow inbound traffic on port 5000 for MLflow"

  ingress {
    protocol       = "TCP"
    description    = "Allow traffic on port 5000 from any source"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 5000
  }

  ingress {
    protocol       = "TCP"
    description    = "SSH"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = 22
  }

  egress {
    protocol       = "ANY"
    description    = "rule2 description"
    v4_cidr_blocks = ["0.0.0.0/0"]
    port           = -1
  }
}