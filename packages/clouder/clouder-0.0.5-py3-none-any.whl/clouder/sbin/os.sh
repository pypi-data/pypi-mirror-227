# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

uname_out="$(uname -s)"

case "${uname_out}" in
    Linux*)     export OS=LINUX;;
    Darwin*)    export OS=MACOS;;
#    CYGWIN*)    OS=CYGWIND;;
#    MINGW*)     OS=MINGW;;
    *)          export OS="UNSUPPORTED:${unameOut}"
esac
