#!/bin/bash

find /root -type f -name "*.key" -mtime +1 -delete
