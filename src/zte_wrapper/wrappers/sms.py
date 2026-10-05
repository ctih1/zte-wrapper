from __future__ import annotations

import json
import logging

from ..authwrapper import ZTEAuthWrapper
from ..helpers import (
    get_zte_timestring,
    utf_16_decode,
    utf_16_encode,
    parse_zte_timestring,
)
from ..types import PhoneNumber, SMSMessage, SMSRole

logger = logging.getLogger("zte")


class SmsWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_sms(self) -> dict[PhoneNumber, list[SMSMessage]] | None:
        res = await self.auth.request(
            "GET",
            self.auth.construct_url(
                "goform_get_cmd_process",
                {
                    "isTest": "false",
                    "cmd": "sms_data_total",
                    "page": "0",
                    "data_per_page": "1500",
                    "mem_store": "1",
                    "tags": "10",
                    "order_by": "order by id desc",
                    "_": self.auth.get_timestamp(),
                },
            ),
        )

        jason: dict = json.loads(await res.text())

        if jason.get("sms_data_total") == "" or jason.get("messages") is None:
            logger.error(f"Failed to retrieve sms data: {jason}")
            return None

        results: dict[PhoneNumber, list[SMSMessage]] = {}
        for message in jason["messages"]:
            phone_number = utf_16_decode(message["number"])

            if phone_number not in results:
                results[phone_number] = []

            mode: SMSRole = "UNKNOWN"
            if message["tag"] == "2":
                mode = "SENT_BY_SELF"
            if message["tag"] == "0":
                mode = "SENT_BY_OTHER"

            results[phone_number].append(
                SMSMessage(
                    content=utf_16_decode(message["content"]),
                    tag=int(message["tag"]),
                    id=int(message["id"]),
                    mode=mode,
                    date=parse_zte_timestring(message["date"]),
                    sms_class=int(message["sms_class"]),
                )
            )

        return results

    async def send_sms(
        self, phone_number: str, message: str, tz_offset_hours: int
    ) -> bool:
        if len(message) > 160:
            logger.error("Message too long!")
            return False
        res = await self.auth.request(
            "POST",
            self.auth.construct_url("goform_set_cmd_process", {}),
            data={
                "isTest": "false",
                "goformId": "SEND_SMS",
                "notCallback": "true",
                "Number": phone_number,
                "sms_time": get_zte_timestring(tz_offset_hours),
                "MessageBody": utf_16_encode(message),
                "ID": "-1",
                "encode_type": "GSM7_default",
                "AD": await self.auth.construct_ad_token(),
            },
        )

        data = json.loads(await res.text())
        success = data["result"] == "success"
        if not success:
            logger.error(f"Failed to send SMS: {data}")
        else:
            logger.info(f"Sent SMS to {phone_number[3:]}...{phone_number[:2]}")
        return success
