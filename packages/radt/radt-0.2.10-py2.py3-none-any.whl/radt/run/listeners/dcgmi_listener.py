import io
import mlflow
import os
import subprocess

from multiprocessing import Process

DCGMI_GROUP_ID = os.getenv("RADT_DCGMI_GROUP")

METRIC_NAMES = [
    "Power Usage",
    "Total Energy Consumption",
    "PCIE TX Throughput",
    "PCIE RX Throughput",
    "GPU Utilization",
    "Memory Copy Utilization",
    "GR Engine Active",
    "SN Active",
    "SM Occupancy",
    "Tensor Active",
    "DRAM Active",
    "FP64 Active",
    "FP32 Active",
    "FP16 Active",
    "PCIE TX Bytes",
    "PCIE RX Bytes",
    "NVlink TX Bytes",
    "NVlink RX Bytes",
]


class DCGMIThread(Process):
    def __init__(self, run_id, experiment_id=88):
        super(DCGMIThread, self).__init__()
        self.run_id = run_id
        self.experiment_id = experiment_id

    def run(self):
        self.dcgm = subprocess.Popen(
            f"dcgmi dmon -e 155,156,200,201,203,204,1001,1002,1003,1004,1005,1006,1007,1008,1009,1010,1011,1012 -g {DCGMI_GROUP_ID}".split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.monitor()

        # If advanced metrics are not available, restart the service with limited collection
        if "Error setting watches" not in str(self.dcgm.stderr.read()):
            return

        self.dcgm = subprocess.Popen(
            f"dcgmi dmon -e 155,156,200,201,203,204 -g {DCGMI_GROUP_ID}".split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.monitor()

    def monitor(self):
        for line in io.TextIOWrapper(self.dcgm.stdout, encoding="utf-8"):
            if "Error" in line:
                raise Exception("DCGMI handler could not find required group!")
            line = line.split()

            if "POWER" in line:
                continue

            if line[0].lower().strip() not in ["#", "id"]:
                m = {}
                for value, name in zip(
                    line[2:], METRIC_NAMES
                ):  # [2:] to get rid of gpu name
                    if value.strip() == "N/A":
                        value = 0
                    m[f"DCGMI - {name}"] = float(value)

                mlflow.log_metrics(m)
