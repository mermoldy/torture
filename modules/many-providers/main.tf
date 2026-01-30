terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.0"
    }
    helm = {
      source  = "hashicorp/helm"
      version = "~> 2.0"
    }
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
    vault = {
      source  = "hashicorp/vault"
      version = "~> 3.0"
    }
    consul = {
      source  = "hashicorp/consul"
      version = "~> 2.0"
    }
    nomad = {
      source  = "hashicorp/nomad"
      version = "~> 2.0"
    }
    datadog = {
      source  = "DataDog/datadog"
      version = "~> 3.0"
    }
    newrelic = {
      source  = "newrelic/newrelic"
      version = "~> 3.0"
    }
    pagerduty = {
      source  = "PagerDuty/pagerduty"
      version = "~> 3.0"
    }
    github = {
      source  = "integrations/github"
      version = "~> 6.0"
    }
    gitlab = {
      source  = "gitlabhq/gitlab"
      version = "~> 17.0"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.0"
    }
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
    linode = {
      source  = "linode/linode"
      version = "~> 2.0"
    }
    heroku = {
      source  = "heroku/heroku"
      version = "~> 5.0"
    }
    mongodbatlas = {
      source  = "mongodb/mongodbatlas"
      version = "~> 1.0"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.90"
    }
    databricks = {
      source  = "databricks/databricks"
      version = "~> 1.0"
    }
    okta = {
      source  = "okta/okta"
      version = "~> 4.0"
    }
    auth0 = {
      source  = "auth0/auth0"
      version = "~> 1.0"
    }
    grafana = {
      source  = "grafana/grafana"
      version = "~> 3.0"
    }
    elasticsearch = {
      source  = "phillbaker/elasticsearch"
      version = "~> 2.0"
    }
    mysql = {
      source  = "petoju/mysql"
      version = "~> 3.0"
    }
    postgresql = {
      source  = "cyrilgdn/postgresql"
      version = "~> 1.0"
    }
    mailgun = {
      source  = "wgebis/mailgun"
      version = "~> 0.7"
    }
    twilio = {
      source  = "twilio/twilio"
      version = "~> 0.18"
    }
    opsgenie = {
      source  = "opsgenie/opsgenie"
      version = "~> 0.6"
    }
    tfe = {
      source  = "hashicorp/tfe"
      version = "~> 0.50"
    }
    time = {
      source  = "hashicorp/time"
      version = "~> 0.10"
    }
    http = {
      source  = "hashicorp/http"
      version = "~> 3.0"
    }
    external = {
      source  = "hashicorp/external"
      version = "~> 2.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
    tls = {
      source  = "hashicorp/tls"
      version = "~> 4.0"
    }
    acme = {
      source  = "vancluever/acme"
      version = "~> 2.0"
    }
    cloudinit = {
      source  = "hashicorp/cloudinit"
      version = "~> 2.0"
    }
    ad = {
      source  = "hashicorp/ad"
      version = "~> 0.4"
    }
    dns = {
      source  = "hashicorp/dns"
      version = "~> 3.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

# Dummy resource to force provider downloads
resource "null_resource" "provider_init" {
  triggers = {
    timestamp = timestamp()
  }
}
