import sys, telemetry_server, metrics, threading, logging, debug_test_tools, os, time, subprocess, psutil, argparse, console, check_internet

"""Main script"""


def add_log():
    try:
        with open(path) as f:
            _buf = f.read()
            _log = str(os.getcwd()) + "/log/telemetry_log.log"
            try:
                with open(_log, "a") as _f:
                    _f.write(_buf)
            except IOError:
                subprocess.Popen(['notify-send', "Error: Unable to add new log"])
                return False
    except IOError:
        subprocess.Popen(['notify-send', "Error: Unable read temp log"])
        return False
    return True


def temp_log():
    telemetry = metrics.Telemetry()
    log_time = time.time()
    try:
        telemetry.to_do_logs()
    except RuntimeError:
        logging.info("---FINISHED WITH ERRORS---")
        subprocess.Popen(['notify-send', "Runtime service`s error"])
    logging.info("Execution time: %s" % (str((time.time() - log_time))))


def critical_monitor():
    monitor = metrics.Prcss()
    _val = ""
    while True:
        critical_pids = monitor.critical_prcss()
        if critical_pids is None:
            break
        elif critical_pids == _val:
            break
        else:
            critical_names = [psutil.Process(i).name() for i in critical_pids]
            critical_processes = "Critical processes: " + str(critical_names)
            subprocess.Popen(['notify-send', critical_processes])
            _val = critical_pids
        time.sleep(6)


def server():
    while not check_internet.internet():
        time.sleep(5)
    con = telemetry_server.SockSsl()
    con.set()
    try:
        with open(path, "rb") as _buf:
            con.send(_buf)
            return True
    except IOError:
        subprocess.Popen(['notify-send', "Error: corrupted temp log file"])
        return False


if __name__ == "__main__":
    path = str(os.getcwd()) + "/logs/temp.log"
    temp_log()
    if server():
        if add_log():
            os.remove(path)
    #_Tmonitor = threading.Thread(target=critical_monitor(), args="")
    #_Tmonitor.start()
    #_Tconsole = threading.Thread(target=console.console(), args="")
    #_Tconsole.start()

    sys.exit(0)
