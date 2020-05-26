#!/bin/bash

service_name="test_service"

ENV=dev

[[ $ENV == 'local_testing' ]] && \
docker build -t ${service_name} . && \
docker \
run \
-ti \
--rm \
--env ENV=${ENV} \
--name ${service_name}_container \
${service_name}

[[ $ENV == 'dev' ]] && \
docker build -t ${service_name} . && \
docker \
run \
-ti \
--rm \
--env ENV=${ENV} \
--mount type=bind,source="$(pwd)"/,target=/root/ \
--name ${service_name}_container \
--entrypoint bash \
${service_name}
