provider "helm" {
   kubernetes {
    host                   = local.aks_cluster.kube_config.0.host
    client_certificate     = base64decode(local.aks_cluster.kube_config.0.client_certificate)
    client_key             = base64decode(local.aks_cluster.kube_config.0.client_key)
    cluster_ca_certificate = base64decode(local.aks_cluster.kube_config.0.cluster_ca_certificate)
  }
}


resource "helm_release" "data_simulator" {
  name       = "data-simulator"
  chart      = "../helm/data-simulator"
  namespace  = "default"
  depends_on = [local.aks_cluster]

  set {
    name  = "image.repository"
    value = "llmretriever.azurecr.io/data-simulator"
  }

  set {
    name  = "image.tag"
    value = "latest"
  }

}

resource "helm_release" "data_retriever" {
  name       = "data-retriever"
  chart      = "../helm/data-retriever"
  namespace  = "default"
  depends_on = [local.aks_cluster]

  set {
    name  = "image.repository"
    value = "llmretriever.azurecr.io/data-retriever"
  }

  set {
    name  = "image.tag"
    value = "latest"
  }

}