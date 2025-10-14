


#!/bin/bash

export DOCKER_BUILDKIT=1

docker-compose down 

# docker system prune -f
# docker volume prune -f

# rm -rf workflows/workflow_use/recorder/user_data_dir/Default/Cache/ 2>/dev/null || true

# df -h
# docker system df

# docker-compose build --no-cache  
docker-compose build 

docker-compose up -d

docker-compose logs -f
