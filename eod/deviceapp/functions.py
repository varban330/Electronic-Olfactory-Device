from .models import Device, DeviceLog, DangerLog
import random

smell_classes = ["Air", "Lime", "Vodka", "Beer", "Vinegar", "Wine", "Acetone", "Ethanol", "Isopropanol"]
dangerous = ["Isopropanol"]
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

def save_device_status(request):
    device = Device.objects.filter(device_id = request["device_id"])[0]
    filter_list = DeviceLog.objects.filter(device = device)
    if filter_list:
        device_status = filter_list[0]
    else:
        device_status = DeviceLog()
        device_status.device = device
    device_status.smell_class = request["smell_class"]
    device_status.avg_temp = request["avg_temp"]
    device_status.avg_pres = request["avg_pres"]
    device_status.avg_co = request["avg_co"]
    device_status.avg_lpg = request["avg_lpg"]
    device_status.avg_smoke = request["avg_smoke"]
    device_status.pushed = False
    device_status.save()
    if request["smell_class"] in dangerous:
        dangerlog = DangerLog()
        dangerlog.device = device_status.device
        dangerlog.smell_class = request["smell_class"]
        dangerlog.avg_temp = request["avg_temp"]
        dangerlog.avg_pres = request["avg_pres"]
        dangerlog.avg_co = request["avg_co"]
        dangerlog.avg_lpg = request["avg_lpg"]
        dangerlog.avg_smoke = request["avg_smoke"]
        dangerlog.pushed = False
        dangerlog.save()
    return True
