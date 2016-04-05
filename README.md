# pygbc

A gameboy color emulator written in pure python. This project is experimental and does not load any games.

## Setting up the Environment

To setup the environment for this code, just use ``virtualenv`` and ``pip``:

```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Tests

This project includes a comprehensive set of tests. You can run them after setting up your environment by using ``py.test``:

```
py.test --cov gbc
```

## Resources

There are a few resources out there on the GBC hardware that are useful when developing on the emulator:

- [The GameBoy CPU Manual](http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf)

