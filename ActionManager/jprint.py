#Format it like json!
#Just literal processing.

def jformat(astr, indent=4):
  astr = ''.join([c for c in astr if c != ' '])
  nstr = ''
  indent_level = 0
  insmall = False
  for i in range(len(astr)):
    char = astr[i]
    if char == '(':
      insmall = True
    if char == ')':
      insmall = False
    if char in ',[]{}':
      if char == ',' and not insmall:
        char = char+'\n'+' '*(indent*indent_level)
      if char in '[{':
        indent_level += 1
        char = char+'\n'+' '*(indent*indent_level)
      if char in ']}':
        indent_level -= 1
        char = '\n'+' '*(indent*indent_level)+char
    nstr += char
  return nstr

def jprint(obj, indent=4):
  print(jformat(repr(obj), indent=indent))