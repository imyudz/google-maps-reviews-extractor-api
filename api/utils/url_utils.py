from urllib.parse import quote_plus as _quote_plus

def mount_bussiness_base_url(bussiness_maps_name: str) -> str:
    formatted_bussiness_maps_name = _quote_plus(bussiness_maps_name)
    print(formatted_bussiness_maps_name)
    return f"https://www.google.com/search?q={formatted_bussiness_maps_name}&oq={formatted_bussiness_maps_name}&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgNGB4yCAgCEAAYDRgeMggIAxAAGA0YHjIICAQQABgNGB4yCAgFEAAYDRgeMgYIBhBFGDwyBggHEEUYPDIGCAgQRRg80gEHMTg0ajBqNKgCALACAA&sourceid=chrome&ie=UTF-8"
    
def mount_bussiness_review_url(bussiness_base_url: str, lrd: str) -> str:
    return f"{bussiness_base_url}#lrd={lrd},1,,,,"
