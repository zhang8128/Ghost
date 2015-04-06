from json import *
import requests
import marisa_trie
import random

url = 'https://script.google.com/macros/s/AKfycbyAxXCGK8-dDaUm_ijKBpiVNqJFqzowP0tu7h4eupTmIHbWJkMg/exec' 
url += '?user=Sonic2&hash='
hash_value = 'new'
word_fragment = ''
player_turn = 'even'
chars = 'abcdefghijklmnopqrstuvwxyz'

#checking for forced victory 1 move ahead
def odd_start(prefix, trie):
  for letter in chars:
    test = prefix + letter
    e = 0
    o = 0
    for word in trie.keys(str(test)):
      if len(word) % 2 == 0:
        e += 1
      else:
        o += 1
    if e == 0 and o > 0:
      return letter
  return second_guess_odd(prefix, trie)

def even_start(prefix, trie):
  for letter in chars:
    test = prefix + letter
    e = 0
    o = 0
    for word in trie.keys(str(test)):
      if len(word) % 2 == 0:
        e += 1
      else:
        o += 1
    if o == 0 and e > 0:
      return letter
  return second_guess_even(prefix, trie)

#checking for greater probability of victory
def second_guess_odd(prefix, trie):
  for letter in chars:
    print(letter)
    test = prefix + letter
    e = 0
    o = 0
    print(trie)
    for word in trie.keys(str(test)):
      print('1')
      if len(word) % 2 == 0:
        e += 1
      else:
        o += 1
    if e < o :
      if (u'%s' %test in trie) == False:
        if second_guess_odd_chal(test, trie) != 0:
          return letter
    return third_guess_odd(prefix, trie)

def second_guess_even(prefix, trie):
  for letter in chars:
    test = prefix + letter
    e = 0
    o = 0
    for word in trie.keys(str(test)):
      if len(word) % 2 == 0:
        e += 1
      else:
        o += 1
    if e > o:
      if (u'%s' %test in trie) == False:
        if second_guess_even_chal(test, trie) != 0:
          return letter
    return third_guess_even(prefix, trie)

#checking for opponent's victory choices
def second_guess_odd_chal(prefix, trie):
  for letter in chars:
    test = prefix + letter
    e = 0
    o = 0
    for word in trie.keys(str(test)):
      if len(word) % 2 == 0:
        e += 1
      else:
        o += 1
    if o == 0 and e > 0:
      return 0
  return 1

def second_guess_even_chal(prefix, trie):
  for letter in chars:
    test = prefix + letter
    e = 0
    o = 0
    for word in trie.keys(str(test)):
      if len(word) % 2 == 0:
        e += 1
      else:
        o += 1
    if e == 0 and o > 0:
      return 0
  return 1

#looking for choices that may have potential
def third_guess_odd(prefix, trie):
  for letter in chars:
    test = prefix + letter
    e = 0
    o = 0
    for word in trie.keys(str(test)):
      if len(word) % 2 == 0:
        e += 1
      else:
        o += 1
    if e < o :
      if (u'%s' %test in trie) == False:
        return letter
  return loss(prefix, trie)

def third_guess_even(prefix, trie):
  for letter in chars:
    test = prefix + letter
    e = 0
    o = 0
    for word in trie.keys(str(test)):
      if len(word) % 2 == 0:
        e += 1
      else:
        o += 1
    if e > o:
      if (u'%s' %test in trie) == False:
        return letter
  return loss(prefix, trie)

#just returning with a word
def loss(prefix, trie):
  rev = chars[::-1]
  for loss_letter in rev:
    test = prefix + loss_letter
    for word in trie.keys(str(test)):
      out = loss_letter
      return out

def play_second(hash_value, word_fragment):

  files = open("words.txt")
  fl = files.read().splitlines()
  files.close()

  trie = marisa_trie.Trie(fl)

  response = url + hash_value + '&fragment=' + word_fragment
  req = requests.get(response)
  data = req.json()
  hash_value = data['hash']
  frag = data['fragment']
  print (data['message'])
  if str(data['message']).find('I have lost') != -1:
    print ('Victory')
    return
  if str(data['message']).find('You win') != -1:
    print ('Victory')
    return
  if str(data['message']).find('I win') != -1:
    print ('Loss')
    return
  word_fragment = frag + odd_start(frag, trie)
  print ('Prefix: ' + word_fragment)
  play_second(hash_value, word_fragment)

def play_first(hash_value, word_fragment):

  files = open("words.txt")
  fl = files.read().splitlines()
  files.close()

  trie = marisa_trie.Trie(fl)
  if word_fragment == '':
    word_fragment = str(random.sample(set('abcdefghijklmnopqrstuvwxyz'), 1))
  response = url + hash_value + '&fragment=' + word_fragment
  req = requests.get(response)
  data = req.json()
  hash_value = data['hash']
  frag = data['fragment']
  print (data['message'])
  if str(data['message']).find('I have lost') != -1:
    print ('Victory')
    return
  if str(data['message']).find('You win') != -1:
    print ('Victory')
    return
  if str(data['message']).find('I win') != -1:
    print ('Loss')
    return
  word_fragment = frag + even_start(frag, trie)
  print ('Prefix: ' + word_fragment)
  play_first(hash_value, word_fragment)

play_second(hash_value, '')

#def auto(word_fragment):
#
#  files = open("words.txt")
#  fl = files.read().splitlines()
#  files.close()
#  trie = marisa_trie.Trie(fl)
  
#  if word_fragment == '':
#    word_fragment = str(random.sample(set('abcdefghijklmnopqrstuvwxyz'), 1))
#    print (word_fragment)
#  else:
#    word_fragment += even_start(word_fragment, trie)
#    print (word_fragment)
#  
#  print(odd_start(word_fragment, trie))
#  print (word_fragment)
#  for words in trie.keys(str(word_fragment)):
#    if word_fragment == words:
#      print('End')
#  auto(word_fragment)



#used to create word list
#for letter in 'acklmnoswx':
#  files = open("%s.txt" % letter)
#  fl = files.read().splitlines()
#  for word in fl:
#    if len(word) > 3:
#      fa.write(str(word) + "\n")
#  print letter
#  print(len(fl))
#  count = 0
#  first = first_sort(fl)
# for count in range(0, 10):
#    first = first_sort(first)
#  for word in first:
#    f.write(str(word) + "\n")

#  print(len(first))
#  f.close()
#  files.close()

