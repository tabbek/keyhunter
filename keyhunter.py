#!/usr/bin/python

import binascii
import os
import hashlib
import sys

# bytes to read at a time from file (10meg)
readlength=10*1024*1024

if len(sys.argv)!=2:
  print "./keyhunter.py <filename>"
  exit()

filename = sys.argv[1]


magic = '\x01\x30\x82\x01\x13\x02\x01\x01\x04\x20'
magiclen = len(magic)



##### start code from pywallet.py #############
__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58encode(v):
  """ encode v, which is a string of bytes, to base58.
  """

  long_value = 0L
  for (i, c) in enumerate(v[::-1]):
    long_value += (256**i) * ord(c)

  result = ''
  while long_value >= __b58base:
    div, mod = divmod(long_value, __b58base)
    result = __b58chars[mod] + result
    long_value = div
  result = __b58chars[long_value] + result

  # Bitcoin does a little leading-zero-compression:
  # leading 0-bytes in the input become leading-1s
  nPad = 0
  for c in v:
    if c == '\0': nPad += 1
    else: break

  return (__b58chars[0]*nPad) + result

def Hash(data):
  return hashlib.sha256(hashlib.sha256(data).digest()).digest()

def EncodeBase58Check(secret):
  hash = Hash(secret)
  return b58encode(secret + hash[0:4])

########## end code from pywallet.py ############


with open(filename, 'r') as f:


  # read through target file
  # one block at a time
  while True:
    data = f.read(readlength)
    if not data:
      break

    # look in this block for keys
    x=0
    while True:
      # find the magic number
      pos=data.find(magic,x)
      #pos=data.find('\13\02\01\01\04\20',0)
      if pos==-1:
        break
      print EncodeBase58Check('\x80'+data[pos+magiclen:pos+magiclen+32])
      x+=(pos+1)
  
    # are we at the end of the file?
    if len(data) < readlength:
      break

    # make sure we didn't miss any keys at the end of the block
    f.seek(f.tell()-(32+magiclen))

# code grabbed from pywallet.py

