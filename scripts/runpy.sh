# Files using relative import can be executed in any place using runner.sh.
#
# Example directory structure:
# cwd
# ├─ runpy.sh
# └─ app
#    ├─ common
#    │  └─ util.py
#    └─ tourapi
#       └─ main.py (from common import util)

# Usage: ./runpy.sh app/ app/tourapi/main.py

scripts_dir=$(dirname "$0")
runpoetry="$scripts_dir/runpoetry.sh"

if [[ -z "$1" || -z "$2" ]]; then
    echo "Usage: $0 <directory> <directory/script.py>"
    exit 1
fi

py_dir_abspath=$(realpath "$1")
py_script_abspath=$(realpath "$2")

"$runpoetry" "$py_dir_abspath" python "$py_script_abspath"
