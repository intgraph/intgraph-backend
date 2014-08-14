import pyparsing as pp

key  = pp.LineStart().suppress() + pp.Word(pp.alphanums) + pp.Suppress(':')
value = pp.restOfLine + pp.LineEnd().suppress() 

kvParser = pp.dictOf(key, value)

###

session_name = pp.OneOrMore(pp.Word(pp.alphanums))
session = (pp.LineStart().suppress() + pp.Suppress('[') + session_name + pp.Suppress(']') + pp.LineEnd().suppress()) 

zeroOrMoreEmptyLines = pp.ZeroOrMore(pp.LineEnd().suppress())

line = pp.LineStart() \
        + pp.SkipTo(pp.LineEnd(), failOn=session) \
        + pp.LineEnd().suppress()
lines = pp.Group(pp.ZeroOrMore(line.leaveWhitespace()))

contentParser = pp.dictOf(session, lines)

Parser = pp.Keyword('[Metadata]').suppress() \
            + pp.LineEnd().suppress() \
            + kvParser.setResultsName('Metadata') \
        + pp.Keyword('[Tags]').suppress() \
            + pp.LineEnd().suppress() \
            + kvParser.setResultsName('Tags') \
        + pp.Group(contentParser).setResultsName('Content')

def parse(fc):
    return Parser.parseString(fc)

'''
print stats.Metadata.kvlist
print stats.Tags.kvlist
print stats.Content['Description']
print stats.Content['Solution']
'''

if __name__ == '__main__':
    md = '''\
[Metadata]
title: Hello World
date: 2014-08-10 23:13:31 

[Tags]
difficulty: 3
categories: simulation, no algorithm
source: unknown

[Description]
This is a example problem. Just calculate a + b.

[Solution]
The solution here is ready to play.
         

Are you sure?

```python
import sys
for line in sys.stdin:
    (a, b) = map(int, line.split())
    print a + b
```
'''
    stats = parse(md)
    print dir(stats.Metadata)
    print stats.Tags
    for key, value in stats.Content:
        print key, value
