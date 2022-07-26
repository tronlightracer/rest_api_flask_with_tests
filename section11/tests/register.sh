#!/bin/bash

curl -d '{"username": "'$1'", "password": "'$2'"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:3200/register