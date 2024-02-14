import sys
import subprocess
import os

def get_base_prefix_compat():
    """Get base/real prefix, or sys.prefix if there is none."""
    return (
        getattr(sys, "base_prefix", None)
        or getattr(sys, "real_prefix", None)
        or sys.prefix
    )

def in_virtualenv():
    return sys.prefix != get_base_prefix_compat()

def activate(env_name, python_ver):
    if not in_virtualenv():
        subprocess.run(". ./" + env_name + "/bin/activate", shell = True)
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),
                            env_name,
                            "lib",
                            python_ver,
                            "site-packages")))


