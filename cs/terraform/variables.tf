variable "proyect_name" {
    type        = string
    description = "Nombre base para los recursos"
    default     = "catsup"
}

variable "azure_location" {
    type        = string
    description = "Region de Azure"
    default     = "East US" # Puedes cambiarlo a la región que les hayan asignado
}