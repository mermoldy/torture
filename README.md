# torture

The IACP pipeline test generator and framework for OpenTofu/Terraform automations.

## Performance focus

Targets pipeline bottlenecks: plan graph size, state size, provider/module downloads,
CPU-heavy interpolation, and apply/destroy log volume.

## Resource types

- `null_resource` (small/medium/heavy): large counts, big trigger payloads, and CPU-heavy hashing/encoding
- `local_file`: optional mass file generation to stress init and IO

## Init stress tests

- Providers: optional download of ~50 providers via `modules/extra_providers`
- Modules: optional download of 50 git modules via `modules/extra_modules`

## Run test locally

To execute test locally, run:

```sh
make plan
```

## Run in remote environment

If you want to run this as a module from another configuration:

```hcl
module "torture" {
  source = "git::https://github.com/mermoldy/torture.git?ref=main"
  
  # Plan processing testing - generate heavy plan files
  small_resource_count  = 5000  # adds many cheap plan nodes
  medium_resource_count = 2000  # increases plan/state size (~1MB triggers each)
  heavy_resource_count  = 1000  # adds CPU-heavy interpolation during plan/apply
  
  # Run console logging stress testing
  medium_log_lines_per_resource = 50   # apply/destroy log volume per medium resource
  heavy_log_lines_per_resource  = 100 # apply/destroy log volume per heavy resource
  
  # Initialization caching stress testing
  enable_providers = false # init time + disk/network from provider downloads
  enable_modules   = false # init time + disk/network from git module downloads
  
  # Configuration version changes stress testing
  local_files_count = 0 # init I/O + disk usage from generated files, compress/upload changes
}
```

This configuration produce following artifacts:

```console
-rw-r--r--@  1 mermoldy  staff    65M Jan 30 18:23 plan.bin
-rw-r--r--@  1 mermoldy  staff   457M Jan 30 18:23 plan.json
-rw-r--r--@  1 mermoldy  staff   258M Jan 30 18:23 plan.log
```

<!-- BEGIN_TF_DOCS -->
## Requirements

| Name | Version |
|------|---------|
| <a name="requirement_terraform"></a> [terraform](#requirement\_terraform) | >= 1.0 |
| <a name="requirement_null"></a> [null](#requirement\_null) | ~> 3.2 |
| <a name="requirement_random"></a> [random](#requirement\_random) | ~> 3.6 |

## Providers

| Name | Version |
|------|---------|
| <a name="provider_local"></a> [local](#provider\_local) | 2.6.2 |
| <a name="provider_null"></a> [null](#provider\_null) | 3.2.4 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| <a name="module_extra_modules"></a> [extra\_modules](#module\_extra\_modules) | ./modules/extra_modules | n/a |
| <a name="module_extra_providers"></a> [extra\_providers](#module\_extra\_providers) | ./modules/extra_providers | n/a |

## Resources

| Name | Type |
|------|------|
| [local_file.init_files](https://registry.terraform.io/providers/hashicorp/local/latest/docs/resources/file) | resource |
| [null_resource.heavy_resource](https://registry.terraform.io/providers/hashicorp/null/latest/docs/resources/resource) | resource |
| [null_resource.medium_resource](https://registry.terraform.io/providers/hashicorp/null/latest/docs/resources/resource) | resource |
| [null_resource.small_resource](https://registry.terraform.io/providers/hashicorp/null/latest/docs/resources/resource) | resource |

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|:--------:|
| <a name="input_enable_modules"></a> [enable\_modules](#input\_enable\_modules) | Enable loading of 50 git modules during terraform init | `bool` | `false` | no |
| <a name="input_enable_providers"></a> [enable\_providers](#input\_enable\_providers) | Enable installation of 50 providers during terraform init | `bool` | `false` | no |
| <a name="input_heavy_log_lines_per_resource"></a> [heavy\_log\_lines\_per\_resource](#input\_heavy\_log\_lines\_per\_resource) | Number of log lines generated while applying each heavy resource | `number` | `1000` | no |
| <a name="input_heavy_resource_count"></a> [heavy\_resource\_count](#input\_heavy\_resource\_count) | Number of heavy resources to create. Heavy resources are expensive to plan. | `number` | `1000` | no |
| <a name="input_local_files_count"></a> [local\_files\_count](#input\_local\_files\_count) | Number of local files to create during initialization (0 to disabled) | `number` | `0` | no |
| <a name="input_medium_log_lines_per_resource"></a> [medium\_log\_lines\_per\_resource](#input\_medium\_log\_lines\_per\_resource) | Number of log lines generated while applying each medium resource | `number` | `10` | no |
| <a name="input_medium_resource_count"></a> [medium\_resource\_count](#input\_medium\_resource\_count) | Number of medium resources to create. Medium resources are medium-cost to plan. | `number` | `1000` | no |
| <a name="input_small_resource_count"></a> [small\_resource\_count](#input\_small\_resource\_count) | Number of small resources to create. Small resources are low-cost to plan. | `number` | `1000` | no |

## Outputs

| Name | Description |
|------|-------------|
| <a name="output_initialization_summary"></a> [initialization\_summary](#output\_initialization\_summary) | Summary of initialization resources |
| <a name="output_resource_summary"></a> [resource\_summary](#output\_resource\_summary) | Summary of all resources created |
<!-- END_TF_DOCS -->
