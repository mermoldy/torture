terraform {
  required_version = ">= 1.0"

  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

# Small resource - minimal data, fast to plan
resource "null_resource" "small_resource" {
  count = var.small_resource_count

  triggers = {
    index     = count.index
    timestamp = timestamp()
  }
}

# Medium resource - ~1MB per resource, low CPU usage
resource "null_resource" "medium_resource" {
  count = var.medium_resource_count

  triggers = {
    index                  = count.index
    timestamp              = timestamp()
    log_lines_per_resource = var.medium_log_lines_per_resource

    # ~100KB per attribute × 10 attributes = ~1MB total
    attribute_1  = join("", [for i in range(100) : "AAAAAAAAAA_STATIC_PADDING_BLOCK_RESOURCE_DATA_SEGMENT_${count.index}_${i}_"])
    attribute_2  = join("", [for i in range(100) : "BBBBBBBBBB_FIXED_CONTENT_FILLER_TEXT_ATTRIBUTE_VALUE_${count.index}_${i}_"])
    attribute_3  = join("", [for i in range(100) : "CCCCCCCCCC_HARDCODED_STRING_REPEATED_PATTERN_DATA_${count.index}_${i}_"])
    attribute_4  = join("", [for i in range(100) : "DDDDDDDDDD_CONSTANT_VALUE_PADDING_INFORMATION_BLOCK_${count.index}_${i}_"])
    attribute_5  = join("", [for i in range(100) : "EEEEEEEEEE_PREDETERMINED_TEXT_STATIC_RESOURCE_DATA_${count.index}_${i}_"])
    attribute_6  = join("", [for i in range(100) : "FFFFFFFFFF_LITERAL_STRING_FIXED_PATTERN_CONTENT_${count.index}_${i}_"])
    attribute_7  = join("", [for i in range(100) : "GGGGGGGGGG_INVARIANT_DATA_HARDCODED_SEGMENT_BLOCK_${count.index}_${i}_"])
    attribute_8  = join("", [for i in range(100) : "HHHHHHHHHH_STATIC_FILLER_PREDETERMINED_VALUE_TEXT_${count.index}_${i}_"])
    attribute_9  = join("", [for i in range(100) : "IIIIIIIIII_CONSTANT_PATTERN_FIXED_RESOURCE_PADDING_${count.index}_${i}_"])
    attribute_10 = join("", [for i in range(100) : "JJJJJJJJJJ_LITERAL_CONTENT_HARDCODED_DATA_SEGMENT_${count.index}_${i}_"])
  }

  provisioner "local-exec" {
    when    = create
    command = <<-EOT
      echo "==== Starting provisioning for resource ${count.index} ===="
      for i in $(seq 1 ${var.medium_log_lines_per_resource}); do
        echo "[Resource ${count.index}] Log line $i: Processing operation $(date +%s%N) with detailed information about the current state and configuration changes being applied to the infrastructure"
        sleep 0.1
      done
      echo "==== Completed provisioning for resource ${count.index} ===="
    EOT
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<-EOT
      echo "==== Starting destruction for resource ${self.triggers.index} ===="
      for i in $(seq 1 ${self.triggers.log_lines_per_resource}); do
        echo "[Resource ${self.triggers.index}] Destroy log line $i: Removing resource $(date +%s%N) and cleaning up all associated configurations and state"
        sleep 0.1
      done
      echo "==== Completed destruction for resource ${self.triggers.index} ===="
    EOT
  }
}

# Heavy resource - ~1MB per resource, high CPU usage (hashing, encoding)
resource "null_resource" "heavy_resource" {
  count = var.heavy_resource_count

  triggers = {
    index                  = count.index
    timestamp              = timestamp()
    log_lines_per_resource = var.heavy_log_lines_per_resource

    # ~100KB per attribute with CPU-intensive operations
    attribute_1 = join("", [
      for i in range(200) :
      "${md5("${count.index}-${i}")}_${base64encode("data-${i}")}_"
    ])

    attribute_2 = join("", [
      for i in range(200) :
      "${sha256("resource-${count.index}-segment-${i}")}_"
    ])

    attribute_3 = jsonencode({
      for i in range(100) :
      "key_${i}" => {
        hash   = md5("${count.index}-${i}")
        b64    = base64encode("value-${count.index}-${i}")
        nested = "DATA_${i}_${count.index}_${formatdate("YYYYMMDDhhmmss", timestamp())}"
      }
    })

    attribute_4 = join("", [
      for i in range(200) :
      "${md5("heavy-${i}-${count.index}")}_${sha1("segment-${i}")}_"
    ])

    attribute_5 = join("", [
      for i in range(200) :
      "${base64encode("${count.index}-${i}-${md5("salt-${i}")}")}_"
    ])

    attribute_6 = jsonencode({
      for i in range(80) :
      "item_${i}" => {
        md5_hash    = md5("item-${count.index}-${i}")
        sha256_hash = sha256("data-${i}")
        encoded     = base64encode("resource-${count.index}-item-${i}")
        timestamp   = formatdate("YYYY-MM-DD'T'hh:mm:ss", timestamp())
      }
    })

    attribute_7 = join("", [
      for i in range(200) :
      "${sha256("attr7-${count.index}-${i}")}_${md5("${i}")}_"
    ])

    attribute_8 = join("", [
      for i in range(200) :
      "${base64encode(md5("combined-${count.index}-${i}"))}_"
    ])

    attribute_9 = jsonencode([
      for i in range(150) :
      {
        index = i
        hash  = md5("array-${count.index}-${i}")
        data  = base64encode("element-${i}")
        sha   = sha1("value-${count.index}-${i}")
      }
    ])

    attribute_10 = join("", [
      for i in range(200) :
      "${md5("final-${i}")}_${sha256("${count.index}-${i}")}_${base64encode("end-${i}")}_"
    ])
  }

  provisioner "local-exec" {
    when    = create
    command = <<-EOT
      echo "==== Starting provisioning for resource ${count.index} ===="
      for i in $(seq 1 ${var.heavy_log_lines_per_resource}); do
        echo "[Resource ${count.index}] Log line $i: Processing operation $(date +%s%N) with detailed information about the current state and configuration changes being applied to the infrastructure"
        sleep 0.1
      done
      echo "==== Completed provisioning for resource ${count.index} ===="
    EOT
  }

  provisioner "local-exec" {
    when    = destroy
    command = <<-EOT
      echo "==== Starting destruction for resource ${self.triggers.index} ===="
      for i in $(seq 1 ${self.triggers.log_lines_per_resource}); do
        echo "[Resource ${self.triggers.index}] Destroy log line $i: Removing resource $(date +%s%N) and cleaning up all associated configurations and state"
        sleep 0.1
      done
      echo "==== Completed destruction for resource ${self.triggers.index} ===="
    EOT
  }
}

module "extra_providers" {
  count  = var.enable_providers ? 1 : 0
  source = var.enable_providers ? "./modules/many-providers" : "./modules/empty"
}

module "extra_modules" {
  count  = var.enable_modules ? 1 : 0
  source = var.enable_modules ? "./modules/many-modules" : "./modules/empty"
}

resource "local_file" "init_files" {
  count    = var.local_files_count
  filename = "${path.module}/generated_files/file_${count.index}.txt"
  content  = <<-EOT
    # Generated file ${count.index}
    # This file is created during terraform init phase
    # Purpose: Inflate initialization time and storage

    File Index: ${count.index}
    Generated At: ${timestamp()}

    ${join("\n", [for i in range(100) : "DATA_LINE_${i}_PADDING_CONTENT_FOR_FILE_${count.index}_SEGMENT_${i}"])}
  EOT
}
