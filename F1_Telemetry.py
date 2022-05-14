import matplotlib.pyplot as plt
import fastf1.plotting
import os
import tkinter as tk

def get_data(gp, year, stype, lap_nr, driver, X, Y):

    pwd = os.getcwd()
    if not (os.path.exists(pwd + '/doc_cache')):
        os.mkdir(pwd + "/doc_cache")



    fastf1.Cache.enable_cache(pwd + '/doc_cache')  # replace with your cache directory

    # enable some matplotlib patches for plotting timedelta values and load
    # FastF1's default color scheme
    fastf1.plotting.setup_mpl()

    try:
        # load a session and its telemetry data
        session = fastf1.get_session(int(year), gp, stype)
        session.load()


        if lap_nr == "F":
            lap = session.laps.pick_driver(driver).pick_fastest()
        else:
            lap = session.laps.pick_driver(driver).iloc[int(lap_nr)-1]


        tel = lap.get_car_data().add_distance().add_differential_distance().add_relative_distance().add_driver_ahead()
    except Exception as e:
            tk.messagebox.showerror('Error', e)

    make_plot(tel = tel, driver = driver, session = session, stype=stype, lap_nr = lap_nr, X = X, Y = Y)



def make_plot(tel, driver, session, stype, lap_nr, X, Y):

    color = fastf1.plotting.driver_color(driver)

    if lap_nr == "F":
        lap_nr = "fastest"

    fig, ax = plt.subplots()
    ax.plot(tel[X], tel[Y], color=color, label=driver)

    ax.set_xlabel(X)
    ax.set_ylabel(Y)

    ax.legend()
    plt.suptitle(f"{X} vs. {Y} Plot \n "
                 f"{session.event['EventName']} {session.event.year} {session.event.get_session_name(stype)} Lap {lap_nr}")

    plt.show()


def main():

    color1 = "#555555"
    color2 = "#777777"

    window = tk.Tk()
    window.title("F1 Telemetry")
    window.configure(bg=color2)



    options = ["RelativeDistance", "Time", "SessionTime", "Date", "DifferentialDistance", "Distance", "DriverAhead", "Speed", "RPM", "nGear", "Throttle", "Brake", "DRS"]

    tk.Label(text="Grand Prix Name:",anchor="w",width=25, bg=color2, fg= "white").grid(row=0,column=0, padx=5, pady=5)

    gp_entry = tk.Entry(bg=color1, fg= "white")
    gp_entry.grid(row=0,column=1, padx=5, pady=5)

    tk.Label(text="Grand Prix Year [yyyy]:",anchor="w",width=25, bg=color2, fg= "white").grid(row=1,column=0, padx=5, pady=5)

    yr_entry = tk.Entry(bg=color1, fg= "white")
    yr_entry.grid(row=1,column=1, padx=5, pady=5)

    tk.Label(text="Session [FP1-3, Q, sprint,  R]:",anchor="w",width=25, bg=color2, fg= "white").grid(row=2,column=0, padx=5, pady=5)

    session_entry = tk.Entry(bg=color1, fg= "white")
    session_entry.grid(row=2,column=1, padx=5, pady=5)

    tk.Label(text="Driver [number or abbreviation]:",anchor="w",width=25, bg=color2, fg= "white").grid(row=3,column=0, padx=5, pady=5)

    driver_entry = tk.Entry(bg=color1, fg= "white")
    driver_entry.grid(row=3,column=1, padx=5, pady=5)

    tk.Label(text="Lap [F for fastest or ##]:",anchor="w",width=25, bg=color2, fg= "white").grid(row=4,column=0, padx=5, pady=5)

    lap_entry = tk.Entry(bg=color1, fg= "white")
    lap_entry.grid(row=4,column=1, padx=5, pady=5)

    tk.Label(text="X Axis:", anchor="w", width=25, bg=color2, fg= "white").grid(row=5, column=0, padx=5, pady=5)

    x_val = tk.StringVar()
    x_val.set(options[0])

    x_drop = tk.OptionMenu(window, x_val, *options)
    x_drop.configure(width=15, bg=color1, fg= "white",highlightthickness=0)
    x_drop.grid(row=5,column=1, padx=5, pady=5)

    tk.Label(text="Y Axis:", anchor="w", width=25, bg=color2, fg= "white").grid(row=6, column=0, padx=5, pady=5)

    y_val = tk.StringVar()
    y_val.set(options[7])

    y_drop = tk.OptionMenu(window, y_val, *options)
    y_drop.grid(row=6,column=1, padx=5, pady=5)
    y_drop.configure(width=15, bg=color1, fg= "white", highlightthickness=0)



    button = tk.Button(text= "Go", bg=color1, fg= "white", command = lambda: get_data(gp=gp_entry.get(), year=yr_entry.get(), stype=session_entry.get(), lap_nr=lap_entry.get(), driver=driver_entry.get(), X= x_val.get(), Y=y_val.get()))
    button.grid(row=7, sticky="ew", columnspan=2, padx=5, pady=5)

    window.mainloop()


if __name__ == '__main__':
    main()