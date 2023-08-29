# Usage


## FUNCTIONS

### *Format*

+ `toString` convert argument to str
> ```python
> toString(input, separator)
> ```

```python
toString([1, 2, 3, 4, 5], ' and ')
```
```
>> 1 and 2 and 3 and 4 and 5
```

+ `toList`convert argument to list
> ```python
> toList(input, separator)
> ```

```python
toList('1 and 2 and 3 and 4 and 5', ' and ')
```
```
>> [1, 2, 3, 4, 5]
```

+ `toTuple` convert argument to tuple
> ```python
> toTuple(input, separator)
> ```

```python
toTuple('1 and 2 and 3 and 4 and 5', ' and ')
```
```
>> (1, 2, 3, 4, 5)
```

+ `toSet` convert argument to set
> ```python
> toSet(input, separator)
> ```

```python
toSet([1, 1, 2, 2, 3, 3, 4, 4, 5, 5])
```
```
>> {1, 2, 3, 4, 5}
```
<br>

```python
toSet("1, 1, 2, 2, 3, 3, 4, 4, 5, 5", ", ")
```

```
>> {1, 2, 3, 4, 5}
```

+ `list_format` change format of the items in list
> ```python
> list_format(list, format)
> ```

```python
list_format([1, 2, 3, 4, 5], str)
```
```
>> ['1', '2', '3', '4', '5']
```

+ `hac_syntax` a syntax for special symbols
> ```python
> hac_syntax(text)
> ```

```python
hac_syntax('$quos;$quos;$quos;$quos;$quos;$n;$lsqubra;$rsqubra;')
```
```
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
> ```python
> text(*values, hac_syntax, separator, start, end)
> ```

```python
text(1,'$colon; one', _hac_syntax=True)
```
```
>> 1: one
```
<br>

```python
text(1, ': one', start='^_^ ', end='.')
```
```
>> ^_^ 1: one.
```

### *Pause*

+ `sleep`, `pause`, `wait` pause script
> ```python
> sleep(second)
> ```

```python
sleep(0.5)
```

### *Mouse Position*

+ `get_mouse_x` get mouse x position
> ```python
> get_mouse_x()
> ```

```python
get_mouse_x()
```
```
>> 670
```

+ `get_mouse_y` get mouse y position
> ```python
> get_mouse_y()
> ```

```python
get_mouse_y()
```
```
>> 150
```

+ `get_mouse_position` get mouse position
> ```python
> get_mouse_position()
> ```

```python
get_mouse_position()
```
```
>> (670, 150)
```

### *Terminal*

+ `console` execute command in console
> ```python
> console(command)
> ```

```python
console('echo Hello World!')
```
```
>> Hello World!
```

+ `clear`, `cls` clear console output
> ```python
> clear(x) # print x after cleared
> ```

```python
clear('cleared')
```
```
>> cleared
```

+ `set_console_title` set console title
> ```python
> set_console_title(title)
> ```

```python
set_console_title('Title')
```

+ `input_password` get input that is invisible
> ```python
> input_password(prompt)
> ```

```python
input_password("input password: ")
```

```
>> input password: |
```

+ `terminal_size` get terminal size
> ```python
> terminal_size()
> ```

```python
terminal_size()
```

```
>> (120, 30)
```

### *Random*

+ `randint` get random integer from a to b (if only insert one argument, it will start from 0)python
> ```
> randint(a, b)

```python
randint(10)
```

```
>> 3
```
<br>

```python
randint(5,10)
```

```
>> 7
```

+ `random` get random number from a to b (if only insert one argument, it will start from 0)python
```
random(a, b)
```

```python
random(10)
```
```
>> 1.296316281186084
```
<br>

```python
random(5,10)
```

```
>> 8.563297850355834
```

+ `choice` choose k items in population
> ```python
> choice(population, k)
> ```

```python
choice([1, 2, 3, 4, 5], 2)
```
```
>> [2, 4]
```

+ `shuffle` shuffle list
> ```python
> shuffle(list)
> ```

```python
shuffle([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
```
```
>> [7, 9, 8, 5, 4, 3, 1, 0, 6, 2]
```


### *Keyboard*

+ `is_pressed` check if the key is pressed
> ```python
> is_pressed(key)
> ```

```python
is_pressed('enter')
```
```
>> False
```

+ `is_release` check if the key is release
> ```python
> is_release(key)
> ```

```python
is_release('enter')
```
```
>> True
```

+ `press_and_released` if the key is pressed, wait until it released
> ```python
> press_and_released(key)
> ```

```python
press_and_released('enter')
```
```
>> True
```

+ `send` send key
> ```python
> send(key)
> ```

```python
send('enter')
```

+ `waitkey` wait until key is pressed
> ```python
> waitkey()
> ```

```python
waitkey('enter')
```

+ `add_hotkey` add a hotkey
> ```python
> add_hotkey(hotkey, function)
> ```

```python
add_hotkey("win+c", lambda: print("win+c pressed"))
```

### *Browser*
+ `open_url` open a link in browser
> ```python
> open_url(url)
> ```

```python
open_url("https://pypi.org/")
```


### *File*

+ `txtget` get contents of a txt file
> ```python
> txtget(file_name, encoding)
> ```

```python
txtget('docx/test.txt', 'utf-8')
```
```
>> Hello world
   this is the second line

   this ise the forth line
```

+ `csvget` get formatted contents of a csv file
> ```python
> csvget(file_name, delimiter, comments, encoding)
> ```

```python
csvget('docx/test.csv', ',', '#', 'utf-8')
```
```
>> [['1', '2', '3', '4', '5'], ['6', '7', '8', '9', '0']]
```

+ `jsonget` get formatted contents of a json file
> ```python
> jsonget(file_name, encoding)
> ```

```python
jsonget('docx/test.json', 'utf-8')
```
```
>> {'name': 'hactool', 'birthday': '20220420'}
```

**+ `glob` get all files/folders in the path**
> ```python
> glob(pathname)
> ```

```python
glob('.\*')
```
```
>> ['.\\hactool', '.\\LICENSE', '.\\MANIFEST.in',
    '.\\README', '.\\README.md', '.\\setup.py']
```

+ `exist` check if file/folder exist
> ```python
> exist(path)
> ```

```python
exist('README.md')
```
```
>> True
```

+ `is_file` check if the path is a file
> ```python
> is_file(path)
> ```

```python
is_file('README.md')
```
```
>> True
```

+ `is_folder`, `is_dir` check if the path is a folder
> ```python
> is_folder(path)
> ```

```python
is_folder('README.md')
```
```
>> False
```

+ `file_dialog` open a window to ask path
> ```python
> file_dialog(mode, title, initialdir, filetypes)
> ```

```python
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
> ```python
> table(content, header, table_format, align, show_index)
> ```

```python
table([[1, 2, 3, 4], [5, 6, 7, 8]], ["a", "b", "c", "d"])
```


```
>> ╒═════╤═════╤═════╤═════╕
   │  a  │  b  │  c  │  d  │
   ╞═════╪═════╪═════╪═════╡
   │  1  │  2  │  3  │  4  │
   ├─────┼─────┼─────┼─────┤
   │  5  │  6  │  7  │  8  │
   ╘═════╧═════╧═════╧═════╛
```

+ `type_animate` typing animation
> ```python
> type_animate(text, sep)
> ```

```python
type_animate('ABCDEFG', 0.1)
```

```
>> ABCDEFG
```

### *Clipboard*

+ `copy` copy text to system clipboard
> ```python
> copy(text)
> ```

```python
copy('ABCDEFG')
```

### *Other*

+ `ka`  it can do nothing \\(@^0^@)/
```
ka()
```

+ `pick` generate a console pick menu
> ```python
> pick(title, options, indicator, default_index,
>   multi_select, min_select_count, options_map,
>   multi_select_fg, multi_select_bg)
> ```

```python
pick('choose your favorite thing', ['apple','banana','strawberry'])
```

+ `time_str` return a string time
> ```python
> time_str(format)
> ```

```python
time_str()
```
```
>> 2022/11/14 (Monday) 19:17:1

time_str('$Y $y $Mo $mo $D $d $H $h $m $s $yd $wd $i')
```
```
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
> ```python
> exit(x) # print x before exit
> ```

```python
exit("script ended")
```
```
>> script ended
```

+ `just_try` just try a function without deal with an exception
> ```python
> just_try(function)
> ```

```python
just_try(lambda: print("hello"))
```
```
>> hello
```

+ `apply` apply multiple functions to object
> ```python
> apply(object, *functions)
> ```

```python
apply(12345, str, lambda x: x[:4], list)
```
```
>> ['1', '2', '3', '4']
```

<hr>

## CLASS

+ `Now` a time class
    > ```python
    > now = Now()
    > ```
    

    + `update` update time
    > ```python
    > update()
    > ```
    
    ```python
    now.update()
    ```

    + `get_time` get time by type
    > ```python
    > get_time(type)
    > ```
    
    ```python
    now.get_time('year')
    ```
    ```
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
    > ```python
    > get_times()
    > ```
    
    ```python
    now.get_times()
    ```
    ```
    >> {'year': 2022, 'month': 11, 'date': 14, 'hour': 20, 'min': 33,
        'sec': 44, 'day': 'Monday', 'yday': 318, 'isdst': False}
    ```

    + `time_str` return a string time
    > ```python
    > time_str(format)
    > ```
    
    ```python
    now.time_str()
    ```
    ```
    >> 2022/11/14 (Monday) 19:17:1

    now.time_str('$Y $y $Mo $mo $D $d $H $h $m $s $yd $wd $i')
    ```
    ```
    >> 2022 22 November Nov. 14 Monday 19 7 21 15 318 1 False
    ```

<br><br>

+ `Thread` run script in a different progress
    > ```python
    > thread = Thread(target)
    > ```
    
    ```python    ```


    + `start` start execute target
    > ```python
    > start()
    > ```
    
    ```python
    thread.start()
    ```

    + `stop` stop execute target
    > ```python
    > stop()
    > ```
    
    ```python
    thread.stop()
    ```


<br><br>

+ `Syntax` make a syntax
    > ```python
    > Syntax(before, after)
    > ```
    
    ```python
    syntax = Syntax('1', 'one')
    ```

    + `trans` translate text
    > ```python
    > syntax.trans(text)
    > ```
    
    ```python
    syntax.trans('123')
    ```
    ```
    >> one23
    ```


<br><br><hr>

[Back to README](../README.md)