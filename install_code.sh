CIRCUITPY_VOLUME=/Volumes/CIRCUITPY

if [ -d "$CIRCUITPY_VOLUME" ]; then
    echo "$CIRCUITPY_VOLUME is present, copying files..."
else 
    echo "$CIRCUITPY_VOLUME is not present, aborting..."
    exit 1
fi


echo "Removing old files..."
rm -f "$CIRCUITPY_VOLUME"/code.py
rm -f "$CIRCUITPY_VOLUME"/main.py
rm -rf "$CIRCUITPY_VOLUME"/lib

echo "Copying new files..."
echo "  Copying main.py..."
cp main.py "$CIRCUITPY_VOLUME/main.py"

echo "  Copying lib..."
cp -r lib "$CIRCUITPY_VOLUME/"

echo "Done!"
