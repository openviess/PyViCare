#! /bin/bash


PYVICARE_EMAIL=
PYVICARE_PASSWORD=
PYVICARE_CLIENT_ID=

source ./env

if [ -z "$PYVICARE_EMAIL" ]
then
    echo "Disable integration tests as no secrets set. Create a 'env' file with:"
    echo "PYVICARE_EMAIL=[your email]"
    echo "PYVICARE_PASSWORD=[your password]"
    echo "PYVICARE_CLIENT_ID=[your client id"
    EXEC_TESTS=0
else
    EXEC_TESTS=1
fi

PYVICARE_EMAIL=$PYVICARE_EMAIL \
PYVICARE_PASSWORD=$PYVICARE_PASSWORD \
PYVICARE_CLIENT_ID=$PYVICARE_CLIENT_ID \
EXEC_INTEGRATION_TEST=$EXEC_TESTS \
    pytest