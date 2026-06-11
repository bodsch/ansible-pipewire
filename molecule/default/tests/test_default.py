# coding: utf-8
from __future__ import unicode_literals

import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('instance')


@pytest.mark.parametrize("package", [
    "pipewire",
    "wireplumber",
])
def test_packages(host, package):
    assert host.package(package).is_installed


@pytest.mark.parametrize("config_file", [
    "/etc/pipewire/pipewire.conf.d/10-pipewire.conf",
])
def test_global_config(host, config_file):
    f = host.file(config_file)
    assert f.exists
    assert f.is_file
    assert "default.clock.rate" in f.content_string


def test_pw_config_parses(host):
    """
    pw-config parses the merged configuration; a malformed drop-in makes it fail.
    Not every distribution ships the pw-config helper, so skip when absent.
    """
    if not host.exists("pw-config"):
        pytest.skip("pw-config is not available on this distribution")
    cmd = host.run("pw-config")
    assert cmd.rc == 0
