#!/bin/bash

# $1 and $2 are positional arguments called when the script is ran
curl -d '{"username": "'$1'", "password": "'$1'"}' -H "Content-Type: application/json" -X POST "http://127.0.0.1:3200/login"
