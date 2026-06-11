# coding: utf-8
from __future__ import unicode_literals

import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('instance')

USER = "pipetester"


@pytest.mark.parametrize("package", [
    "pipewire",
    "wireplumber",
    "pipewire-pulse",
])
def test_packages(host, package):
    assert host.package(package).is_installed


def test_global_config(host):
    f = host.file("/etc/pipewire/pipewire.conf.d/10-pipewire.conf")
    assert f.exists
    assert "default.clock.rate          = 48000" in f.content_string


def test_pw_config_parses(host):
    if not host.exists("pw-config"):
        pytest.skip("pw-config is not available on this distribution")
    cmd = host.run("pw-config")
    assert cmd.rc == 0


def test_user_config(host):
    """
    the per-user drop-in must carry the user specific override (clock_rate 44100).
    """
    f = host.file(f"/home/{USER}/.config/pipewire/pipewire.conf.d/10-pipewire.conf")
    assert f.exists
    assert f.user == USER
    assert "default.clock.rate          = 44100" in f.content_string


def test_linger_enabled(host):
    assert host.file(f"/var/lib/systemd/linger/{USER}").exists


def test_user_socket_enabled(host):
    uid = host.user(USER).uid
    cmd = host.run(
        "sudo -u %s XDG_RUNTIME_DIR=/run/user/%d "
        "systemctl --user is-enabled pipewire.socket" % (USER, uid)
    )
    assert "enabled" in cmd.stdout
