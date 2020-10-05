"""A simple tool that generates certificates for local testing"""

import argparse
import pathlib
import trustme
import typing
import os
import sys

__all__ = ["main"]
__version__ = "2020.2.28"


def main(argv: typing.Sequence[str] = None) -> None:
    parser = argparse.ArgumentParser(prog="trustme-cli")
    parser.add_argument(
        "-d",
        "--dir",
        default=os.getcwd(),
        help="Directory where certificates and keys are written to. Defaults to cwd",
    )
    parser.add_argument(
        "-i",
        "--identities",
        nargs="+",
        default=("localhost", "127.0.0.1", "::1"),
        help="Identities for the certificate. Defaults to ",
    )
    parser.add_argument(
        "--common-name",
        nargs=1,
        default=None,
        help="Also sets the deprecated 'commonName' field for all relevant identities",
    )
    parser.add_argument(
        "--key-size",
        type=int,
        default=2048,
        help="Key size of the certificate generated. Defaults to 2048",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Doesn't print out helpful information for humans",
    )

    args = parser.parse_args(argv or sys.argv[1:])
    if len(args.identities) < 1:
        raise ValueError("Must include at least one identity")
    cert_dir = pathlib.Path(args.dir)
    if not cert_dir.is_dir():
        raise ValueError(f"--dir={cert_dir} is not a directory")
    common_name = args.common_name[0] if args.common_name else None

    # Generate the CA certificate
    trustme._KEY_SIZE = args.key_size
    ca = trustme.CA()
    cert = ca.issue_cert(*args.identities, common_name=common_name)

    # Write the certificate and private key the server should use
    server_key = cert_dir / "server.key"
    server_cert = cert_dir / "server.pem"
    cert.private_key_pem.write_to_path(path=str(server_key))
    with server_cert.open(mode="w") as f:
        f.truncate()
    for blob in cert.cert_chain_pems:
        blob.write_to_path(path=str(server_cert), append=True)

    # Write the certificate the client should trust
    client_cert = cert_dir / "client.pem"
    ca.cert_pem.write_to_path(path=str(client_cert))

    if not args.quiet:
        idents = "', '".join(args.identities)
        print(f"Generated a certificate for '{idents}'")
        print("Configure your server to use the following files:")
        print(f"  cert={server_cert}")
        print(f"  key={server_key}")
        print("Configure your client to use the following files:")
        print(f"  cert={client_cert}")


if __name__ == "__main__":
    main()
