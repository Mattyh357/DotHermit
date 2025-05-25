#!/bin/bash

# Get the list of current workspaces
workspaces=$(i3-msg -t get_workspaces | grep -oP '"num":\K\d+')

# Start with workspace 1 and find the first available one
for i in {1..20}; do
  if ! echo "$workspaces" | grep -q "^$i$"; then
    i3-msg workspace number $i
    break
  fi
done
