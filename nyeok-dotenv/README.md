# nyeok-dotenv

`nyeok-dotenv` manages environment variables from `.env` files for different build types.

## Installation

To install `nyeok-dotenv`, run:

```sh
pip install nyeok-dotenv
```

## Usage

### Setup Directory Structure

`sample_env.py` will load `.env` files from the same directory.

```
.
├── .env.dev
├── .env.prod
├── .env.stage
├── .secret
├── main.py
└── sample_env.py
```

### Create a New Environment Variable Class

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
    # Define environment variables as type hints

    # nyeok-dotenv will not load _ prefix variables
    _hidden_variable: str

    # From .env
    POSTGRES_USER: str

    # From .secret
    POSTGRES_PASSWORD: str

# Create the environment class and export it
env = SampleEnv(
    runtime_type_cls=RuntimeType,
    files_to_load={
        RuntimeType.PROD: [".env.prod"],  # secret will be set by k8s
        RuntimeType.STAGE: [".env.stage", ".secret"],
        RuntimeType.DEV: [".env.dev", ".secret"],
    },
    # .env files will be searched in the same directory as sample_env.py
    directory=os.path.dirname(__file__),

    # Environment variable with key "RUNTIME_TYPE" will be used to determine the runtime type
    env_variable_for_type="RUNTIME_TYPE",

    # Default to RuntimeType.DEV if RUNTIME_TYPE is not set
    default_type=RuntimeType.DEV,
)
```

### Load Environment Variables

Run the application with the desired runtime type:

```sh
RUNTIME_TYPE=dev; python -m main
```

```py
# main.py

from .sample_env import env

# Check the runtime type
assert env._runtime_type == RuntimeType.DEV

print(env.POSTGRES_USER)
print(env.POSTGRES_PASSWORD)
```

## Examples

### Handling Secrets

You may have `.secret` files locally but don't want to include them in production. Instead, set environment variables directly in Kubernetes, and `nyeok-dotenv` will load them.

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

**Create Kubernetes Secret from Local `.secret` File (Using Kustomize)**

```yaml
# ./k8s/kustomization.yaml
secretGenerator:
  - name: backend-secret
    envs:
      - ./.secret
```

```sh
# Update the secret file to match the local development environment
cp .secret k8s/.secret
kubectl apply -k k8s
```

**Load Secret in Kubernetes Deployment**

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

**Use Env in Code**

You can now use `env.POSTGRES_PASSWORD` in both development and production environments.

### Without RuntimeType

> [!CAUTION]
> This feature is not implemented yet.

If you want to manage environment variables for only one build type, you can use `nyeok-dotenv` without `RuntimeType`.

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

### Load Files from Different Directories

Specify the `directory` to load `.env` files from different locations.

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
> If you don't specify directory, nyeok-dotenv will search .env files from the current working directory.

---
