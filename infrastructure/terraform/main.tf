terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstatellmbenchmark"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
  use_cli = true
  subscription_id = var.subscription_id
  client_id       = var.client_id
  client_secret   = var.client_secret
  tenant_id       = var.tenant_id
}

variable "subscription_id" {
  description = "The Azure subscription ID"
  type        = string
}

variable "client_id" {
  description = "The Azure client ID"
  type        = string
}

variable "client_secret" {
  description = "The Azure client secret"
  type        = string
  sensitive   = true
}

variable "tenant_id" {
  description = "The Azure tenant ID"
  type        = string
}

data "azurerm_resource_group" "aks_rg" {
  name = "llm-benchmark-rg-new-old-old"
}

data "azurerm_kubernetes_cluster" "existing_aks" {
  name                = "llm-benchmark-aks-new-old-old"
  resource_group_name = data.azurerm_resource_group.aks_rg.name
  count               = can(data.azurerm_resource_group.aks_rg.id) ? 1 : 0
}

resource "azurerm_kubernetes_cluster" "aks" {
  count               = length(data.azurerm_kubernetes_cluster.existing_aks) == 0 ? 1 : 0
  name                = "llm-benchmark-aks-new-old-old"
  location            = data.azurerm_resource_group.aks_rg.location
  resource_group_name = data.azurerm_resource_group.aks_rg.name
  dns_prefix          = "llm-benchmark"

  default_node_pool {
    name       = "default"
    node_count = 2
    vm_size    = "Standard_D2_v2"
  }

  identity {
    type = "SystemAssigned"
  }
}

locals {
  aks_cluster = length(data.azurerm_kubernetes_cluster.existing_aks) > 0 ? data.azurerm_kubernetes_cluster.existing_aks[0] : azurerm_kubernetes_cluster.aks[0]
}

provider "kubernetes" {
  host                   = local.aks_cluster.kube_config.0.host
  client_certificate     = base64decode(local.aks_cluster.kube_config.0.client_certificate)
  client_key             = base64decode(local.aks_cluster.kube_config.0.client_key)
  cluster_ca_certificate = base64decode(local.aks_cluster.kube_config.0.cluster_ca_certificate)
}

output "kube_config" {
  value     = local.aks_cluster.kube_config_raw
  sensitive = true
}