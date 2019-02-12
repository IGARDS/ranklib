#docker run -d -p 8080:80 -p 8021:21 -p 8022:22 bgruening/galaxy-stable

# Run a docker with the env boot script
#-e "PROXY_PREFIX=/galaxy" \
#    -v /mnt/disk1/export/:/export/
docker run -d -v `pwd`/deps:/deps bgruening/galaxy-stable 

# Get the container ID of the last run docker (above)
export CONTAINER_ID=`docker ps -lq`

docker exec -it $CONTAINER_ID /deps/image_setup.sh

# Commit the container state (returns an image_id with sha256: prefix cut off)
# and write the IMAGE_ID to disk at ~/.docker_image_id
(docker commit $CONTAINER_ID | cut -c8-) > ~/.docker_image_id
