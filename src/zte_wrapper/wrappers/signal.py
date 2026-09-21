from ..authwrapper import ZTEAuthWrapper
import json
from ..types import SignalStrength, NetworkDetails


class SignalWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_signal_strength(self) -> SignalStrength:
        res = await self.auth.request(
            "GET",
            self.auth.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "Z5g_SINR,Z5g_rsrp,Z5g_rsrq,Z5g_rssi,lte_pci,lte_rsrq,lte_rssi,lte_snr,network_Z5g_CELLINFO_band,network_ZCELLINFO_band,network_lte_rsrp",
                    "multi_data": "1",
                    "_": self.auth.get_timestamp(),
                },
            ),
        )

        jason = json.loads(await res.text())

        return SignalStrength(
            sinr_5g=float(jason["Z5g_SINR"]),
            rsrp_5g=float(jason["Z5g_rsrp"]),
            rsrq_5g=float(jason["Z5g_rsrq"]),
            rssi_5g=float(jason["Z5g_rssi"]),
            band_5g=jason["network_Z5g_CELLINFO_band"],
            band_lte=jason["network_ZCELLINFO_band"],
            pci_lte=float(jason["lte_pci"]),
            rsrq_lte=float(jason["lte_rsrq"]),
            rsrp_lte=float(jason["network_lte_rsrp"]),
            rssi_lte=float(jason["lte_rssi"]),
            snr_lte=float(jason["lte_snr"]),
        )

    async def get_network_details(self) -> NetworkDetails:
        res = await self.auth.request(
            "GET",
            self.auth.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "network_provider_fullname,flux_realtime_tx_thrpt,flux_realtime_rx_thrpt,flux_monthly_tx_bytes,flux_monthly_rx_bytes",
                    "multi_data": "1",
                    "_": self.auth.get_timestamp(),
                },
            ),
        )

        jason = json.loads(await res.text())

        return NetworkDetails(
            isp_name=jason["network_provider_fullname"],
            download_mbps=(float(jason["flux_realtime_rx_thrpt"]) * 8) / (1024 * 1024),
            upload_mbps=(float(jason["flux_realtime_tx_thrpt"]) * 8) / (1024 * 1024),
            monthly_download_megabytes=float(jason["flux_monthly_rx_bytes"])
            / (1024 * 1024),
            monthly_upload_megabytes=float(jason["flux_monthly_tx_bytes"])
            / (1024 * 1024),
        )
