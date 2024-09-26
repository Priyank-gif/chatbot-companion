provider "aws" {
  region = "us-east-1" # Modify as needed
}

# Fetch the default VPC and subnets
data "aws_vpc" "default" {
  default = true
}

resource "aws_iam_role" "ec2_role" {
  name = "${local.app_name}-ec2-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      },
    ]
  })

  tags = merge(var.common_tags, { Name = "${local.app_name}-ec2-role" })
}

resource "aws_iam_policy" "ssm_policy" {
  name        = "${local.app_name}-ssm-policy"
  description = "Allow access to Secrets Manager and SSM Parameter Store"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ssm:GetParameter",
          "ssm:GetParameters",
          "ssm:GetParametersByPath",
          "secretsmanager:GetSecretValue"
        ]
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "ssm:DescribeParameters"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_ssm_policy" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.ssm_policy.arn
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "${local.app_name}-instance-profile"
  role = aws_iam_role.ec2_role.name
}

# data "aws_subnets" "public_subnets" {
#   filter {
#     name = "vpc-id"
#     values = [data.aws_vpc.default.id]
#   }
#
#   filter {
#     name = "subnet-type"
#     values = ["public"]
#   }
# }

# External file for tags (tags.tfvars)
# variable "common_tags" {
#   type = map(string)
# }

# Generate a random ID for conflict safety
resource "random_id" "resource_id" {
  byte_length = 4
}

# Combine app name from tags and random UUID
locals {
  app_name = "${var.common_tags["app"]}-${random_id.resource_id.hex}"
  subnets = ["subnet-06ca5b1fa649b2241", "subnet-0e1893daba9e469ec"]
}

# Application Load Balancer
resource "aws_lb" "app_load_balancer" {
  name                       = local.app_name
  internal                   = false
  load_balancer_type         = "application"
  security_groups = [aws_security_group.alb_sg.id]
  subnets                    = local.subnets
  enable_deletion_protection = false

  tags = merge(var.common_tags, { Name = "${local.app_name}-lt" })
}

# Security Group for ALB
resource "aws_security_group" "alb_sg" {
  vpc_id      = data.aws_vpc.default.id
  description = "Allow inbound HTTP/HTTPS traffic"

  # Security Group rules
  ingress {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.common_tags

  name = "${local.app_name}-alb-sg"
}

# Target Group
resource "aws_lb_target_group" "app_target_group" {
  name        = "${local.app_name}-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.default.id
  target_type = "instance"
  health_check {
    path                = "/health"
    protocol            = "HTTP"
    matcher             = "200"
    interval            = 30
    timeout             = 5
    healthy_threshold   = 5
    unhealthy_threshold = 2
  }

  tags = var.common_tags
}

# ALB Listener
resource "aws_lb_listener" "http_listener" {
  load_balancer_arn = aws_lb.app_load_balancer.arn
  port              = 80
  protocol          = "HTTP"
  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.app_target_group.arn
  }

  tags = var.common_tags
}

# Security Group for EC2 instances
resource "aws_security_group" "ec2_sg" {
  vpc_id      = data.aws_vpc.default.id
  description = "Allow all traffic to EC2 instances"

  ingress {
    from_port = 0
    to_port   = 65535
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.common_tags

  name = "${local.app_name}-ec2-sg"
}

# Launch Template for EC2
resource "aws_launch_template" "app_launch_template" {
  name_prefix   = "${local.app_name}-template"
  image_id      = data.aws_ami.ubuntu.id
  instance_type = "t3.small"
  key_name      = "kafka-burner"
  iam_instance_profile {
    name = aws_iam_instance_profile.ec2_instance_profile.name  # Use the instance profile here
  }
  # Clone Git repo and start Python app
  user_data = base64encode(<<-EOF
              #!/bin/bash
              cd /home/ubuntu/chatbot-companion
              git checkout tharun
              git pull
              sudo chmod +x deployment/
              ./deployment/env_init.sh
              ./deployment/run_app.sh
              EOF
  )

  vpc_security_group_ids = [aws_security_group.ec2_sg.id]

  tags = var.common_tags
}

# Auto Scaling Group for Canary Deployment
resource "aws_autoscaling_group" "app_asg" {
  desired_capacity = 1
  max_size         = 3
  min_size         = 1
  launch_template {
    id      = aws_launch_template.app_launch_template.id
    version = "$Latest"
  }
  vpc_zone_identifier = local.subnets
  target_group_arns = [aws_lb_target_group.app_target_group.arn]

  health_check_type         = "EC2"
  health_check_grace_period = 300
  default_cooldown          = 45
  tag {
    key                 = "Name"
    value = local.app_name  # Update to use your variable
    propagate_at_launch = true
  }
  lifecycle {
    create_before_destroy = true
  }
  force_delete = true
  # Add other tags as needed

}

# SSM Parameter to get latest Ubuntu AMI
data "aws_ssm_parameter" "ubuntu" {
  name = "/aws/service/canonical/ubuntu/server/20.04/stable/current/amd64/hvm/ebs-gp2/ami-id"
}

# Get the latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true
  owners = ["099720109477"] # Canonical Ubuntu
  filter {
    name = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }
}
