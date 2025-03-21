# Deploy several copies

resource "yandex_compute_instance" "nixys" {
  count = var.copies
  name        = "nixys-${count.index + 1}"
  platform_id = "standard-v1"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = "fd8tvc3529h2cpjvpkr5"
    }
  }

  network_interface {
    subnet_id      = "e2lsa9cv0qvodorot0ku"
    nat            = true
  }

  metadata = {
    ssh-keys  = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
  }
}

output "vm_names_and_ips" {
  value = {
    for instance in yandex_compute_instance.nixys :
    instance.name => instance.network_interface.0.nat_ip_address
  }
}