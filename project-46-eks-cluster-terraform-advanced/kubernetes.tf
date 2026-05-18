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
        security_context {
          seccomp_profile {
            type = "RuntimeDefault"
          }
        }

        container {
          image = "nginx:1.27-alpine"
          name  = "project102"

          port {
            container_port = 80
          }

          liveness_probe {
            http_get {
              path = "/"
              port = 80
            }

            initial_delay_seconds = 15
            period_seconds        = 20
          }

          readiness_probe {
            http_get {
              path = "/"
              port = 80
            }

            initial_delay_seconds = 5
            period_seconds        = 10
          }

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

          security_context {
            allow_privilege_escalation = false
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
      test = "Myproject102App"
    }
    port {
      port        = 80
      target_port = 80
      node_port   = 30010
    }

    type = "LoadBalancer"
  }
}
