from pathlib import Path
from urllib.parse import urlparse

import click

from . import utils


@click.command()
@click.argument("handle")
@click.option("-o", "--output-dir", "output_dir", default="./")
@click.option("--timeout", "timeout", default="5")
def cli(handle: str, output_dir: str, timeout: str = "5"):
    """Save the raw robots.txt of the provided site."""
    # Get the site
    site = utils.get_site(handle)

    # Get the robots.txt
    robotstxt = _get_robotstxt(site["url"], int(timeout))

    # Set the output path
    output_path = Path(output_dir) / f"{utils.safe_ia_handle(handle)}.robots.txt"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Write it out
    with output_path.open("w") as f:
        f.write(robotstxt)


def _get_robotstxt(
    site_url: str,
    timeout: int = 5,
    user_agent: str = "NewsHomepagesBot (https://homepages.news)",
) -> str:
    """Get the raw robots.txt for a site."""
    robotstxt_url = urlparse(site_url)._replace(path="robots.txt").geturl()
    r = utils.get_url(robotstxt_url, timeout=timeout, user_agent=user_agent)
    return r.text


if __name__ == "__main__":
    cli()
