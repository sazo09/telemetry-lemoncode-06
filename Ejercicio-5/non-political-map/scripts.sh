docker build -t app-map-api -f build/Dockerfile.api .

docker run -d -p 4000:4000 app-map-api

docker build -t app-map -f build/Dockerfile.app .

docker run -d -p 4000:4000 app-map