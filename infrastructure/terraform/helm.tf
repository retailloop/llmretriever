provider "helm" {
  kubernetes {
    host                   = azurerm_kubernetes_cluster.aks.kube_config.0.host
    client_certificate     = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_certificate)
    client_key             = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.client_key)
    cluster_ca_certificate = base64decode(azurerm_kubernetes_cluster.aks.kube_config.0.cluster_ca_certificate)
  }
}

resource "kubernetes_secret" "llm_benchmark_secret" {
    metadata {
      name = "llm-benchmark-secret"
   }

   data = {
    DATABASE_URL = file("${path.module}/../../.env")
    RABBITMQ_URL = file("${path.module}/../../.env")
    REDIS_URL    = base64encode(file("${path.module}/../../.env"))
    API_PORT     = base64encode(file("${path.module}/../../.env"))
  }

  type = "Opaque"
}

resource "helm_release" "data_simulator" {
  name       = "data-simulator"
  chart      = "../helm/data-simulator"
  namespace  = "default"
  depends_on = [azurerm_kubernetes_cluster.aks, kubernetes_secret.llm_benchmark_secret]

  set {
    name  = "image.repository"
    value = "llmretriever.azurecr.io/data-simulator"
  }

  set {
    name  = "image.tag"
    value = "latest"
  }

  set {
    name = "envFromSecret"
    value = kubernetes_secret.llm_benchmark_secret.metadata[0].name
  }
}

resource "helm_release" "data_retriever" {
  name       = "data-retriever"
  chart      = "../helm/data-retriever"
  namespace  = "default"
  depends_on = [azurerm_kubernetes_cluster.aks, kubernetes_secret.llm_benchmark_secret]

  set {
    name  = "image.repository"
    value = "llmretriever.azurecr.io/data-retriever"
  }

  set {
    name  = "image.tag"
    value = "latest"
  }

  set {
    name  = "envFromSecret"
    value = kubernetes_secret.llm_benchmark_secret.metadata[0].name
  }
}