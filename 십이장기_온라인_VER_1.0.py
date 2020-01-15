import firebase_admin, turtle, time
from firebase_admin import credentials, db
from random import randint, choice

Key=107 ,101 ,121 ,46 ,106 ,115 ,111 ,110
Url=104 ,116 ,116 ,112 ,115 ,58 ,47 ,47 ,97 ,112 ,112 ,105 ,111 ,116 ,116 ,46 ,102 ,105 ,114 ,101 ,98 ,97 ,115 ,101 ,105 ,111 ,46 ,99 ,111 ,109 ,47
Cred=credentials.Certificate(''.join([chr(i) for i in Key]))
firebase_admin.initialize_app(Cred, {'databaseURL':''.join([chr(i) for i in Url])})

Ref=None #경로 기본값
Roomnumber=None #방 번호 기본값

level='??'
Version='1.0.1'
Left_d=0 #판 전체 왼쪽으로 이동
Down_d=0 #판 전체 아래로 이동
Sizeofsqare=160 #사각형 하나의 크기
Sizeofsqare2=100 #내가 잡은 말의 크기
Beginning_font='타이포_꾸미기 입체채움' #게임시작폰트
Game_font='Arial' #장기말 폰트

#Gamestart=0 #게임이 시작되면 1
Dont_click=0 #얘가 1이면 터치가 안됨

Turn=-1 #선후공 결정(초기값) 1이 선공, 0이 후공
Check=0 #체크 상태
Check_x=Check_y=0
Choice=0 #말 선택
Choice_x=Choice_y=0

Can={} #갈 수 있는 행마 저장
My_piece=[] #내가 갖고 있는 포로
Your_piece=[] #상대가 갖고 있는 포로


turtle.tracer(False)

T=turtle.Pen()
Highlight=turtle.Pen()
S=T.getscreen()

My_piece_t=turtle.Pen()
My_piece_t.ht()
My_piece_t.pu()
My_piece_t.pensize(5)
My_piece_t.speed(0)
Your_piece_t=turtle.Pen()
Your_piece_t.ht()
Your_piece_t.pu()
Your_piece_t.pensize(5)
Your_piece_t.speed(0)

My_piece_xy=Sizeofsqare*1.6+Sizeofsqare2*.1-Left_d, -Sizeofsqare*2+Sizeofsqare2*1.2-Down_d
My_piece_t.goto(*My_piece_xy)

Your_piece_xy=-Sizeofsqare*1.6-Sizeofsqare2*3.3, Sizeofsqare*2-Sizeofsqare2*1.1
Your_piece_t.goto(*Your_piece_xy)

Highlight.ht()
Highlight.pu()
Highlight.speed(0)

Emoji_list=['♂♀','§§','☞☜','ΞΞ','◐◑','XX','☣☣','☢☢','❦❧','[]','¿？','『』','【】',
    '☯☯','♝♞','♚♛','☸☸','☪☪','⌠⌡',('༼༽','༼༽'),'☫☬','✿❀','☤☤','♨♨',]
class jang:
    def __init__(self, Turn):
        self.T=turtle.Pen() #각각에 대해 turtle 생성
        self.T.pu()
        self.T.speed(0)
        self.T.ht()
        self.Turn=Turn #자신의 팀을 지정함
        self.Realname='將'
        self.Name='장'

class king:
    def __init__(self, Turn):
        self.T=turtle.Pen()
        self.T.pu()
        self.T.speed(0)
        self.T.ht()
        self.Turn=Turn
        self.Realname='王'
        self.Name='왕'

class sang:
    def __init__(self, Turn):
        self.T=turtle.Pen()
        self.T.pu()
        self.T.speed(0)
        self.T.ht()
        self.Turn=Turn
        self.Realname='相'
        self.Name='상'

class za:
    def __init__(self, Turn):
        self.T=turtle.Pen()
        self.T.pu()
        self.T.speed(0)
        self.T.ht()
        self.Turn=Turn
        self.Realname='子'
        self.Name='자'

#My_piece=[jang(1),jang(1)]
Gamebored=[
[jang(0),king(0),sang(0)],
[0, za(0), 0],
[0, za(1), 0],
[sang(1),king(1),jang(1)]
]

#사각형 그리는 함수, 매개변수는 가로, 세로, turtle 객체, [펜 굵기, 텍스트, 폰트, 폰트사이즈, 색깔]
def Draw_sqare(Width, Depth, Turtle, Pensize=7, Text='', Font='', Fontsize=80, Color='black'):
    Turtle.pu()
    Turtle.speed(0)
    Turtle.ht()
    Turtle.pensize(Pensize)
    Turtle.color(Color)
    Turtle.fd(Width/2)
    Turtle.write(Text, move=False, align='center', font=(Font, Fontsize, 'normal'))
    Turtle.bk(Width/2)
    Turtle.pd()
    if Width>0 and Depth>0:
        for i in range(4):
            Turtle.fd(Width if i%2==0 else Depth)
            Turtle.left(90)
    Turtle.pu()

#현재 자신의 포로를 다 그리는 함수
def Draw_turn_piece(Turn):
    turtle.tracer(False)
    if Turn:
        My_piece_t.clear()
        My_piece_t.goto(*My_piece_xy)
        for i in range(len(My_piece)):
            print(i)
            Draw_sqare(Sizeofsqare2, Sizeofsqare2, My_piece_t, 7, Text=My_piece[i].Realname, Font=Game_font, Fontsize=int(Sizeofsqare2*.6), Color='blue' if Turn else 'red')
            My_piece_t.fd(Sizeofsqare2*1.1)
            if i==2:
                My_piece_t.goto(My_piece_t.xcor()-Sizeofsqare2*3.3, My_piece_t.ycor()-Sizeofsqare2*1.1)
    else:
        Your_piece_t.clear()
        Your_piece_t.goto(*Your_piece_xy)
        for i in range(len(Your_piece)):
            Draw_sqare(Sizeofsqare2, Sizeofsqare2, Your_piece_t, 7, Text=Your_piece[i].Realname, Font=Game_font, Fontsize=int(Sizeofsqare2*.6), Color='blue' if Turn else 'red')
            Your_piece_t.fd(Sizeofsqare2*1.1)
            if i==2:
                Your_piece_t.goto(Your_piece_t.xcor()-Sizeofsqare2*3.3, Your_piece_t.ycor()-Sizeofsqare2*1.1)
    turtle.tracer(True)

#선후공 창띄우는 함수
def Set_turn(Font, T):
    T.ht()
    T.speed(0)
    T.pu()
    T.goto(0,0)
    T.color('#%06x'%(randint(0,0xFFFFFF)))
    Emoji=tuple(choice(Emoji_list))
    T.write('%s십이장기%s'%Emoji, move=False, align='center', font=(Beginning_font,240,'normal'))
    turtle.title('십이장기')
    T.color('black')
    T.goto(0,-50)
    T.write('↓선후공을 골라 주세요↓', move=False, align='center', font=(Beginning_font,50,'normal'))
    T.goto(-400,-200)
    Draw_sqare(370, 100, T, 7, '선공하기♪', Font, 80, 'blue')
    T.goto(60,-200)
    Draw_sqare(370, 100, T, 7, '후공하기♬', Font, 80, 'red')
    T.color('black')
    T.goto(0,-300)
    T.write('ONLINE VER %s'%Version, move=False, align='center', font=(Beginning_font,50,'normal'))
    T.goto(0,-350)
    T.write('Made by 김서윤 ©', move=False, align='center', font=(Beginning_font,30,'normal'))
    #T.write('-제 %s단계 ai-'%단계, move=False, align='center', font=(Beginning_font,50,'normal'))

#게임판 그리는 함수
def Screen(T):
    T.ht()
    T.speed(0)
    T.goto(-Sizeofsqare*1.5, -Sizeofsqare*2)
    T.begin_fill()
    Draw_sqare(Sizeofsqare*3, Sizeofsqare, T, Pensize=1, Text='', Font='', Fontsize=80, Color='#B1CDFC')
    T.end_fill()
    T.goto(-Sizeofsqare*1.5, Sizeofsqare)
    T.begin_fill()
    Draw_sqare(Sizeofsqare*3, Sizeofsqare, T, Pensize=1, Text='', Font='', Fontsize=80, Color='#FCC2F1')
    T.end_fill()
    T.pensize(7)
    T.color('black')
    for i in range(-2,3):
        T.pu()
        T.goto(-1.5*Sizeofsqare-Left_d, i*Sizeofsqare-Down_d)
        T.pd()
        T.fd(Sizeofsqare*3)
    T.right(90)
    for i in range(-1,3):
        T.pu()
        T.goto((i-.5)*Sizeofsqare-Left_d, 2*Sizeofsqare-Down_d)
        T.pd()
        T.fd(4*Sizeofsqare)
    T.pu()
    T.left(90)
    for i in range(4):
        for j in range(3):
            K=Gamebored[i][j]
            if K!=0:
                exec('{0}.goto({2},{1}-Sizeofsqare*.4)'.format('K.T', Pos_y_r(i, Down_d), Pos_x_r(j, Left_d)))
                Draw_sqare(0, 0, K.T, 7, Text=K.Realname, Font=Game_font, Fontsize=int(Sizeofsqare*.5), Color='blue' if K.Turn else 'red')
    #따먹은 기물 표시
    T.goto(Sizeofsqare*1.6, -Sizeofsqare*2+Sizeofsqare2*2.3)
    T.write('플레이어 1의 기물', move=True, align='left', font=(Beginning_font, int(Sizeofsqare2*.5), 'normal'))
    T.goto(Sizeofsqare*1.6, -Sizeofsqare*2)
    Draw_sqare(Sizeofsqare2*3.4, Sizeofsqare2*2.3, T, 7, Text='', Font=Game_font, Fontsize=int(Sizeofsqare*.5), Color='black')
    T.goto(-Sizeofsqare*1.6, Sizeofsqare*2-Sizeofsqare2*3)
    T.write('플레이어 2의 기물', move=True, align='right', font=(Beginning_font, int(Sizeofsqare2*.5), 'normal'))
    T.goto(-Sizeofsqare*1.6-Sizeofsqare2*3.4, Sizeofsqare*2-Sizeofsqare2*2.3)
    Draw_sqare(Sizeofsqare2*3.4, Sizeofsqare2*2.3, T, 7, Text='', Font=Game_font, Fontsize=int(Sizeofsqare*.5), Color='black')
    Draw_turn_piece(0)
    Draw_turn_piece(1)

def Highlighter(Turn, X, Y, option=0):
    Highlight.pu()
    Highlight.speed(0)
    Highlight.clear()
    turtle.tracer(False)
    if option:
        Highlight.goto(X, Y)
        Highlight.dot(Sizeofsqare2*.3, 'black')
        for i,j in Can[-1]:
            Highlight.goto(Pos_x_r(j,Left_d), Pos_y_r(i,Down_d))
            Highlight.dot(Sizeofsqare*.1, '#424242')
    else:
        Highlight.goto(Pos_x_r(X,Left_d+Sizeofsqare*.4), Pos_y_r(Y,Down_d+Sizeofsqare*.4))
        Draw_sqare(Sizeofsqare*.8, Sizeofsqare*.8, Highlight, Pensize=7, Text='', Font='', Fontsize=80, Color='red' if Turn else 'blue')
        for i,j in Can[(Y, X)]:
            Highlight.goto(Pos_x_r(j,Left_d), Pos_y_r(i,Down_d))
            Highlight.dot(Sizeofsqare*.1, '#424242')
    turtle.tracer(True)

#클릭한 x좌표를 칸 x좌표로 바꾸는 용도
def Pos_x(X, Left_d):
    for i in range(3):
        if Sizeofsqare*(i-1.5)-Left_d<=X<=Sizeofsqare*(i-.5)-Left_d:
            return i
    return -1

def Pos_y(Y, Down_d):
    for i in range(4):
        if Sizeofsqare*(-i+1)-Down_d<=Y<=Sizeofsqare*(-i+2)-Down_d:
            return i
    return -1

#칸 X, Y 좌표를 turtle 좌표로 변환, Pos_x함수의 역함수라는 의미
def Pos_x_r(X, Left_d):
    return Sizeofsqare*(X-1)-Left_d

def Pos_y_r(Y ,Down_d):
    return Sizeofsqare*(-Y+1.5)-Down_d

#턴 상태, X좌표, Y좌표
def Start(Turn, Y, X):
    global Check_x, Check_y
    Highlight.clear()
    if Gamebored[Y][X]: #이 if문은 따먹은 말 처리함
        K=Gamebored[Y][X]
        if K.Name=='후':
            K.Name='자'
            K.Realname='子'
        K.Turn=Turn
        K.T.clear()
        turtle.tracer(False)
        if Turn:
            My_piece.append(K)
            if len(My_piece)==4:
                My_piece_t.goto(My_piece_t.xcor()-Sizeofsqare2*3.3, My_piece_t.ycor()-Sizeofsqare2*1.1)
            Draw_sqare(Sizeofsqare2, Sizeofsqare2, My_piece_t, 7, Text=My_piece[-1].Realname, Font=Game_font, Fontsize=int(Sizeofsqare2*.6), Color='blue' if Turn else 'red')
            My_piece_t.fd(Sizeofsqare2*1.1)
        else:
            Your_piece.append(K)
            if len(Your_piece)==4:
                Your_piece_t.goto(Your_piece_t.xcor()-Sizeofsqare2*3.3, Your_piece_t.ycor()-Sizeofsqare2*1.1)
            Draw_sqare(Sizeofsqare2, Sizeofsqare2, Your_piece_t, 7, Text=Your_piece[-1].Realname, Font=Game_font, Fontsize=int(Sizeofsqare2*.6), Color='blue' if Turn else 'red')
            Your_piece_t.fd(Sizeofsqare2*1.1)
        turtle.tracer(True)
    Gamebored[Y][X]=Gamebored[Choice_y][Choice_x] #새로 Gamebored를 바꿈
    Gamebored[Choice_y][Choice_x]=0
    K=Gamebored[Y][X]
    if K.Name=='자': #자가 끝까지 도달하면 후로 바꿈
        if (Turn==1 and Y==0) or (Turn==0 and Y==3):
            K.Name='후'
            K.Realname='侯'
    K.T.clear() #모니터 시각화
    exec('{0}.goto({2},{1}-Sizeofsqare*.4)'.format('K.T', Pos_y_r(Y, Down_d), Pos_x_r(X, Left_d)))
    Draw_sqare(0, 0, K.T, 7, Text=K.Realname, Font=Game_font, Fontsize=int(Sizeofsqare*.5), Color='blue' if K.Turn else 'red')
    Check_ques=Piece_go(K.Name, Y, X, K.Turn)
    print("Check_ques=", Check_ques)
    for i,j in Check_ques:
        if Gamebored[i][j] and Gamebored[i][j].Name=='왕' and Gamebored[i][j].Turn!=Turn:
            Check_x, Check_y=X, Y
            print("Checked!")
            return 1
    print("Not Checked!")
    Check_x=Check_y=None
    return 0

#말 놓을 때 쓰는 함수, 턴 상태, Y, X, 리스트 (인덱스는 전역변수 Choice_y)
def Start2(Turn, Y, X, List):
    global Check_x, Check_y
    Highlight.clear()
    K=List[Choice_y]
    del List[Choice_y]
    Gamebored[Y][X]=K
    exec('{0}.goto({2},{1}-Sizeofsqare*.4)'.format('K.T', Pos_y_r(Y, Down_d), Pos_x_r(X, Left_d)))
    Draw_sqare(0, 0, K.T, 7, Text=K.Realname, Font=Game_font, Fontsize=int(Sizeofsqare*.5), Color='blue' if K.Turn else 'red')
    Draw_turn_piece(Turn)
    Check_ques=Piece_go(K.Name, Y, X, K.Turn)
    print("Check_ques=", Check_ques)
    for i,j in Check_ques:
        if Gamebored[i][j] and Gamebored[i][j].Name=='왕' and Gamebored[i][j].Turn!=Turn:
            Check_x, Check_y=X, Y
            print("Checked!")
            return 1
    print("Not Checked!")
    Check_x=Check_y=None
    return 0

#Turn 일때 갈수있는 모든 좌표들
def Can_go(Turn, Check, Check_x, Check_y, Gamebored):
    Can.clear()
    Opponent=[] #내 왕이 갈 수 없는 좌표 모음
    for i in range(4):
        for j in range(3):
            K=Gamebored[i][j] #(Y,X)
            if K and K.Turn!=Turn:
                Opponent+=Piece_go(K.Name, i, j, K.Turn)
    for i in range(4):
        for j in range(3):
            Go=[]
            K=Gamebored[i][j] #(Y,X)
            if K and K.Turn==Turn:
                for Y,X in Piece_go(K.Name, i, j, K.Turn): #1차적으로 갈 수 있는곳 걸러냄
                    if K.Name=='왕':
                        if (Gamebored[Y][X]==0 or Gamebored[Y][X].Turn!=Turn) and ((Y,X) not in Opponent):
                            Go.append((Y, X))
                    else:
                        if Check==1:
                            if Y==Check_y and X==Check_x:
                                Go.append((Y,X))
                        else:
                            if Gamebored[Y][X]==0 or Gamebored[Y][X].Turn!=Turn:
                                Go.append((Y,X))
            else:
                continue
            Can[(i, j)]=Go
    Go=[]
    if Check==0 and (My_piece if Turn else Your_piece):
        for i in range(4):
            for j in range(3):
                if (i!=0 and Gamebored[i][j]==0 and Turn) or (i!=3 and Gamebored[i][j]==0 and not Turn):
                    Go.append((i,j))
    Can[-1]=Go


Bored_reverse=lambda F: (3-F[0],2-F[1])
Right=lambda F: 0<=F[0]<=3 and 0<=F[1]<=2

def Piece_go(Name, Y, X, Turn):
    if Name=='자':
        if Turn:
            K=(Y-1,X), #끝에 , 떼면 절! 대! 안됨(튜플 자료형)
        else:
            K=(Y+1,X),
    elif Name=='장':
        K=(Y+1,X),(Y-1,X),(Y,X+1),(Y,X-1)
    elif Name=='상':
        K=(Y+1,X+1),(Y-1,X+1),(Y+1,X-1),(Y-1,X-1)
    elif Name=='왕':
        K=[(Y+i,X+j) for i in [-1,0,1] for j in [-1,0,1] if not(i==0 and j==0)]
    elif Name=='후':
        K=[(Y+i,X+j) for i in [-1,0,1] for j in [-1,0,1] if not(i==0 and j==0)]
        if Turn:
            K.remove((Y+1,X-1))
            K.remove((Y+1,X+1))
        else:
            K.remove((Y-1,X-1))
            K.remove((Y-1,X+1))
    return list(filter(Right, K))

def Checkmate(Turn, Y=None, X=None): #Turn이 체크메이트를 시켰는지 확인(당한 게 아님)
    if not any(Can.values()):
        Win_message(Turn)
        return True
    elif Y!=None:
        if Gamebored[Y][X] and Gamebored[Y][X].Name=='왕' and Y==(0 if Turn else 3):
            Win_message(Turn)
            return True
    return False

def Win_message(Win_turn):
    T.goto(0,-Sizeofsqare*.6)
    T.color('purple')
    T.write('승리!!' if Turn==Win_turn else '패배..', move=False, align='center', font=(Beginning_font, int(Sizeofsqare*1.2), 'normal'))

def Return(X, Y):
    global Turn, Choice, Choice_x, Choice_y, Check, Dont_click
    global Roomnumber, Ref
    if Dont_click:
        return
    if Turn==-1:
        if -200<Y<-100:
            if -400<X<-30:
                Turn=1 #선공
            elif 30<X<400:
                Turn=0 #후공
            else:
                return
            Dont_click=1
            Ref=db.reference('gameroom') #온라인 연결
            Dic=Ref.get()
            for i in Dic:
                if Dic[i]['user%s'%Turn]==0:
                    Roomnumber=Dic[i]['roomnumber']
                    Ref=db.reference('gameroom/game%d'%Roomnumber)
                    Ref.update({'user%d'%Turn:1})
                    T.clear()
                    T.goto(0,0)
                    T.write('로딩중...', move=False, align='center', font=(Beginning_font, 50, 'normal'))
                    T.goto(0,-50)
                    T.write('%d번 채널 입장(%s)'%(Roomnumber,'선공' if Turn else '후공'), move=False, align='center',font=(Beginning_font, 30, 'normal'))
                    while Ref.get()['user%d'%(int(not Turn))]!=1:
                        time.sleep(0.2)
                    break
            else:
                T.clear()
                T.goto(0,0)
                T.write('방이 부족합니다. 나중에 다시 접속해주세요.', move=False, align='center', font=(Beginning_font, 30, 'normal'))
                return
            Dont_click=0
        else:
            return
        Dont_click=1
        Can_go(Turn, 0, 0, 0, Gamebored[:])
        T.clear()
        Screen(T)
        if not Turn: #후공일시 대기
            Loading()
        Dont_click=0
    elif Turn==Ref.get()['turn']:
        #단순히 말 클릭해서 옮길 때
        Dont_click=1
        if -Sizeofsqare*1.5<=X<=Sizeofsqare*1.5 and -Sizeofsqare*2<=Y<=Sizeofsqare*2:
            X=Pos_x(int(X), Left_d)
            Y=Pos_y(int(Y), Down_d)#들어온 값을 정수 값으로 리턴
            if not (0<=X<=2 and 0<=Y<=3):
                Highlight.clear()
                Choice=False
                Dont_click=0
                return
            if Choice==True:
                #print(Can)
                if (Y,X) in Can[(Choice_y, Choice_x)]:
                    Check=Start(Turn, Y, X) #Start함수는 말을 옮기고 check 값을 반환함
                    Can_go(int(not Turn), Check, Check_x, Check_y, Gamebored[:])
                    Choice=False
                    Ref.update({'movement':'%d %d %d %d'%(Choice_y, Choice_x, Y, X), 'turn':int(not Turn)})
                    if Checkmate(Turn, Y, X):
                        return
                    #맨 마지막에 상대가 갈 수 있는 위치 저장함(말 옮기면서 턴 종료하는 부분)
                    Loading()
                elif Gamebored[Y][X] and Gamebored[Y][X].Turn==Turn:
                    Highlighter(Turn, X, Y)
                    Choice_y, Choice_x=Y, X
                    Choice=True
            elif Choice==(True,):
                if (Y,X) in Can[-1]:
                    Check=Start2(Turn, Y, X, My_piece if Turn else Your_piece) #Start2 함수는 말을 놓고 check값을 반환함
                    Can_go(int(not Turn), Check, Check_x, Check_y, Gamebored[:])
                    Choice=False #Choice_x에 -1이 들어감
                    Ref.update({'movement':'%d %d %d %d'%(Choice_y, Choice_x, Y, X), 'turn':int(not Turn)})
                    if Checkmate(Turn):
                        return
                    #맨 마지막에 상대가 갈 수 있는 위치 저장함(포로 소환하면서 턴 종료하는 부분)
                    Loading()
                elif Gamebored[Y][X] and Gamebored[Y][X].Turn==Turn:
                    Highlighter(Turn, X, Y)
                    Choice_y, Choice_x=Y, X
                    Choice=True
            elif Gamebored[Y][X] and Gamebored[Y][X].Turn==Turn:
                Highlighter(Turn, X, Y)
                Choice_y, Choice_x=Y, X
                Choice=True
        #포로 선택할 때
        elif Turn:
            if Sizeofsqare*1.6<=X+Left_d<=Sizeofsqare*1.6+Sizeofsqare2*3.4 and -Sizeofsqare*2<=Y+Down_d<=-Sizeofsqare*2+Sizeofsqare2*2.3:
                for i in range(len(My_piece)):
                    My_piece_x, My_piece_y=My_piece_xy
                    Start_x, End_x=My_piece_x+Sizeofsqare2*(i%3)*1.1-Left_d, My_piece_x+Sizeofsqare2*(i%3*1.1+1)-Left_d
                    Start_y, End_y=My_piece_y+(0 if 0<=i<=2 else -Sizeofsqare2*1.1)-Down_d, My_piece_y+Sizeofsqare2*(1 if 0<=i<=2 else -.1)-Down_d
                    if Start_x<=X<=End_x and Start_y<=Y<=End_y:
                        break
                else:
                    Dont_click=0
                    return
                Highlighter(Turn, (Start_x+End_x)/2, (Start_y+End_y)/2, option=1)
                Choice=True,
                Choice_x=-1
                Choice_y=i
        else:
            if -Sizeofsqare*1.6-Sizeofsqare2*3.4<=X<=-Sizeofsqare*1.6 and Sizeofsqare*2-Sizeofsqare2*2.3<=Y<=Sizeofsqare*2:
                for i in range(len(Your_piece)):
                    Your_piece_x, Your_piece_y=Your_piece_xy
                    Start_x, End_x=Your_piece_x+Sizeofsqare2*(i%3)*1.1-Left_d, Your_piece_x+Sizeofsqare2*(i%3*1.1+1)-Left_d
                    Start_y, End_y=Your_piece_y+(0 if 0<=i<=2 else -Sizeofsqare2*1.1)-Down_d, Your_piece_y+Sizeofsqare2*(1 if 0<=i<=2 else -.1)-Down_d
                    if Start_x<=X<=End_x and Start_y<=Y<=End_y:
                        break
                else:
                    Dont_click=0
                    return
                Highlighter(Turn, (Start_x+End_x)/2, (Start_y+End_y)/2, option=1)
                Choice=True,
                Choice_x=-1
                Choice_y=i
        Dont_click=0

def Loading():
    global Choice_y, Choice_x
    while Ref.get()['turn']!=Turn:
        time.sleep(0.2)
    Choice_y, Choice_x, Y, X=map(int,Ref.get()['movement'].split())
    Check=Start2(not Turn, Y, X, My_piece if not Turn else Your_piece) if Choice_x==-1 else Start(not Turn, Y, X)
    Can_go(Turn, Check, Check_x, Check_y, Gamebored[:])
    Checkmate(not Turn, Y, X) if Choice_x==-1 else Checkmate(not Turn)



if __name__=='__main__':
    #value=turtle.textinput("","닉네임을 입력해 주세요")
    Dont_click=1
    Set_turn(Beginning_font,T) #선후공 창띄우기
    S.onclick(Return)#클릭 시 RETURN 함수 실행
    Dont_click=0
    turtle.tracer(1)
    turtle.mainloop()
