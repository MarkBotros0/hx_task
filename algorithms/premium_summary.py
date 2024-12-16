from helper_functions.json_file_handler import save_dataset, load_dataset
from constants.constants import FIXED_PREMIUM_FOR_NON_FLYING_CAMERAS, FIXED_PREMIUM_FOR_NON_FLYING_DRONES


def _get_gross_prem_drones_hull(net_prem_drones_hull, brokerage):
    """
    Calculates the gross hull premium for drones, given the net hull premium and brokerage rate.
    """
    return net_prem_drones_hull/(1-brokerage)


def _get_gross_prem_drones_tpl(net_prem_drones_tpl, brokerage):
    """
    Calculates the gross TPL (third-party liability) premium for drones
    """
    return net_prem_drones_tpl/(1-brokerage)


def _get_gross_prem_cameras_hull(net_prem_cameras_hull, brokerage):
    """
    Calculates the gross hull premium for cameras, given the net hull premium and brokerage rate.
    """
    return net_prem_cameras_hull/(1-brokerage)


def _get_gross_prem_total(gross_prem_drones_hull, gross_prem_drones_tpl, gross_prem_cameras_hull):
    """
    Calculates the total gross premium by summing the gross premiums for drones' hull,
    drones' TPL, and cameras' hull premiums.
    """
    return sum(
        [gross_prem_drones_hull, gross_prem_drones_tpl, gross_prem_cameras_hull]
    )


def _get_net_prem_drones_hull(drones):
    """
    Calculates the total hull premium for all drones in the data.
    """
    return sum(
        drone["hull_premium"] for drone in drones
    )


def _get_net_prem_drones_tpl(drones):
    """
    Calculates the total TPL (third-party liability) layer premium for all drones.
    """
    return sum(
        drone["tpl_layer_premium"] for drone in drones
    )


def _get_net_prem_cameras_hull(detachable_cameras):
    """
    Calculates the total hull premium for all detachable cameras.
    """
    return sum(
        camera["hull_premium"] for camera in detachable_cameras
    )


def _get_net_prem_total(net_prem_drones_hull, net_prem_drones_tpl, net_prem_cameras_hull):
    """
    Calculates the total net premium by summing the premiums from drones' hull,
    drones' TPL, and cameras' hull premiums.
    """
    return sum(
        [net_prem_drones_hull, net_prem_drones_tpl, net_prem_cameras_hull]
    )


def computeSummary():
    """
    Performs the calculation of the net and gross premium summary, and updates the data model.
    """
    data = load_dataset()
    net_drones_hull = _get_net_prem_drones_hull(data["drones"])
    net_drones_tpl = _get_net_prem_drones_tpl(data["drones"])
    net_cameras_hull = _get_net_prem_cameras_hull(data["detachable_cameras"])
    net_total = _get_net_prem_total(
        net_drones_hull,
        net_drones_tpl,
        net_cameras_hull)

    brokerage = data["brokerage"]
    gross_drones_hull = _get_gross_prem_drones_hull(net_drones_hull, brokerage)
    gross_drones_tpl = _get_gross_prem_drones_tpl(net_drones_tpl, brokerage)
    gross_cameras_hull = _get_gross_prem_cameras_hull(
        net_cameras_hull,
        brokerage)
    gross_total = _get_gross_prem_total(
        gross_drones_hull,
        gross_drones_tpl,
        gross_cameras_hull)

    summary = {
        "net_prem": {
            "drones_hull": net_drones_hull,
            "drones_tpl": net_drones_tpl,
            "cameras_hull": net_cameras_hull,
            "total": net_total
        },
        "gross_prem": {
            "drones_hull": gross_drones_hull,
            "drones_tpl": gross_drones_tpl,
            "cameras_hull": gross_cameras_hull,
            "total": gross_total
        }
    }

    data.update(summary)
    return data


def apply_extensions(max_drones_in_air, cameras_in_the_air):
    data = load_dataset()
    drones_sorted = sorted(
        data["drones"],
        # key=lambda x: (x['hull_premium'] + x['tpl_layer_premium']),
        key=lambda x: x['hull_premium'],
        reverse=True)

    for drone in drones_sorted[max_drones_in_air:]:
        drone['hull_premium'] = FIXED_PREMIUM_FOR_NON_FLYING_DRONES

    sorted_cameras = sorted(
        data["detachable_cameras"],
        key=lambda x: x["value"],
        reverse=True)

    for camera in sorted_cameras[cameras_in_the_air:]:
        camera["hull_premium"] = FIXED_PREMIUM_FOR_NON_FLYING_CAMERAS

    data["detachable_cameras"] = sorted_cameras
    save_dataset(data)
    return computeSummary()


def printSummary():
    data = load_dataset()

    headers = ["Category", "Gross Summary", "Net Summary"]

    data = [
        ["Drones Hull",
         round(data["net_prem"]["drones_hull"]),
         round(data["gross_prem"]["drones_hull"])
         ],
        ["Drones TPL",
         round(data["net_prem"]["drones_tpl"]),
         round(data["gross_prem"]["drones_tpl"])
         ],
        ["Cameras Hull",
         round(data["net_prem"]["cameras_hull"]),
         round(data["gross_prem"]["cameras_hull"])
         ],
        ["Total",
         round(data["net_prem"]["total"]),
         round(data["gross_prem"]["total"])
         ],
    ]
    print("="*56)
    print(f"{headers[0]:<18}||{headers[1]:<16}||{headers[2]:<16}||")
    print("="*56)
    for row in data:
        print(f"{row[0]:<18}||{row[1]:<16}||{row[2]:<16}||")
    print()
