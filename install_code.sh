CIRCUITPY_VOLUME=/Volumes/CIRCUITPY

# If --skip-libs is passed, skip copying the libraries
SKIP_LIBS=0
if [[ " $@ " =~ " --skip-libs " ]]; then
    SKIP_LIBS=1
fi

if [ -d "$CIRCUITPY_VOLUME" ]; then
    echo "$CIRCUITPY_VOLUME is present, copying files..."
else 
    echo "$CIRCUITPY_VOLUME is not present, aborting..."
    exit 1
fi


echo "Removing old files..."
rm -f "$CIRCUITPY_VOLUME"/code.py
rm -f "$CIRCUITPY_VOLUME"/main.py

if [ $SKIP_LIBS -eq 0 ]; then
    echo "  Removing libraries..."
    rm -rf "$CIRCUITPY_VOLUME"/lib
else
    echo "  Skipping libraries..."
fi

echo "Copying new files..."
echo "  Copying main.py..."
cp main.py "$CIRCUITPY_VOLUME/main.py"

if [ $SKIP_LIBS -eq 0 ]; then
    echo "  Copying Adafruit libraries..."
    cp -r ext/adafruit "$CIRCUITPY_VOLUME/lib/"
    echo "  Copying Pimoroni libraries..."
    cp -r ext/pimoroni/pmk "$CIRCUITPY_VOLUME/lib/"
else
    echo "  Skipping libraries..."
fi

echo "Done!"
