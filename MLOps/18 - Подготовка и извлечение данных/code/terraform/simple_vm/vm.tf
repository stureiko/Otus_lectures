resource "yandex_compute_instance" "vm" {
  name        = "nixys"
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
    subnet_id      = "e2lga3gq6j31jgqnm309"
    nat            = true
  }

  metadata = {
    ssh-keys  = "ubuntu:${file("~/.ssh/id_ed25519.pub")}"
  }
}

output "external_ip_address_vm_1" {
  value = yandex_compute_instance.vm.network_interface.0.nat_ip_address
}
