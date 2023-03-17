# TCP-Server
Python Dockerised local network tcp server ( FIT - PSI)


## Sample quickstart

Navigate to the Sample directory using:
```
cd Sample
```

### Server
Run the server side using docker:
```
docker build -t my-python-server .
docker run -p 8080:8080 my-python-server
```
### Client
You can test the server using a client by running:
```
python client.py
```