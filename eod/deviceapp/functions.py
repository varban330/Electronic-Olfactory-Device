from .models import Device, DeviceLog

def log_generator(device):
    DeviceLog.objects.filter(device = device).delete()
    log = DeviceLog()
    log.device = device
    log.avg_temp = 1
    log.avg_voc = 1
    log.avg_pres= 1
    log.smell_class = "Khoosbuu"
    log.save()
