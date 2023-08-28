import re
from typing import List, Dict

from log_translate.data_struct import Log, Level
from log_translate.gloable import pids, remember_dict
from log_translate.log_translator import TagPatternTranslator


class CrashPatternTranslator(TagPatternTranslator):
    def __init__(self):
        super().__init__({
            r"AndroidRuntime|FATAL.*|System.err.*|DEBUG.?": CrashLogMsgTranslator()
        })


class CrashLogMsgTranslator:
    def translate(self, tag, msg):
        # remember_dict["packages"].append("99")
        # DEBUG   : Process name is com.heytap.health:transport, not key_process
        if "Process name is " in msg:
            result = re.search("is (.*), ", msg)
            if result:
                if result.group(1) in remember_dict["packages"]:
                    return Log(translated=" %s > %s " % (tag, msg), level=Level.e)
        # AndroidRuntime: Process: com.heytap.health, PID: 30260
        if "Process: " in msg:
            # 开始需要收集日志
            result = re.search("Process: (.*), ", msg)
            if result:
                if result.group(1) in remember_dict["packages"]:
                    return Log(translated=" %s > %s " % (tag, msg), level=Level.e)
        if remember_dict["pid"] in pids:
            return Log(translated=" %s > %s " % (tag, msg), level=Level.e)
        return None


def process_dict(my_dict: Dict[str, int]):
    # 对字典进行操作
    for key, value in my_dict.items():
        print(key, value)


if __name__ == '__main__':
    print(re.compile(".*Task").match("aaTas8km"))
    print(CrashPatternTranslator().translate("FATAL EION", "你好"))
