import curses
import pick

def main(stdscr):
    stdscr.addstr("hello world?\n")
    stdscr.get_wch()

    y, x = stdscr.getyx()
    
    title = "Please choose your favorite programming language: "
    options = ["Java", "JavaScript", "Python", "PHP", "C++", "Erlang", "Haskell"]
    option, index = pick.pick(
        options,
        title,
        indicator="=>",
        default_index=2,
        screen=stdscr,
        position=pick.Position(y=y, x=0)  # comment this to demonstrate the issue it solves
    )

    stdscr.addstr(f"\nYou choosed {option} at index {index}\n")
    stdscr.get_wch()

curses.wrapper(main)
