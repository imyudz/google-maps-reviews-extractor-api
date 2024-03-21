from urllib.parse import quote_plus as _quote_plus

def mount_bussiness_base_url(bussiness_maps_name: str, bussiness_full_address: str) -> str:
    formatted_bussiness_maps_name = _quote_plus(bussiness_maps_name)
    formatted_bussiness_real_address = _quote_plus(bussiness_full_address)
    print(formatted_bussiness_maps_name)
    return f"https://www.google.com/search?q={formatted_bussiness_maps_name}+{formatted_bussiness_real_address}&oq={formatted_bussiness_maps_name}+{formatted_bussiness_real_address}&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIICAEQABgNGB4yCAgCEAAYDRgeMggIAxAAGA0YHjIICAQQABgNGB4yCAgFEAAYDRgeMgYIBhBFGDwyBggHEEUYPDIGCAgQRRg80gEHMTg0ajBqNKgCALACAA&sourceid=chrome&ie=UTF-8"
    
def mount_bussiness_review_url(bussiness_base_url: str, lrd: str) -> str:
    return f"{bussiness_base_url}#lrd={lrd},1,,,,"
