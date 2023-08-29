<!-- GETTING STARTED -->
## Getting Started

### Installation

Install protoc
* MacOS
  ```sh
  brew install protobuf
  protoc --version  # Ensure compiler version is 3+
  ```
* Linux
  ```sh
  apt install -y protobuf-compiler
  protoc --version  # Ensure compiler version is 3+
  ```

### Venv

1. Clone library repo
   ```sh
   git clone https://github.com/bot-auto/botdata-sdk.git
   ```
2. Create virtual environment
   ```sh
   cd botdata-sdk
   python3 -m venv venv
   source venv/bin/activate
   ```

### Venv

1. Clone library repo
   ```sh
   git clone https://github.com/bot-auto/botdata-sdk.git
   ```
2. Create virtual environment
   ```sh
   cd botdata-sdk
   python3 -m venv venv
   source venv/bin/activate
   ```

### Pre-commit

1. Get pre-commit installed
   ```sh
   pip3 install pre-commit # linux
   pip3 install pylint
   pip3 install flake8
   brew install pre-commit # mac
   pre-commit --version
   pre-commit install # install .pre-commit-config.yaml
   ```
2. Register pre-commit with git and run
   ```sh
   git add .pre-commit-config.yaml # register git commit enforced runing with pre-commit
   pre-commit run --all-files # run all files
   ```

### Build

1. Clone proto repo
   ```sh
   cd ~/workstation
   git clone https://github.com/bot-auto/idl-proto.git
   cd idl-proto
   ```
2. Install protoc
   ```sh
   brew install protobuf # mac
   pip3 install protobuf # linux
   protoc --version
   ```
3. Build grpc proto
   ```sh
   mkdir ../botdata-sdk/botdata_sdk/protobuf/grpc_generated
   SRC_DIR=botdata-sdk
   DST_DIR=../botdata-sdk/botdata_sdk/protobuf/grpc_generated
   protoc -I=$SRC_DIR --proto_path=botdata-sdk --init_python_out=$DST_DIR --python_out=$DST_DIR --pyi_out=$DST_DIR $SRC_DIR/botdata.proto #pyhon
   protoc -I=$SRC_DIR --cpp_out=$DST_DIR $SRC_DIR/botdata.proto #C++
   ```
