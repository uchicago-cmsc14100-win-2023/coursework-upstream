#!/bin/bash

echo "Getting files..."

wget -nv -O hw6.tgz http://people.cs.uchicago.edu/~amr/hw6.tgz

echo "Unbundling files..."

tar -xzf hw6.tgz

rm hw6.tgz
