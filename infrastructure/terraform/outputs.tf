output "data_retriever_ip" {
  value = data.kubernetes_service.data_retriever.status.0.load_balancer.0.ingress.0.ip
}

data "kubernetes_service" "data_retriever" {
  metadata {
    name = "data-retriever"
  }

  depends_on = [helm_release.data_retriever]
}