import multiprocessing
import subprocess
import signal
import sys


def run_get_invoices():
    process = subprocess.Popen(["python", "C:\\edemco\\edemco-backend-python\\microservice_get-invoices\\get_invoices.py"])
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait()


def run_obser():
    process = subprocess.Popen(["python", "C:\\edemco\\edemco-backend-python\\microservice_get-invoices\\cufe.py"])
    try:
        process.wait()
    except KeyboardInterrupt:
        process.terminate()
        process.wait()


def signal_handler(sig, frame):
    print("\nEjecución detenida.")
    p1.terminate()
    p2.terminate()
    p1.join()
    p2.join()
    sys.exit(0)


if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_get_invoices)
    p2 = multiprocessing.Process(target=run_obser)

    p1.start()
    p2.start()

    # Capturar la señal de interrupción (Ctrl+C)
    signal.signal(signal.SIGINT, signal_handler)

    try:
        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("\nEjecución detenida.")
        p1.terminate()
        p2.terminate()
        p1.join()
        p2.join()
        sys.exit(0)
