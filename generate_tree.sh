#!/bin/bash
# =============================================
# Script: generate_tree.sh
# Descripción: Genera un árbol de directorios
# que incluye archivos .java, .json y .yml,
# excluyendo carpetas irrelevantes (target, test, build, etc.)
# Compatible con macOS y Linux.
# =============================================

# Nombre del archivo de salida
OUTPUT_FILE="directory_tree.txt"

# Carpetas a excluir
EXCLUDES=(
  ".git"
  ".idea"
  ".vscode"
  "target"
  "build"
  "out"
  "test"
)

# Construir argumentos de exclusión para find
EXCLUDE_ARGS=()
for dir in "${EXCLUDES[@]}"; do
  EXCLUDE_ARGS+=(-path "./$dir" -prune -o)
done

echo "🧩 Generando árbol de directorios del proyecto..."
echo "   (Se excluirán: ${EXCLUDES[*]})"
echo "==============================================="

# Generar árbol: incluye carpetas y archivos .java, .json, .yml
# Se ajusta la lógica de 'find' para que las exclusiones funcionen correctamente
find . \
  \( "${EXCLUDE_ARGS[@]}" -type f \( -name "*.java" -o -name "*.json" -o -name "*.yml" -o -name "*.py" \) -print -o -type d -print \) \
  | sed -e 's;[^/]*/;|____;g' > "$OUTPUT_FILE"

echo "✅ Árbol generado exitosamente en '$OUTPUT_FILE'"
