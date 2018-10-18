#!/usr/bin/env bash

set -e

get_script_dir () {
     SOURCE="${BASH_SOURCE[0]}"
     while [ -h "$SOURCE" ]; do
          DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
          SOURCE="$( readlink "$SOURCE" )"
          [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
     done
     $( cd -P "$( dirname "$SOURCE" )" )
     pwd
}

SCRIPT_DIR="$( get_script_dir )"
CACHE_DIR="${SCRIPT_DIR}/cache"
BUILD_DIR="${SCRIPT_DIR}/build"
TMP_DIR=$(mktemp -d)
START_DIR=`pwd`

mkdir -p $BUILD_DIR $CACHE_DIR

echo "Building lambda… "

echo "Working in ${TMP_DIR}"

rm -rf "${BUILD_DIR}/lambda.zip" "${BUILD_DIR}/lambda"

cp lambda.py "${TMP_DIR}/lambda_function.py"

cd "${TMP_DIR}"
pip install -t . requests
rm -rf tests *.dist-info
zip -r "${BUILD_DIR}/lambda.zip" * -x Pillow\* > /dev/null

echo "Lambda file at '${BUILD_DIR}/lambda.zip' updated"
cd "${START_DIR}"

echo "… Done"

if [[ "$1" == "--upload" ]]; then
    AWSREGION="eu-west-1"
    aws lambda update-function-code --function-name receiveBeerBotMail --region "$AWSREGION" --zip-file "fileb://${BUILD_DIR}/lambda.zip"
fi