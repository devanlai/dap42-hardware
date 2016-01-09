#!/bin/sh
if [ -z "$1" ]; then
	echo "Pass in filename without .dch extension"
else
	docker run -i --rm --entrypoint="/tmp/bin/export-asc.sh" devanlai/diptrace-export:beta < $1.dch > $1.asc
	./remove-scaling.py < $1.asc > $1.filtered.asc
	docker run -i --rm --entrypoint="/tmp/bin/import-asc.sh" devanlai/diptrace-export:beta < $1.filtered.asc > $1.filtered.dch
	docker run -i --rm devanlai/diptrace-export:beta $1 < $1.filtered.dch > temp.zip
	mkdir -p renders/
	unzip -j -d renders/$1/ temp.zip
	mogrify -define png:exclude-chunks=date,time -strip -format png renders/$1/*.bmp
	rm renders/$1/*.bmp
	rm temp.zip
	rm $1.asc
	rm $1.filtered.asc
	rm $1.filtered.dch
fi
