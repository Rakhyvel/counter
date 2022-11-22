# A program that counts source lines of code and tokens, skipping comments, of all files of a given folder
# Usage: counter.py <dir_name> <lang>

import sys
import os
import random

file_extensions = {
    "python" : {".py"},
    "javascript" : {".js"},
    "typescript" : {".js", ".ts"},
    "go" : {".go"},
    "c++" : {".cpp", ".hpp", ".c", ".h"},
    "rust" : {".rs"},
    "java" : {".java"},
    "c#" : {".cs"},
    "kotlin" : {".kt"},
    "c": {".c", ".h"},
    "php" : {"php"},
    "typescript" : {".ts"},
    "swift" : {".swift"},
    "zig" : {".zig"},
    "julia" : {".jl"},
    "scala" : {".scala"},
    "elixir" : {".ex"},
    "ruby" : {".rb"},
    "blade" : {".b"},
    "pascal" : {".pas"},
    "prolog" : {".pl"},
    "nim" : {".nim"},
    "groovy" : {".groovy"},
    "visual_basic" : {".vb"},
    "ocaml" : {".ml"},
    "haskell" : {".hs"},
    "fortran" : {".F"},
    "f#" : {".fs"},
    "clojure" : {".cj"},
    "perl" : {".pl"},
    "odin" : {".odin"},
    "crystal" : {".cr"},
    "tcl" : {".tcl"},
    "smalltalk" : {".st"},
    "lisp" : {".lisp"},
    "objective-c" : {".m", ".h"},
    "ada" : {".ads", ".adb"},
    "haxe" : {".hx"},
    "racket" : {".rkt"},
    "erlang" : {".erl"},
    "sml" : {".ml"},
    "d" : {".d"},
    "scheme" : {".scm"},
    "orng" : {".orng"},
}

line_comment = {
    "python" : "#",
    "go" : "//",
    "c++" : "//",
    "rust" : "//",
    "java" : "//",
    "c" : "//"
}

block_comment_begin = {
    "python" : '"""',
    "go" : "/*",
    "c++" : "/*",
    "rust" : "/*",
    "java" : "/*",
    "c" : "/*"
}

block_comment_end = {
    "python" : '"""',
    "go" : "*/",
    "c++" : "*/",
    "rust" : "*/",
    "java" : "*/",
    "c" : "*/"
}

string_delimiter = {
    "python" : "'",
    "go" : '"',
    "c++" : '"',
    "rust" : '"',
    "java" : '"',
    "c" : '"'
}

lang = sys.argv[2]
if lang not in file_extensions:
    print(f"error: unknown file-extensions for {lang}")
    sys.exit(1)
if lang not in line_comment:
    print(f"error: unknown line comment token for {lang}")
    sys.exit(1)

class File:
    def __init__(self, file_name, sloc, tokens):
        self.file_name = file_name
        self.sloc = sloc
        self.tokens = tokens

 
# Get the list of all files and directories
def read_files(dir)->list[File]:
    files = []
    try:
        dir_list = os.listdir(dir)
    except:
        return files
    for file_name in dir_list:
        if os.path.isdir(dir + "/" + file_name):
            try:
                files += read_files(dir + "/" + file_name)
            except:
                continue
        else:
            ext_set = file_extensions[lang]
            for ext in ext_set:
                if file_name.endswith(ext):
                    files.append(read_file(dir + "/" + file_name))
    return files

def get_char_class(c:str):
    if c.isalnum() or c == "_":
        return 0
    elif c in {"\n", "(", ")", "[", "]", "{", "}", "\"", "'", "`"}:
        return random.randint(3, 100000000000)
    elif c.isspace():
        return 1
    else:
        return 2


def read_file(file_name)->File:
    sloc = 1
    tokens = 0
    with open(file_name) as f:
        line = f.read()

    token_list:list[str] = []
    data = line[0]
    past_c = line[0]
    count = 1
    for c in line[1:]:
        if get_char_class(c) != get_char_class(past_c) or c == "\n":
            if c == "\n":
                count += 1
            token_list.append(data)
            data = ""
        if (not c.isspace()) or c == "\n":
            data += c
        past_c = c
    token_list.append(data)

    in_line_comment = False
    in_block_comment = False
    in_string = False
    prev_wasnt_newline = False
    for t in token_list:
        if in_line_comment:
            if t == "\n":
                in_line_comment = False
        elif in_block_comment:
            if block_comment_end[lang] in t:
                in_block_comment = False
        elif in_string:
            if string_delimiter[lang] in t:
                in_string = False
        elif t.startswith(line_comment[lang]) or t.endswith(line_comment[lang]):
            in_line_comment = True
        elif lang in block_comment_begin and t.startswith(block_comment_begin[lang]):
            in_block_comment = True
        elif t.startswith(string_delimiter[lang]):
            in_string = True
            tokens += 1
        else:
            if not t.isspace() and len(t) > 0:
                tokens += 1
            if prev_wasnt_newline and t == "\n":
                sloc += 1
        prev_wasnt_newline = t != "\n"

    return File(file_name, sloc, tokens)
    

files = read_files(sys.argv[1])
files.sort(key = lambda file: -file.tokens)
max_filename_length = 0
for file in files:
    max_filename_length = max(max_filename_length, len(file.file_name))

total_files = 0
total_sloc = 0
total_tokens = 0
total_wideness = 0
for file in files:
    total_files += 1
    total_sloc += file.sloc
    total_tokens += file.tokens
    if file.sloc > 0:
        total_wideness += file.tokens / file.sloc
        print(f"{file.file_name.ljust(max_filename_length)} sloc: {file.sloc:<6} tokens: {file.tokens:<6} wideness: {round(file.tokens/file.sloc)}")
    else:
        print(f"{file.file_name.ljust(max_filename_length)} sloc: {file.sloc:<6} tokens: {file.tokens:<6} wideness: 0")

if total_files > 0:
    print(f"{'total'.ljust(max_filename_length)} sloc: {total_sloc:<6} tokens: {total_tokens:<6} wideness: {round(total_wideness / total_files)}")
else:
    print(f"error: no {lang} files found in directory `{sys.argv[1]}`")