# Argument: major, minor, patch

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
else
    echo "Invalid argument. Please use major, minor, or patch"
    exit 1
fi

docker build --tag kimkun07/nyeok-backend:$(poetry version) .
docker push kimkun07/nyeok-backend:$(poetry version)
