#!/usr/bin/env python3

import subprocess
import sys
sys.path.append('lib')

from ops.charm import CharmBase
from ops.framework import StoredState
from ops.main import main
from ops.model import (
    ActiveStatus,
    MaintenanceStatus,
)


def snap_local_install(snap_path):
    cmd = ['snap', 'install']
    cmd.append('--dangerous')
    cmd.append(snap_path)
    subprocess.check_call(cmd)


class SLURMDBDCharm(CharmBase):
    state = StoredState()

    def __init__(self, framework, key):
        super().__init__(framework, key)
        self.framework.observe(self.on.install, self.on_install)
        self.state.set_default(slurmdbd_snap_installed=False)


    def on_install(self, event):
        unit = self.framework.model.unit

        # Install the Munge snap.
        munge_snap = self.framework.model.resources.fetch("munge-snap")
        unit.status = MaintenanceStatus("Installing Munge snap.")
        snap_local_install(
            snap_path=munge_snap
        )

        # Install SlurmDBD snap.
        slurmdbd_snap = self.framework.model.resources.fetch("slurmdbd-snap")
        unit.status = MaintenanceStatus("Installing SlurmDBD snap.")
        snap_local_install(
            snap_path=slurmdbd_snap
        )

        unit.status = ActiveStatus()

        self.state.slurmdbd_snap_installed = True


if __name__ == '__main__':
    main(SLURMDBDCharm)
