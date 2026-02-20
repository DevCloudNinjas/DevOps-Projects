variable "bastion_vpc_cidr" {
  default = "192.168.0.0/16"
}

variable "app_vpc_cidr" {
  default = "172.32.0.0/16"
}

variable "jfrog_username" {
  description = "Username for JFrog Artifactory"
  type        = string
}

variable "jfrog_password" {
  description = "Password for JFrog Artifactory"
  type        = string
  sensitive   = true
}

variable "sonar_token" {
  description = "SonarCloud authentication token"
  type        = string
  sensitive   = true
}

variable "mysql_host" {
  description = "Hostname of the MySQL instance"
  type        = string
}

variable "mysql_database" {
  description = "Name of the MySQL database"
  type        = string
}

variable "mysql_database_name" {
  description = "Name of the MySQL database"
  type        = string
}

variable "sonar_project_key" {
  description = "SonarCloud project key"
  type        = string
}

variable "sonar_url" {
  description = "SonarCloud project key"
  type        = string
}

variable "sonar_organization" {
  description = "SonarCloud organization"
  type        = string
}

variable "jfrog_url" {
  description = "URL of the JFrog Artifactory instance"
  type        = string
}

variable "db_password" {
  description = "Password for the RDS instance"
  type        = string
}