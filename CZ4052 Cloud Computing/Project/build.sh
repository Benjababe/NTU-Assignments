#!/bin/bash

rm -rf ./backend/build
cd frontend && npm run build-low-mem;
mv build ../backend/