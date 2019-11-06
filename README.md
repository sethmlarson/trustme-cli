# trustme-cli

A simple tool that generates certificates for local testing

Basically a CLI for [`trustme`](https://github.com/python-trio/trustme) which
is an amazing library for generating certificates programmatically.

## Getting Started

```console
$ python -m pip install trustme-cli

##################
# Show all options
##################

$ trustme-cli --help
usage: trustme-cli [-h] [-d DIR]
                   [-i IDENTITIES [IDENTITIES ...]]
                   [--common-name COMMON_NAME]
                   [--key-size KEY_SIZE] [-q]

optional arguments:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     Directory where certificates and keys
                        are written to. Defaults to cwd
  -i IDENTITIES [IDENTITIES ...], --identities IDENTITIES [IDENTITIES ...]
                        Identities for the certificate.
                        Defaults to
  --common-name COMMON_NAME
                        Also sets the deprecated 'commonName'
                        field for all relevant identities
  --key-size KEY_SIZE   Key size of the certificate generated.
                        Defaults to 2048
  -q, --quiet           Doesn't print out helpful information
                        for humans


#######################
# Default configuration
#######################

$ trustme-cli
Generated a certificate for 'localhost', '127.0.0.1', '::1'
Configure your server to use the following files:
  cert=/tmp/server.pem
  key=/tmp/server.key
Configure your client to use the following files:
  cert=/tmp/client.pem


################################
# Designate different identities
################################

$ trustme-cli -i www.google.com google.com
Generated a certificate for 'www.google.com', 'google.com'
Configure your server to use the following files:
  cert=/tmp/server.pem
  key=/tmp/server.key
Configure your client to use the following files:
  cert=/tmp/client.pem

#################################
# Generate files into a directory
#################################

$ mkdir /tmp/a
$ trustme-cli -d /tmp/a
Generated a certificate for 'localhost', '127.0.0.1', '::1'
Configure your server to use the following files:
  cert=/tmp/a/server.pem
  key=/tmp/a/server.key
Configure your client to use the following files:
  cert=/tmp/a/client.pem

###################################
# Configure certs for server/client
###################################

$ gunicorn --keyfile=/tmp/a/server.key --certfile=/tmp/a/server.cert app:app
$ curl --with-ca-path=/tmp/a/client.pem https://127.0.0.1/
Hello, world!
```

## License

MIT
