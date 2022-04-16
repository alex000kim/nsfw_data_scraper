#!/bin/bash

scripts_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
wget https://github.com/RipMeApp/ripme/releases/download/1.7.95/ripme.jar -O $scripts_dir/ripme.jar
