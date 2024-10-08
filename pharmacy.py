import tkinter as tk
from tkinter import ttk, messagebox
import pymysql


class medicine():
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Management")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root, text="Pharmacy Management System",fg="green", bd=4, relief="solid", bg=self.clr(160,160,160), font=("Arial",50,"bold"))
        title.pack(side="top", fill="x")

        # add Frame

        addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(150,220,150))
        addFrame.place(width=self.width/3, height=self.height-180, x=15, y=100)

        medLbl = tk.Label(addFrame, bg=self.clr(150,220,150), text="Medicine:", font=("Arial",15,"bold"))
        medLbl.grid(row=0, column=0, padx=20, pady=30)
        self.medIn = tk.Entry(addFrame, width=20, bd=2, font=("Arial",15))
        self.medIn.grid(row=0, column=1, padx=10, pady=30)

        priceLbl = tk.Label(addFrame, bg=self.clr(150,220,150), text="Price:", font=("Arial",15,"bold"))
        priceLbl.grid(row=1, column=0, padx=20, pady=30)
        self.priceIn = tk.Entry(addFrame, width=20, bd=2, font=("Arial",15))
        self.priceIn.grid(row=1, column=1, padx=10, pady=30)

        quantLbl = tk.Label(addFrame, bg=self.clr(150,220,150), text="Quantity:", font=("Arial",15,"bold"))
        quantLbl.grid(row=2, column=0, padx=20, pady=30)
        self.quantIn= tk.Entry(addFrame, width=20, bd=2, font=("Arial",15))
        self.quantIn.grid(row=2, column=1, padx=10, pady=30)

        expLbl = tk.Label(addFrame, bg=self.clr(150,220,150), text="Expiry:", font=("Arial",15,"bold"))
        expLbl.grid(row=3, column=0, padx=20, pady=30)
        self.expIn = tk.Entry(addFrame, width=20, bd=2, font=("Arial",15))
        self.expIn.grid(row=3, column=1, padx=10, pady=30)

        addBtn = tk.Button(addFrame,command=self.addFun, text="Add Medicine", width=20, font=("Arial",20,"bold"), bd=2, relief="raised")
        addBtn.grid(row=4,column=0, padx=30, pady=40, columnspan=2)

        # detail Frame 

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(150,150,220))
        self.detFrame.place(width=self.width/3+100, height=self.height-180, x=self.width/3+30, y=100)

        detLbl = tk.Label(self.detFrame, text="Medicine Details", bd=4, relief="groove", bg=self.clr(150,200,200), font=("Arial",30,"bold"))
        detLbl.pack(side="top", fill="x")

        self.tabFun()

        # Button Frame

        btnFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(220,150,150))
        btnFrame.place(width=self.width/4-65, height=self.height-180, x=self.width-280, y=100)

        srchBtn = tk.Button(btnFrame,command=self.searchFun, text="Search",width=12,bd=3,relief="raised", font=("Arial",18,"bold"))
        srchBtn.grid(row=0, column=0, padx=30, pady=40)

        saleBtn = tk.Button(btnFrame,command=self.saleFun, text="Sale",width=12,bd=3,relief="raised", font=("Arial",18,"bold"))
        saleBtn.grid(row=1, column=0, padx=30, pady=40)

        updBtn = tk.Button(btnFrame,command=self.updFun, text="Update",width=12,bd=3,relief="raised", font=("Arial",18,"bold"))
        updBtn.grid(row=2, column=0, padx=30, pady=40)

        allBtn = tk.Button(btnFrame,command=self.showAll, text="Show_All",width=12,bd=3,relief="raised", font=("Arial",18,"bold"))
        allBtn.grid(row=3, column=0, padx=30, pady=40)

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken")
        tabFrame.place(width=self.width/3+60, height=self.height-280, x=17, y=70)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame,xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("med","price","quant","exp") )
        
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("med", text="Medicine")
        self.table.heading("price", text="Price")
        self.table.heading("quant", text="Quantity")
        self.table.heading("exp", text="Expiry")
        self.table["show"]="headings"

        self.table.column("med", width=150)
        self.table.column("price", width=120)
        self.table.column("quant", width=100)
        self.table.column("exp", width=150)
        
        self.table.pack(fill="both", expand=1)

    def addFun(self):
        med = self.medIn.get()
        p = self.priceIn.get()
        q = self.quantIn.get()
        exp = self.expIn.get()

        if med and p and q and exp:
            price = int(p)
            quant = int(q)
            try:
                self.dbFun()
                self.cur.execute("insert into medics(medicine,price,quant,exp) values(%s,%s,%s,%s)",
                                 (med,price,quant,exp))
                self.con.commit()
                tk.messagebox.showinfo("Success",f"Medicine {med} is added Successfuly!")
                self.cur.execute("select * from medics where medicine=%s",med)
                row = self.cur.fetchone()
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END, values=row)

                self.medIn.delete(0,tk.END)
                self.priceIn.delete(0,tk.END)
                self.quantIn.delete(0,tk.END)
                self.expIn.delete(0,tk.END)

                self.con.close()
            except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")

        else:
            tk.messagebox.showerror("Error","Please Fill All Input Fields!")

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()

    def searchFun(self):
        self.srchFrame = tk.Frame(self.root,bd=5,relief="ridge", bg="light gray")
        self.srchFrame.place(width=self.width/3, height=self.height-400, x=self.width-720, y=100)

        lbl = tk.Label(self.srchFrame, text="Medicine", bg="light gray", font=("Arial",20,"bold"))
        lbl.grid(row=0, column=0, padx=20, pady=50)
        self.searchIn = tk.Entry(self.srchFrame, width=20, bd=2, font=("Arial",15,"bold"))
        self.searchIn.grid(row=0, column=1, padx=10, pady=50)

        btn = tk.Button(self.srchFrame,command=self.searchMed, text="Ok", width=20, font=("Arial",20,"bold"))
        btn.grid(row=1,column=0, columnspan=2, padx=30, pady=50)

    def searchMed(self):
        med = self.searchIn.get()
        try:
            self.dbFun()
            self.cur.execute("select * from medics where medicine=%s",med)
            info = self.cur.fetchone()
            if info:
                self.tabFun()
                self.table.delete(*self.table.get_children())
                self.table.insert('',tk.END, values=info)

                self.con.close()
                self.srchFrame.destroy()

            else:
                tk.messagebox.showerror("Error","Your Entered Medicine Does Not Exist!")

        
        except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")

    def saleFun(self):
        self.saleFrame = tk.Frame(self.root,bd=5,relief="ridge", bg="light gray")
        self.saleFrame.place(width=self.width/3, height=self.height-400, x=self.width-720, y=100)

        lbl = tk.Label(self.saleFrame, text="Medicine", bg="light gray", font=("Arial",20,"bold"))
        lbl.grid(row=0, column=0, padx=20, pady=30)
        self.saleIn = tk.Entry(self.saleFrame, width=20, bd=2, font=("Arial",15,"bold"))
        self.saleIn.grid(row=0, column=1, padx=10, pady=30)

        lbl2 = tk.Label(self.saleFrame, text="Quantity", bg="light gray", font=("Arial",20,"bold"))
        lbl2.grid(row=1, column=0, padx=20, pady=30)
        self.saleQuant = tk.Entry(self.saleFrame, width=20, bd=2, font=("Arial",15,"bold"))
        self.saleQuant.grid(row=1, column=1)

        btn = tk.Button(self.saleFrame,command=self.saleMed, text="Ok", width=20, font=("Arial",20,"bold"))
        btn.grid(row=2,column=0, columnspan=2, padx=30, pady=40)

    def saleMed(self):
        med = self.saleIn.get()
        quant = int(self.saleQuant.get())
        try:
            self.dbFun()
            self.cur.execute("select price,quant from medics where medicine=%s",med)
            row = self.cur.fetchone()
            if row:
                if row[1] >=quant:
                    upd = row[1]-quant
                    amount = row[0]*quant
                    self.cur.execute("update medics set quant=%s where medicine=%s",(upd,med))
                   
                    self.con.commit()
                    tk.messagebox.showinfo("Success",f"Your have Purchased {quant} {med}\nPay {amount} for this Medicine")
                    self.cur.execute("select * from medics where medicine=%s",med)
                    data = self.cur.fetchone()
                    self.tabFun()
                    self.table.delete(*self.table.get_children())
                    self.table.insert('',tk.END, values=data)
                    self.saleFrame.destroy()

                    self.con.close()
                else:
                    tk.messagebox.showerror("Error","Your Entered Medicine is Out of Stock!")

            else:
                tk.messagebox.showerror("Error","Your Entered Medicine Does Not Exist!")

        except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")

    def updFun(self):
        self.updFrame = tk.Frame(self.root,bd=5,relief="ridge", bg="light gray")
        self.updFrame.place(width=self.width/3, height=self.height-400, x=self.width-720, y=100)

        lbl = tk.Label(self.updFrame, text="Medicine", bg="light gray", font=("Arial",20,"bold"))
        lbl.grid(row=0, column=0, padx=20, pady=30)
        self.updIn = tk.Entry(self.updFrame, width=20, bd=2, font=("Arial",15,"bold"))
        self.updIn.grid(row=0, column=1, padx=10, pady=30)

        lbl2 = tk.Label(self.updFrame, text="Quantity", bg="light gray", font=("Arial",20,"bold"))
        lbl2.grid(row=1, column=0, padx=20, pady=30)
        self.updQuant = tk.Entry(self.updFrame, width=20, bd=2, font=("Arial",15,"bold"))
        self.updQuant.grid(row=1, column=1)

        btn = tk.Button(self.updFrame,command=self.updMed, text="Ok", width=20, font=("Arial",20,"bold"))
        btn.grid(row=2,column=0, columnspan=2, padx=30, pady=40)

    def updMed(self):
        med = self.updIn.get()
        quant = int(self.updQuant.get())

        try:

            self.dbFun()
            self.cur.execute("select quant from medics where medicine=%s",med)
            data = self.cur.fetchone()
            newQuant = data[0]+quant
            self.cur.execute("update medics set quant=%s where medicine=%s",(newQuant,med))
            self.con.commit()

            tk.messagebox.showinfo("Success",f"{quant} Quantity is added for Medicine {med}")

            self.cur.execute("select * from medics where medicine=%s",med)
            row= self.cur.fetchone()

            self.tabFun()
            self.table.delete(*self.table.get_children())
            self.table.insert('',tk.END, values=row)
            self.updFrame.destroy()

            self.con.close()

        except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")

    def showAll(self):
        try:
            self.dbFun()
            self.cur.execute("select * from medics")
            data = self.cur.fetchall()
            self.tabFun()
            self.table.delete(*self.table.get_children())

            for i in data:
                 self.table.insert('',tk.END,values=i)

            self.con.close()

        except Exception as e:
                tk.messagebox.showerror("Error",f"Error: {e}")

    def clr(self, r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"

root = tk.Tk()
obj = medicine(root)
root.mainloop()