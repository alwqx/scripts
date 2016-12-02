#!/bin/bash
echo "start config git alias..."

git config --global alias.st status
git config --global alias.co checkout
git config --global alias.lg log
git config --global alias.br branch
git config --global alias.ci commit

echo "config done.your current git alias is:"
git config --list|grep 'alias'
