#!/usr/bin/env python3
import shutil
import subprocess
from pathlib import Path

import click

from src.torture import git, modulegen

ARTIFACTS = Path("artifacts")


@click.group()
def cli():
    """The IACP pipeline test generator and framework for OpenTofu/Terraform automations."""


@cli.command()
def plan() -> None:
    """Run local plan."""
    if ARTIFACTS.exists():
        shutil.rmtree(ARTIFACTS)
    ARTIFACTS.mkdir()

    var_file = Path("torture.plan.tfvars")
    subprocess.run(["tofu", "init"])
    subprocess.run(
        [
            "sh",
            "-c",
            f"tofu plan -out artifacts/plan.bin -var-file={var_file.as_posix()} > artifacts/plan.log",
        ]
    )
    subprocess.run(
        ["sh", "-c", "tofu show -json artifacts/plan.bin > artifacts/plan.json"]
    )

    click.echo(f"\nGenerated artifacts for {var_file.as_posix()}:")
    subprocess.run(["sh", "-c", 'ls -alh artifacts | grep "plan."'])


@cli.command()
def gen_modules() -> None:
    """Generate module templates."""

    if modulegen.MODULES_DIR.exists():
        for m in modulegen.MODULES_DIR.glob("module-*"):
            click.echo(f"Removing existing module: {m}")
            shutil.rmtree(m)
            click.echo("Done")

    modulegen.MODULES_DIR.mkdir(parents=True, exist_ok=True)
    click.echo()

    # Create all modules
    modulegen.create_module_01_huge_single_file()
    modulegen.create_module_02_multiple_large_files()
    modulegen.create_module_03_many_tiny_files()
    modulegen.create_module_04_medium_complexity()
    modulegen.create_module_05_deep_nested()
    modulegen.create_module_06_data_heavy()
    modulegen.create_module_07_variable_explosion()
    modulegen.create_module_08_mixed_sizes()
    modulegen.create_module_09_submodules()
    modulegen.create_module_10_extreme()

    for m in modulegen.MODULES_DIR.glob("module-*"):
        click.echo("Commiting module to own repository")
        git.push_module_to_github(m)


if __name__ == "__main__":
    cli()
