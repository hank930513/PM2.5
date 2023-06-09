def rbCity(): #點選縣市選項按鈕後處理函式
    global sitelist, listradio
    sitelist.clear()    #清除原有測站串列
    for r in listradio: #移除原有測站選項按鈕   
        r.destroy()
    n=0
    for c1 in data["county"]:   #逐一取出選取縣式的測站
        if(c1 == city.get()):
            site1=data.iloc[n, 0]
            if(site1 not in sitelist):
                sitelist.append(site1)
        n += 1
    sitemake()
    rbSite()

def rbSite():
    n=0
    for s in data.iloc[:, 0]:   #逐一取得測站
        if(s == site.get()):    #取得選取點選的測站
            pm = data.iloc[n,2] #取的pm2.4的值
            if(pm=='' or pm=='ND'):  #如果沒有資料
                result1.set(s + "站的PM2.5值目前無資料!")
            else:   #如果有資料
                if(int(pm)<=35):    #轉換等級
                    grade1 = "低"
                elif(int(pm)<=53):
                    grade1 = "中"
                elif(int(pm)<=70):
                    grade1 = "高"
                else:
                    grade1 = "非常高"
                result1.set(s + "站的PM2.5值為【"+str(pm)+"】:【"+grade1+"】等級ˊ")
            break
        n+=1
def clickRefresh(): #重新讀取資料
    global data
    data = pd.read_csv("https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV")
    rbSite()    #更新測站資料
def sitemake():
    global sitelist,listradio
    for c1 in sitelist: #逐一建立選項按鈕
        rbtem = tk.Radiobutton(frame2, text=c1,variable=site,
            value=c1, command=rbSite)
        listradio.append(rbtem) #加入選項按鈕串列
        if(c1==sitelist[0]):    #預設選取第1個項目
            rbtem.select()
        rbtem.pack(side="left") 
import tkinter as tk
import pandas as pd
data = pd.read_csv("https://data.epa.gov.tw/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&sort=datacreationdate%20desc&format=CSV")

win=tk.Tk()
win.geometry("800x270")
win.title("PM2.5 監測") 

city = tk.StringVar()#縣市文字變數
site = tk.StringVar()#測站文字變數
result1 = tk.StringVar() #訊息文字變數  
citylist = [] #縣市串列 
sitelist = [] #鄉鎮串列
listradio = [] #鄉鎮選項按鈕串列

#建立縣市串列
for c1 in data["county"]:
    if(c1 not in citylist): #如果串列中無該縣市就將其加入
        citylist.append(c1)
#建立第一個縣市的測站串列
count = 0
for c1 in data["county"]:
    if(c1 == citylist[0]):  #第1個縣市的測站
        site1 = data.iloc[count, 0]
        if(site1 not in sitelist):
            sitelist.append(site1)
    count +=1

lable1 = tk.Label(win, text="縣市",pady=9, fg="blue",
    font=("新細明體",12))
lable1.pack()
frame1 = tk.Frame(win)  #縣市容器
frame1.pack()
for i in range(0,3):    #3列選項按鈕   
    for j in range(0,8):    #每列8個選項按鈕
        n = i*8+j #第n個選項按鈕
        if(n< len(citylist)):
            city1 = citylist[n] #取得縣市名稱
            rbtem = tk.Radiobutton(frame1, text=city1, variable=city,
                value=city1, command=rbCity) #建立選項按鈕 
            rbtem.grid(row=i, column=j)     #設定選項按鈕位置       
            if(n==0): #選去第一個縣市
                rbtem.select()

lable2 = tk.Label(win, text="測站",pady=6, fg="blue",
    font=("新細明體",12))
lable2.pack()
frame2 = tk.Frame(win)  #測站容器
frame2.pack()
sitemake()

btnDown = tk.Button(win,text="更新資料",font=("新細明體",12)
             , command=clickRefresh) #建立選項按鈕 
btnDown.pack(pady=6)
lblResult1 = tk.Label(win,  textvariable=result1, fg="red"
        ,font=("新細明體",16))
lblResult1.pack(pady=6)
rbSite()

win.mainloop()