module "huge_single_file" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-01-huge-single-file?ref=main"
}

module "multiple_large_files" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-02-multiple-large-files?ref=main"
}

module "many_tiny_files" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-03-many-tiny-files?ref=main"
}

module "medium_complexity" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-04-medium-complexity?ref=main"
}

module "deep_nested" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-05-deep-nested?ref=main"
}

module "data_heavy" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-06-data-heavy?ref=main"
}

module "variable_explosion" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-07-variable-explosion?ref=main"
}

module "mixed_sizes" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-08-mixed-sizes?ref=main"
}

module "submodules" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-09-submodules?ref=main"
}

module "extreme" {
  source = "git::https://github.com/mermoldy/terraform-torture-module-10-extreme?ref=main"
}
