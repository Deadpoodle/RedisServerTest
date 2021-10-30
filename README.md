# NS1 Take Home Test - Joe Fahey

## Overview
In a language of your choice, using only its stdlib, create an in-memory key-value store that supports Redis wire protocol’s GET, DEL and SET. Both keys and values may be of any primitive type.

## Success Metrics
While running your solution, the following commands respond as such, where redis-cli is the official Redis CLI binary that is included with Redis:
* $ <start solution>
* $ redis-cli set x 1
    > OK
* $ redis-cli get x
     > “1”
* $ redis-cli del x
    > (integer) 1
* $ redis-cli get x
    > (nil)

OS resources do not leak under sustained use (specifically memory and file descriptors)
Unsupported commands receive a response indicating they are not supported
Multiple clients can simultaneously access the application, potentially the same key


## Notes
* The makefile provides some useful targets, see them with: `make help`
* Dependencies for testing are managed with [Pipenv](https://realpython.com/pipenv-guide/): `pip install pipenv`
* Precommit hooks are used to maintain code quality at time of commit
    * See [here](https://pre-commit.com/hooks.html) for an explanation of what each hook does.
    * They can be installed with `make setup_precommit`
* Before running tests, enter Pipenv shell with: `pipenv shell`
* Sync dependencies using: `make install`
* To run tests: `make unit_test`

### TODO
* Multi-user concurrency
* If passed from cli, ints come in as strings, will this always be the case?
    * Likely not, need to make sure the string split still works in this case
* Unit tests
