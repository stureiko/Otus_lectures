// Создание бакета с использованием ключа
resource "yandex_storage_bucket" "my-test-bucket" {
  bucket                = "my-new-test-bucket"
  max_size              = 0
  anonymous_access_flags {
    read        = true
    list        = true
    config_read = true
  }
  tags = {
    out_name = "otus"
  }
}