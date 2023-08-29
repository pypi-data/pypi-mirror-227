#-*-coding:utf-8-*-

import curses

__all__ = ['Picker','pick']


KEYS_ENTER = (curses.KEY_ENTER,ord('\n'),ord('\r'))
KEYS_UP = (curses.KEY_UP,ord('k'))
KEYS_DOWN = (curses.KEY_DOWN,ord('j'))
KEYS_SELECT = (curses.KEY_RIGHT,ord(' '))

MULTI_SELECT_COLOR_PAIR_NUMBER = 1
COLORS = {
    'COLOR_BLACK': curses.COLOR_BLACK,
    'COLOR_BLUE': curses.COLOR_BLUE,
    'COLOR_CYAN': curses.COLOR_CYAN,
    'COLOR_GREEN': curses.COLOR_GREEN,
    'COLOR_MAGENTA': curses.COLOR_MAGENTA,
    'COLOR_RED': curses.COLOR_RED,
    'COLOR_WHITE': curses.COLOR_WHITE,
    'COLOR_YELLOW': curses.COLOR_YELLOW
}

class Picker(object):

    def __init__(self,
        options,title=None,indicator='*',
        default_index=0,multi_select=False,
        min_selection_count=0,
        options_map=None,
        multi_select_foreground_color='COLOR_GREEN',
        multi_select_background_color='COLOR_WHITE',
        pre_select=[]):

        if len(options) == 0: raise ValueError('options should not be an empty list')


        self.options,self.title,self.indicator,self.multi_select,self.min_selection_count,self.options_map,self.all_selected = \
        options,title,indicator,multi_select,min_selection_count,options_map,pre_select


        if default_index >= len(options): raise ValueError('default_index should be less than the length of options')
        if (multi_select)and(min_selection_count > len(options)): raise ValueError('min_selection_count is bigger than the available options,you will not be able to make any selection')
        if (options_map is not None)and(not callable(options_map)): raise ValueError('options_map must be a callable function')
        if (multi_select_foreground_color)and(multi_select_foreground_color not in COLORS): raise ValueError('multi_select_foreground_color must be one of: [\'{0}\']'.format('\',\''.join(list(COLORS))))
        if (multi_select_background_color)and(multi_select_background_color not in COLORS): raise ValueError('multi_select_background_color must be one of: [\'{0}\']'.format('\',\''.join(list(COLORS))))

        self.multi_select_foreground_color,self.multi_select_background_color,self.index,self.custom_handlers = \
        COLORS[multi_select_foreground_color],COLORS[multi_select_background_color],default_index,{}

    def register_custom_handler(self,key,func): self.custom_handlers[key] = func

    def move_up(self):
        self.index -= 1
        if self.index < 0: self.index = len(self.options) - 1

    def move_down(self):
        self.index += 1
        if self.index >= len(self.options): self.index = 0

    def mark_index(self):
        if self.multi_select:
            if self.index in self.all_selected: self.all_selected.remove(self.index)
            else: self.all_selected.append(self.index)

    def get_selected(self):
        if self.multi_select:
            return_tuples = []
            for selected in self.all_selected: return_tuples.append((self.options[selected],selected))
            return return_tuples
        else: return self.options[self.index],self.index

    def get_title_lines(self):
        if self.title: return self.title.split('\n') + ['']
        return []

    def get_option_lines(self):
        lines = []
        for index,option in enumerate(self.options):
            if self.options_map: option = self.options_map(option)

            if index == self.index: prefix = self.indicator
            else: prefix = len(self.indicator) * ' '

            if (self.multi_select)and(index in self.all_selected):
                _format = curses.color_pair(MULTI_SELECT_COLOR_PAIR_NUMBER)
                line = ('{0} {1}'.format(prefix,option),_format)
            else: line = '{0} {1}'.format(prefix,option)
            lines.append(line)

        return lines

    def get_lines(self):
        title_lines = self.get_title_lines()
        option_lines = self.get_option_lines()
        lines = title_lines + option_lines
        current_line = self.index + len(title_lines) + 1
        return lines,current_line

    def draw(self):
        self.screen.clear()

        x,y = 1,1
        max_y,max_x = self.screen.getmaxyx()
        max_rows = max_y - y

        lines,current_line = self.get_lines()

        scroll_top = getattr(self,'scroll_top',0)
        if current_line <= scroll_top: scroll_top = 0
        elif current_line - scroll_top > max_rows: scroll_top = current_line - max_rows
        self.scroll_top = scroll_top

        lines_to_draw = lines[scroll_top:scroll_top+max_rows]

        for line in lines_to_draw:
            if type(line) is tuple: self.screen.addnstr(y,x,line[0],max_x-2,line[1])
            else: self.screen.addnstr(y,x,line,max_x-2)
            y += 1

        self.screen.refresh()

    def run_loop(self):
        while True:
            self.draw()
            c = self.screen.getch()
            if c in KEYS_UP: self.move_up()
            elif c in KEYS_DOWN: self.move_down()
            elif c in KEYS_ENTER:
                if (self.multi_select)and(len(self.all_selected) < self.min_selection_count): continue
                return self.get_selected()
            elif (c in KEYS_SELECT)and(self.multi_select): self.mark_index()
            elif c in self.custom_handlers:
                ret = self.custom_handlers[c](self)
                if ret: return ret

    def config_curses(self):
        curses.use_default_colors()
        curses.curs_set(0)
        curses.init_pair(MULTI_SELECT_COLOR_PAIR_NUMBER,self.multi_select_foreground_color,self.multi_select_background_color)

    def _start(self,screen):
        self.screen = screen
        self.config_curses()
        return self.run_loop()

    def start(self):
        return curses.wrapper(self._start)


def pick(
    options,title=None,indicator='*',default_index=0,
    multi_select=False,
    min_selection_count=0,
    options_map=None,
    multi_select_foreground_color='COLOR_GREEN',
    multi_select_background_color='COLOR_WHITE'
    ):

    picker = Picker(
        options,title,indicator,default_index,
        multi_select,
        min_selection_count,
        options_map,
        multi_select_foreground_color,
        multi_select_background_color
    )
    return picker.start()
