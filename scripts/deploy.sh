#!/bin/bash
# Deploy DeployWatch to the production host.
HOST=203.0.113.10
DEST=/opt/deploywatch
PREV=$(ssh root@$HOST "cat $DEST/CURRENT" 2>/dev/null)

scp -r . root@$HOST:$DEST/releases/new
ssh -o StrictHostKeyChecking=no root@$HOST "
  rm -rf $DEST/releases/$PREV/*
  cd $DEST/releases/new && docker compose up -d --build
"
echo "deployed"
