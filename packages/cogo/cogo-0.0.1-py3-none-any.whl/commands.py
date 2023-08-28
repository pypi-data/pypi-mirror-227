import toml
import os
from pprint import pprint
import shutil


def find(lst, pred):
    for x in lst:
        if pred(x):
            return x
    return None


def load_config_raw():
    repo_path = get_repo_path()
    current_host = get_current_host()

    print(current_host + " @ " + repo_path + "\n")

    # with open(os.path.join(repo_path, "config.toml"), "rb") as f:
    #     print(f.read())
    #     config = toml.loads(f.read())
    config = toml.load(os.path.join(repo_path, "config.toml"))

    return config, current_host


def load_host_config():
    config, current_host = load_config_raw()

    assert (
        config["config_version"] == 1
    ), "Only config version 1 is supported, but got " + str(config["config_version"])

    h = find(config["machines"], lambda x: x["hostname"] == current_host)
    assert h is not None, f"Host '{current_host}' not found in config"

    return h


def get_repo_path():
    return os.environ["COGO_REPO"].strip()


def get_files_path():
    return os.path.join(get_repo_path(), "files")


def get_current_host():
    return os.environ["COGO_HOST"].strip()


def iter_files(host_config):
    for f in host_config["files"]:
        yield f["repo"], f["dest"]


def mkdir_if_needed(path):
    if not os.path.exists(path):
        os.makedirs(path)


def config(ns):
    config = load_config_raw()
    pprint(config)


def collect(ns):
    config = load_host_config()

    if ns.dry_run:
        print("dry run")

    files_path = get_files_path()
    mkdir_if_needed(files_path)

    for repo, dest in iter_files(config):
        repo = os.path.join(files_path, repo)
        print(f"  copy {dest} -> {repo}")
        if ns.dry_run:
            continue

        mkdir_if_needed(os.path.dirname(repo))
        shutil.copyfile(dest, repo)


def distribute(ns):
    config = load_host_config()

    if ns.dry_run:
        print("dry run")

    files_path = get_files_path()

    for repo, dest in iter_files(config):
        repo = os.path.join(files_path, repo)
        print(f"  copy {repo} -> {dest}")
        if ns.dry_run:
            continue

        mkdir_if_needed(os.path.dirname(dest))
        shutil.copyfile(repo, dest)
