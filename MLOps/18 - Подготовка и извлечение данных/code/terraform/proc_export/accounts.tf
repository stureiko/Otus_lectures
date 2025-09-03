resource "yandex_iam_service_account" "dataproc" {
  depends_on = [ data.yandex_resourcemanager_folder.foo ]
  name        = "dataproc"
  description = "service account to manage Dataproc Cluster"
  folder_id   = data.yandex_resourcemanager_folder.foo.id
}

data "yandex_resourcemanager_folder" "foo" {
  folder_id = var.folder_id
}

resource "yandex_resourcemanager_folder_iam_binding" "dataproc" {
  folder_id = data.yandex_resourcemanager_folder.foo.id
  role      = "mdb.dataproc.agent"
  members = [
    "serviceAccount:${yandex_iam_service_account.dataproc.id}",
  ]
}