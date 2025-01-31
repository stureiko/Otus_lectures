resource "yandex_compute_instance" "vm-1" {
  name = "vm-1"
	platform_id = "standard-v1"
  zone        = "ru-central1-b"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    disk_id = yandex_compute_disk.boot-disk-1.id
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.subnet-1.id
    nat       = true
    security_group_ids = [yandex_vpc_security_group.mlflow-sg.id] # Assign the security group
  }

  metadata = {
    ssh-keys = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
  }

  provisioner "file" {
    source      = "mlflow-script.sh"       # Локальный файл, который будет скопирован
    destination = "/home/ubuntu/my-script.sh"

    connection {
    type     = "ssh"
    user     = "ubuntu"
    host     = self.network_interface.0.nat_ip_address
    agent = true # использовать ssh-agent для авторизации
    }
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /home/ubuntu/my-script.sh",  # Делаем скрипт исполняемым
      "/home/ubuntu/my-script.sh"           # Запускаем скрипт
    ]

    connection {
      type        = "ssh"
      user        = "ubuntu"
      host        = self.network_interface.0.nat_ip_address
      agent = true # использовать ssh-agent для авторизации)
    }
  }
}

output "external_ip_address_vm_1" {
  value = yandex_compute_instance.vm-1.network_interface.0.nat_ip_address
}
