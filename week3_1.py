'''
Author: yhh
Date: 2022-08-05 09:59:12
LastEditTime: 2022-09-13 11:28:47
LastEditors: yhh
Description: 
FilePath: \PythonFile\week3_1.py
yhh
'''
from collections import UserList
import time

class selfException(Exception):
    def __init__(self,msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class ATM():
    def __init__(self) -> None:
        global user_list
        global operation
        global operation_record
        global current_user
        user_list = [
            {'user': 'yhh' , 'password' : 'password' , 'count' : 100},
            {'user': 'admin' , 'password' : 'password' , 'count' : 100}
        ]
        operation = ['Deposit:存款', 'Draw:取款', 'Transfer:转账', 'Check_Remaining:查询账户余额', 'Check_latest_operations:查询最近10笔交易', 'Withdraw:退出']
        operation_record=[]
        current_user= None #用于记录当前登陆用户信息的全局变量
        self.menu()

    def DepositInputError(self,value):
        while 1:
            try:
                if value.count(".") != 1:  # 非小数
                    if value.isdigit() and int(value) >= 0:  # 判断是否为正整数
                        return int(value)
                    else:
                        raise selfException(value)
                elif value.count(".") == 1:  # 可能为小数
                    left = value.split(".")[0]
                    right = value.split(".")[1]
                    if left.isdigit() and int(left) >= 0:  
                        if right.isdigit() and int(right) >= 0 and len(right) <= 3:  
                            return float(value)
                        else:
                            raise selfException(value)
                    else:
                        raise selfException(value)
                else:
                    raise selfException(value)
            except selfException as f:
                print('Your input is : %s,Type error,Please input the right type!  Like 999.999' % f.msg)
                value = input("Please input again: ")

    def WithdrawInputError(self,value):
        while 1:
            try:
                if value.isdigit() :  # 是数字
                    if len(value)>2 and int(value)>0 and int(value) %100 == 0:  # 判断是否为正整数且是100的倍数
                        return int(value)
                    else:
                        raise selfException(value)
                else:
                    raise selfException(value)
            except selfException as f:
                print('Your input is : %s,Type error,Your input should be the Multiples of 100,Please input the right type!  Like 500' % f.msg)
                value = input("Please input again: ")

    def TransferInputError(self,other):
        
        while 1:
            index = 0
            try:
                if current_user['user'] == other:
                    raise selfException('Cant transfer to yourself!')
                else:
                    for user in user_list:
                        index +=1
                        if user['user'] == other:
                            while 1:
                                print('Remaining money is ',current_user['count'])
                                value = input('Please input the number: (q to exit)')
                                if(value=='q'):
                                    return
                                money = self.check_transf_value(value)
                                if money >= 0:
                                    if current_user['count'] >= money:
                                        current_user['count'] -= money
                                        user['count'] += money
                                        print('Success! Remaining money is ',current_user['count'])
                                        self.record('Transfer_account',value)
                                        return
                                    else:
                                        raise selfException('The remaining amount does not support the transfer operation!')
                                else:
                                    raise selfException('Type Error!')
                        elif index>len(user_list):
                            raise selfException('%s is not exist!' % other)
            except selfException as f:
                print(f.msg)
                other  = input("input the username you want to transfer money to:")

    def data_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())

    def record(self,operation,value):
        now = self.data_time()
        data = [now,current_user['user'],operation,value,current_user['count']]
        operation_record.insert(0,data)
        if(len(operation_record) > 10):
            operation_record.pop()

    def login(self):
        while 1:
            us = input('Please input your username: ')
            ps = input('Please input your password: ')
            for user in user_list:
                if(user['user'] == us and user['password'] == ps):
                    print('Welcome %s' % us)
                    global current_user
                    current_user = user
                    return
            print('Username or Password ERROR!')

    def check_transf_value(self,value):
        """判断字符串是否为正整数(1)或者浮点数(2)
        参数:value为字符串
        返回:如果是正整数、浮点数,则返回转换后的数字(浮点数只保留小数点后3位),否则返回-1
        """
        if value.count(".") != 1:  # 非小数
            if value.isdigit() and int(value) >= 0:  # 判断是否为正整数
                return int(value)
            else:
                return -1
        elif value.count(".") == 1:  # 可能为小数
            left = value.split(".")[0]
            right = value.split(".")[1]
            if left.isdigit() and int(left) >= 0:  
                if right.isdigit() and int(right) >= 0 and len(right) <= 3:  
                    return float(value)
                else:
                    return -1
            else:
                return -1
        else:
            return -1

    def Deposit(self):  #存款
        while True:
            value = input('Please enter the amount that you want to deposit: ')
            deposit = self.DepositInputError(value)
            if deposit >= 0:
                current_user['count'] += deposit
                print('Success! current money: ',current_user['count'])
                self.record('Deposit',deposit)
                return
            else:
                print('Type error,Please input the right type!  Like 999.999')

    def Draw(self):  #取款
        while True:
            value = input('Please enter the amount that you want to draw: ')
            draw = self.WithdrawInputError(value)
            if draw >= 0:
                if(current_user['count'] >= draw):
                    current_user['count'] -= draw
                    print('Success! current money: ',current_user['count'])
                    self.record('Draw', draw)
                else:
                    print('The amount left is not enough!')
                return
            else:
                print('Type error,Please input the right type!  Like 999.999')

    def Transfer_account(self):#转账
        other = input('Please input the username that you want to transfer money to: ')
        self.TransferInputError(other)
        # if current_user['user'] == other:
        #     print('Cant transfer to yourself!')
        # else:
        #     for user in user_list:
        #         if user['user'] == other:
        #             while 1:
        #                 print('Remaining money is ',current_user['count'])
        #                 value = input('Please input the number: (q to exit)')
        #                 if(value=='q'):
        #                     break
        #                 money = self.check_transf_value(value)
        #                 if money >= 0:
        #                     if current_user['count'] >= money:
        #                         current_user['count'] -= money
        #                         user['count'] += money
        #                         print('Success! Remaining money is ',current_user['count'])
        #                         self.record('Transfer_account',value)
        #                         return
        #                     else:
        #                         print('The remaining amount does not support the transfer operation!')
        #                 else:
        #                     print('Type Error!')
        #         else:
        #             print('%s is not exist!' % other)

    def print_latest_10(self):
        length = len(operation_record)
        if length ==0:
            print('There is no operation recently!')
        if length <= 10:
            for i in range(length):
                print('======================================= The Recent %dth Operation ========================================' % (i+1))
                print('Time: %s, Operation_user: %s, Operation: %s, Operation_number: %s, Remaining: %d' %(operation_record[i][0],operation_record[i][1],operation_record[i][2],operation_record[i][3],operation_record[i][4]))
                print('=========================================================================================================')
        else:
            for i in range(0,10):
                print('======================================= The Recent %dth Operation ========================================' % i)
                print('Time: %s, Operation_user: %s, Operation: %s, Operation_number: %s, Remaining: %d' %(operation_record[i][0],operation_record[i][1],operation_record[i][2],operation_record[i][3],operation_record[i][4]))
                print('=========================================================================================================')

    def Check_Remaining(self):
        print('USER: %s,Remaining is %f'%(current_user['user'],current_user['count']))

    def menu(self):
        self.login()
        while 1:
            index = 0
            for i in operation:
                index += 1
                print('%d.%s' %(index,i))
            option = input('Please input the choice : ')
            if(option >'5' and option <'0'):
                print('Input Error!')
                continue
            if option == '1':
                self.Deposit()
            elif option == '2':
                self.Draw()
            elif option == '3':
                self.Transfer_account()
            elif option =='4':
                self.Check_Remaining()
            elif option =='5':
                self.print_latest_10()
            elif option =='6':
                return
            else:
                print('Please input the right choice！')

ATM()