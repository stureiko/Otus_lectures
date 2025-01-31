terraform {
  required_providers {
    yandex = {
      source = "yandex-cloud/yandex"
    }
  }
  required_version = ">= 0.13"
}

provider "yandex" {
  service_account_key_file = "key.json"
  cloud_id                 = "b1g59fgabceft2f099ji"
  folder_id                = "b1gd3fqn5rn2107tg9b8"
  zone = "ru-central1-b"
}
