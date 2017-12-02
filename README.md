# Macronaut
Macronaut is simple macro creator for simplification repetitive tasks.


### Installation:

  ```
  sudo ./install.sh
  ```
  
### Help:
  ```
  Usage:
    macronaut record <name>
    macronaut compile <name> [--speed=<num>]
    macronaut play <name> [--speed=<num>] [--repeat=<num>]
    macronaut delete <name>
    macronaut (ls | list)
    macronaut (-h | --help)
    macronaut (-v | --version)
  
  Options:
    -h --help           Show this screen.
    -v --version        Show version.
    -s --speed=<num>    Speed in float number [default: 1].
    -r --repeat=<num>   Number of repeating [default: 1].
    -d --delay=<sec>    Delay time in seconds before run macro [default: 0].
  ```


### Examples:
   ```
   $ macronaut record macro1
   $ macronaut play macro1
   ```

### Special thanks:

 - [xdotool](http://www.semicomplete.com/projects/xdotool/): Tool lets you simulate keyboard input and mouse activity.
 - [Pynput](https://github.com/moses-palmer/pynput): Library for control and monitor input devices.
 - [docopt](http://docopt.org/): Awesome argument parser for beautiful command line interface.



### Authors:

 - Martin Jablečník


