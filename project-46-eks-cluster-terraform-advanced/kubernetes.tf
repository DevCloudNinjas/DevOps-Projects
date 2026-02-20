###### root/kubernetes.tf

resource "kubernetes_deployment" "project102" {
  metadata {
    name = "terraform-project102"
    labels = {
      test = "Myproject102App"
    }
  }

  spec {
    replicas = 2
    selector {
      match_labels = {
        test = "Myproject102App"
      }
    }
    template {
      metadata {
        labels = {
          test = "Myproject102App"
        }
      }
      spec {
        container {
          image = "nginx:1.7.8"
          name  = "project102"

          resources {
            limits = {
              cpu    = "0.5"
              memory = "512Mi"
            }
            requests = {
              cpu    = "250m"
              memory = "50Mi"
            }
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "project102" {
  metadata {
    name = "terraform-project102"
  }

  spec {
    selector = {
      test = "myproject102App"
    }
    port {
      port        = 80
      target_port = 80
      node_port   = 30010
    }

    type = "LoadBalancer"
  }
}
