import re

from log_translate.data_struct import Log, Level
from log_translate.gloable import remember_dict, chek_gloable_value_equal

from log_translate.log_translator import SubTagTranslator, TagStrTranslator


class SecTagDemoTranslator(SubTagTranslator):
    def __init__(self):
        super().__init__("DFJ",
                         lambda string: re.search(r"(?P<tag>.*?) *:(?P<msg>.*)", string),
                         [
                             TagStrTranslator({
                                 "sec_tag": self.new_tag
                             })
                         ])

    def new_tag(self, tag, msg):
        return Log(translated=msg)


class BluetoothTranslator(TagStrTranslator):
    def __init__(self):
        super().__init__({
            "BluetoothAdapter": bluetooth_adapter,
            "BluetoothGatt": bluetooth_gatt,
            "bt_btm": bt_btm,
            "BluetoothBondStateMachine": bluetooth_pairing_action,
            "WS_BT_BluetoothPairingRequest": bluetooth_pairing_action,
            "BluetoothDevice": bluetooth_pairing_action,
            "vendor.qti.bluetooth.*?[btstateinfo|uart_logs|logger]": bluetoothError,
            "ActivityTaskManager": bluetooth_pairing_dialog
        })


code_state = {
    "10": "手机系统蓝牙 已关闭",
    "12": "手机系统蓝牙 已打开",
    "OFF": "手机系统蓝牙 已关闭",
    "ON": "手机系统蓝牙 已打开"
}

ConfirmReqReply = {
    "0": "Command succeeded",
    "1": "Command started OK. ",
    "2": "Device busy with another command ",
    "3": "No resources to issue command",
    "4": "Request for 1 or more unsupported modes",
    "5": "Illegal parameter value  ",
    "6": "Device in wrong mode for request ",
    "7": "Unknown remote BD address",
    "8": "Device timeout",
    "9": "A bad value was received from HCI",
    "10": "Generic error ",
    "11": "Authorization failed",
    "12": "Device has been reset",
    "13": "request is stored in control block",
    "14": "state machine gets illegal command",
    "15": "delay the check on encryption",
    "16": "Bad SCO over HCI data length",
    "17": "security passed, no security set ",
    "18": "security failed",
    "19": "repeated attempts for LE security requests",
    "20": "Secure Connections Only Mode can't be supported",
    "21": "The device is restrict listed",
    "22": "Handle for Pin or Key Missing"
}


def bt_btm(msg):
    # bt_btm              com.android.bluetooth        I  BTM_ConfirmReqReply() State: WAIT_NUM_CONFIRM  Res: 0
    # bt_btm              com.android.bluetooth        I  BTM_ConfirmReqReply() State: WAIT_NUM_CONFIRM  Res: 11
    if "BTM_ConfirmReqReply() State: WAIT_NUM_CONFIRM" in msg:
        result = re.search("Res: (\d+)", msg)
        if result:
            state = ConfirmReqReply[result.group(1)]
            if state:
                return Log(translated=">>>>>>>>>> pin码配对 确认结果 %s  <<<<<<<< " % state, level=Level.i)
    return None


def bluetooth_pairing_dialog(msg):
    # ActivityTaskManager: Displayed com.oplus.wirelesssettings/com.android.settings.bluetooth.BluetoothPairingDialog
    # port_rfc_closed: RFCOMM connection closed, index=3, state=2 reason=Closed[19], UUID=111F, bd_addr=ac:73:52:3f:5b:0a, is_server=1
    if "BluetoothPairingDialog" in msg:
        result = re.search("Displayed.*BluetoothPairingDialog", msg)
        if result:
            return Log(translated=" ---------------- 配对PIN码弹窗弹出 ----------------- ")
    return None


# BluetoothBondStateMachine | WS_BT_BluetoothPairingRequestBluetoothBondStateMachine|WS_BT_BluetoothPairingRequest|BluetoothAdapter.*called by
def bluetooth_pairing_action(msg):
    # 开始配对
    # WS_BT_BluetoothPairingRequest: onReceive() action is android.bluetooth.device.action.PAIRING_REQUEST
    if "action.PAIRING_REQUEST" in msg:
        return Log(
            translated=f" >>>>>>>>>> 收到配对请求的广播: android.bluetooth.device.action.PAIRING_REQUEST <<<<<<<< ")

    # PIN码
    # BluetoothBondStateMachine: sspRequestCallback: [B@4e743fe name: [B@1a3875f cod: 7936 pairingVariant 0 passkey: 211603
    if "passkey" in msg:
        result = re.search("(?<=passkey: )\d+", msg)
        return Log(translated=f" >>>>>>>>>> 蓝牙连接认证请求 passkey: {result.group()} <<<<<<<< ", level=Level.i)
    # 取消配对
    # BluetoothBondStateMachine: Bond State Change Intent:E4:40:97:3C:EB:1C BOND_BONDED => BOND_NONE
    # 确定配对
    # BluetoothBondStateMachine: Bond State Change Intent:E4:40:97:3C:EB:1C BOND_BONDING => BOND_BONDED
    if "BOND_NONE => BOND_BONDING" in msg:
        # 未绑定到绑定中 请求绑定
        result = re.search(r"(?<=:).*?(?= )", msg)
        return Log(translated=f" >>>>>>>>>> 设备: {result.group()} 正请求绑定 <<<<<<<< ", level=Level.i)
    if "BOND_BONDED => BOND_NONE" in msg:
        result = re.search(r"(?<=:).*?(?= )", msg)
        return Log(translated=f" >>>>>>>>>> 设备: {result.group()} 解除绑定 <<<<<<<< ", level=Level.i)
    if "BOND_BONDING => BOND_NONE" in msg:
        result = re.search(r"(?<=:).*?(?= )", msg)
        return Log(translated=f" >>>>>>>>>> 设备: {result.group()} 取消绑定 <<<<<<<< ", level=Level.i)
    if " => BOND_BONDED" in msg:
        result = re.search(r"(?<=:).*?(?= )", msg)
        return Log(translated=f" >>>>>>>>>> 设备: {result.group()} 绑定成功 <<<<<<<< ", level=Level.i)

        # com.oplus.wirelesssettings   D  Pairing dialog accepted
        # BluetoothDevice    setPairingConfirmation(): confirm: true, called by: com.oplus.wirelesssettings
        # BluetoothDevice     cancelBondProcess() for device 74:86:69:FE:6F:14 called by pid: 31290 tid: 32523
        # BluetoothDevice: setPairingConfirmation(): confirm: true, called by: com.oplus.wirelesssettings
        # ActivityTaskManager: Displayed com.oplus.wirelesssettings/com.android.settings.bluetooth.BluetoothPairingDialog
    if "Pairing dialog accepted" in msg:
        return Log(translated=" ----------------- 点击配对按钮,用户同意配对 ----------------- ")
    if "Pairing dialog canceled" in msg:
        return Log(translated=" ----------------- 点击取消按钮,用户取消配对 ----------------- ",
                   level=Level.i)
    if "setPairingConfirmation(): confirm: true" in msg:
        return Log(translated=" ----------------- 点击配对按钮,用户同意配对 ----------------- ",
                   level=Level.i)
    if "cancelBondProcess() for device" in msg:
        return Log(translated=" ----------------- 点击取消按钮,用户取消配对 ----------------- ",
                   level=Level.i)
    return None


def bluetooth_adapter(msg):
    if "getState()" in msg:
        # BluetoothAdapter: 251847304: getState(). Returning TURNING_ON
        # BluetoothAdapter: 134396450: getState(). Returning ON
        # BluetoothAdapter: 251847304: getState(). Returning OFF
        result = re.search("(?<=Returning ).*", msg)
        # result = re.search("Returning (.*)", msg)
        # result.grop(1)
        if result:
            result_group = result.group()
            if result_group in code_state:
                state = code_state[result_group]
                if chek_gloable_value_equal("bluetooth_state", state):
                    return None
                return Log(translated=">>>>>>>>>>  %s  <<<<<<<< " % state, level=Level.d)
    #  BluetoothAdapter: disable(): called by: com.android.systemui
    #  BluetoothAdapter: enable(): called by: com.android.systemui
    if "disable(): called by" in msg:
        result = re.search("(?<=by: ).*", msg)
        return Log(translated=f">>>>>>>>>>  通过【{result.group()}】关闭系统蓝牙  <<<<<<<< ", level=Level.e)
    if "enable(): called by" in msg:
        result = re.search("(?<=by: ).*", msg)
        return Log(translated=f">>>>>>>>>>  通过【{result.group()}】打开系统蓝牙  <<<<<<<< ", level=Level.e)
    return None


# noinspection PyTypeChecker
def bluetooth_gatt(msg: object) -> object:
    # 	行 30: 08-05 15:16:32.334 10352 10596 D BluetoothGatt: connect() - device: 30:E7:BC:68:B3:1F, auto: false
    # 	行 31: 08-05 15:16:32.334 10352 10596 D BluetoothGatt: registerApp()
    # 	行 32: 08-05 15:16:32.334 10352 10596 D BluetoothGatt: registerApp() - UUID=f4571777-e0da-45cc-b829-bb1cdec8b87a
    # 	行 33: 08-05 15:16:32.336 10352 23202 D BluetoothGatt: onClientRegistered() - status=0 clientIf=8
    # 	行 36: 08-05 15:16:32.346 10352 23202 D BluetoothGatt: onClientConnectionState() - status=257 clientIf=8 device=30:E7:BC:68:B3:1F
    if "cancelOpen()" in msg:
        result = re.search("device: (.*)", msg)
        return Log(translated=">>>>>>>>>>  gatt 手机主动断开连接 %s  <<<<<<<< " % (result.group(1)), level=Level.i)
    if "close()" in msg:
        return Log(translated=">>>>>>>>>>  gatt 手机主动关闭连接  <<<<<<<< ", level=Level.i)
    if "connect()" in msg:
        # connect() - device: 34:47:9A:31:52:CF, auto: false, eattSupport: false
        result = re.search("device: (.*?),", msg)
        return Log(translated=">>>>>>>>>>  gatt 发起设备连接 > %s  <<<<<<<< " % (result.group(1)), level=Level.i)
    if "onClientConnectionState()" in msg:
        # BluetoothGatt: onClientConnectionState() - status=257 clientIf=8 device=30:E7:BC:68:B3:1F
        result = re.search("status=(.*?) ", msg)
        if "0" == result.group(1):
            return Log(translated=">>>>>>>>>>  gatt 连接设备成功 > %s  <<<<<<<< " % (result.group(1)), level=Level.i)
        else:
            return Log(translated=">>>>>>>>>>  gatt 连接设备失败 status: > %s  <<<<<<<< " % (result.group(1)), level=Level.i)
    return None


def bluetoothError(tag, msg):
    # 07-09 08:50:07.121  1659  6605 D vendor.qti.bluetooth@1.1-uart_logs: DumpLogs: -->
    # 07-09 08:50:07.121  1659  6605 E vendor.qti.bluetooth@1.1-uart_logs: DumpLogs: Unable to open the Dir /sys/kernel/tracing/instances/hsuart err: Permission denied (13)
    # 07-09 08:50:07.121  1659  6605 D vendor.qti.bluetooth@1.1-logger: ReadSsrLevel crash dump value 1
    # 07-09 08:50:07.121  1659  6605 I vendor.qti.bluetooth@1.1-logger: ReadSsrLevel: ssr_level set to 3
    # 07-09 08:50:07.121  1659  6605 D vendor.qti.bluetooth@1.1-btstateinfo: DumpBtState: Dumping stats into /data/vendor/ssrdump/ramdump_bt_state_2023-07-09_08-50-07.log
    # 07-09 08:50:07.121  1659  6605 D vendor.qti.bluetooth@1.1-btstateinfo: BtPrimaryCrashReason:Rx Thread Stuck
    # 07-09 08:50:07.121  1659  6605 D vendor.qti.bluetooth@1.1-btstateinfo: BtSecondaryCrashReason:Default
    # 07-09 08:50:07.121  1659  6605 D vendor.qti.bluetooth@1.1-btstateinfo: BQR RIE Crash Code : 0x07
    # 07-09 08:50:07.121  1659  6605 D vendor.qti.bluetooth@1.1-btstateinfo: BQR RIE Crash String : Rx Thread Stuck
    # bluetooth\DCS\bt_fw_dump\压缩包内有蓝牙日志
    if re.search(r"DumpLogs|Dumping|crash", msg, re.IGNORECASE):  # 成员运算符和推导式
        return Log(translated="%s %s [系统蓝牙出问题了]" % (tag, msg), level=Level.e)
    return None


if __name__ == '__main__':
    result = re.search("device: (.*?),", "connect() - device: 34:47:9A:31:52:CF, auto: false, eattSupport: false")
    print(result.group(1))
    result = re.search("(?<=:).*?(?= )", "dBond State Change Intent:E4:40:97:3C:EB:1C BOND_B")
    # result = re.search("(?<=by: ).*", "disable(): called by: com.android.systemui")
    # result = re.search("(?<=\*).*", "onReCreateBond: 24:*:35:06")
    print(result.group())
    # (?<=A).+?(?=B) 匹配规则A和B之间的元素 不包括A和B
