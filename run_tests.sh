#! /bin/bash


PYVICARE_EMAIL=
PYVICARE_PASSWORD=
PYVICARE_CLIENT_ID=
PYVICARE_DEVICE_TYPE=Generic

source ./env

if [ -z "$PYVICARE_EMAIL" ]
then
    echo "Disable integration tests as no secrets set. Create a 'env' file with:"
    echo "PYVICARE_EMAIL=[your email]"
    echo "PYVICARE_PASSWORD=[your password]"
    echo "PYVICARE_CLIENT_ID=[your client id]"
    echo "PYVICARE_DEVICE_TYPE=[device type: Generic, GazBoiler, etc.]"
    EXEC_INTEGRATION_TEST=0
else
    EXEC_INTEGRATION_TEST=1
fi

PYVICARE_EMAIL=$PYVICARE_EMAIL \
PYVICARE_PASSWORD=$PYVICARE_PASSWORD \
PYVICARE_CLIENT_ID=$PYVICARE_CLIENT_ID \
PYVICARE_DEVICE_TYPE=$PYVICARE_DEVICE_TYPE \
EXEC_INTEGRATION_TEST=$EXEC_INTEGRATION_TEST \
    pytest