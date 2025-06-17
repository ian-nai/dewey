# Dewey
Dewey is an esolang based around the Dewey Decimal system. All of its statements are written in the format of catalog codes following the general format of the DDC: [three digit number].[three digit number] [optional extra text] (e.g., 000.000 Text).

Each line in your .dewey file must be on a new line. Multiple lines can be combined into one statement, as in the hello world example below:

```
# print “hello world”
900.006 # multiline statement
010.000 # print
700.000 # (
217.85 llo # "hello "
401.000 # +
261.23 orld # "world"
800.000 # )
```

You can run the code in a dewey file via the Python interpeter, like so:
```
python3 interpreter.py test.dewey
```

## Code Structure:

The DDC breaks books into ten general categories denoted by three digit numerical prefixes. This code takes a similar approach to writing statements, utilizing the 10 categories in the Dewey system to structure its code:

* 000:
    * This category handles print statements.

* 100:
    * Used for declaring variables.

* 200:
    * Declares a string or integer.

* 300:
    * Used for if (301) / then (302) / else (303) / while (304) statements.

* 400:
    * Addition (401 for "+" ) and subtraction (402 for "-") operators.

* 500:
    * Multiplication (501 for "*" ) and dividing (502 for "/") operators.

* 600:
    * Used for the “==” operator.

* 700:
    * Used for a left parentheses.

* 800:
    * Used for a right parentheses.

* 900:
    * Used to declare multiline statements.

The two numbers following the main classification category (e.g., the two 0s following the 9 in 900) are used for further modification. The second number is used to denote whether the numbers in the second section will be interpreted as a lowercase string, uppercase string, or integer: 0 means the second section will be interpeted as an integer, 1 as a lowercase string of letters, 2 as all capitals except the letter at the operator location (if one is specified), and 3 as all lowercase except the letter at the operator location (if one is specified). The third is used to denote the operator location (e.g., if only one letter should be capitalized in a string, typing 3 as your second number and 5 as your third will only capitalize the 5th letter of your string.) 

Additionally, the numbers 4, 5, and 6 can be used in conjunction with certain categories of the first section to denote other cases. Using 4 as your second number is required when declaring a variable, and the operator location denotes whether to use the digits of your second section, lowercase letters, or uppercase for your variable value. The third section of your line will always be the variable name. Using 5 in conjunction with the 200 category will allow you to simply type an integer without quotes (e.g., 250.100 becomes 100). Using 6 will interpret the numbers in the second section as a single, double-digit number, allowing you to use those numbers for letters in the alphabet (e.g., 212.23 becomes "w").

# Second Section
The second set of three numbers and the optional additional set of letters can be used to include additional information in each statement. The numbers can be interpreted as digits (if the second number in the first section is 0) or as strings of letters (if the second number is 1, 2, or 3), with the numbers mapped numerically to the Latin alphabet (e.g., "a" = 1). 

Additional modifications can be made by appending numbers following a colon to this second set of three digits. These can be chained together, and can be used for the following symbols:

* 1 = “:”
* 2 = “\t” (tab)
* 3 = “!”
* 4 = “{”
* 5 = “}”
* 6 = “ ” (space)

For example, typing 210.85:6 llo would output "he llo ", as our space is appended after our second set of digits.

# Third Section
This section allows you to include additional letters or numbers that will be appended to your string from the second section. For example, the statement "011.123 123" prints "abc123".

# Comments
Comments are denoted by the ‘#’ sign.
