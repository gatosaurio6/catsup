provider "aws" {
    region = var.aws_region
}

resource "aws_vpc" "main" {
    cidr_block = "10.0.0.0/16"
    enable_dns_hostnames = true
    enable_dns_support = true
    tags = {Name = "vpc-${var.proyect_name}-hibrida"}
}

resource "aws_internet_gateway" "igw" {
    vpc_id = aws_vpc.main.id
    tags = {Name = "igw-${var.proyect_name}"}
}

resource "aws_subnet" "public_az1" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.1.0/24"
    availability_zone = "us-east-1a"
    map_public_ip_on_launch = true
    tags = {Name = "subnet-${var.proyect_name}-public-useast1"}
}

resource "aws_subnet" "public_az2" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.2.0/24"
    availability_zone = "us-east-1b"
    map_public_ip_on_launch = true
    tags = {Name = "subnet-${var.proyect_name}-public-useast2"}
}

resource "aws_subnet" "private_az1" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.3.0/24"
    availability_zone = "us-east-1a"
    tags = {Name = "subnet-${var.proyect_name}-private-az1"}
}

resource "aws_subnet" "private_az2" {
    vpc_id = aws_vpc.main.id
    cidr_block = "10.0.4.0/24"
    availability_zone = "us-east-1b"
    tags = {Name = "subnet-${var.proyect_name}-private-az2"}
}

resource "aws_route_table" "public_rt" {
    vpc_id = aws_vpc.main.id
    route {
        cidr_block = "0.0.0.0/0"
        gateway_id = aws_internet_gateway.igw.id
    }
    tags = {Name = "rt-${var.proyect_name}-publica"}
}

resource "aws_route_table_association" "pub1" {
    subnet_id = aws_subnet.public_az1.id
    route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table_association" "pub2" {
    subnet_id = aws_subnet.public_az2.id
    route_table_id = aws_route_table.public_rt.id
}

resource "aws_security_group" "alb_sg" {
    name = "sg_alb_${var.proyect_name}"
    description = "permite trafico HTTP externo hacia el balanceador"
    vpc_id = aws_vpc.main.id

    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_lb" "app_alb" {
    name = "alb-${var.proyect_name}"
    internal = false
    load_balancer_type = "application"
    security_groups = [aws_security_group.alb_sg.id]
    subnets = [aws_subnet.public_az1.id, aws_subnet.public_az2.id]
    tags = {Name = "alb-${var.proyect_name}"}
}

resource "aws_lb_target_group" "alb_tg" {
    name = "tg-${var.proyect_name}"
    port = 80
    protocol = "HTTP"
    vpc_id = aws_vpc.main.id

    health_check {
        path = "/"
        port = "80"
        protocol = "HTTP"
        healthy_threshold = 3
        unhealthy_threshold = 3
        timeout = 5
        interval = 30
    }
}

#resource "aws_lb_target_group_attachment" "tg_attach" {
#    target_group_arn = aws_lb_target_group.alb_tg.arn
#    target_id = aws_instance.app_server.id
#    port = 80
#}

resource "aws_lb_listener" "http_listener" {
    load_balancer_arn = aws_lb.app_alb.arn
    port = "80"
    protocol = "HTTP"
    default_action {
        type = "forward"
        target_group_arn = aws_lb_target_group.alb_tg.arn
    }
}

resource "aws_security_group" "backend_sg" {
    name = "sg_backend_${var.proyect_name}"
    description = "permite trafico HTTP, HTTPS y SSH al servidor web"
    vpc_id = aws_vpc.main.id
    ingress {
        from_port = 80
        to_port = 80
        protocol = "tcp"
        security_groups = [aws_security_group.alb_sg.id]
    }
    ingress {
        from_port = 443
        to_port = 443
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    ingress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 22
        to_port = 22
        protocol = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }    
}

resource "aws_security_group" "rds_sg" {
    name = "sg_rds_${var.proyect_name}"
    description = "permite conexion a postgreSQL solo desde el servidor web"
    vpc_id = aws_vpc.main.id

    ingress {
        from_port = 5432
        to_port = 5432
        protocol = "tcp"
        security_groups = [aws_security_group.backend_sg.id]
    }
    #ingress {
    #    from_port = 5432
    #    to_port = 5432
    #    protocol = "tcp"
    #    cidr_blocks = [var.azurerm_public_ip]
    #}
    egress {
        from_port = 0
        to_port = 0
        protocol = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_route53_zone" "internal_dns" {
    name = "${var.proyect_name}.local"
    vpc {
        vpc_id = aws_vpc.main.id
    }
}

resource "aws_route53_record" "api_dns" {
    zone_id = aws_route53_zone.internal_dns.zone_id
    name = "api.${var.proyect_name}.local"
    type = "A"
    alias {
        name = aws_lb.app_alb.dns_name
        zone_id = aws_lb.app_alb.zone_id
        evaluate_target_health = true
    }
}

resource "aws_db_subnet_group" "private_subnets" {
    name = "rds-private-subnet-group-${var.proyect_name}"
    subnet_ids = [aws_subnet.private_az1.id, aws_subnet.private_az2.id]
    tags = {Name = "RDS private subnet group"}
}

resource "aws_db_instance" "postgreSQL" {
    allocated_storage = 20
    max_allocated_storage = 100
    engine = "postgres"
    engine_version = "15"
    instance_class = "db.t3.micro"
    db_name = var.db_name
    username = var.db_user
    password = var.db_password

    db_subnet_group_name = aws_db_subnet_group.private_subnets.name
    vpc_security_group_ids = [aws_security_group.rds_sg.id]
    skip_final_snapshot = true
    publicly_accessible = false
    multi_az = true
}

resource "aws_instance" "app_server" {
    ami = "ami-0c7217cdde317cfec"
    instance_type = "t2.micro"
    subnet_id = aws_subnet.public_az1.id
    vpc_security_group_ids = [aws_security_group.backend_sg.id]
    key_name = aws_key_pair.deployer_key.key_name
    tags = {Name = "servidor-${var.proyect_name}"}
}

resource "aws_eip" "app_eip" {
    instance = aws_instance.app_server.id
    domain = "vpc"
    tags = {Name = "eip-${var.proyect_name}"}
}

resource "local_file" "ansibe_inventory" {
    content = <<EOT
    [app_servers]
    ${aws_eip.app_eip.public_ip} ansible_user=ubuntu ansible_ssh_private_key_file=./llave-${var.proyect_name}.pem
    EOT
    filename = "${path.module}/../ansible/inventory.ini"
}

resource "tls_private_key" "vm_key" {
    algorithm = "RSA"
    rsa_bits = 4096
}

resource "aws_key_pair" "deployer_key" {
    key_name = "llave-${var.proyect_name}"
    public_key = tls_private_key.vm_key.public_key_openssh
}

resource "local_file" "private_key_pem" {
    filename = "${path.module}/../ansible/llave-${var.proyect_name}.pem"
    content = tls_private_key.vm_key.private_key_pem
    file_permission = "0400"
}

output "instancia_ip_publica" {
  value       = aws_eip.app_eip.public_ip
  description = "La IP elástica pública del servidor para que sepas a dónde conectarte"
}