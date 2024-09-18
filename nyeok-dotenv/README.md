# nyeok-dotenv

`nyeok-dotenv` manages environment variable from env files for different build types at once.

## Installation

```sh
pip install nyeok-dotenv
```

## Usage

### Setup directory structure

`sample_env.py` will load .env files from the same directory.

```
.
├── .env.dev
├── .env.prod
├── .env.stage
├── .secret
├── main.py
└── sample_env.py
```

### Create a new environment variable class

```py
# sample_env.py

from enum import StrEnum, unique
from nyeok_dotenv.EnvBase import EnvBase

@unique
class RuntimeType(StrEnum):
    # Enum name will be used in code
    # Enum value will be used in RUNTIME_TYPE environment variable
    PROD = "prod"
    STAGE = "staging"
    DEV = "dev"

class SampleEnv(EnvBase[RuntimeType]):
    # Define all environment variables as type hint

    # nyeok-dotenv will not load _ prefix variables
    _hidden_variable: str

    # From .env
    POSTGRES_USER: str

    # From .secret
    POSTGRES_PASSWORD: str

# Create env class and export to other files
env = SampleEnv(
    runtime_type_cls=RuntimeType,
    files_to_load={
        RuntimeType.PROD: [".env.prod"], # secret will be set by k8s
        RuntimeType.STAGE: [".env.stage", ".secret"],
        RuntimeType.DEV: [".env.dev", ".secret"],
    },
    # .env files will be searched in the same directory
    #    with sample_env.py file
    directory=os.path.dirname(__file__),

    # environment variable with key "RUNTIME_TYPE" will be searched
    env_variable_for_type="RUNTIME_TYPE",

    # RuntimeType.DEV will be used when RUNTIME_TYPE is not set
    default_type=RuntimeType.DEV,
)
```

### Load environment variables

Run `RUNTIME_TYPE=dev; python -m main`

```py
# main.py

from .sample_env import env

# You can check the runtime type by accessing _runtime_type
assert env._runtime_type == RuntimeType.DEV

print(env.POSTGRES_USER)
print(env.POSTGRES_PASSWORD)
```

## Examples

### Handling secrets

You may have `.secret` files in local, and set .gitignore for them.
However you don't want to ship `.secret` files to production environment.
Instead, you can set environment variables directly in k8s, and `nyeok-dotenv` will load them in your env class.

```
.
├── .env.prod
├── .env.dev
├── .secret (not present in production)
├── use_secret.py
└── k8s
    ├── .secret (generated from .secret)
    ├── kustomization.yaml
    └── deployment.yaml
```

**Create k8s secret from local `.secret` file (kustomize)**

```yaml
# ./k8s/kustomization.yaml
secretGenerator:
  - name: backend-secret
    envs:
      - ./.secret
```

```sh
# Update secret file to match local development environment
cp .secret k8s/.secret
kubectl apply -k k8s
```

**Load secret in k8s deployment**

```yaml
containers:
  - name: backend-container
    env:
      - name: POSTGRES_PASSWORD
        valueFrom:
          secretKeyRef:
            name: backend-secret
            key: POSTGRES_PASSWORD
```

**Use env in code**

Now you can use `env.POSTGRES_PASSWORD`, both in dev environment and production environment.

### Without RuntimeType

> [!CAUTION]
> This feature is not implemented yet.

One might want to use `nyeok-dotenv` for managing environment variables for only one build type.
i.e. You want to load environment variables from `.env` and `.secret` files and access them by concrete class.

```py
# no_runtime_type.py

from nyeok_dotenv.EnvBase import EnvBase

class SampleEnv(EnvBase[RuntimeType]):
    # From .env
    POSTGRES_USER: str
    # From .secret
    POSTGRES_PASSWORD: str

env = SampleEnv(
    files_to_load=[".env", ".secret"],
    directory=os.path.dirname(__file__),
)
```

### Load files from different directories

You can specify `directory` to load `.env` files from different directories.

```
.
├── dir1
│   ├── .env
│   └── .secret
└── from_different_directory.py
```

```py
# from_different_directory.py

from nyeok_dotenv.EnvBase import EnvBase

class SampleEnv(EnvBase[RuntimeType]):
    # From .env
    POSTGRES_USER: str
    # From .secret
    POSTGRES_PASSWORD: str

env = SampleEnv(
    files_to_load=[".env", ".secret"],
    directory=os.path.join(os.path.dirname(__file__), "dir1"),
)
```

> [!NOTE]  
> If you don't specify `directory`, `nyeok-dotenv` will search `.env` files from the current working directory.
