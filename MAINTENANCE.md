# Thermobox maintenance

## Updating firmware

Go to the CircuitPython page for versions that work with the Pi Pico [here](https://circuitpython.org/board/raspberry_pi_pico/).

Download the latest stable version and add it to `firmware/`.

Update the `firmware.uf2` symlink to point to the new version:

```bash
cd firmware/
rm firmware.uf2
ln -s <the_new_version>.uf2 firmware.uf2
```
