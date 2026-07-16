output "EC2-Prometheus-IP" {
  description = "EC2 instance public-IP for Prometheus instance: "
  value = module.ec2_instance.web1.EC2-instance-publicIP
}

output "EC2-Node-Exporter-IP" {
  description = "EC2 instance public-IP for Node-Exporter instance: "
  value = module.ec2_instance.web2.EC2-instance-publicIP
}