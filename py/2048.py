# coding=utf-8
import random
import copy

def version():
    print('version:1.1.0')

def restart():#重置游戏(finished
    score = 0
    #下一行生成4*4的全零矩阵
    field= [[0 for i in range(4)] for j in range(4)]
    #添加两个随机数
    field = add_add(field)
    field = add_add(field)
    return field,score

def add_number():#随机选择添加数字(finished
    number_type = random.randint(0,3)
    if number_type == 0:
        add_num = 4
    else:
        add_num = 2
    return add_num

def add_add(obj,x_max=3,y_max=3):#选择位置并添加数字(finished
    zero_location =[]#记录零所在的位置
    for y_ind,y_obj in enumerate(obj):
        for x_ind,x_obj in enumerate(y_obj):
            if x_obj == 0:
                zero_location.extend([[x_ind,y_ind]])
    location_ind=random.randint(0,len(zero_location)-1)#用随机数确定位置
    #下面一行是将add_number()生成的数字插入field
    obj[zero_location[location_ind][0]][zero_location[location_ind][1]] = add_number()
    return obj

def print_screen(field,score):#打印屏幕(finished
    print('--------------------')
    print('your score is:',score)
    print('%d\t%d\t%d\t%d'%(field[0][0],field[0][1],field[0][2],field[0][3]))
    print('%d\t%d\t%d\t%d'%(field[1][0],field[1][1],field[1][2],field[1][3]))
    print('%d\t%d\t%d\t%d'%(field[2][0],field[2][1],field[2][2],field[2][3]))
    print('%d\t%d\t%d\t%d'%(field[3][0],field[3][1],field[3][2],field[3][3]))

def operates():#决定输入操作(finished
    operate = input('whats your operate:')
    return operate

def leftward(obj,score):#使field向左滑动(finished
    for ind,y_obj in enumerate(obj):
        num_zero = y_obj.count(0)
        for i in range(0,num_zero):#使数字全部滑到左侧，怀疑bug可能在此处
            obj[ind].remove(0)#怀疑bug可能为我没查到的remove用法，可能性小
            obj[ind].append(0)
        #之后三个if都是使数字逐级相加合并，怀疑bug可能在此处
        #bug可能为field的更新问题
        if y_obj[0] == y_obj[1]:
            obj[ind][0] = y_obj[0] + y_obj[1]
            score += obj[ind][0]
            obj[ind][1] = obj[ind][2]
            obj[ind][2] = obj[ind][3]
            obj[ind][3] = 0
        if y_obj[1] == y_obj[2]:
            obj[ind][1] = y_obj[1] +y_obj[2]
            score += obj[ind][1]
            obj[ind][2] = obj[ind][3]
            obj[ind][3] = 0
        if y_obj[2] == y_obj[3]:
            obj[ind][2] = y_obj[2] + y_obj[3]
            score += obj[ind][2]
            obj[ind][3] = 0
    return obj,score

def Fl2r(obj):#转换field方向（左到右）(finished
    for ind,y_obj in enumerate(obj):
        y_obj.reverse()
        obj[ind] = y_obj
    return obj

def Fl2u(obj):#转换field方向（左到上）(finished
    temp = list(zip(obj[0],obj[1],obj[2],obj[3]))
    obj = []
    for each in temp:
        obj.extend([list(each)])
    return obj
        
def final_operate(field,score):#翻译操作符为具体操作函数(finished
    #我认为bug不可能在此处
    while True:
        operate = operates()
        if operate == 'a':
            field,score = leftward(field,score)
            break
        elif operate == 'w':
            field = Fl2u(field)
            field,score = leftward(field,score)
            field = Fl2u(field)
            break
        elif operate == 'd':
            field = Fl2r(field)
            field,score = leftward(field,score)
            field = Fl2r(field)
            break
        elif operate == 's':
            field = Fl2u(field)
            field = Fl2r(field)
            field,score = leftward(field,score)
            field = Fl2r(field)
            field = Fl2u(field)
            break
        else:
            print('please input w,s,a,d\nmeans up,down,left,right')
            continue
    return field,score

def main(key=0):#主函数
    field,score = restart()
    print_screen(field,score)
    while True:
        tmp = copy.deepcopy(field)
        field,score = final_operate(field,score)
        if tmp != field:
            temp =copy.deepcopy(field)
            #上一行的deepcopy是我对避免bug的一个尝试，但未解决
            #我怀疑为添加的数字将正常数字替换掉而导致bug
            field = add_add(temp)
            print_screen(field,score)
        else:
            print('This move has no efficient')
        zero_number = 0#对field中的空位进行检测
        for each in field:
            zero_number = field.count(0)
        if zero_number != 0:
            print('game over')
            ope = input('do you want play again?')
            if ope == 'y':
                field,score = restart()
                print_screen(field,score)
                continue
            else:
                break

if __name__ == '__main__':
    main()