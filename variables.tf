variable "proyect_name" {
    type = string
}

variable "db_password" {
    type = string
    sensitive = true
}

#variable "hosted_zone_id" {
#    type = string
#}

variable "db_user" {
    type = string
}

variable "db_name" {
    type = string
}

variable "aws_region" {
    type = string
}