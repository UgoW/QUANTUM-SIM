#!/bin/bash

# Generate pydoc HTML documentation for all modules in quantum_sim
# Usage: chmod +x generate_docs.sh && ./generate_docs.sh

PROJECT_ROOT=$(pwd)
DOCS_DIR="$PROJECT_ROOT/docs/api"

# Create docs directory if it doesn't exist
mkdir -p "$DOCS_DIR"
echo "Created directory: $DOCS_DIR"

# Generate documentation for main package
echo "Generating: quantum_sim"
python -m pydoc -w quantum_sim
mv quantum_sim.html "$DOCS_DIR/"

# Generate documentation for each subpackage and module
echo ""
echo "Generating subpackages and modules..."

# # Main subpackages
for pkg in errors potentials solver utils validators waves; do
    echo "Generating: quantum_sim.$pkg"
    python -m pydoc -w quantum_sim.$pkg 2>/dev/null
    mv quantum_sim.${pkg}.html "$DOCS_DIR/" 2>/dev/null
done

# Waves submodules
for module in plane_wave wave_function wave_packet wave_result; do
    echo "Generating: quantum_sim.waves.$module"
    python -m pydoc -w quantum_sim.waves.$module 2>/dev/null
    mv quantum_sim.waves.${module}.html "$DOCS_DIR/" 2>/dev/null
done

# TODO: Uncomment when potentials submodules are implemented
# # Potentials submodules
# for module in potential free_potential infinite_well step_potential; do
#     echo "Generating: quantum_sim.potentials.$module"
#     python -m pydoc -w quantum_sim.potentials.$module 2>/dev/null
#     mv quantum_sim.potentials.${module}.html "$DOCS_DIR/" 2>/dev/null
# done

# Validators submodules
echo "Generating: quantum_sim.validators.wave_validators"
python -m pydoc -w quantum_sim.validators.wave_validators 2>/dev/null
mv quantum_sim.validators.wave_validators.html "$DOCS_DIR/" 2>/dev/null

# Errors submodules
echo "Generating: quantum_sim.errors.exceptions"
python -m pydoc -w quantum_sim.errors.exceptions 2>/dev/null
mv quantum_sim.errors.exceptions.html "$DOCS_DIR/" 2>/dev/null

# Add CSS link to all HTML files
echo ""
echo "Adding CSS styling..."
for html in "$DOCS_DIR"/*.html; do
    if [ -f "$html" ]; then
        sed -i '/<\/head>/i\<link rel="stylesheet" href="style.css">' "$html"
    fi
done

# Clean up broken links and unnecessary index links
echo ""
echo "Cleaning up HTML files..."
python ./scripts/clean_links.py

echo ""
echo "✓ Documentation generated in: $DOCS_DIR"
echo "✓ Open $DOCS_DIR/quantum_sim.html to start browsing"
