from datetime import date
from mfc_attendance import Attendance

target_day = date.today().strftime('%Y-%m-%d')
stamper = Attendance()

stamper.login()
stamper.stamp(target_day)
