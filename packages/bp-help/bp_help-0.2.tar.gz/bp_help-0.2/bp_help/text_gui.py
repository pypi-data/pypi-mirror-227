
import re
import random
import os
import pickle
import datetime
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

from urllib.request import urlopen
import locale
locale.setlocale(locale.LC_ALL, '')  # Use '' for auto, or force e.g. to 'en_US.UTF-8'

progress = None

# from .controls import (topic_probs, praise, encouragement, score_multiplier, 
#                        course_week_nr, leaf_prob, course_start_week, score_goals)

from .controls import *


class Expression:
    pass

class NumberLiteral(Expression):
    def __init__(self, num):
        self.num = num

    def __str__(self):
        return str(self.num)

class Number(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)
    
class String(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

class List(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

class Dict(Expression):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return str(self.name)

class GetIndexExpression(Expression):
    def __init__(self, name, i):
        self.name = name
        self.i = i

    def __str__(self):
        return str(self.name) + '[' + str(self.i) + ']'

class NoArgMethodExpression(Expression):
    def __init__(self, name, method):
        self.name = name
        self.method = method

    def __str__(self):
        return str(self.name) + f'.{self.method}()'

class ArgMethodExpression(Expression):
    def __init__(self, name, method, arg):
        self.name = name
        self.method = method
        self.arg = arg

    def __str__(self):
        return str(self.name) + f'.{self.method}({self.arg})'

class GetValueKeyExpression(Expression):
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __str__(self):
        return str(self.name) + '[' + repr(self.key) + ']'

class GetVariableKeyExpression(Expression):
    def __init__(self, name, key):
        self.name = name
        self.key = key

    def __str__(self):
        return str(self.name) + '[' + self.key + ']'

class SliceFrontExpression(Expression):
    def __init__(self, name, i):
        self.name = name
        self.i = i

    def __str__(self):
        return str(self.name) + '[:' + str(self.i) + ']'    

class SliceExpression(Expression):
    def __init__(self, name, i, j):
        self.name = name
        self.i = i
        self.j = j

    def __str__(self):
        return str(self.name) + '[' + str(self.i) + ':' + str(self.j) + ']'    

class SliceBackExpression(Expression):
    def __init__(self, name, i):
        self.name = name
        self.i = i

    def __str__(self):
        return str(self.name) + '[' + str(self.i) + ':]'    

class BinaryExpression(Expression):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return str(self.left) + " " + self.op + " "  + str(self.right)

class NotExpression(Expression):
    def __init__(self, left):
        self.left = left

    def __str__(self):
        return "not " + str(self.left)

class ParenthesizedExpression(Expression):
    def __init__(self, exp):
        self.exp = exp

    def __str__(self):
        return "(" + str(self.exp) + ")"

class FunctionExpression(Expression):
    def __init__(self, exp, fun):
        self.exp = exp
        self.fun = fun

    def __str__(self):
        return self.fun + "(" + str(self.exp) + ")"
    

def find_variable_for_key(keys, variables):
    vars = []
    for var in variables:
        val = globals()[var]
        if val in keys:
            vars.append(var)
    if vars:
        return random.choice(vars)
    else:
        return None
    

def find_variable_for_index(indices, variables):
    vars = []
    for var in variables:
        val = globals()[var]
        if val in indices:
            vars.append(var)
    if vars:
        return random.choice(vars)
    else:
        return None    


def get_expression(prob, leaf_prob, topic_probs):
    return str(randomExpression(prob, leaf_prob, topic_probs))


def randomExpression(prob, leaf_prob, topic_probs):
    """To make sure all sub expressions are valid"""
    expr = _randomExpression(prob, leaf_prob, topic_probs)
    # TODO: find bugs instead of try/except hack...
    for x in range(100):
        try:
            eval(str(expr))
        except:
            expr = _randomExpression(prob, leaf_prob, topic_probs)
            continue
        break
    return expr


def _randomExpression(prob, leaf_prob, topic_probs):

    p = random.random()

    # if random.random() > prob:
    if leaf_prob > prob:
        # variable or number
        random.random()
        if topic_probs['types']['dicts'] > p:
            d = Dict(random.choice(dicts))
            keys = list(globals()[d.name].keys())
            variable_key = find_variable_for_key(keys, strings+numbers)
            if variable_key and random.random() > 0.3:
                return GetVariableKeyExpression(d.name, variable_key)            
            else:
                key = random.choice(keys)
                return GetValueKeyExpression(d.name, key)
        elif topic_probs['types']['lists'] > p:
            sl = Dict(random.choice(lists))
            i = random.randint(0,len(globals()[sl.name])-1)
            j = random.randint(i,len(globals()[sl.name])-1)
            variable_idx = find_variable_for_key([i], numbers)
            if variable_idx:
                i = variable_idx
            variable_idx = find_variable_for_key([j], numbers)
            if variable_idx:
                j = variable_idx
            # if random.random() > 0.7:
            #     method = random.choice(['split'])
            #     arg = random.choice(strings)
            #     return ArgMethodExpression(sl, method, arg)
            if random.random() > 0.7:
                # list indexing
                return GetIndexExpression(sl, i)
            elif random.random() > 0.5:
                # list slicing
                return SliceFrontExpression(sl, i)
            elif random.random() > 0.3:
                # list slicing
                return SliceBackExpression(sl, i)
            else:
                # list slicing
                return SliceExpression(sl, i, j)
        elif topic_probs['types']['strings'] > p:
            sl = Dict(random.choice(strings))
            i = random.randint(0,len(globals()[sl.name])-1)
            j = random.randint(i,len(globals()[sl.name])-1)
            variable_idx = find_variable_for_key([i], numbers)
            if variable_idx:
                i = variable_idx
            variable_idx = find_variable_for_key([j], numbers)
            if variable_idx:
                j = variable_idx
            if random.random() > 0.7:
                method = random.choice(['upper', 'isdigit', 'lower'])
                return NoArgMethodExpression(sl, method)
            if random.random() > 0.6:
                for _ in range(100):
                    arg = random.choice(lists)
                    if all([type(x) is str for x in arg]):
                        break
                method = random.choice(['join'])
                return ArgMethodExpression(sl, method, arg)
            elif random.random() > 0.3:
                # string indexing
                return GetIndexExpression(sl, i)
            elif random.random() > 0.2:
                # string slicing
                return SliceFrontExpression(sl, i)
            elif random.random() > 0.1:
                # string slicing
                return SliceBackExpression(sl, i)
            else:
                # string slicing
                return SliceExpression(sl, i, j)
        elif topic_probs['types']['number'] > p:
            return Number(random.choice(numbers))
        else:
            return NumberLiteral(random.randint(1, 3))
    else:
        left = randomExpression(prob / 1.2, leaf_prob, topic_probs)
        if type(left) is GetIndexExpression and type(eval(str(left))) is list:
            # nested list
            return GetIndexExpression(left, random.randint(0,len(eval(str(left)))-1))
        elif type(left) is GetValueKeyExpression and type(eval(str(left))) is dict:
            # nested dict
            keys = list(eval(str(left)).keys())
            variable_key = find_variable_for_key(keys, strings+numbers)
            if variable_key:
                return GetVariableKeyExpression(left, variable_key)            
            else:
                key = random.choice(keys)
                return GetValueKeyExpression(left, key)
        elif topic_probs['operations']['parentheses'] > p:
            # parentheses
            if type(left) is BinaryExpression:
                return ParenthesizedExpression(left)
            else:
                return left
        elif topic_probs['operations']['abs'] > p:
            # len function
            if type(eval(str(left))) in [int, float]:
                return FunctionExpression(left, 'abs')
            else:
                return left
        elif topic_probs['operations']['len'] > p:
            # len function
            if type(eval(str(left))) in [str, list, dict]:
                return FunctionExpression(left, 'len')
            else:
                return left
        elif topic_probs['operations']['sorted'] > p:
            # len function
            if type(eval(str(left))) in [list]:
                return FunctionExpression(left, 'sorted')
            else:
                return left                
        elif topic_probs['operations']['list'] > p:
            # len function
            if type(eval(str(left))) in [str]:
                return FunctionExpression(left, 'list')
            else:
                return left                
        elif topic_probs['operations']['not_op'] > p:
            # not
            if type(left) is not NotExpression:
                return NotExpression(left)
            else:
                return left
        elif topic_probs['operations']['logic_op'] > p:
            # logic operator
            right = randomExpression(prob / 1.2, leaf_prob, topic_probs)
            operators = ['>', '<', '>=', '<=', '==', '>', 'and', 'or']
            weights = [2, 2, 2, 2, 2, 2, 1, 1]
            for x in range(100):
                op = random.choices(operators, weights=weights)[0]
                expr = BinaryExpression(left, op, right)
                try:
                    eval(str(expr))
                except:
                    continue
                break
            return expr
        else:
            # arithmetic operator
            right = randomExpression(prob / 1.2, leaf_prob, topic_probs)
            operators = ["+", "-", "*", "/", "//", "%"]
            weights = [5, 5, 2, 2, 1, 1]
            for x in range(100):
                op = random.choices(operators, weights=weights)[0]
                expr = BinaryExpression(left, op, right)
                try:
                    eval(str(expr))
                except:
                    continue
                break
            return expr


#####################


exec(open(os.path.dirname(__file__) + '/steps.py').read())


from textual.app import App, ComposeResult, RenderResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Static
from textual.screen import Screen
from textual import events
from textual.widgets import RichLog, DataTable
from textual.message import Message

from rich.align import Align
from rich.text import Text
from rich.style import Style as RichStyle

from art import text2art

from pygments import highlight
from pygments.style import Style
from pygments.token import Token
from pygments.lexers import Python3Lexer
from pygments.formatters import Terminal256Formatter, BBCodeFormatter, HtmlFormatter

class MyStyle(Style):
        styles = {
            Token.String:     'ansigreen',
            Token.Number:     'ansiblue',
            Token.Keyword: 'ansired',
            Token.Literal: 'ansiyellow',
            Token.Operator: 'ansibrightblue',
            Token.Text: 'ansibrightred',
            Token.Token: 'ansibrightcyan',
            Token.Name: 'ansigray',
            Token.Other: 'ansicyan',
            Token.Generic: 'ansiblack'
        }

def highlight_code(code):
    s = highlight(code, Python3Lexer(), BBCodeFormatter(style=MyStyle))
    color = '#ffffff'
    s = re.sub(fr'\[color={color}\](\s+?)\[/color\]', r'\1', s)
    for color, repl in [('#007f00', 'red3'), ('#0000ff', 'black'), ('#7f0000', 'dark_magenta'), ('#00007f', 'dark_goldenrod')]:
        s = re.sub(fr'color={color}(\].*?\[/)color', fr'{repl}\1{repl}', s)
    return s

def sparkline_bars(data):
    BARS = u' ▁▂▃▄▅▆▇█'
    if sum(data) == 0:
        return ''
    
    from statistics import mean, variance
    from math import sqrt
    cv = sqrt(variance(data)) / mean(data)
    gold, silver, bronse = u'🥇', u'🥈', u'🥉'  
    if cv < 0.3:
        medal = gold
    elif cv < 0.4:
        medal = silver
    elif cv < 0.5:
        medal = bronse
    else:
        medal = ''

                #https://www.i2symbol.com/symbols/smileys
    # gold, silver, bronse = u'🥇', u'🥈', u'🥉'

    # data = [1, 2, 3, 4, 5, 6, 7]
#    data = [float(x) for x in data if x]
    data = [(len(BARS)-1)*n/max(data) for n in data]
    incr = min(data)
    width = (max(data) - min(data)) / (len(BARS) - 1)
    bins = [i*width+incr for i in range(len(BARS))]
    indexes = []
    for n in data:
        for i, thres in enumerate(bins):
            if thres <= n < thres+width:
                indexes.append(i)
                break
    sparkline = ''.join(BARS[i] for i in indexes) + medal
    return sparkline

def streak_stars(streak, emoji=''):

    if streak == 5:
        return u"|[bright_red]★★★★★★★[/bright_red]|🏆"
    elif streak == 4:
        return u"|[red]★★★★★★ [/red]|"
    elif streak == 4:
        return u"|★★★★   |"
    elif streak == 3:
        return u"|★★★    |"
    elif streak == 2:
        return u"|★★     |"
    elif streak == 1:
        return u"|★      |"



class KeyLogger(RichLog):

    class Updated(Message):
        """Update data table message."""
        
        def __init__(self):
            super().__init__()

    def __init__(self, markup=True):
        super().__init__(markup=markup)

    def on_mount(self):
        self.next_expression()

    def on_key(self, event: events.Key):
        if not self.is_correct and event.key.isdigit():
            line_num = int(event.key)
            if line_num <= len(self.steps_list):
                self.attempts += 1
                self.clear()
                self.focal = line_num
                self.write_steps()
        elif event.key == 'enter':
            self.next_expression()

    def key_up(self):
        if not self.is_correct and self.focal is not None and self.focal > 1:
            i = self.focal - 1
            self.steps_list[i], self.steps_list[i-1] = self.steps_list[i-1], self.steps_list[i]
            self.focal -= 1
            self.clear()
            self.write_steps()
            if self.is_correct_order():
                self.write(f'\nPress Enter to get next one or Ctrl-C to quit')

    def key_down(self):
        if not self.is_correct and self.focal is not None and self.focal <= len(self.steps_list):
            i = self.focal - 1
            self.steps_list[i], self.steps_list[i+1] = self.steps_list[i+1], self.steps_list[i]
            self.focal += 1
            self.clear()
            self.write_steps()
            if self.is_correct_order():
                self.write('\nPress Enter to get next one or Ctrl-C to quit')


    def is_correct_order(self):
        self.is_correct = all(x == y for x, y in zip(self.steps_list, self.correct_order))
        if self.is_correct:
            # update progress
            score = course_week_nr * len(self.steps_list)/(self.attempts+1)

            progress['scores'].append((score, datetime.datetime.now()))
            progress['current_score'] = sum(s for (s, t) in progress['scores'][-20:])/20 #* 0.9**(time.time() - progress['time'])/(60 * 60 * 24)
            progress['highscores'][course_week_nr] = max(progress['current_score'], progress['highscores'][course_week_nr])
            with open(pickle_file_name, 'wb') as pickle_file:
                pickle.dump(progress, pickle_file)

            self.write(f'CORRECT! You did it in {self.attempts} swaps and earned {int(score*score_multiplier)} points')

            self.post_message(self.Updated())

            # points_missing = goal_score - progress['current_score']  * 1000000
            # if points_missing > 0  and points_missing < 100000000:
            #     print('Almost there...')
            #     print('Earn', 'XX' 'to reach goal')

        return self.is_correct

    def write_steps(self):

        lst = []
        for (i, s) in enumerate(self.steps_list):
            if i+1 == self.focal:
                lst.append(f'[red][bold]{i+1:>2}[/bold][/red]   ' + highlight_code(s))
            else:
                lst.append(f'{i+1:>2}   ' + highlight_code(s))
        self.write(''.join(lst))

    def next_expression(self):
        self.clear()
        self.focal = None
        self.attempts = 0
        self.is_correct = False

        steps_list = []
        while len(steps_list) < min_steps or len(steps_list) > max_steps or any(len(x) > max_expr_len for x in steps_list):
            expr = get_expression(1, leaf_prob=leaf_prob, topic_probs=topic_probs) 
            try:
                steps_list = _steps(expr)
            except Exception as e:
                # TODO: make it more robust instead of catching exceptions...
                continue

        self.correct_order = steps_list[:]
        for _ in range(100):
            random.shuffle(steps_list)
            if not all(x == y for x, y in zip(steps_list, self.correct_order)):
                break
            
        self.steps_list = steps_list
        self.write_steps()


def format_score(score, current=False):
    if current:
        style = RichStyle(bold=True, blink=True)
        score = Text(str(score), style=style, justify='right')
    else:
        score = Text(str(score), justify='right')
    return score

def format_score_goal():
    score_goal = score_goals[course_week_nr]
    missing_points = int(score_goal - progress['current_score'] * score_multiplier)
    if missing_points < 0:
       return f"[bold]This week's score gloal: {score_goal:>10}[/bold]\n" f"[green]You are ahead by:        {-missing_points:>10}[/green]\n\n" f"[bold]{next(praise).upper()}![/bold]"
    else:
       return f"[bold]This week's score gloal: {score_goal:>10}[/bold]\n" f"[red]You still need to earn:  {missing_points:>10}[/red]\n\n" f"[bold]{next(encouragement).upper()}![/bold]"


def compute_streaks():
    working_days = defaultdict(list)
    for score, date in progress['scores']:
        weeknr = date.isocalendar().week - course_start_week + 1
        weeknr = max(1, weeknr)
        weekday = date.weekday()+1
        working_days[weeknr].append(weekday)

    for weeknr in working_days:
        working_days[weeknr] = sorted(list(set(working_days[weeknr])))

    def conseq(args):
        i, x = args
        return i - x
        
    streaks = defaultdict(int)
    for weeknr in range(1, 15):
        days = sorted(working_days[weeknr])
        streak = 0
        conseq_days = []
        for d, g in groupby(enumerate(days), conseq):
            conseq_days = list(map(itemgetter(1), g))
            if weeknr == course_week_nr:
                if datetime.date.today().weekday()+1 in conseq_days:
                    break
            elif 7 in conseq_days:
                break

        streak = len(conseq_days)
        streaks[weeknr] = streak

    return streaks

def compute_effort():
    problems_solved = defaultdict(list)
    for score, date in progress['scores']:
        weeknr = date.isocalendar().week - course_start_week + 1
        weeknr = max(1, weeknr)
        weekday = date.weekday()+1
        problems_solved[weeknr].append(weekday)

    effort = {}
    for weeknr in range(1, 15):
        effort[weeknr] = [problems_solved[weeknr].count(d) for d in range(1, 8)]

    return effort

class PlayerStats(DataTable):

    def on_mount(self):        

        streaks = compute_streaks()

        effort = compute_effort()

        #https://www.i2symbol.com/symbols/smileys

        rows = [("", "Stamina", "Streak", "High score"),]
        for weeknr in range(1, 15):

            score = int(progress['highscores'][weeknr] * score_multiplier)
            if weeknr > course_week_nr:
                score = ''

            if weeknr == course_week_nr:
                score = format_score(score, current=True)
            else:
                score = format_score(score)

            if weeknr <= course_week_nr:
                sparkline = sparkline_bars(effort[weeknr])
            else:
                sparkline = ''

            rows.append((weeknr,
                        sparkline,
                        streak_stars(streaks[weeknr]),
                        score
            ))

        header_style = RichStyle(color='bright_white', bold=False, blink=False)
        styled_header = [
            Text(str(cell), style=header_style, justify='left') for cell in rows[0]
        ]
        self.add_columns(*styled_header)
        self.add_rows(rows[1:])
        self.show_cursor = False
        self.zebra_stripes = True

# TODO: welcome screen with pep talk and status for reaching score goal, 
# appreaciation for getting back to the program if it has been a while
# encouragement, personal comments based on past streaks (you can do it again)


class STEPS(Screen):
    BINDINGS = [("h", "app.pop_screen", "Pop screen")]

    def compose(self) -> ComposeResult:
#        yield Header()
        with Container(id="header"):
            # text = text2art("STEP-TRAINER", font="tarty3")
            text = text2art("WAX ON - WAX OFF", font="tarty3")
            head = Align(f'{text}', align='center', vertical='middle')
            yield Static(head)
        with Container(id="app-grid"):
            with Vertical(id="left-pane"):
                # yield Header()
                yield KeyLogger()
            with Horizontal(id="top-right"):
                # yield Header(show_clock=True)
                self.player_stats = PlayerStats()
                yield self.player_stats
            with Horizontal(id="bottom-right"):
                # yield Header()
                s = format_score_goal()
                # s = Text(s, style=RichStyle(
                #     # color='bright_red',
                #     # bgcolor='yellow', 
                #     italic=False, 
                #     bold=True, 
                #     blink=False), 
                #     justify='left')
                self.message_panel = Static(s)
                yield self.message_panel

    # def on_color_button_selected(self):

    #     self.screen.styles.animate("background", message.color, duration=0.5)


class STEPSApp(App):
    CSS_PATH = "text_gui.css"
    dark = False
    SCREENS = {"steps": STEPS()}
    BINDINGS = [("escape", "push_screen('steps')", "STEPS")]

    def on_mount(self) -> None:        
        self.push_screen(self.SCREENS['steps'])
        # self.install_screen(STEPS(), name="steps")

    def on_key_logger_updated(self):
        score = int(progress['current_score']*score_multiplier)
#        assert 0, format_score(score, current=True)
        streaks = compute_streaks()
        effort = compute_effort()

        self.SCREENS['steps'].player_stats.update_cell_at((course_week_nr-1, 1), 
                                                          sparkline_bars(effort[course_week_nr]))

        self.SCREENS['steps'].player_stats.update_cell_at((course_week_nr-1, 2), 
                                                          streak_stars(streaks[course_week_nr]))
        self.SCREENS['steps'].player_stats.update_cell_at((course_week_nr-1, 3), 
                                                          format_score(score, current=True))

        f"gloal 22, score {progress['current_score']*score_multiplier}"

        self.SCREENS['steps'].message_panel.update(format_score_goal())




# def get_course_week_nr():
#     course_week_nr = datetime.date.today().isocalendar().week - course_start_week + 1    
#     course_week_nr = max(1, course_week_nr)
#     return course_week_nr

def run():

    global course_week_nr, progress, pickle_file_name, score_goals
    # course_week_nr = get_course_week_nr()

    pickle_file_name = os.path.dirname(__file__) + '/progress.pkl'
    if os.path.exists(pickle_file_name):
        with open(pickle_file_name, 'rb') as pickle_file:
            progress = pickle.load(pickle_file)
    else:
        progress = {'scores': [], 'current_score': 0,
                    'highscores': dict([(w, 0) for w in range(1, 15)])}

    app = STEPSApp()
    app.run()


if __name__ == "__main__":
    app = STEPSApp()
    app.run()
