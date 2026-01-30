#!/usr/bin/env python3
import random
import string
import subprocess
from pathlib import Path

import click
from jinja2 import Template

MODULES_DIR = Path("modules")

MAIN_TF_TEMPLATE = Template("""
# {{ module_name }}
# {{ description }}

terraform {
  required_version = ">= 1.0"
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

{% for i in range(resource_count) %}
resource "null_resource" "resource_{{ i }}" {
  triggers = {
    id        = "{{ prefix }}-{{ i }}"
    timestamp = timestamp()
    {% if include_data %}
    data      = "{{ random_data() }}"
    {% endif %}
  }
}
{% endfor %}

output "{{ prefix }}_output" {
  value = {
    {% for i in range(resource_count) %}
    resource_{{ i }} = null_resource.resource_{{ i }}.id
    {% endfor %}
  }
}
""")

VARIABLE_TF_TEMPLATE = Template("""
{% for i in range(var_count) %}
variable "var_{{ i }}" {
  description = "Variable {{ i }} for {{ module_name }}"
  type        = string
  default     = "default_value_{{ i }}"

  validation {
    condition     = length(var.var_{{ i }}) > 0
    error_message = "Variable var_{{ i }} must not be empty."
  }
}

{% endfor %}
""")

OUTPUT_TF_TEMPLATE = Template("""
output "all_variables" {
  description = "All variables from {{ module_name }}"
  value = {
    {% for i in range(var_count) %}
    var_{{ i }} = var.var_{{ i }}
    {% endfor %}
  }
}
""")

LOCALS_TF_TEMPLATE = Template("""
locals {
  {% for i in range(local_count) %}
  local_{{ i }} = "local_value_{{ i }}_{{ random_string() }}"
  {% endfor %}

  {% if include_large_data %}
  large_data_map = {
    {% for i in range(map_size) %}
    "key_{{ i }}" = "{{ random_data() }}"
    {% endfor %}
  }

  large_json_structure = jsonencode({
    {% for i in range(json_items) %}
    item_{{ i }} = {
      id          = {{ i }}
      name        = "Item {{ i }}"
      description = "{{ random_data() }}"
      metadata = {
        {% for j in range(5) %}
        meta_key_{{ j }} = "{{ random_string() }}"
        {% endfor %}
      }
    }
    {% endfor %}
  })
  {% endif %}
}
""")

SMALL_FILE_TEMPLATE = Template("""
# Small file {{ index }}
variable "small_var_{{ index }}" {
  default = "value_{{ index }}"
}

locals {
  small_local_{{ index }} = "local_{{ index }}_{{ random_string() }}"
}

resource "null_resource" "small_{{ index }}" {
  triggers = {
    value = var.small_var_{{ index }}
  }
}
""")

SUBMODULE_TEMPLATE = Template("""
# Submodule {{ name }}
variable "submodule_input" {
  type    = string
  default = "submodule_{{ name }}"
}

{% for i in range(resource_count) %}
resource "null_resource" "sub_{{ name }}_{{ i }}" {
  triggers = {
    input = var.submodule_input
    index = {{ i }}
  }
}
{% endfor %}

output "submodule_{{ name }}_output" {
  value = {
    {% for i in range(resource_count) %}
    resource_{{ i }} = null_resource.sub_{{ name }}_{{ i }}.id
    {% endfor %}
  }
}
""")


def random_string(length=20):
    """Generate random string"""
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def random_data(length=200):
    """Generate random base64-like data"""
    return "".join(
        random.choices(string.ascii_letters + string.digits + "+/=", k=length)
    )


def create_binary_file(filepath, size_mb, compression_level=None):
    """
    Create binary file using dd

    Args:
        filepath: Path to create file
        size_mb: Size in megabytes
        compression_level: If set, compress with gzip (1-9, where 9 is best compression)
    """
    click.echo(
        f"    Creating binary file: {filepath.name} ({size_mb}MB, compression={compression_level})"
    )

    # Create temporary file with dd
    temp_file = filepath.with_suffix(".tmp")

    # Use dd to create file filled with random data
    dd_cmd = [
        "dd",
        "if=/dev/urandom",
        f"of={temp_file}",
        "bs=1M",
        f"count={size_mb}",
        "status=none",
    ]

    subprocess.run(dd_cmd, check=True)

    if compression_level is not None:
        # Compress with gzip
        gzip_cmd = ["gzip", f"-{compression_level}", "-c", str(temp_file)]

        with open(filepath, "wb") as f:
            subprocess.run(gzip_cmd, stdout=f, check=True)

        temp_file.unlink()
    else:
        # Just rename
        temp_file.rename(filepath)


def create_module_01_huge_single_file():
    """Module 1: Single huge Terraform file (10MB)"""
    click.echo("Creating Module 01: Single huge file (10MB)")
    module_dir = MODULES_DIR / "module-01-huge-single-file"
    module_dir.mkdir(parents=True, exist_ok=True)

    content = MAIN_TF_TEMPLATE.render(
        module_name="Module 01",
        description="Single huge Terraform file with 5000 resources",
        resource_count=5000,
        prefix="huge_single",
        include_data=True,
        random_data=random_data,
    )

    (module_dir / "main.tf").write_text(content)

    # Add binary companion file (no compression)
    create_binary_file(module_dir / "data.bin", 5, compression_level=None)

    click.echo(f"  ✓ Module 01 created ({get_dir_size(module_dir)})")


def create_module_02_multiple_large_files():
    """Module 2: Multiple large files (5 files × 2MB each)"""
    click.echo("Creating Module 02: Multiple large files (5 × 2MB)")
    module_dir = MODULES_DIR / "module-02-multiple-large-files"
    module_dir.mkdir(parents=True, exist_ok=True)

    for i in range(1, 6):
        content = MAIN_TF_TEMPLATE.render(
            module_name=f"Module 02 - File {i}",
            description=f"Large file {i} of 5",
            resource_count=1000,
            prefix=f"large_file_{i}",
            include_data=True,
            random_data=random_data,
        )
        (module_dir / f"resources_{i}.tf").write_text(content)

    # Add binary files with different compression levels
    for i in range(1, 6):
        create_binary_file(
            module_dir / f"data_{i}.bin.gz",
            2,
            compression_level=i,  # Varying compression from 1-5
        )

    click.echo(f"  ✓ Module 02 created ({get_dir_size(module_dir)})")


def create_module_03_many_tiny_files():
    """Module 3: Massive number of tiny files (1000 files × 1KB each)"""
    click.echo("Creating Module 03: Many tiny files (1000 × 1KB)")
    module_dir = MODULES_DIR / "module-03-many-tiny-files"
    module_dir.mkdir(parents=True, exist_ok=True)

    for i in range(1, 1001):
        content = SMALL_FILE_TEMPLATE.render(index=i, random_string=random_string)
        (module_dir / f"var_{i:04d}.tf").write_text(content)

    # Create aggregator
    aggregator_vars = "\n".join(
        [f"    var_{i} = var.small_var_{i}" for i in range(1, 1001)]
    )
    (module_dir / "main.tf").write_text(f"""
# Module 03 - Aggregator
resource "null_resource" "aggregator" {{
  triggers = {{
{aggregator_vars}
  }}
}}
""")

    # Add many tiny binary files
    for i in range(1, 51):  # 50 tiny binary files
        create_binary_file(
            module_dir / f"tiny_{i:02d}.dat",
            1,  # 1MB each
            compression_level=9,  # Maximum compression
        )

    click.echo(f"  ✓ Module 03 created ({get_dir_size(module_dir)})")


def create_module_04_medium_complexity():
    """Module 4: Medium complexity (50 medium files × 100KB each)"""
    click.echo("Creating Module 04: Medium complexity (50 × 100KB)")
    module_dir = MODULES_DIR / "module-04-medium-complexity"
    module_dir.mkdir(parents=True, exist_ok=True)

    for i in range(1, 51):
        content = MAIN_TF_TEMPLATE.render(
            module_name=f"Module 04 - Block {i}",
            description=f"Medium file {i} of 50",
            resource_count=50,
            prefix=f"medium_{i}",
            include_data=True,
            random_data=random_data,
        )
        (module_dir / f"block_{i:02d}.tf").write_text(content)

    # Add medium binary files with varying compression
    for i in range(1, 11):
        create_binary_file(
            module_dir / f"medium_{i:02d}.bin.gz",
            3,
            compression_level=(i % 9) + 1,  # Compression 1-9
        )

    click.echo(f"  ✓ Module 04 created ({get_dir_size(module_dir)})")


def create_module_05_deep_nested():
    """Module 5: Deep nested directory structure"""
    click.echo("Creating Module 05: Deep nested structure (10 levels)")
    module_dir = MODULES_DIR / "module-05-deep-nested"
    module_dir.mkdir(parents=True, exist_ok=True)

    current_dir = module_dir
    for depth in range(1, 11):
        current_dir = current_dir / f"level_{depth:02d}"
        current_dir.mkdir(parents=True, exist_ok=True)

        content = MAIN_TF_TEMPLATE.render(
            module_name=f"Module 05 - Level {depth}",
            description=f"Nested at depth {depth}",
            resource_count=100,
            prefix=f"nested_depth_{depth}",
            include_data=True,
            random_data=random_data,
        )
        (current_dir / "resources.tf").write_text(content)

        # Add binary file at each level
        create_binary_file(
            current_dir / f"level_{depth}.dat.gz", 2, compression_level=depth % 9 + 1
        )

    # Create main module file
    (module_dir / "main.tf").write_text("""
# Module 05 - Deep Nested Structure
# Contains 10 levels of nested directories
""")

    click.echo(f"  ✓ Module 05 created ({get_dir_size(module_dir)})")


def create_module_06_data_heavy():
    """Module 6: JSON/YAML heavy (large embedded data)"""
    click.echo("Creating Module 06: Data heavy (large JSON/maps)")
    module_dir = MODULES_DIR / "module-06-data-heavy"
    module_dir.mkdir(parents=True, exist_ok=True)

    content = LOCALS_TF_TEMPLATE.render(
        module_name="Module 06",
        local_count=100,
        include_large_data=True,
        map_size=2000,
        json_items=1000,
        random_string=random_string,
        random_data=random_data,
    )

    (module_dir / "locals.tf").write_text(content)

    # Create main.tf with data processing
    (module_dir / "main.tf").write_text("""
# Module 06 - Data Heavy
resource "null_resource" "data_processor" {
  triggers = {
    json_hash = md5(local.large_json_structure)
    map_hash  = md5(jsonencode(local.large_data_map))
  }
}
""")

    # Add highly compressible binary file (lots of zeros)
    dd_cmd = [
        "dd",
        "if=/dev/zero",
        f"of={module_dir / 'zeros.tmp'}",
        "bs=1M",
        "count=20",
        "status=none",
    ]
    subprocess.run(dd_cmd, check=True)

    # Compress (should compress very well)
    gzip_cmd = ["gzip", "-9", "-c", str(module_dir / "zeros.tmp")]
    with open(module_dir / "highly_compressible.dat.gz", "wb") as f:
        subprocess.run(gzip_cmd, stdout=f, check=True)
    (module_dir / "zeros.tmp").unlink()

    click.echo(f"  ✓ Module 06 created ({get_dir_size(module_dir)})")


def create_module_07_variable_explosion():
    """Module 7: Variable explosion (5000 variables)"""
    click.echo("Creating Module 07: Variable explosion (5000 variables)")
    module_dir = MODULES_DIR / "module-07-variable-explosion"
    module_dir.mkdir(parents=True, exist_ok=True)

    # Create variables file
    content = VARIABLE_TF_TEMPLATE.render(var_count=5000, module_name="Module 07")
    (module_dir / "variables.tf").write_text(content)

    # Create outputs file
    content = OUTPUT_TF_TEMPLATE.render(var_count=5000, module_name="Module 07")
    (module_dir / "outputs.tf").write_text(content)

    # Add uncompressed binary file
    create_binary_file(module_dir / "uncompressed.bin", 10, compression_level=None)

    click.echo(f"  ✓ Module 07 created ({get_dir_size(module_dir)})")


def create_module_08_mixed_sizes():
    """Module 8: Mixed - some large, many small files"""
    click.echo("Creating Module 08: Mixed sizes (3 large + 500 small)")
    module_dir = MODULES_DIR / "module-08-mixed-sizes"
    module_dir.mkdir(parents=True, exist_ok=True)

    # Create 3 large files
    for i in range(1, 4):
        content = MAIN_TF_TEMPLATE.render(
            module_name=f"Module 08 - Large {i}",
            description=f"Large mixed file {i}",
            resource_count=800,
            prefix=f"large_mixed_{i}",
            include_data=True,
            random_data=random_data,
        )
        (module_dir / f"large_{i}.tf").write_text(content)

    # Create 500 small files
    for i in range(1, 501):
        content = SMALL_FILE_TEMPLATE.render(index=i, random_string=random_string)
        (module_dir / f"small_{i:03d}.tf").write_text(content)

    # Mix of binary files with different compression
    create_binary_file(module_dir / "no_compression.bin", 5, compression_level=None)
    create_binary_file(module_dir / "low_compression.bin.gz", 5, compression_level=1)
    create_binary_file(module_dir / "high_compression.bin.gz", 5, compression_level=9)

    click.echo(f"  ✓ Module 08 created ({get_dir_size(module_dir)})")


def create_module_09_submodules():
    """Module 9: Submodules within submodules"""
    click.echo("Creating Module 09: Nested submodules (3 levels deep)")
    module_dir = MODULES_DIR / "module-09-submodules"
    module_dir.mkdir(parents=True, exist_ok=True)

    # Create main module
    (module_dir / "main.tf").write_text("""
# Module 09 - Nested Submodules
module "sub_a" {
  source = "./modules/sub-a"
}

module "sub_b" {
  source = "./modules/sub-b"
}

module "sub_c" {
  source = "./modules/sub-c"
}
""")

    # Create 3 submodules
    for letter in ["a", "b", "c"]:
        sub_dir = module_dir / "modules" / f"sub-{letter}"
        sub_dir.mkdir(parents=True, exist_ok=True)

        # Create submodule main file
        content = SUBMODULE_TEMPLATE.render(name=letter, resource_count=200)
        (sub_dir / "main.tf").write_text(content)

        # Create sub-submodules
        submodule_calls = []
        for num in range(1, 4):
            sub_sub_dir = sub_dir / "submodules" / f"sub-{num}"
            sub_sub_dir.mkdir(parents=True, exist_ok=True)

            content = SUBMODULE_TEMPLATE.render(
                name=f"{letter}_{num}", resource_count=100
            )
            (sub_sub_dir / "main.tf").write_text(content)

            # Add binary file to sub-submodule
            create_binary_file(
                sub_sub_dir / f"data_{letter}_{num}.bin.gz",
                2,
                compression_level=num * 3,
            )

            submodule_calls.append(f"""
module "sub_{letter}_{num}" {{
  source = "./submodules/sub-{num}"
}}
""")

        # Add submodule calls to main submodule
        with open(sub_dir / "main.tf", "a") as f:
            f.write("\n".join(submodule_calls))

    click.echo(f"  ✓ Module 09 created ({get_dir_size(module_dir)})")


def create_module_10_extreme():
    """Module 10: Extreme - combination of all patterns"""
    click.echo("Creating Module 10: Extreme (all patterns combined)")
    module_dir = MODULES_DIR / "module-10-extreme"
    module_dir.mkdir(parents=True, exist_ok=True)

    # One huge file
    content = MAIN_TF_TEMPLATE.render(
        module_name="Module 10 - Huge",
        description="Extreme module - huge file component",
        resource_count=2000,
        prefix="extreme_huge",
        include_data=True,
        random_data=random_data,
    )
    (module_dir / "huge.tf").write_text(content)

    # 100 medium files
    for i in range(1, 101):
        content = MAIN_TF_TEMPLATE.render(
            module_name=f"Module 10 - Medium {i}",
            description=f"Extreme module - medium file {i}",
            resource_count=50,
            prefix=f"extreme_medium_{i}",
            include_data=True,
            random_data=random_data,
        )
        (module_dir / f"medium_{i:03d}.tf").write_text(content)

    # 500 tiny files
    for i in range(1, 501):
        content = SMALL_FILE_TEMPLATE.render(index=i, random_string=random_string)
        (module_dir / f"tiny_{i:03d}.tf").write_text(content)

    # Nested structure
    nested_dir = module_dir / "nested" / "level1" / "level2" / "level3"
    nested_dir.mkdir(parents=True, exist_ok=True)

    content = MAIN_TF_TEMPLATE.render(
        module_name="Module 10 - Nested",
        description="Extreme module - nested component",
        resource_count=100,
        prefix="extreme_nested",
        include_data=True,
        random_data=random_data,
    )
    (nested_dir / "deep.tf").write_text(content)

    # Large data file
    content = LOCALS_TF_TEMPLATE.render(
        module_name="Module 10",
        local_count=200,
        include_large_data=True,
        map_size=1000,
        json_items=1000,
        random_string=random_string,
        random_data=random_data,
    )
    (module_dir / "data.tf").write_text(content)

    # Variety of binary files
    create_binary_file(module_dir / "no_compress.bin", 10, compression_level=None)
    create_binary_file(module_dir / "compress_1.bin.gz", 10, compression_level=1)
    create_binary_file(module_dir / "compress_5.bin.gz", 10, compression_level=5)
    create_binary_file(module_dir / "compress_9.bin.gz", 10, compression_level=9)

    # Create zeros file (highly compressible)
    dd_cmd = [
        "dd",
        "if=/dev/zero",
        f"of={module_dir / 'zeros.tmp'}",
        "bs=1M",
        "count=50",
        "status=none",
    ]
    subprocess.run(dd_cmd, check=True)
    gzip_cmd = ["gzip", "-9", "-c", str(module_dir / "zeros.tmp")]
    with open(module_dir / "zeros_compressed.dat.gz", "wb") as f:
        subprocess.run(gzip_cmd, stdout=f, check=True)
    (module_dir / "zeros.tmp").unlink()

    click.echo(f"  ✓ Module 10 created ({get_dir_size(module_dir)})")


def get_dir_size(path):
    """Get directory size in human-readable format"""
    result = subprocess.run(["du", "-sh", str(path)], capture_output=True, text=True)
    return result.stdout.split()[0]


def count_files(path):
    """Count .tf files in directory"""
    return len(list(Path(path).rglob("*.tf")))
