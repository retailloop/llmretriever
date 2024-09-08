provider "helm" {
  kubernetes {
    host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
    client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
    client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
    cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
  }
}

resource "helm_release" "data_simulator" {
  name       = "data-simulator"
  chart      = "../helm/data-simulator"
  namespace  = "default"
  depends_on = [azurerm_kubernetes_cluster.aks]

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
  depends_on = [azurerm_kubernetes_cluster.aks]

  set {
    name  = "image.repository"
    value = "llmretriever.azurecr.io/data-retriever"
  }

  set {
    name  = "image.tag"
    value = "latest"
  }
}