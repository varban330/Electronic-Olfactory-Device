from deviceapp.models import Device

def get_none_device():
    dev = Device.objects.filter(device_id = "nldevice")[0]
    return dev
