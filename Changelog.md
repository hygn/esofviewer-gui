# changelog

## v0.1a

* GUI wrap
* download

## v0.2b

* scheduled learning
* threading

## v0.3b

* UI improvement
* auto scheduling

## v0.4b

* Auto login by using browser_cookie3
* add warning diagram

## v0.5b

* critical threading bug fix
  * bug: thread doesn't automatically closed when parent is closed
  * solution: change threading module to multiprocessing, add proper close button, when unexpected close detected automatically close all threads
* brought back cookie login option. login method can be selected to cookie or browser_cookie3