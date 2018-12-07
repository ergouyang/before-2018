
import traceback
import xlsxwriter
import random
save_path = 'C:\\Users\yangergou\Desktop\code\data\\user_info.xlsx'
wk = xlsxwriter.Workbook(save_path)
sheet = wk.add_worksheet('user_info')
sheet_title = ['userId','newsId','score']
sheet.write_row('A1', sheet_title)
for i in range(30):
    a = random.randint(1,184)

