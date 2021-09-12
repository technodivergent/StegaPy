# StegaPy
This is a simple steganography tool written in Python 3 to insert secret messages into an image.

## Usage
Use `python StegaPy.py -h` to get a full list of arguments

```
-h, --help              show this help message and exit
-e, --encode            Use in conjunction with -s to ENCODE a file
-d, --decode            Use in conjunction with -s to DECODE a file
-s SOURCE_FILE, --source SOURCE_FILE
                        Use this to specify the file to be encoded/decoded
-m MESSAGE, --message MESSAGE
                        Enter a message inside quotes to encode
-o OUTPUT_FILE, --output OUTPUT_FILE
                        Enter the destination file name
```
## Example
### Encoding
To encode a secret message using the provided lock.png image:

`python StegaPy.py -e -s lock.png -m "SECRET MESSAGE" -o lock-encoded.png`

### Decoding
To decode a message that has been inserted into an image:

`python StegaPy.py -d -s lock-encoded.png`