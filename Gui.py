import tkinter as tk
import CoinMarketCap
import Portfolio_Calculator
import Price_Alert
import Data_Analyzer
import CandleSticks
import Pump_Dump
import Binance_Analyzer
import Future
import threading
from tkmacosx import Button
import warnings
import sys


warnings.filterwarnings("ignore")
sys.tracebacklimit = 0


def start_thread(event, target):
    global submit_thread
    submit_thread = threading.Thread(target=target)
    submit_thread.daemon = True
    submit_thread.start()


def open1():
    top1 = tk.Toplevel()
    top1.geometry("400x200")
    top1.minsize(400, 200)
    top1.maxsize(400, 200)
    top1.title("CoinMarketCap Clone")
    pic = tk.PhotoImage(file="Images/coinmarketcap.png")
    image = Button(top1, width=430, height=220, image=pic)
    image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    startbtn = Button(top1, text="Run Application", command=lambda: start_thread(None, CoinMarketCap.MyFunc1),
                      bg="grey", fg="white").place(x=40, y=150)
    stopbtn = Button(top1, text="Stop Application", command=top1.destroy, bg="grey", fg="white").place(x=220, y=150)


def open2():
    top2 = tk.Toplevel()
    top2.geometry("400x200")
    top2.minsize(400, 200)
    top2.maxsize(400, 200)
    top2.title("Portfolio Calculator")
    pic = tk.PhotoImage(file="Images/portfolio.png")
    image = Button(top2, width=430, height=220, image=pic)
    image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    startbtn = Button(top2, text="Run Application", command=lambda: start_thread(None, Portfolio_Calculator.MyFunc2),
                      bg="grey", fg="white").place(x=40, y=150)
    stopbtn = Button(top2, text="Stop Application", command=top2.destroy, bg="grey", fg="white").place(x=220, y=150)


def open3():
    top3 = tk.Toplevel()
    top3.geometry("400x200")
    top3.minsize(400, 200)
    top3.maxsize(400, 200)
    top3.title("Cryptocurrency Price Alert")
    pic = tk.PhotoImage(file="Images/price alert.png")
    image = Button(top3, width=430, height=220, image=pic)
    image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    startbtn = Button(top3, text="Run Application", command=Price_Alert.MyFunc3,
                      bg="grey", fg="white").place(x=40, y=150)
    stopbtn = Button(top3, text="Stop Application", command=top3.destroy, bg="grey", fg="white").place(x=220, y=150)


def open4():
    top4 = tk.Toplevel()
    top4.geometry("400x200")
    top4.minsize(400, 200)
    top4.maxsize(400, 200)
    top4.title("Simple Data Analyzer")
    pic = tk.PhotoImage(file="Images/simple DA .png")
    image = Button(top4, width=430, height=220, image=pic)
    image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    startbtn = Button(top4, text="Run Application", command=lambda: start_thread(None, Data_Analyzer.MyFunc4),
                      bg="grey", fg="white").place(x=40, y=150)
    stopbtn = Button(top4, text="Stop Application", command=top4.destroy, bg="grey", fg="white").place(x=220, y=150)


def open5():
    top5 = tk.Toplevel()
    top5.geometry("400x200")
    top5.minsize(400, 200)
    top5.maxsize(400, 200)
    top5.title("Candlesticks")
    pic = tk.PhotoImage(file="Images/candlesticks.png")
    image = Button(top5, width=430, height=220, image=pic)
    image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    startbtn = Button(top5, text="Run Application", command=lambda: start_thread(None, CandleSticks.MyFunc5()),
                      bg="grey", fg="white").place(x=40, y=150)
    stopbtn = Button(top5, text="Stop Application", command=top5.destroy, bg="grey", fg="white").place(x=220, y=150)


def open6():
    top6 = tk.Toplevel()
    top6.geometry("400x200")
    top6.minsize(400, 200)
    top6.maxsize(400, 200)
    top6.title("Pump And Dump Bot")
    pic = tk.PhotoImage(file="Images/tradingbot.png")
    image = Button(top6, width=430, height=220, image=pic)
    image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    startbtn = Button(top6, text="Run Application", command=lambda: start_thread(None, Pump_Dump.MyFunc6),
                      bg="grey", fg="white").place(x=40, y=150)
    stopbtn = Button(top6, text="Stop Application", command=top6.destroy, bg="grey", fg="white").place(x=220, y=150)


def open7():
    top7 = tk.Toplevel()
    top7.geometry("400x200")
    top7.minsize(400, 200)
    top7.maxsize(400, 200)
    top7.title("Advanced Data Analyzer")
    pic = tk.PhotoImage(file="Images/advanced DA.png")
    image = Button(top7, width=430, height=220, image=pic)
    image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    startbtn = Button(top7, text="Run Application", command=lambda: start_thread(None, Binance_Analyzer.MyFunc7),
                      bg="grey", fg="white").place(x=40, y=150)
    stopbtn = Button(top7, text="Stop Application", command=top7.destroy, bg="grey", fg="white").place(x=220, y=150)


def open8():
    top8 = tk.Toplevel()
    top8.geometry("400x200")
    top8.minsize(400, 200)
    top8.maxsize(400, 200)
    top8.title("Future Price Predictor")
    pic = tk.PhotoImage(file="Images/future.png")
    image = Button(top8, width=430, height=220, image=pic)
    image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    startbtn = Button(top8, text="Run Application", command=lambda: start_thread(None, Future.MyFunc8),
                      bg="grey", fg="white").place(x=40, y=150)
    #command=Future.MyFunc8
    stopbtn = Button(top8, text="Stop Application", command=top8.destroy, bg="grey", fg="white").place(x=220, y=150)


root = tk.Tk()
root.geometry("960x450")
root.minsize(960, 450)
root.maxsize(960, 450)
root.title("Trading Master")
picture = tk.PhotoImage(file="Images/Image1.png")
image = tk.Button(root, width=960, height=450, image=picture)
image.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

label1 = tk.Label(root, text="CRYPTOCURRENCY TRADING SYSTEM", pady=10, fg="white", bg="black",
                  font="Verdana 20 bold").pack()
picture2 = tk.PhotoImage(file="Images/Image2.png")

btn1 = Button(root, image=picture2, text="CoinMarketCap Clone", compound=tk.LEFT, bg="black", fg="white",
              command=open1).place(x=400, y=70)
btn2 = Button(root, image=picture2, text="Portfolio Calculator", compound=tk.LEFT, bg="black", fg="white",
              command=open2).place(x=650, y=70)

btn3 = Button(root, image=picture2, text="Cryptocurrency Price Alert", compound=tk.LEFT, bg="black", fg="white",
              command=open3).place(x=650, y=270)

btn4 = Button(root, image=picture2, text="Simple Data Analyzer", compound=tk.LEFT, bg="black", fg="white",
              command=open4).place(x=560, y=120)
btn5 = Button(root, image=picture2, text="CandleStick Graph", compound=tk.LEFT, bg="black", fg="white",
              command=open5).place(x=400, y=170)

btn6 = Button(root, image=picture2, text="Pump and Dump Bot", compound=tk.LEFT, bg="black", fg="white",
              command=open6).place(x=650, y=170)

btn7 = Button(root, image=picture2, text="Advanced Data Analyzer", compound=tk.LEFT, bg="black", fg="white",
              command=open7).place(x=520, y=220)
btn8 = Button(root, image=picture2, text="Future Price Predictor", compound=tk.LEFT, bg="black", fg="white",
              command=open8).place(x=400, y=270)

btn9 = Button(root, image=picture2, text="Quit", compound=tk.LEFT, bg="black", fg="white",
              command=sys.exit).place(x=830, y=10)

root.mainloop()
