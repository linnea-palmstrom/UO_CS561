#!/usr/bin/env bash
TVMDIR=~/Dropbox/24S-461-compilers/dev/tiny_vm
#TVMDIR=~/Documents/UO_CS561/tiny_vm/tiny_vm

# Compile and run a Quack program (on my home laptop)
echo "Compiling $1"
python3 quack_front.py $1 >${TVMDIR}/QkASM/qkmain.asm
if [ $? == 0 ]; then
  pushd ${TVMDIR}
  python3 assemble.py QkASM/qkmain.asm > ${TVMDIR}/OBJ/\$Main.json
  if [ $? == 0 ]; then
    bin/tiny_vm \$Main
  fi
  popd

fi
