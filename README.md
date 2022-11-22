# Counter
This program counts the number of files, source-lines-of-code (SLOC) and tokens in your project given a directory and language. 

## Usage
```
python counter.py <project-directory> <language>
```

Running the counter on the following python script:
```
# test.py
password = input("What is the password?")
if password == "orange":
    print("That is correct")
else:
    print("That is incorrect!")
```
Gives:
```
test.py   sloc: 5     tokens: 21
```

## Language
To accurate count the tokens of each language, `counter.py` needs the file extension(s) for the language, the line comment token if any, any block comment tokens if any, and the string delimtier. These are defined as dictionaries that map the language name to the token/set of tokens. Feel free to add it for your language if I've missed it.
