
from ..authwrapper import ZTEAuthWrapper
from ..types import NetworkDetails, SignalStrength


class SignalWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_signal_strength(self) -> SignalStrength:
        data = await self.auth.query_items(
            [
                "Z5g_SINR",
                "Z5g_rsrp",
                "Z5g_rsrq",
                "Z5g_rssi",
                "lte_pci",
                "lte_rsrq",
                "lte_rssi",
                "lte_snr",
                "network_Z5g_CELLINFO_band",
                "network_ZCELLINFO_band",
                "network_lte_rsrp",
            ]
        )

        return SignalStrength(
            sinr_5g=float(data["Z5g_SINR"]),
            rsrp_5g=float(data["Z5g_rsrp"]),
            rsrq_5g=float(data["Z5g_rsrq"]),
            rssi_5g=float(data["Z5g_rssi"]),
            band_5g=data["network_Z5g_CELLINFO_band"],
            band_lte=data["network_ZCELLINFO_band"],
            pci_lte=float(data["lte_pci"]),
            rsrq_lte=float(data["lte_rsrq"]),
            rsrp_lte=float(data["network_lte_rsrp"]),
            rssi_lte=float(data["lte_rssi"]),
            snr_lte=float(data["lte_snr"]),
        )

    async def get_network_details(self) -> NetworkDetails:
        data = await self.auth.query_items(
            [
                "network_provider_fullname",
                "flux_realtime_tx_thrpt",
                "flux_realtime_rx_thrpt",
                "flux_monthly_tx_bytes",
                "flux_monthly_rx_bytes",
            ]
        )
        return NetworkDetails(
            isp_name=data["network_provider_fullname"],
            download_mbps=(float(data["flux_realtime_rx_thrpt"]) * 8) / (1024 * 1024),
            upload_mbps=(float(data["flux_realtime_tx_thrpt"]) * 8) / (1024 * 1024),
            monthly_download_megabytes=float(data["flux_monthly_rx_bytes"])
            / (1024 * 1024),
            monthly_upload_megabytes=float(data["flux_monthly_tx_bytes"])
            / (1024 * 1024),
        )
