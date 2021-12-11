# NS1 Take Home Test

## Overview
In a language of your choice, using only its stdlib, create an in-memory key-value store that supports Redis wire protocol’s GET, DEL and SET. Both keys and values may be of any primitive type.

## Success Metrics
While running your solution, the following commands respond as such, where redis-cli is the official Redis CLI binary that is included with Redis:
* $ \<start solution\>
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
* Before running tests, enter Pipenv shell with: `pipenv shell`
* Precommit hooks are used to maintain code quality at time of commit
    * See [here](https://pre-commit.com/hooks.html) for an explanation of what each hook does.
    * They can be installed with `make setup_precommit`
* Dependencies are synced with `make install`
* To run tests: `make unit_test`
