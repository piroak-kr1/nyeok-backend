# Argument: major, minor, patch

# Change directory for subsequent poetry commands
cd "./database-setup"

prev_version=$(poetry version)

if [ "$1" == "major" ]; then
    echo "Bumping major version"
    poetry version major
elif [ "$1" == "minor" ]; then
    echo "Bumping minor version"
    poetry version minor
elif [ "$1" == "patch" ]; then
    echo "Bumping patch version"
    poetry version patch
elif [ "$1" == "again" ]; then
    echo "Not changing version: build & publish again"
else
    echo "Invalid argument. Please use major, minor, or patch (again)"
    exit 1
fi

# NOTE: You should have installed poetry-plugin-mono-repo-deps plugin
poetry export --without-hashes --output requirements.txt

docker build --tag kimkun07/nyeok-database-setup:$(poetry version --short) .
docker push kimkun07/nyeok-database-setup:$(poetry version --short)
