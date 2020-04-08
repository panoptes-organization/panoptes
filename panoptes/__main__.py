from panoptes.app import app

from argparse import ArgumentParser, RawTextHelpFormatter
import sys

if __name__ == '__main__':

    print('Number of arguments:', len(sys.argv), 'arguments')
    print('Argument List:', str(sys.argv))
    parser = ArgumentParser(
        description=__doc__,
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        "--ip", "--IP" "--host",
        dest="ip",
        help="Set the IP of the panoptes server",
        metavar="text",
        required=False
    )

    parser.add_argument(
        "--port",
        dest="port",
        help="The port of the server",
        metavar="text",
        required=False
    )

    parser.add_argument(
        "--db-path",
        dest="db_path",
        help="The path of the database",
        metavar="text",
        required=False
    )
    parser.add_argument(
        "--auth-key",
        dest="auth_key",
        help="The path of the auth key",
        metavar="text",
        required=False
    )
    parser.add_argument(
        "--verbose",
        dest="verbose",
        help="The verbose of the printed logs",
        metavar="int",
        required=False
    )

    args = parser.parse_args()
    if args.ip:
        ip = args.ip
    else:
        ip = '0.0.0.0'
    if args.port:
        port = args.port
    else:
        port = '5000'

    app.run(host=ip, port=port)
