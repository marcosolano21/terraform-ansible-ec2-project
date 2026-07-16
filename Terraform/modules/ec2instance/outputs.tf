output "EC2-instance-publicIP" {
    description = "EC2 public IP"
    value = aws_instance.EC2-instance.public_ip
}

output "subnet-ID-EC2-instance" {
  description = "Subnet ID for the EC2 instance"
  value = aws_instance.EC2-instance.subnet_id
}