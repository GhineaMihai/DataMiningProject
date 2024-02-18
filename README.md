# How to Run

## Install IDE and Libraries
1. **Install an IDE**, we used `PyCharm`
2. **Clone the project**.
3. **Install the libraries** (`nltk`, `whoosh`, `openapi`). On PyCharm you can click the imports that give an error and the top solution should be to install them.

## Download the necessary files
1. **Download** the `wiki_files` and the `wiki_index` from this  [link](https://drive.google.com/file/d/1bdJMXs7Prtkcewp6E-U4NZSlO6vnGSBX/view?usp=sharing). Place the .7z archive in the project directory and extract.
2. **If you want** to create the `index`, delete the files inside the `wiki_index` directory. **Delete only the files, not the directory**

## Run
**When running**, the program will ask the following questions 
1. **Do you want to create the index? (Y/N)**
2. **Do you want to use the categories when searching the index file? (Y/N)**
3. **Do you want to use ChatGPT? (Y/N)**

**Use**, `Y` or `N`. Capitalized and no spaces. If something else is used the program will prompt you with:

`Use Y or N, capitalized`

**ChatGPT** might not work, with the currently used `api_key`, try to use one of your own by going into `methods.py` ar line 105 and changing the field `api_key=""`

## Result
**After Running**, generally you will see the following output in the console:

1. `P@1=<number>`
2. `ResInFirst10=<number>`

`P@1` is the number of times the first answer for a query was also the correct one. divided by 100.

`ResInFirst10` is the number of times the answers for a query also contained the correct one in the top 10 results, divided by 100.

`<number>` is a number between 0 and 1

**For example**, the result for running the program and using the categories is:

**P@1=0.22**

**ResInFirst10=0.38**

**If ChatGPT** is used you also have:
- `ResChatGPT=<number>`