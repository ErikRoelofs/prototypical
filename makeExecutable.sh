pyinstaller.exe --onefile --windowed prototypical.py
cp *.md dist/
cp data -r dist/
cp LICENSE dist/
cp demogame.xls dist/
git describe --tags $(git rev-list --tags --max-count=1) >> dist/data/version