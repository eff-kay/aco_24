advent of code 2022
===================

https://adventofcode.com/2022

### basic commands
```bash
# downloads the input and creates an input.txt file
cp 00 01 -r

cd 01/

# downloads the input and creates an input.txt file
aoc-download-input

# submit the first one
python first.py input.txt | aoc-submit --part 1

# submit the second one
python second.py input.txt | aoc-submit --part 2
```

### Support library

The support library is copied from https://github.com/anthonywritescode/aoc2015/tree/948e1fe13a89667707adfbef1487809584d95176/support, with some modifications of my own.