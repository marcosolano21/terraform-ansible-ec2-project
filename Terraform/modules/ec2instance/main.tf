resource "aws_instance" "EC2-instance" {
    ami = var.ami_value
    instance_type = var.instance_type_value
    subnet_id = var.subnet_id_value
    associate_public_ip_address = true
    key_name = "aws_login"
    vpc_security_group_ids = [var.security-group]
}
