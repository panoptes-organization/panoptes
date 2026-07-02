#!/usr/bin/env python

from panoptes.app import app
from panoptes._version import __version__
from argparse import ArgumentParser, RawTextHelpFormatter
import sys

_API_EPILOG = """\
API endpoints:
  GET    /api/service-info                        server status
  GET    /api/workflows                           all workflows
  GET    /api/workflow/<id>                       one workflow
  GET    /api/workflow/<id>/jobs                  all jobs of a workflow
  GET    /api/workflow/<id>/job/<job-id>          one job
  PUT    /api/workflow/<id>                       rename a workflow ({"name": ...})
  POST   /api/workflow/<id>/cancel                cancel a workflow (-> Cancelled)
  DELETE /api/workflow/<id>                       delete a workflow (403 while Running)
  DELETE /api/workflows/all                       clean up the database

Used by the snakemake-logger-plugin-panoptes plugin:
  GET    /create_workflow                         register a workflow
  POST   /update_workflow_status                  ingest a workflow event

Environment variables:
  PANOPTES_DB_URL          database URL [Default: sqlite:///.panoptes.db]
  PANOPTES_STALE_HOURS     hours of silence before a Running workflow is
                           marked Stale; 0 disables [Default: 48]
"""


def build_parser():
    parser = ArgumentParser(
        description="panoptes: monitor computational workflows in real-time",
        epilog=_API_EPILOG,
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        "--ip",
        dest="ip",
        help="Set the IP of the panoptes server [Default: 0.0.0.0]",
        default="0.0.0.0",
        required=False
    )

    parser.add_argument(
        "--port",
        dest="port",
        help="The port of the server [Default: 5000]",
        default="5000",
        required=False
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        dest="verbose",
        default=False,
        required=False,
        help="Be Verbose"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"panoptes {__version__}"
    )

    return parser


def main():
    args = build_parser().parse_args()
    app.run(host=args.ip,
            port=args.port)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt!\n")
        sys.exit(0)
