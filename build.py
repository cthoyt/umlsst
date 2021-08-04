"""Build the UMLS Semantic Types Site"""

from pathlib import Path
from textwrap import dedent
from typing import Optional

import pystow

HERE = Path(__file__).parent.resolve()
DOCS = HERE.joinpath("DOCS")
DATA = DOCS.joinpath("DATA")
OUT = DATA.joinpath('table.yml')
MODULE = pystow.module('umls', 'semantic-types')


def get_latest_version(version: Optional[str] = None) -> str:
    return "2018AB" if version is None else version


def get_url(version: Optional[str] = None) -> str:
    """Get the URL for the specific version."""
    if version is None:
        version = get_latest_version()
    return f'https://metamap.nlm.nih.gov/Docs/SemanticTypes_{version}.txt'


def main(version: Optional[str] = None, force: bool = False):
    version = get_latest_version(version=version)
    url = get_url(version=version)
    df = MODULE.ensure_csv(
        url=url,
        force=force,
        read_csv_kwargs=dict(sep='|', header=0, names=["umsst", "sty", "name"]),
    )

    home_html = ''
    for umlsst, sty, name in df.values:
        home_html += dedent(f'''\
        <tr>
            <td><a href="{umlsst}">{umlsst}</a></td>
            <td>{sty}</td>
            <td>{name}</td>
        </tr>
        ''')

        directory = DOCS.joinpath(umlsst)
        directory.mkdir(exist_ok=True, parents=True)
        with directory.joinpath('index.html').open('w') as file:
            content = dedent(f'''\
            <html lang="en">
            <body>
            <h1>{umlsst}</h1>
            <dl>
                <dt>Version</dt>
                <dd><a href="{url}">{version}</a></dd>
                <dt>Semantic Type Ontology ID</dt>
                <dd><a href="http://purl.bioontology.org/ontology/STY/{sty}">{sty}</a></dd>
                <dt>Semantic Type Ontology Label</dt>
                <dd>{name}</dd>
            </dl>
            </body>
            </html>
            ''')
            print(content, file=file)

    with DOCS.joinpath('index.html').open('w') as file:
        content = dedent(f'''\
            <html lang="en">
            <body>
            <h1>UMLS Semantic Types</h1>
            <p>
            This page was generated from <a href="https://github.com/cthoyt/umlsst/">https://github.com/cthoyt/umlsst/
            </a> using version {version} and <a href="{url}">{url}</a>.
            </p>
            <table>
            {home_html}
            </table>
            </body>
            </html>
            ''')
        print(content, file=file)


if __name__ == '__main__':
    main()
