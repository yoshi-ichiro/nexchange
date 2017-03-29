#!/bin/bash

RUNNING_CONTAINER=$(docker ps -q --filter name="wercker-pipeline-" --filter status=running)

function use_running_container {
    coverage_cmd="coverage erase"
    coverage_cmd="${coverage_cmd} && coverage run --source='.' --omit='src/' manage.py test -v 3 --pattern='test_*.py'"
    coverage_cmd="${coverage_cmd} && coverage report "
    coverage_cmd="${coverage_cmd} && coverage html -d cover"

    echo "${coverage_cmd}"

    static_validation_cmd_py="cd /pipeline/source && ./static-validation-py.sh"
    static_validation_cmd_js="cd /pipeline/source && ./static-validation-js.sh"
    backend_tests="cd /pipeline/source && export DJANGO_SETTINGS_MODULE=nexchange.settings_test && ${coverage_cmd}"
    frontend_tests="cd /pipeline/source && PHANTOMJS_BIN=node_modules/.bin/phantomjs  npm run-script test"

    docker exec -t ${RUNNING_CONTAINER} bash -c "${static_validation_cmd_py}" &&
        docker exec -t ${RUNNING_CONTAINER} bash -c "${static_validation_cmd_js}" &&
            docker exec -t ${RUNNING_CONTAINER} bash -c "${backend_tests}"
}

function use_wercker {
    wercker build --direct-mount --pipeline static-validation-py &&
        wercker build --direct-mount --pipeline static-validation-js &&
            wercker build --direct-mount --pipeline tests
}

autopep8 --in-place --aggressive --aggressive **/**/**py
if [ -z "${RUNNING_CONTAINER}" ]; then
    echo -e "\e[33mDid not found a running container for the nexchange project. Starting one to execute the pre-commit hook.\e[39m"
    use_wercker
else
    echo -e "\e[32mRunning pre-commit hook inside the container with id ${RUNNING_CONTAINER}, which is believed to be nexchange dev.\e[39m"
    use_running_container
fi
