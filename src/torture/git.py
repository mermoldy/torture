import shutil
import subprocess
from pathlib import Path

import click


def push_module_to_github(module: Path):
    repo_name = f"mermoldy/terraform-torture-{module.name}"

    subprocess.run(["git", "init"], cwd=module.as_posix(), check=True)
    subprocess.run(["git", "add", "."], cwd=module.as_posix(), check=True)
    subprocess.run(
        ["git", "commit", "-m", "Update module"],
        cwd=module.as_posix(),
        capture_output=True,
    )

    try:
        check_repo = subprocess.run(
            ["gh", "repo", "view", repo_name], capture_output=True, text=True
        )
        if check_repo.returncode == 0:
            click.echo(f"♻️  Updating existing repository: {repo_name}")
            subprocess.run(
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    f"git@github.com:{repo_name}.git",
                ],
                cwd=module.as_posix(),
                capture_output=True,
            )
            subprocess.run(
                ["git", "branch", "-M", "main"], cwd=module.as_posix(), check=True
            )
            push_result = subprocess.run(
                ["git", "push", "-f", "origin", "main"],
                cwd=module.as_posix(),
                capture_output=True,
                text=True,
            )
            if push_result.returncode != 0:
                click.echo(f"❌ Failed to push: {push_result.stderr}")
                return
            click.echo(f"✓ Updated repository: {repo_name}")
            shutil.rmtree(module)
            return
        else:
            click.echo(f"📦 Creating new repository: {repo_name}")
            create_result = subprocess.run(
                [
                    "gh",
                    "repo",
                    "create",
                    repo_name,
                    "--public",
                    "--source=.",
                    "--push",
                ],
                cwd=module.as_posix(),
                capture_output=True,
                text=True,
            )

            if create_result.returncode != 0:
                click.echo(f"❌ Failed to create repository: {create_result.stderr}")
                return
            click.echo(f"✓ Created and pushed repository: {repo_name}")
            shutil.rmtree(module)
    except Exception as e:
        click.echo(f"❌ Error processing {module.name}: {str(e)}")
