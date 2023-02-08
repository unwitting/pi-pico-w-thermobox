PI_VOLUME=/Volumes/RPI-RP2

if [ -d "$PI_VOLUME" ]; then
    echo "$PI_VOLUME is present, copying files..."
else 
    echo "$PI_VOLUME is not present, aborting..."
    exit 1
fi

echo "Installing firmware..."
cp firmware/firmware.uf2 "$PI_VOLUME/firmware.uf2"

echo "Done!"
