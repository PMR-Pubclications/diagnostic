mkdir -p scripts/voice
#!/bin/bash
# Build script for AudioVideoEngine-CPP integration

ENGINE_DIR="AudioVideoEngine-CPP"

if [ ! -d "$ENGINE_DIR" ]; then
    echo "Cloning or linking AudioVideoEngine-CPP repository..."
    # If pulled via submodule or direct clone
    git clone https://github.com/PMR-Pubclications/AudioVideoEngine-CPP.git
fi

cd "$ENGINE_DIR" || exit
mkdir -p build && cd build
cmake ..
make -j$(nproc)

echo "C++ Engine build complete."
