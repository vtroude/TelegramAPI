from datetime       import datetime

def get_signal(message, time):
    part    = message.split("\n")

    return {
                "message time": time,
                "signal time": datetime.strptime(":".join(part[1].split(":")[1:])[1:], '%Y-%m-%d %H:%M:%S %Z').isoformat(),
                "open": float(part[2].split(":")[1][1:]),
                "signal": part[3].split(":")[1][1:].lower(),
                "take profit": float(part[4].split(":")[1][1:]),
                "stop loss": float(part[5].split(":")[1][1:]),
            }