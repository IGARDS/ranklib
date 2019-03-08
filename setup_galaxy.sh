# Run a docker with the env boot script
#-e "PROXY_PREFIX=/galaxy" \
docker run -d -e "NONUSE=slurmctld" -p 8080:80 -p 8021:21 -p 8022:22 -v /export:/export -v $HOME/.ssh:/.ssh -v /ranklib/:/ranklib bgruening/galaxy-stable 

sleep 5

# Get the container ID of the last run docker (above)
export CONTAINER_ID=`docker ps -lq`
echo $CONTAINER_ID

docker exec -it $CONTAINER_ID /ranklib/deps/image_setup.sh

# Commit the container state (returns an image_id with sha256: prefix cut off)
# and write the IMAGE_ID to disk at ~/.docker_image_id
#(docker commit $CONTAINER_ID | cut -c8-) > ~/.docker_image_id

docker exec $CONTAINER_ID supervisorctl restart galaxy:

#ln -s /export/galaxy-central /galaxy-central

#groupadd -g 1450 galaxy
#useradd -u 1450 -g 1450 galaxy
#mkdir /home/galaxy
#mkdir /home/galaxy/.ssh
#cp -Rp $HOME/.ssh/* /home/galaxy/.ssh
#chown -R galaxy:galaxy /home/galaxy
