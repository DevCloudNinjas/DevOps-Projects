terraform {
  required_providers {
    github = {
      source = "integrations/github"
      version = "5.44.0"
    }
  }
}

provider "github" {
  # Configuration options
}

resource "github_branch" "development" {
  repository = "Github-Examples"
  branch     = "sdks"
}