# Usage


## FUNCTIONS

### *Format*

+ `list2str`, `l2str` turn list to str
```python
list2str(list, separator)

list2str([1, 2, 3, 4, 5], ' and ')
>> 1 and 2 and 3 and 4 and 5
```

+ `str2list`, `str2l` turn str to list
```python
str2list(str, separator)

str2list('1 and 2 and 3 and 4 and 5', ' and ')
>> [1, 2, 3, 4, 5]
```

+ `tuple2str`, `t2str` turn tuple to str
```python
tuple2str(tuple, separator)

tuple2str((1, 2, 3, 4, 5), ' and ')
>> 1 and 2 and 3 and 4 and 5
```

+ `str2tuple`, `str2t` turn str to tuple
```python
str2tuple(str, separator)

str2tuple('1 and 2 and 3 and 4 and 5', ' and ')
>> (1, 2, 3, 4, 5)
```

+ `list2set`, `l2set` turn list to set
```python
list2set(list)

list2set([1, 1, 2, 2, 3, 3, 4, 4, 5, 5])
>> {1, 2, 3, 4, 5}
```

+ `tuple2set`, `t2set` turn tuple to set
```python
tuple2set(tuple)

tuple2set((1, 1, 2, 2, 3, 3, 4, 4, 5, 5))
>> {1, 2, 3, 4, 5}
```

+ `str2set` turn str to set
```python
str2set(str, separator)

str2set('1 and 1 and 2 and 2 and 3 and 3 and 4 and 4 and 5 and 5', ' and ')
>> {'1', '2', '3', '4', '5'}
```

+ `list_format` change format of the items in list
```python
list_format(list, format)

list_format([1, 2, 3, 4, 5], str)
>> ['1', '2', '3', '4', '5']
```

+ `hac_syntax` a syntax for special symbols
```python
hac_syntax(text)

hac_syntax('$quos;$quos;$quos;$quos;$quos;$n;$lsqubra;$rsqubra;')
>> ?????
>> []
```

_**All syntax**_
| hac syntax | symbol || hac syntax | symbol |
| --- | --- | --- | --- | --- |
|`$n;`|`\n`| |`$bslash;`|`\`|
|`$comma;`|`,`| |`$under;`|`_`|
|`$period;`|`.`| |`$pipe;`|`|`|
|`$bang;`|`!`| |`$tilde;`|`~`|
|`$quos;`|`?`| |`$backtick;`|`\``|
|`$colon;`|`:`| |`$at;`|`@`|
|`$semi;`|`;`| |`$hash;`|`#`|
|`$dash;`|`-`| |`$dollar;`|`$`|
|`$lparen;`|`(`| |`$per;`|`%`|
|`$rparen;`|`)`| |`$caret;`|`^`|
|`$lsqubra;`|`[`| |`$and;`|`&`|
|`$rsqubra;`|`]`| |`$aster;`|`*`|
|`$lbrace;`|`{`| |`$plus;`|`+`|
|`$rbrace;`|`}`| |`$min;`|`-`|
|`$lang;`|`<`| |`$mul;`|`×`|
|`$rang;`|`>`| |`$div;`|`÷`|
|`$apost;`|`'`| |`$equ;`|`=`|
|`$slash;`|`/`| | | |

+ `text`, `t` a formatter of text
```python
text(*values, hac_syntax, separator, start, end)

text(1,'$colon; one', _hac_syntax=True)
>> 1: one

text(1, ': one', start='^_^ ', end='.')
>> ^_^ 1: one.

```

### *Pause*

+ `sleep`, `pause`, `wait` pause script
```python
sleep(second)

sleep(0.5)

```

### *Mouse Position*

+ `get_mouse_x` get mouse x position
```python
get_mouse_x()
>> 674
```

+ `get_mouse_y` get mouse y position
```python
get_mouse_y()
>> 150
```

+ `get_mouse_position` get mouse position
```python
get_mouse_position()
>> (674, 150)
```

### *Terminal*

+ `console` execute command in console
```python
console(command)

console('echo Hello World!')
>> Hello World!
```

+ `clear`, `cls` clear console output
```python
clear(x) # x print after cleared

clear('cleared')
>> cleared
```

+ `set_console_title` set console title
```python
set_console_title(title)

set_console_title('Title')
```

### *Random*

+ `randint` get random integer from a to b (if only insert one argument, it will start from 0)python
```
randint(a, b)

randint(10)
>> 3

randint(5,10)
>> 7
```

+ `random` get random number from a to b (if only insert one argument, it will start from 0)python
```
random(a, b)

random(10)
>> 1.296316281186084

random(5,10)
>> 8.563297850355834
```

+ `choice` choose k items in population
```python
choice(population, k)

choice([1, 2, 3, 4, 5], 2)
>> [2, 4]
```

+ `shuffle` shuffle list
```python
shuffle(list)

shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
>> [7, 9, 8, 5, 4, 3, 1, 0, 6, 2]
```


### *Keyboard*

+ `is_pressed` check if the key is pressed
```python
is_pressed(key)

is_pressed('enter')
>> False
```

+ `is_release` check if the key is release
```python
is_release(key)

is_release('enter')
>> True
```

+ `send` send key
```python
send(key)

send('enter')
```

+ `waitkey` wait until key is pressed
```python
waitkey()

waitkey('enter')
```

### *File*

+ `fileget` get formatted contents of a file
```python
fileget(file_name, delimiter, comments, encoding)

fileget('README/test.csv', ',', '#', 'utf-8')
>> [['1', '2', '3', '4', '5'], ['6', '7', '8', '9', '0']]
```

**+ `glob` get all files/folders in the path**
```python
glob(pathname)

glob('.\*')
>> ['.\\hactool', '.\\LICENSE', '.\\MANIFEST.in',
    '.\\README', '.\\README.md', '.\\setup.py']
```

+ `exist` check if file/folder exist
```python
exist(path)

exist('README.md')
>> True
```

+ `is_file` check if the path is a file
```python
is_file(path)

is_file('README.md)
>> True
```

+ `is_folder`, `is_dir` check if the path is a folder
```python
is_folder(path)

is_folder('README.md')
>> False
```

+ `file_dialog` open a window to ask path
```python
file_dialog(mode, title, initialdir, filetypes)

**file_dialog('open file', 'open a file', '/', (('All files', '*.*'), ))**
```
_**All modes**_
| mode | function |
| --- | --- |
| 'open file' | open file |
| 'open files' | open multiple files |
| 'save file' | save file |
| 'save as file' | save as file |
| 'ask dir' | ask dir |

### *Print*

+ `table` list to table
```python
table(content, header, table_format, align, show_index)
>> ╒═════╤═════╤═════╤═════╕
   │  a  │  b  │  c  │  d  │
   ╞═════╪═════╪═════╪═════╡
   │  1  │  2  │  3  │  4  │
   ├─────┼─────┼─────┼─────┤
   │  5  │  6  │  7  │  8  │
   ╘═════╧═════╧═════╧═════╛

```

+ `type_animate` typing animation
```python
type_animate('ABCDEFG', 0.1)
>> ABCDEFG
```

### *Clipboard*

+ `copy` copy text to system clipboard
```python
copy(text)

copy('ABCDEFG')
```

### *Other*

+ `ka`  it can do nothing \\(@^0^@)/
```
ka()
```

+ `pick` generate a console pick menu
```python
pick(title, options, indicator, default_index,
    multi_select, min_select_count, options_map,
    multi_select_fg, multi_select_bg)

pick('choose your favorite thing', ['apple','banana','strawberry'])
```

+ `time_str` return a string time
```python
time_str(format)

time_str()
>> 2022/11/14 (Monday) 19:17:1

time_str('$Y $y $Mo $mo $D $d $H $h $m $s $yd $wd $i')
>> 2022 22 November Nov. 14 Monday 19 7 21 15 318 1 False
```

_**All formats**_
| format | mean |
|  ---   | --- |
|  `$Y`  | year (4 numbers) |
|  `$y`  | year (2 numbers) |
|  `$Mo` | month (English) |
|  `$mo` | month (abbreviations) |
|  `$mn` | month (number) |
|  `$D`  | date |
|  `$d`  | day |
|  `$H`  | 24 hour |
|  `$h`  | 12 hour |
|  `$m`  | minute |
|  `$s`  | second |
|  `$yd` | day of the year |
|  `$wd` | day of the week |
|  `$i`  | is daylight saving time |

+ `exit` exit script
```python
exit()

exit()
```

<hr>

## CLASS

+ `Now` a time class
    ```python
    now = Now()
    ```

    + `update` update time
    ```python
    update()

    now.update()
    ```

    + `get_time` get time by type
    ```python
    get_time(type)

    now.get_time('year')
    >> 2022
    ```
    _**All types**_
    | format | mean |
    |  ---   | --- |
    | 'year' | year |
    | 'mon' | month |
    | 'date' | date |
    | 'hour' | hour |
    | 'min' | minute |
    | 'sec' | second |
    | 'day' | day |
    | 'yday' | day of the year |
    | 'wday' | day of teh week |
    | 'isdst' | is daylight saving time |


    + `get_times` get time as a dict
    ```python
    get_times()

    now.get_times()
    >> {'year': 2022, 'month': 11, 'date': 14, 'hour': 20, 'min': 33,
        'sec': 44, 'day': 'Monday', 'yday': 318, 'isdst': False}
    ```

    + `time_str` return a string time
    ```python
    time_str(format)

    now.time_str()
    >> 2022/11/14 (Monday) 19:17:1

    now.time_str('$Y $y $Mo $mo $D $d $H $h $m $s $yd $wd $i')
    >> 2022 22 November Nov. 14 Monday 19 7 21 15 318 1 False
    ```

<br><br>

+ `Thread` run script in a different progress
    ```python
    thread = Thread(target)
    ```


    + `start` start execute target
    ```python
    start()

    thread.start()
    ```

    + `stop` stop execute target
    ```python
    stop()

    thread.stop()
    ```


<br><br>

+ `Syntax` make a syntax
    ```python
    Syntax(before, after)

    syntax = Syntax('1', 'one)
    ```

    + `trans` translate text
    ```python
    syntax.trans(text)

    syntax.trans('123')
    >> one23
    ```


<br><br><hr>

[Back to README](../README.md)