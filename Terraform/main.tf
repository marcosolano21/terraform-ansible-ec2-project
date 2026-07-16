module "ec2_instance" {

  for_each = {
    web1 = {
      name          = "web-server-1"
      instance_type = "t2.micro"
      security-group = module.VPC.security-group-output
      tags = {
        Name = "Prometheus-Instance"
      }
    }
    web2 = {
      name          = "web-server-2"
      instance_type = "t2.micro"
      security-group = module.VPC.security-group-Node-Exporter-output
      tags = {
        Name = "Node-Exporter-Instance"
      }
    }
  }
  source = "./modules/ec2instance"
  ami_value = "ami-091138d0f0d41ff90" # Ubuntu 20.04 en us-east-1
  instance_type_value = each.value.instance_type
  subnet_id_value = module.VPC.subnet-id-output
  security-group = each.value.security-group
}

module "VPC" {
  source = "./modules/vpc"
  availability_zone = "us-east-1a"
  IP_Source = "0.0.0.0/0" # IP where you want to connect from, in this case it allows connections from all directions
}
