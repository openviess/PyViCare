#! /bin/bash

if [ -z "$PYVICARE_CLIENT_ID" ]
then
    echo "Disable integration tests as no secrets set. Create a '.env' file with:"
    echo "PYVICARE_CLIENT_ID=[your client id]"
    EXEC_INTEGRATION_TEST=0
else
    EXEC_INTEGRATION_TEST=1
fi

EXEC_INTEGRATION_TEST=$EXEC_INTEGRATION_TEST \
PYVICARE_CLIENT_ID=$PYVICARE_CLIENT_ID \
    pytest