Please edit the configuration file after installation. This file is
located in the `conf` directory where NXLog was installed (default
`C:\Program Files\nxlog\conf\nxlog.conf` on 64-bit Windows). If
you chose a custom installation directory, you will need to update the
ROOT directory specified in the configuration file before the NXLog
service will start.

The NXLog service will start automatically after installation and on system boot.
The service `Startup type` of newer versions of NXLog is set to
`Automatic (Delayed Start)` instead of `Automatic`. To change this option, open
the service control manager and alter the `Startup type` in the `General` tab.

Alternatively, it can be started from the Services console (run `services.msc`),
or by executing `nxlog.exe`, located in the installation directory (by default
`C:\Program Files\nxlog\nxlog.exe`). Use the `-f` command line argument to run
NXLog in the foreground.

By default, NXLog will write its own messages to the log file named
`nxlog.log` in the `data` directory (default `C:\Program Files\
nxlog\data\nxlog.log` on 64-bit Windows). If you have trouble
starting or running NXLog, check that file for errors.

See the NXLog Reference Manual for details about configuration and
usage. The Reference Manual is installed in the `doc` directory
(default `C:\Program Files\nxlog\doc` on 64-bit Windows) and
should also be available online at <https://nxlog.co/resources>.
