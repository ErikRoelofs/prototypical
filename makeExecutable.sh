pyinstaller.exe --onefile --windowed prototypical.py
cp data -r dist/
cp LICENSE dist/
cp demogame.xls dist/
git describe --tags $(git rev-list --tags --max-count=1) >> dist/data/version
pandoc -s -o readme.html readme.md
pandoc -s -o reference.html reference.md
cp *.html dist/
