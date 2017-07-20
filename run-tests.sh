#!/bin/bash

coverage erase
coverage run --source="." --omit="src/**,core/tests/test_ui/*" manage.py test -v=3 --pattern="test_*.py" --settings=nexchange.settings_test
while getopts ":c:" opt; do
    COVERALLS_REPO_TOKEN=Y9cfC0hPig5JrjZe4zxgvgcuoZ3AmxZYo coveralls
done
TEST_STATUS_CODE=$?
coverage report
coverage html -d cover

#!/bin/bash

touch /root/test 2> /dev/null

if [ ${TEST_STATUS_CODE} -eq 0 ]
then
   echo "TESTS PASSED"
   exit 0
else
  echo "TESTS FAILED"
  exit 1
fi
