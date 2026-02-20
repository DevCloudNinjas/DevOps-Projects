terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
    gitlab = {
      source = "gitlabhq/gitlab"
      version = "~> 3.0"
    }  
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "<= 2.0.0"
    }
    rancher2 = {
      source = "rancher/rancher2"
      version = ">= 1.10.0" 
    }
  }
}
#
provider "gitlab" {
  base_url = "https://gitlab.clarusway.com/"
}

# Configure the AWS Provider
provider "aws" {
  region = "us-east-2"
}

data "gitlab_project" "my_project" {
  id = "{{ci_project_path}}"
}

resource gitlab_project_cluster "k3s" {
  project                       = "19"
  name                          = "cluster"
  domain                        = "my_DNS.nip.io"
  enabled                       = true
  kubernetes_api_url            = "https://ec2-private_ip:6443"
  kubernetes_token              = templatefile("./linux.txt", { })
  kubernetes_ca_cert            = templatefile("./cert.txt", { })
  kubernetes_namespace          = "linux-dev"
  kubernetes_authorization_type = "rbac"
  environment_scope             = "*"
  management_project_id         = "19"
  depends_on = [ time_sleep.wait ]
  
}
