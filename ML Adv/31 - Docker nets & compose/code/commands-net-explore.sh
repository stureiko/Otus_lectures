docker network create -d bridge my-network

docker run -d -it --rm --name C1 alpine

docker run -d -it --rm --name C2 --network my-network alpine
docker run -d -it --rm --name C3 --network my-network alpine

docker exec -it C2 sh
docker exec -it C3 sh