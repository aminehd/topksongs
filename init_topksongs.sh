mkdir -p docker/{kafka,spark}

# Create producer project
poetry new producer
cd producer
poetry install

# Create consumer project
cd ..
poetry new consumer
cd consumer
poetry install



# docker run -d \
#   -p 9000:9000 \
#   --name portainer \
#   --restart=always \
#     -v /var/run/docker.sock:/var/run/docker.sock \
#     -v /home/amineh/WorkSpace/SimulatePaxos:/home/amineh/WorkSpace/SimulatePaxos \
#     -v portainer_data:/data \
#   portainer/portainer-ce
