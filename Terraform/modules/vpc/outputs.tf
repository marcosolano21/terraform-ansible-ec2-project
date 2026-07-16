output "subnet-id-output" {
  description = "Subnet-id-value"
  value = aws_subnet.subnet1.id
}

output "VPC-EC2-instance" {
  description = "VPC for the EC2 instance"
  value = aws_vpc.my_vpc.id
}

output "security-group-output" {
  description = "Output for the security group"
  value = aws_security_group.webSg.id
}

output "security-group-Node-Exporter-output" {
  description = "Output for the Node Exporter security group"
  value = aws_security_group.SG-Node-Exporter.id
}