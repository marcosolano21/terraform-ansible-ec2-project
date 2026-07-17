output "Monitoring-Instance-Public-IP" {
  description = "EC2 instance public-IP for Prometheus instance: "
  value = module.ec2_instance.web1.EC2-instance-publicIP
}

output "Target-Instance-Public-IP" {
  description = "EC2 instance public-IP for Node-Exporter instance: "
  value = module.ec2_instance.web2.EC2-instance-publicIP
}