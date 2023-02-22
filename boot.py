import board  # type: ignore
import digitalio  # type: ignore
import storage  # type: ignore

# Jump GP22 to GND to make the drive writable
switch = digitalio.DigitalInOut(board.GP22)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
storage.remount("/", not switch.value)
