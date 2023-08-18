# Scope H/

```
.
├── Dockerfile
├── Makefile
├── README.md
├── opt
│ ├── client
│ ├── docker-compose.yml
│ └── server
├── requirements.txt
└── src
├── Roboto-Regular.ttf
├── bubble(700x100).png
├── cover.png
├── main.py
├── user_posts.csv
└── users.csv
```

src contains the main challenge (creating a report), it uses Docker.

Opt directory contains the optional challenge built in:

- FastAPI (server)
- Vite + React (client)
- Docker

The optional challenge.

## Main Challenge (Getting Started)

First download the project from GitHub: 
- Click the Code button. 
- Click download zip. 
- Unzip the folder and open in a [code editor of your choice](https://code.visualstudio.com/download)

This project uses Docker. Download [Orbstack](https://orbstack.dev/) a light-weight Docker client and [install it](https://docs.orbstack.dev/quick-start). That's all you need to get started running the project.

## Main Challenge (Run)

To run the main challenge, open the terminal via Ctrl +` and type the following: 

```bash 
make run
```

It will create an `influencer.pdf` file in the src directory. 

## Optional Challenge (run)
To run the main challenge, open the terminal via Ctrl +` and type the following: 

```bash 
make up
```

It will start the FastAPI server and client app which can be found [here](http://localhost:3000)