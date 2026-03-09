
<div align="center">
    <img src="docs/assets/banner.png" height=150 alt="banner"/>

-----
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/data-centric-ai/dcbench/CI)
![GitHub](https://img.shields.io/github/license/data-centric-ai/dcbench)
[![Documentation Status](https://readthedocs.org/projects/dcbench/badge/?version=latest)](https://dcbench.readthedocs.io/en/latest/?badge=latest)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dcbench)](https://pypi.org/project/dcbench/)
[![codecov](https://codecov.io/gh/data-centric-ai/dcbench/branch/main/graph/badge.svg?token=MOLQYUSYQU)](https://codecov.io/gh/data-centric-ai/dcbench)

A benchmark of data-centric tasks from across the machine learning lifecycle.

[**Getting Started**](#%EF%B8%8F-quickstart)
| [**What is dcbench?**](#-what-is-dcbench)
| [**Docs**](https://dcbench.readthedocs.io/en/latest/index.html)
| [**Contributing**](CONTRIBUTING.md)
| [**Website**](https://www.datacentricai.cc/)
| [**About**](#%EF%B8%8F-about)
</div>


## ⚡️ Quickstart

```bash
pip install dcbench
```
> Optional: some parts of Meerkat rely on optional dependencies. If you know which optional dependencies you'd like to install, you can do so using something like `pip install dcbench[dev]` instead. See setup.py for a full list of optional dependencies.

> Installing from dev: `pip install "dcbench[dev] @ git+https://github.com/data-centric-ai/dcbench@main"`

Using a Jupyter notebook or some other interactive environment, you can import the library 
and explore the data-centric problems in the benchmark:

```python
import dcbench
dcbench.tasks
```
To learn more, follow the [walkthrough](https://dcbench.readthedocs.io/en/latest/intro.html#api-walkthrough) in the docs. 

## Install from local

```bash
conda create -n dcbench python=3.10 -y
conda activate dcbench
pip install -e .
```

### Configuring with YAML
To change the configuration, you can create a YAML file. For example, to set up a local data directory named `.dcbench` in the current repository:

1. **Create the configuration file:**
   ```bash
   cat <<EOF > dcbench-config.yaml
   local_dir: ./.dcbench
   public_bucket_name: dcbench
   hidden_bucket_name: dcbench-hidden
   celeba_dir: ./.dcbench/datasets/celeba
   imagenet_dir: ./.dcbench/datasets/imagenet
   EOF
   ```

2. **Set the environment variable `DCBENCH_CONFIG` to point to the file:**
   ```bash
   export DCBENCH_CONFIG="$(pwd)/dcbench-config.yaml"
   ```

If you’re using conda, you can permanently set this variable for your environment:
```bash
conda env config vars set DCBENCH_CONFIG="$(pwd)/dcbench-config.yaml"
conda activate dcbench
```

### Linking ImageNet from SDBench
If ImageNet is already managed by SDBench (located in `data/base_dataset/imagenet`), you can link it to `dcbench` to avoid re-downloading. **Execute these commands from the `dcbench/` root directory:**

1. **Ensure the `.dcbench` directory exists:**
   ```bash
   mkdir -p .dcbench/datasets
   ```

2. **Create a symbolic link to the SDBench ImageNet directory:**
   ```bash
   # From the dcbench/ directory:
   ln -s ../../../data/base_dataset/imagenet .dcbench/datasets/imagenet
   ```

3. **Verify the configuration in `dcbench-config.yaml`:**
   Ensure `imagenet_dir` points to the relative path:
   ```yaml
   imagenet_dir: ./.dcbench/datasets/imagenet
   ```

### Unlinking ImageNet
To remove the link (this will not delete the original data in SDBench):
```bash
rm .dcbench/datasets/imagenet
```


## 💡 What is dcbench?
This benchmark evaluates the steps in your machine learning workflow beyond model training and tuning. This includes feature cleaning, slice discovery, and coreset selection. We call these “data-centric” tasks because they're focused on exploring and manipulating data – not training models. ``dcbench`` supports a growing list of them:

* [Minimal Data Selection](https://dcbench.readthedocs.io/en/latest/tasks.html#minimal-data-selection)
* [Slice Discovery](https://dcbench.readthedocs.io/en/latest/tasks.html#slice-discovery)
* [Minimal Feature Cleaning](https://dcbench.readthedocs.io/en/latest/tasks.html#minimal-feature-cleaning)


``dcbench`` includes tasks that look very different from one another: the inputs and
outputs of the slice discovery task are not the same as those of the
minimal data cleaning task. However, we think it important that
researchers and practitioners be able to run evaluations on data-centric
tasks across the ML lifecycle without having to learn a bunch of
different APIs or rewrite evaluation scripts.

So, ``dcbench`` is designed to be a common home for these diverse, but
related, tasks. In ``dcbench`` all of these tasks are structured in a
similar manner and they are supported by a common Python API that makes
it easy to download data, run evaluations, and compare methods.


## ✉️ About
`dcbench` is being developed alongside the data-centric-ai benchmark. Reach out to Bojan Karlaš (karlasb [at] inf [dot] ethz [dot] ch) and Sabri Eyuboglu (eyuboglu [at] stanford [dot] edu if you would like to get involved or contribute!)
