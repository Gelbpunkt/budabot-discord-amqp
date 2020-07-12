# Budabot Discord AMQP Relay

This is a simple chat relay for Budabot to Discord using only AMQP and Discord for communication. It requires Nadyita's Budabot fork from [here](https://github.com/Nadyita/Budabot).

## Configuration File

The bot expects a configuration file based on `config.example.py` to be in the working directory under the name `config.py`.

## Running It

```sh
docker build -t discord-relay:latest .
docker run --rm -it -v /path/to/config.py:/bot/config.py discord-relay:latest
```
