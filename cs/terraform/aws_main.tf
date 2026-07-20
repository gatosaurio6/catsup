# 1. Le decimos a Terraform que use Azure
provider "azurerm" {
  features {}
}

# 2. Grupo de Recursos (La "carpeta" donde vivirá todo en Azure)
resource "azurerm_resource_group" "rg" {
  name     = "${var.proyect_name}-rg"
  location = var.azure_location
}

# 3. BLOB STORAGE (Lo que te pidió tu compañero para las fotos)
resource "azurerm_storage_account" "storage" {
  name                     = "${var.proyect_name}storage2026" # Azure exige que este nombre no tenga guiones y sea único
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "blob" {
  name                  = "imagenes"
  storage_account_name  = azurerm_storage_account.storage.name
  container_access_type = "private"
}

# 4. IP PÚBLICA (La que debes poner luego en el default.conf de Nginx)
resource "azurerm_public_ip" "lb_ip" {
  name                = "ip-balanceador-${var.proyect_name}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# 5. BALANCEADOR DE CARGA (Load Balancer)
resource "azurerm_lb" "alb" {
  name                = "lb-${var.proyect_name}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "ip_publica_frontal"
    public_ip_address_id = azurerm_public_ip.lb_ip.id
  }
}

# 6. OUTPUT: Esto te mostrará la IP en la terminal al terminar
output "ip_azure" {
  value       = azurerm_public_ip.lb_ip.ip_address
  description = "Esta es la IP que debes copiar y pegar en Nginx"
}