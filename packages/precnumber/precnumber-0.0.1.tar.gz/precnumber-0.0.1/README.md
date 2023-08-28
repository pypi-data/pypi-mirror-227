## Float Point Arithmetic is Imprecise

Many new python coders will be frustrated at the seemingly nonsensical way the language handles floating point numbers: even operations as simple as 0.1 + 0.2 should be easy to compute, right? Turns out floating point number storage yields many issues, and many minds smarter than me decided imprecision is better than storage and processing cost. The idea of this project is to invert that notion, storing floating point numbers as ratios.

```python
0.1 + 0.2 == 0.3 #True
Number.parse("0.1") + Number.parse("0.2") == Number.parse("0.3") #False
Number.parse("0.92") / Number.parse("245") #23/6125
```

## Operation Examples

This library provides all basic arithmetic operations needed for numbers: addition, substration, multiplication, and division, as well as helper functions such as floor, ceil, opposite, inverse, and the equality operator.

```python
Number.parse("3.2") + Number.parse("4.7") #79/10
Number.parse("9.21") - Number.parse("18.45") #231/-25
Number.parse("1.6") * Number.parse("2.4") #96/25
Number.parse("1.4") / Number.parse("3.3") #14/33
Number.parse("1.5") == Number(3, 2) #True
Number.parse("3.4").floor() #3
Number.parse("0.2").ceil() #1
Number.parse("-3").opposite() #3
Number.parse("0.5").inverse() #2
```
