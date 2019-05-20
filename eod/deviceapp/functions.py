from .models import Device, DeviceLog
import random

smell_classes = ["Air", "Lime", "Vodka", "Beer", "Vinegar", "Wine", "Acetone", "Ethanol", "Isopropanol"]
def log_generator(device):
    DeviceLog.objects.filter(device = device).delete()
    log = DeviceLog()
    log.device = device
    avg_temp = random.uniform(10.5,37.5)
    log.avg_temp = round(avg_temp,2)
    avg_voc = random.uniform(0,100)
    log.avg_voc = round(avg_voc,2)
    avg_pres = random.uniform(0,2)
    log.avg_pres = round(avg_pres,2)
    log.smell_class = random.choice(smell_classes)
    log.save()
