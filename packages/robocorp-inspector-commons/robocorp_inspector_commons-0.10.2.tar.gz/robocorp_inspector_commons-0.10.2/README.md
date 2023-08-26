# Robocorp Inspector Commons

Robocorp Inspector Commons is the commons package for Robocorp Inspector.

## Dependencies

You might need to create a `.npmrc` file at project level with contents similar to the following, but with your own `authToken`.
This is needed for private repositories.

```
registry=https://registry.npmjs.org/
@robocorp:registry=https://npm.pkg.github.com/
//npm.pkg.github.com/:_authToken=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

## Development

The project uses `invoke` for overall project management, `poetry` for
python dependencies and environments, and `npm` for Javascript dependencies
and building.

Both `invoke` and `poetry` should be installed via pip: `pip install poetry invoke`

- To see all possible tasks: `invoke --list`

All source code is hosted on [GitHub](https://github.com/robocorp/inspector-commons/).

## Usage

Robocorp Inspector Commons is distributed as a Python package with all browser overlay
components compiled and included statically.

### Link to Automation Studio and running with Automation Studio

1. Terminal 1:
   1. ***Automation Studio***: run `invoke build-dev`
   2. ***Inspector-commons***: run `invoke linkas`
   3. ***Inspector-commons***: run `invoke watch`
2. Terminal 2:
   1. ***Automation Studio/robotd***: run `invoke start`
3. Terminal 3:
   1. ***Automation Studio***: run `invoke start --port=<PORT robotd started in>`

---

<p align="center">
  <img height="100" src="https://cdn.robocorp.com/brand/Logo/Dark%20logo%20transparent%20with%20buffer%20space/Dark%20logo%20transparent%20with%20buffer%20space.svg">
</p>
