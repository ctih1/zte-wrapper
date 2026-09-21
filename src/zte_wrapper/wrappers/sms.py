from ..authwrapper import ZTEAuthWrapper
import json
from ..types import PhoneNumber, SMSMessage, AuthError
from ..helpers import utf_16_encode, utf_16_decode, get_zte_timestring
from typing import List, Dict
import logging

logger = logging.getLogger("zte")


class SmsWrapper:
    def __init__(self, auth: ZTEAuthWrapper):
        self.auth = auth

    async def get_sms(self) -> Dict[PhoneNumber, List[SMSMessage]] | None:
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

        results: Dict[PhoneNumber, List[SMSMessage]] = {}
        for message in jason["messages"]:
            phone_number = utf_16_decode(message["number"])

            if phone_number not in results:
                results[phone_number] = []

            results[phone_number].append(
                SMSMessage(
                    content=utf_16_decode(message["content"]), tag=int(message["tag"])
                )
            )

        return results

    async def send_sms(
        self, phone_number: str, message: str, tz_offset_hours: int
    ) -> bool:
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
