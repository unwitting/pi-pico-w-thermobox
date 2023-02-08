# Thermobox

## Set up

### Firmware

Hold down the boot selection button on the Pi and plug it in, it should mount as `RPI-RP2`.

Once it's available, run:

```bash
./install_firmware.sh
```

After the copy is complete, the Pi should reboot into run mode and remound as `CIRCUITPY`. You've just added the CircuitPython firmware to the Pi.

### Code

Once the `CIRCUITPY` volume mounts, run:

```bash
./install_code.sh
```

To install external libraries from Adafruit and Pimoroni, alongside `code.py`. The Pi should reboot and run!

In development, if you want to install code to the Pi but haven't changed the contents of `ext/`, you can instead run:

```bash
./install_code.sh --skip-libs
```

To only copy "our" code and save a minute.
