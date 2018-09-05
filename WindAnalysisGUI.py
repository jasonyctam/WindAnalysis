__author__ = "Jason Tam"
import datetime as dt
import time
from os import path
import numpy as np
import subprocess
import tkinter
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
from tkinter.filedialog import asksaveasfilename
import seaborn as sns

import numpy as np
plt.ion() # Turning interactive mode on
import sys

from WindAnalysis import WindAnalysis

###################################################################
###################################################################
###################################################################
###################################################################

class WindAnalysis_GUI:
    
    def __init__(self, master):
        self.master = master
        self.master.title("Wind Data Analysis")
        self.master.geometry("1000x700")
        self.loadFileSuccessful = False

        #self.configFilePath = 'filepaths.conf'
        #self.filePaths = self.getFilePaths(self.configFilePath)
        
        # Create top frame box for path inputs
        self.topFrame = tkinter.Frame()

        # Create main frame box for lists and buttons
        self.mainFrame = tkinter.Frame()

        # Create bottom frame box
        self.bottomFrame = tkinter.Frame()
        
        # Add frame for path to raw data file
        self.F_RawData = tkinter.Frame(self.topFrame)
        self.rawFilePathBox = tkinter.Entry(self.F_RawData, width=80)
        
        #self.addFilePathBox(self.F_RawData, self.rawFilePathBox, "Path to Raw data file", self.filePaths['RAWDATAFILE'])
        self.addFilePathBox(self.F_RawData, self.rawFilePathBox, "Path to Raw data file", '')
        
        # Add frame for load raw file button
        self.F_loadFileButton = tkinter.Frame(self.F_RawData)

        # Define button for load raw file
        self.loadFileBut = tkinter.Button(self.F_loadFileButton, text="Load File", fg="green", command=lambda: self.loadFile())

        # Adding the load raw file button to the GUI
        self.loadFileBut.pack(side=tkinter.TOP, expand=tkinter.YES)

        self.F_loadFileButton.pack(side=tkinter.RIGHT)

        # Add frame for dropdown boxes for load options
        self.F_loadOptions = tkinter.Frame(self.mainFrame)
        
        # Set width for dropdown boxes
        self.loadOptionsDropBoxWidth = 10
        
        # Create frame date column selection
        self.F_DateCol = tkinter.Frame(self.F_loadOptions)
        
        self.DateColTitle = tkinter.Label(self.F_DateCol, text="Date: ")
        self.DateColTitle.pack(side=tkinter.LEFT)
        
        self.DateColString = tkinter.StringVar(self.F_DateCol)
        self.DateColString.set("") # default value
        self.DateColDropDown = tkinter.OptionMenu(self.F_DateCol, self.DateColString,"")
        self.DateColDropDown.config(width=self.loadOptionsDropBoxWidth)
        self.DateColDropDown.pack(side=tkinter.LEFT)
        
        # Create frame date column selection
        self.F_TimeCol = tkinter.Frame(self.F_loadOptions)
        
        self.TimeColTitle = tkinter.Label(self.F_TimeCol, text="Time: ")
        self.TimeColTitle.pack(side=tkinter.LEFT)
        
        self.TimeColString = tkinter.StringVar(self.F_TimeCol)
        self.TimeColString.set("")
        self.TimeColDropDown = tkinter.OptionMenu(self.F_TimeCol, self.TimeColString,"")
        self.TimeColDropDown.config(width=self.loadOptionsDropBoxWidth)
        self.TimeColDropDown.pack(side=tkinter.LEFT)
        
        # Create frame date column selection
        self.F_DirCol = tkinter.Frame(self.F_loadOptions)
        
        self.DirColTitle = tkinter.Label(self.F_DirCol, text="Wind direction: ")
        self.DirColTitle.pack(side=tkinter.LEFT)
        
        self.DirColString = tkinter.StringVar(self.F_DirCol)
        self.DirColString.set("")
        self.DirColDropDown = tkinter.OptionMenu(self.F_DirCol, self.DirColString,"")
        self.DirColDropDown.config(width=self.loadOptionsDropBoxWidth)
        self.DirColDropDown.pack(side=tkinter.LEFT)
        
        # Create frame date column selection
        self.F_SpeedCol = tkinter.Frame(self.F_loadOptions)
        
        self.SpeedColTitle = tkinter.Label(self.F_SpeedCol, text="Wind speed: ")
        self.SpeedColTitle.pack(side=tkinter.LEFT)
        
        self.SpeedColString = tkinter.StringVar(self.F_SpeedCol)
        self.SpeedColString.set("") # default value
        self.SpeedColDropDown = tkinter.OptionMenu(self.F_SpeedCol, self.SpeedColString,"")
        self.SpeedColDropDown.config(width=self.loadOptionsDropBoxWidth)
        self.SpeedColDropDown.pack(side=tkinter.LEFT)
        
        # Add frame for Update Raw Files list button
        self.F_loadResultsButton = tkinter.Frame(self.F_loadOptions)

        # Define button for updating the raw files list
        self.loadResultsBut = tkinter.Button(self.F_loadResultsButton, text="Load Results", fg="blue", command=lambda: self.loadResults())

        # Adding the update files button to the GUI
        self.loadResultsBut.pack(side=tkinter.TOP, expand=tkinter.YES)
        
        self.F_DateCol.pack(side=tkinter.LEFT)
        self.F_TimeCol.pack(side=tkinter.LEFT)
        self.F_DirCol.pack(side=tkinter.LEFT)
        self.F_SpeedCol.pack(side=tkinter.LEFT)
        self.F_loadResultsButton.pack(side=tkinter.RIGHT)
        self.F_loadOptions.pack()
        
        self.nb = ttk.Notebook(self.mainFrame, width=950, height=580)
        self.tab_OutputData = ttk.Frame(self.nb)   # first tab
        self.tab_DailyAVG = ttk.Frame(self.nb)   # second tab
        self.tab_HourlyAVG = ttk.Frame(self.nb)   # third tab
        self.tab_TimeSeries = ttk.Frame(self.nb)   # forth tab

        self.nb.add(self.tab_OutputData, text='Instructions and Results')
        self.nb.add(self.tab_DailyAVG, text='Daily Averages')
        self.nb.add(self.tab_HourlyAVG, text='Hourly Averages')
        self.nb.add(self.tab_TimeSeries, text='Time Series')

        
        ##################################################################
        #### First tab
        ##################################################################
        
        ###### Instructions Box ########
        
        # Add frame for instructions box
        self.F_InsBox = tkinter.Frame(self.tab_OutputData)
        self.InsBox_ListTitle = tkinter.Label(self.F_InsBox, text="Instructions")
        self.InsBox_ListTitle.pack(side=tkinter.TOP)        
        self.instructionsBox = tkinter.Text(self.F_InsBox, width=130, height=20)
        self.instructions = """1) Please choose an input file at the top of the window, and press "Load File".
    - This will populate the four drop-down boxes near the top with column headers of the input file.
2) Please choose the associated header from the drop-down boxes respectively for Date, Time, Wind Direction and Wind Speed, and press "Load Results".
    - This will populate the components in all of the tabs, including the box on this tab that displays the data gaps.
    - An error message will prompt and interrupt this process if a duplicate timestamp is present in the input file.
    - The user will be required to remove the duplicate manually and restart his process.
3) Graphing tools have been implemented in the other tabs for data inspection.
    - The green arrow in the polar plots represent the averaged result
    - The yellow arrows represent the data used to calculate the average.
    - The hourly averages are calculated using data at 10-min intervals (input)
    - The daily averages are calculated using the computed hourly averages.
    - The arrows point to where the wind blows to, while the heading in both the input data and the graph title is where the wind comes from.
4) Tabulated results can be saved as a CSV or XLS file through this tab.
    - The U and V components can be included in the result file via the check box.
    - Please ensure the file extension is entered as part of the file name (Windows)
    
    
Author: Jason Tam
"""
        self.instructionsBox.insert(tkinter.INSERT, self.instructions)
        self.instructionsBox.config(state=tkinter.DISABLED)
        self.instructionsBox.bind("<1>", lambda event: self.instructionsBox.focus_set())
        self.instructionsBox.pack()
        self.F_InsBox.pack(side=tkinter.TOP)
        
        # Add frame for saving components
        #self.F_saveComp = tkinter.Frame(self.tab_OutputData)
        
        # Add frame for path to raw data file
        self.F_OutputFile = tkinter.Frame(self.tab_OutputData)
        self.outputFilePathBox = tkinter.Entry(self.F_OutputFile, width=80)
        
        self.addFilePathBox(self.F_OutputFile, self.outputFilePathBox, "Path to output file",'','save')
        
        self.F_saveOptions = tkinter.Frame(self.tab_OutputData)
        
        # Add Check box for xcomp and ycomp data in result file
        self.Check_UVComp = tkinter.IntVar()
        self.Check_UVCompBox = tkinter.Checkbutton(self.F_saveOptions, text="U,V components", variable=self.Check_UVComp)
        
        self.Check_UVCompBox.pack(side=tkinter.LEFT)
        
        # Add frame for load raw file button
        self.F_saveFileButton = tkinter.Frame(self.F_saveOptions)

        # Define button for load raw file
        self.saveCSVFileBut = tkinter.Button(self.F_saveFileButton, text="Save results to file", fg="green", command=lambda: self.saveToFile(self.outputFilePathBox))

        # Adding the load raw file button to the GUI
        self.saveCSVFileBut.pack(side=tkinter.TOP, expand=tkinter.YES)

        self.F_saveFileButton.pack(side=tkinter.LEFT)
        self.F_saveOptions.pack()
        
        self.F_DataGap_Terminal = tkinter.Frame(self.tab_OutputData)
        
        ###### Data Gap Box ########
        # Add frame for Data Gaps
        self.F_DataGap = tkinter.Frame(self.F_DataGap_Terminal)

        # Add scrollbar
        self.DataGap_ListScrollbar = tkinter.Scrollbar(self.F_DataGap)

        # Add box to list the data gaps
        self.DataGap_ListBox = tkinter.Listbox(self.F_DataGap, width=30, exportselection=0, height=10)
        self.DataGap_ListTitle = tkinter.Label(self.F_DataGap, text="Data Gaps")
        self.DataGap_ListTitle.pack(side=tkinter.TOP)

        # Putting the scrollbar on the right
        self.DataGap_ListScrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # Putting the list box to the left
        self.DataGap_ListBox.pack(side=tkinter.TOP, fill=tkinter.Y)

        # Linking between the scollbar and the list box
        self.DataGap_ListScrollbar['command'] = self.DataGap_ListBox.yview
        self.DataGap_ListBox['yscrollcommand'] = self.DataGap_ListScrollbar.set
        
        ###### Terminal ########
        '''
        # Add frame for instructions box
        self.F_Terminal = tkinter.Frame(self.F_DataGap_Terminal)
        
        # Add scrollbar
        self.terminal_Scrollbar = tkinter.Scrollbar(self.F_Terminal)
        self.termainal_Title = tkinter.Label(self.F_Terminal, text="Terminal output")
        self.termainal_Title.pack(side=tkinter.TOP)        
        self.terminalBox = tkinter.Text(self.F_Terminal, width=70, height=11)
        #self.terminalBox.insert(tkinter.INSERT, '')
        self.terminalBox.config(state=tkinter.DISABLED)
        self.terminalBox.bind("<1>", lambda event: self.instructionsBox.focus_set())

        # Putting the scrollbar on the right
        self.terminal_Scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        
        # Linking between the scollbar and the list box
        self.terminal_Scrollbar['command'] = self.terminalBox.yview
        self.terminalBox['yscrollcommand'] = self.terminal_Scrollbar.set
        self.terminalBox.pack(side=tkinter.TOP, fill=tkinter.Y)
        '''
        
        ###### Packing ########
        self.F_DataGap.pack()#side=tkinter.LEFT)
        #self.F_Terminal.pack(side=tkinter.LEFT)
        self.F_DataGap_Terminal.pack()
        
        ##################################################################
        #### Second tab
        ##################################################################
        
        self.F_DailySelectionPanel = tkinter.Frame(self.tab_DailyAVG)
        
        ############# List box ################
        
        # Add frame for Dates List
        self.F_DailyAVG_Dates = tkinter.Frame(self.F_DailySelectionPanel)

        # Add scrollbar
        self.DailyAVG_dateListScrollbar = tkinter.Scrollbar(self.F_DailyAVG_Dates)

        # Add box to list the files
        self.DailyAVG_dateListBox = tkinter.Listbox(self.F_DailyAVG_Dates)
        self.DailyAVG_dateListTitle = tkinter.Label(self.F_DailyAVG_Dates, text="Dates")
        self.DailyAVG_dateListTitle.pack(side=tkinter.TOP)

        # Putting the scrollbar on the right
        self.DailyAVG_dateListScrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # Putting the list box to the left
        self.DailyAVG_dateListBox.pack(side=tkinter.TOP, fill=tkinter.Y)

        # Linking between the scollbar and the list box
        self.DailyAVG_dateListScrollbar['command'] = self.DailyAVG_dateListBox.yview
        self.DailyAVG_dateListBox['yscrollcommand'] = self.DailyAVG_dateListScrollbar.set

        ############# Plot Button ################
        
        # Add frame for plot button
        self.F_DailyAVG_plotButton = tkinter.Frame(self.F_DailySelectionPanel)
        
        # Add plot button
        self.DailyAVG_plotButton = tkinter.Button(self.F_DailyAVG_plotButton, text="Plot", command=lambda: self.plotDailyData(self.DailyAVG_canvas,self.DailyAVG_ax))
        self.DailyAVG_plotButton.pack()
        
        ############# Pop-out Plot Button ################
        
        # Add frame for plot button
        self.F_DailyAVG_popPlotButton = tkinter.Frame(self.F_DailySelectionPanel)
        
        # Add plot button
        self.DailyAVG_popPlotButton = tkinter.Button(self.F_DailyAVG_popPlotButton, text="Pop-out Plot", command=lambda: self.plotDailyDataPop())
        self.DailyAVG_popPlotButton.pack()

        ############# Plot ################
        
        # Add frame for plot
        self.F_DailyAVG_plot = tkinter.Frame(self.tab_DailyAVG)
        
        #self.DailyAVG_fig = plt.figure(figsize=(6,6))
        self.DailyAVG_fig = Figure(figsize=(6,6))
        self.DailyAVG_ax = self.DailyAVG_fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        self.DailyAVG_ax.set_theta_zero_location("N")
        self.DailyAVG_ax.set_theta_direction(-1)
        self.DailyAVG_canvas = FigureCanvasTkAgg(self.DailyAVG_fig,self.F_DailyAVG_plot)
        
        # Pack F_DailyAVG_Dates to the left of mainFrame
        self.F_DailyAVG_Dates.pack()
        self.F_DailyAVG_popPlotButton.pack()
        self.F_DailyAVG_plotButton.pack()
        self.F_DailyAVG_plot.pack(side=tkinter.RIGHT)
        self.F_DailySelectionPanel.pack()

        self.DailyAVG_canvas.get_tk_widget().pack()
        self.DailyAVG_canvas.draw()

        ##################################################################
        #### Third tab
        ##################################################################
        
        ############# List boxes ################
        
        # Add frame for Dates and Times List
        self.F_HourlyAVG_DateTimes = tkinter.Frame(self.tab_HourlyAVG)
        
        ###### Date box ########
        # Add frame for Dates List
        self.F_HourlyAVG_Dates = tkinter.Frame(self.F_HourlyAVG_DateTimes)

        # Add scrollbar
        self.HourlyAVG_dateListScrollbar = tkinter.Scrollbar(self.F_HourlyAVG_Dates)

        # Add box to list the files
        self.HourlyAVG_dateListBox = tkinter.Listbox(self.F_HourlyAVG_Dates, exportselection=0)
        self.HourlyAVG_dateListTitle = tkinter.Label(self.F_HourlyAVG_Dates, text="Dates")
        self.HourlyAVG_dateListTitle.pack(side=tkinter.TOP)

        # Putting the scrollbar on the right
        self.HourlyAVG_dateListScrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # Putting the list box to the left
        self.HourlyAVG_dateListBox.pack(side=tkinter.TOP, fill=tkinter.Y)

        # Linking between the scollbar and the list box
        self.HourlyAVG_dateListScrollbar['command'] = self.HourlyAVG_dateListBox.yview
        self.HourlyAVG_dateListBox['yscrollcommand'] = self.HourlyAVG_dateListScrollbar.set

        ###### Hour box ########
        # Add frame for Dates List
        self.F_HourlyAVG_Hours = tkinter.Frame(self.F_HourlyAVG_DateTimes)

        # Add scrollbar
        self.HourlyAVG_hourListScrollbar = tkinter.Scrollbar(self.F_HourlyAVG_Hours)

        # Add box to list the files
        self.HourlyAVG_hourListBox = tkinter.Listbox(self.F_HourlyAVG_Hours, exportselection=0)
        self.HourlyAVG_hourListTitle = tkinter.Label(self.F_HourlyAVG_Hours, text="Hours")
        self.HourlyAVG_hourListTitle.pack(side=tkinter.TOP)

        # Putting the scrollbar on the right
        self.HourlyAVG_hourListScrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

        # Putting the list box to the left
        self.HourlyAVG_hourListBox.pack(side=tkinter.TOP, fill=tkinter.Y)

        # Linking between the scollbar and the list box
        self.HourlyAVG_hourListScrollbar['command'] = self.HourlyAVG_hourListBox.yview
        self.HourlyAVG_hourListBox['yscrollcommand'] = self.HourlyAVG_hourListScrollbar.set
        
        ############# Plot Button ################
        
        # Add frame for plot button
        self.F_HourlyAVG_plotButton = tkinter.Frame(self.F_HourlyAVG_DateTimes)
        
        # Add plot button
        self.HourlyAVG_plotButton = tkinter.Button(self.F_HourlyAVG_plotButton, text="Plot", command=lambda: self.plotHourlyData(self.HourlyAVG_canvas,self.HourlyAVG_ax))
        self.HourlyAVG_plotButton.pack()
        
        ############# Pop-out Plot Button ################
        # Add frame for plot button
        self.F_HourlyAVG_popPlotButton = tkinter.Frame(self.F_HourlyAVG_DateTimes)
        
        # Add plot button
        self.HourlyAVG_popPlotButton = tkinter.Button(self.F_HourlyAVG_popPlotButton, text="Pop-out Plot", command=lambda: self.plotHourlyDataPop())
        self.HourlyAVG_popPlotButton.pack()
        
        self.F_HourlyAVG_Dates.pack(side=tkinter.TOP)
        self.F_HourlyAVG_Hours.pack()
        self.F_HourlyAVG_plotButton.pack(side=tkinter.BOTTOM)
        self.F_HourlyAVG_popPlotButton.pack(side=tkinter.BOTTOM)
        
        ############# Plot ################
        # Add frame for plot
        self.F_HourlyAVG_plot = tkinter.Frame(self.tab_HourlyAVG)
        
        #self.fig = plt.figure(figsize=(6,6))
        self.HourlyAVG_fig = Figure(figsize=(6,6))
        self.HourlyAVG_ax = self.HourlyAVG_fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        self.HourlyAVG_ax.set_theta_zero_location("N")
        self.HourlyAVG_ax.set_theta_direction(-1)
        self.HourlyAVG_canvas = FigureCanvasTkAgg(self.HourlyAVG_fig,self.F_HourlyAVG_plot)
        
        # Pack F_HourlyAVG_Dates to the left of mainFrame
        self.F_HourlyAVG_plot.pack(side=tkinter.RIGHT)
        self.F_HourlyAVG_DateTimes.pack()
        self.HourlyAVG_canvas.get_tk_widget().pack()#grid(row=0,column=1)
        self.HourlyAVG_canvas.draw()
        
        ##################################################################
        #### Forth tab
        ##################################################################

        ############# List boxes ################
        
        # Create frame for start and end dates selection
        self.F_StartAndEndDates = tkinter.Frame(self.tab_TimeSeries)
        self.startAndEndDateTitle = tkinter.Label(self.F_StartAndEndDates, text="Please choose a time range")
        self.startAndEndDateTitle.pack(side=tkinter.TOP)
        
        self.timeSeriesDropBoxWidth = 10
        
        # Create frame for start date selection
        self.F_StartDate = tkinter.Frame(self.F_StartAndEndDates)
        
        self.startDateTitle = tkinter.Label(self.F_StartDate, text="Start Date")
        self.startDateTitle.pack(side=tkinter.TOP)
        
        self.startDateString = tkinter.StringVar(self.F_StartDate)
        self.startDateString.set("") # default value
        self.startDateDropDown = tkinter.OptionMenu(self.F_StartDate, self.startDateString,"")
        self.startDateDropDown.config(width=self.timeSeriesDropBoxWidth)
        
        # Create frame for start time selection
        self.F_StartTime = tkinter.Frame(self.F_StartAndEndDates)
        
        self.startTimeTitle = tkinter.Label(self.F_StartTime, text="Start Time")
        self.startTimeTitle.pack(side=tkinter.TOP)
        
        self.startTimeString = tkinter.StringVar(self.F_StartTime)
        self.startTimeString.set("")
        self.startTimeDropDown = tkinter.OptionMenu(self.F_StartTime, self.startTimeString, "")
        self.startTimeDropDown.config(width=self.timeSeriesDropBoxWidth)
        
        # Create frame for end date selection
        self.F_EndDate = tkinter.Frame(self.F_StartAndEndDates)
        
        self.endDateTitle = tkinter.Label(self.F_EndDate, text="End Date")
        self.endDateTitle.pack(side=tkinter.TOP)
        
        self.endDateString = tkinter.StringVar(self.F_EndDate)
        self.endDateString.set("")
        self.endDateDropDown = tkinter.OptionMenu(self.F_EndDate, self.endDateString, "")
        self.endDateDropDown.config(width=self.timeSeriesDropBoxWidth)
        
        # Create frame for end time selection
        self.F_EndTime = tkinter.Frame(self.F_StartAndEndDates)
        
        self.endTimeTitle = tkinter.Label(self.F_EndTime, text="End Time")
        self.endTimeTitle.pack(side=tkinter.TOP)
        
        self.endTimeString = tkinter.StringVar(self.F_EndTime)
        self.endTimeString.set("")
        self.endTimeDropDown = tkinter.OptionMenu(self.F_EndTime, self.endTimeString, "")
        self.endTimeDropDown.config(width=self.timeSeriesDropBoxWidth)
        
        ############# Plot Button ################
        
        # Add frame for plot button
        self.F_TimeSeries_plotButton = tkinter.Frame(self.F_StartAndEndDates)
        
        # Add plot button
        self.timeSeries_plotButton = tkinter.Button(self.F_TimeSeries_plotButton, text="Plot", command=lambda: self.refreshTimeSeriesPlots())
        
        ############# Pop-out Plot Button ################
        
        # Add frame for plot button
        self.F_TimeSeries_popPlotButton = tkinter.Frame(self.F_StartAndEndDates)
        
        # Add plot button
        self.timeSeries_popPlotButton = tkinter.Button(self.F_TimeSeries_popPlotButton, text="Pop-out Plot", command=lambda: self.plotTimeSeriesDataPop())
        
        ############# Plot Option Checkboxes ################
        
        self.F_TimeSeries_plotOptions = tkinter.Frame(self.F_StartAndEndDates)
        self.Check_10Min = tkinter.IntVar()
        self.Check_10MinBox = tkinter.Checkbutton(self.F_TimeSeries_plotOptions, text="10 Min Data", variable=self.Check_10Min)
        self.Check_Hourly = tkinter.IntVar()
        self.Check_HourlyBox = tkinter.Checkbutton(self.F_TimeSeries_plotOptions, text="Hourly Data", variable=self.Check_Hourly)
        self.Check_Daily = tkinter.IntVar()
        self.Check_DailyBox = tkinter.Checkbutton(self.F_TimeSeries_plotOptions, text="Daily Data", variable=self.Check_Daily)
        
        self.startDateDropDown.pack()
        self.startTimeDropDown.pack()
        self.endDateDropDown.pack()
        self.endTimeDropDown.pack()
        self.timeSeries_plotButton.pack()
        self.timeSeries_popPlotButton.pack()
        self.Check_10MinBox.pack()
        self.Check_HourlyBox.pack()
        self.Check_DailyBox.pack()

        self.F_StartDate.pack(side=tkinter.TOP)
        self.F_StartTime.pack(side=tkinter.TOP)
        self.F_EndDate.pack(side=tkinter.TOP)
        self.F_EndTime.pack(side=tkinter.TOP)
        self.F_TimeSeries_plotOptions.pack(side=tkinter.TOP)
        self.F_TimeSeries_plotButton.pack(side=tkinter.TOP)
        self.F_TimeSeries_popPlotButton.pack(side=tkinter.TOP)

            
        ############# Plots ################
        # Add frame for plot
        self.F_TimeSeriesPlots = tkinter.Frame(self.tab_TimeSeries)
        
        self.timeSeriesPlotsWidth = 7.8
        self.timeSeriesPlotsHeight = 6
        self.timeSeriesSubPlotsHeight = 1.31
        
        self.windDir_Title = 'Wind Direction'
        self.windSpeed_Title = 'Wind Speed'
        self.windU_Title = 'Wind U Component'
        self.windV_Title = 'Wind V Component'
        self.timeSeries_subPlotTitleSize = 10
        
        self.leftMargin = 0.08
        self.rightMargin = 0.98
        self.bottomMargin = 0.12
        self.topMargin = 0.95
        
        self.timeSeries_fig = Figure(figsize=(self.timeSeriesPlotsWidth,self.timeSeriesPlotsHeight), dpi = 100)
        self.timeSeries_fig.subplots_adjust(left=self.leftMargin,right=self.rightMargin,bottom=self.bottomMargin,top=self.topMargin)
        
        # Add subplots to figure
        self.windDir_ax = self.timeSeries_fig.add_subplot(411)
        self.windSpeed_ax = self.timeSeries_fig.add_subplot(412, sharex=self.windDir_ax)
        self.windU_ax = self.timeSeries_fig.add_subplot(413, sharex=self.windDir_ax)
        self.windV_ax = self.timeSeries_fig.add_subplot(414, sharex=self.windDir_ax)
        
        # Set title to all of the subplots
        self.windDir_ax.set_title(self.windDir_Title, fontsize=self.timeSeries_subPlotTitleSize)
        self.windSpeed_ax.set_title(self.windSpeed_Title, fontsize=self.timeSeries_subPlotTitleSize)
        self.windU_ax.set_title(self.windU_Title, fontsize=self.timeSeries_subPlotTitleSize)
        self.windV_ax.set_title(self.windV_Title, fontsize=self.timeSeries_subPlotTitleSize)
        
        # Set all xaxis to be invisible apart from the bottom
        self.windDir_ax.get_xaxis().set_visible(False)
        self.windSpeed_ax.get_xaxis().set_visible(False)
        self.windU_ax.get_xaxis().set_visible(False)
        
        self.timeSeries_canvas = FigureCanvasTkAgg(self.timeSeries_fig, self.F_TimeSeriesPlots)
        self.timeSeries_canvas.get_tk_widget().pack()
            
        self.F_StartAndEndDates.pack(side=tkinter.LEFT)
        self.F_TimeSeriesPlots.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
        
        ##################################################################
        ##################################################################
        
        self.nb.pack()
        self.topFrame.pack()
        self.mainFrame.pack()
        
        self.close_button = tkinter.Button(master, text="Close", command=self.on_closing)
        self.close_button.pack()

        # Runs on_closing function when close window x button is pressed
        master.protocol("WM_DELETE_WINDOW", self.on_closing)


###################################################################
###################################################################

    def saveToFile(self, textBox):
        
        outputFilePath = self.outputFilePathBox.get()
        uvCompOption = self.Check_UVComp.get()

        if hasattr(self,'windAnalysis'):
            if len(outputFilePath) == 0:
                messagebox.showinfo("Choose Output File", "Please choose an output file")
                self.chooseFile(textBox)
            else:
                if path.exists(outputFilePath):
                    result = messagebox.askyesno("Overwrite existing file", "Are you sure you would like to overwrite an existing file?")
                    if result == True:
                        if self.windAnalysis.writeDataToOutput(outputFilePath, uvCompOption):
                            messagebox.showinfo("Save successful", "Output file saved successfully.")
                    else:
                        self.chooseFile(textBox)
                else:
                    if self.windAnalysis.writeDataToOutput(outputFilePath, uvCompOption):
                        messagebox.showinfo("Save successful", "Output file saved successfully.")
        else:
            messagebox.showinfo("Load file and results", "Please load file and results")
        
        return

###################################################################
###################################################################

    def loadFile(self):
        if self.loadFiles():
            
            print("Loading file...")
            
            self.duplicateFound = False
            
            # Clear existing content from dropdown boxes
            self.DateColDropDown["menu"].delete(0, "end")
            self.TimeColDropDown["menu"].delete(0, "end")
            self.DirColDropDown["menu"].delete(0, "end")
            self.SpeedColDropDown["menu"].delete(0, "end")
            
            # Getting headers from the input file
            headerArray = []
            inputFileArray = self.getFileArray(self.rawDataFileName,",")
            self.trimmedInputFileArray = inputFileArray[2:]

            ## Trim possible quotation marks from the strings
            for m in range(0,len(self.trimmedInputFileArray[0])):
                headerElement = self.trimmedInputFileArray[0][m].replace("\"","")
                headerArray.append(headerElement)
            
            # Insert headers into the dropdown boxes
            for i in range(0,len(headerArray)):
                self.DateColDropDown["menu"].add_command(label=headerArray[i], command=lambda value=headerArray[i]: self.DateColString.set(value))
                self.TimeColDropDown["menu"].add_command(label=headerArray[i], command=lambda value=headerArray[i]: self.TimeColString.set(value))
                self.DirColDropDown["menu"].add_command(label=headerArray[i], command=lambda value=headerArray[i]: self.DirColString.set(value))
                self.SpeedColDropDown["menu"].add_command(label=headerArray[i], command=lambda value=headerArray[i]: self.SpeedColString.set(value))

            for i in range(0,len(headerArray)):
                if "Date" in headerArray[i]:
                    self.DateColString.set(headerArray[i])
                if "Time" in headerArray[i]:
                    self.TimeColString.set(headerArray[i])
                if "WDR_RAW 10min" in headerArray[i]:
                    self.DirColString.set(headerArray[i])
                if "WSP_RAW 10min" in headerArray[i]:
                    self.SpeedColString.set(headerArray[i])
                
            self.loadFileSuccessful = True
            print("File loaded successfully")
                    
        else:
            self.loadFileSuccessful = False
        
        return self.loadFileSuccessful
        
###################################################################
###################################################################

    def getFilePaths(self, configFilePath):
        
        configDict = {}

        with open(configFilePath) as f:
            for line in f:
                if line[0] != '#' :
                    line = line.strip()
                    if line.find(':') != -1 :
                        (key, val) = line.split(':')
                        configDict[key.upper()] = val
        
        return configDict

###################################################################
###################################################################

    def addFilePathBox(self, subFrame, textBox, label, filepath='', function='open'):
        # Add text entry for path to raw data file
        #filePathBox = tkinter.Entry(textBox, width=80)
        filePathBoxTitle = tkinter.Label(subFrame, text=label)
        textBox.insert(0, filepath)
        if function=='save':
            filePathBrowseBut = tkinter.Button(subFrame, text="Browse", command=lambda: self.chooseSaveFile(textBox))
            
        else:
            filePathBrowseBut = tkinter.Button(subFrame, text="Browse", command=lambda: self.chooseFile(textBox))

        # Putting the list box to the left
        filePathBoxTitle.pack(side=tkinter.TOP)
        textBox.pack(side=tkinter.LEFT, fill=tkinter.Y)
        filePathBrowseBut.pack(side=tkinter.LEFT, fill=tkinter.Y)
        
        subFrame.pack()
        
        return

###################################################################
###################################################################
    
    def loadResults(self):
        
        print("Loading results....")
        
        loadStartTime = time.time()
    
        if self.loadFileSuccessful:
            # Acquire the content into string arrays
            # self.rawDataArray = self.getFileArray(self.rawDataFileName, ",")

            # Get the selected columns from the column dropdown boxes
            dateCol = self.DateColString.get()
            timeCol = self.TimeColString.get()
            dirCol = self.DirColString.get()
            speedCol = self.SpeedColString.get()
            
            dateColIndex = -9999
            timeColIndex = -9999
            
            dateTimeArray = []
            
            ## Look for chosen date and time columns in the input file
            for m in range(0,len(self.trimmedInputFileArray[0])):
                headerElement = self.trimmedInputFileArray[0][m].replace("\"","")
                if dateCol in headerElement:
                    dateColIndex = m
                if timeCol in headerElement:
                    timeColIndex = m
            
            # Loop through the trimmed array
            for i in range(1,len(self.trimmedInputFileArray)):
                dateString = self.trimmedInputFileArray[i][dateColIndex]
                timeString = self.trimmedInputFileArray[i][timeColIndex]
                if '24:00' in timeString:
                    dateObject = dt.datetime.strptime(dateString,'%d/%m/%Y')
                    adjustedDateObject = dateObject + dt.timedelta(days=1)
                    adjustedDateString = adjustedDateObject.strftime('%d/%m/%Y')
                    dateString = adjustedDateString
                    timeString = timeString.replace("24:00", "00:00")
                
                dateTimeString = dateString + " " + timeString
                dateTimeObject = dt.datetime.strptime(dateTimeString,'%d/%m/%Y %H:%M')
                dateTimeArray.append(dateTimeString)
                
            for i in range(0,len(dateTimeArray)):
                if dateTimeArray.count(dateTimeArray[i]) > 1:
                    message = "Please remove duplicate timestamp: " + repr(dateTimeArray[i])
                    duplicateMSGBox = messagebox.showinfo("Duplicate timestamp", message)
                    #self.messageWindow("Duplicate timestamp", message, geometry="500x50")
                    self.duplicateFound = True
                    return False
            
            # Perform analysis on the imput file
            self.windAnalysis = WindAnalysis(self.rawDataFileName, dateCol, timeCol, dirCol, speedCol)
            
            # Acquire results of the analysis
            self.hourlyDateTimeArray, self.hourlyDirArray, self.hourlySpeedArray, self.hourlyUArray, self.hourlyVArray = self.windAnalysis.getHourlyAVG()
            self.dailyDateTimeArray, self.dailyDirArray, self.dailySpeedArray, self.dailyUArray, self.dailyVArray = self.windAnalysis.getDailyAVG()
            self.DateTimeArray, self.Dir_10Min, self.Speed_10Min, self.U_10Min, self.V_10Min = self.windAnalysis.get10MinValues()
            self.dataGapStartdateTimeArray, self.dataGapEnddateTimeArray = self.windAnalysis.getDataGapArrays()

            # Clear existing content from list boxes
            self.DailyAVG_dateListBox.delete(0,self.DailyAVG_dateListBox.size()-1)
            self.HourlyAVG_dateListBox.delete(0,self.HourlyAVG_dateListBox.size()-1)
            self.HourlyAVG_hourListBox.delete(0,self.HourlyAVG_hourListBox.size()-1)
            
            # Clear existing content from dropdown boxes
            self.startDateDropDown["menu"].delete(0, "end")
            self.startTimeDropDown["menu"].delete(0, "end")
            self.endDateDropDown["menu"].delete(0, "end")
            self.endTimeDropDown["menu"].delete(0, "end")
            
            # Clear plots
            self.DailyAVG_ax.clear()
            self.DailyAVG_ax.set_theta_zero_location("N")
            self.DailyAVG_ax.set_theta_direction(-1)
            self.DailyAVG_canvas.draw()
            self.HourlyAVG_ax.clear()
            self.HourlyAVG_ax.set_theta_zero_location("N")
            self.HourlyAVG_ax.set_theta_direction(-1)
            self.HourlyAVG_canvas.draw()

            # Inserting each date into the Daily AVG list box
            for i in range(0, len(self.dailyDateTimeArray)):
                dateString = self.dailyDateTimeArray[i].strftime('%Y-%m-%d')
                self.DailyAVG_dateListBox.insert(tkinter.END, dateString)
                self.HourlyAVG_dateListBox.insert(tkinter.END, dateString)
                self.startDateDropDown["menu"].add_command(label=dateString, command=lambda value=dateString: self.startDateString.set(value))
                self.endDateDropDown["menu"].add_command(label=dateString, command=lambda value=dateString: self.endDateString.set(value))
            
            # Inserting each hour into the Hourly AVG list box
            for i in range(0, len(self.hourlyDateTimeArray)):
                if self.dailyDateTimeArray[0].strftime('%Y-%m-%d') == self.hourlyDateTimeArray[i].strftime('%Y-%m-%d'):
                    hourString = self.hourlyDateTimeArray[i].strftime('%H:%M')
                    self.HourlyAVG_hourListBox.insert(tkinter.END, hourString)
                    self.startTimeDropDown["menu"].add_command(label=hourString, command=lambda value=hourString: self.startTimeString.set(value))
                    self.endTimeDropDown["menu"].add_command(label=hourString, command=lambda value=hourString: self.endTimeString.set(value))
                    
            for i in range(0,len(self.dataGapStartdateTimeArray)):
                dataGapStart = self.dataGapStartdateTimeArray[i].strftime('%Y-%m-%d %H:%M')
                dataGapEnd = self.dataGapEnddateTimeArray[i].strftime('%Y-%m-%d %H:%M')
                dataGapBoxString = dataGapStart + " - " + dataGapEnd
                self.DataGap_ListBox.insert(tkinter.END, dataGapBoxString)
            
            # Setting default values (first and last) into the time series drop boxes
            startDate = self.dailyDateTimeArray[0].strftime('%Y-%m-%d')
            startTime = self.hourlyDateTimeArray[0].strftime('%H:%M')
            endDate = self.dailyDateTimeArray[len(self.dailyDateTimeArray)-1].strftime('%Y-%m-%d')
            endTime = self.hourlyDateTimeArray[len(self.hourlyDateTimeArray)-1].strftime('%H:%M')
            
            self.startDateString.set(startDate)
            self.startTimeString.set(startTime)
            self.endDateString.set(endDate)
            self.endTimeString.set(endTime)
            
            # Checking all the plot options
            self.Check_10MinBox.select()
            self.Check_HourlyBox.select()
            self.Check_DailyBox.select()
            self.Check_UVCompBox.select()
            
            # Plotting the time series graphs for the whole span
            #self.plotTimeSeriesData(startDate, startTime, endDate, endTime)
            self.plotTimeSeriesData(self.timeSeries_canvas,self.windDir_ax,self.windSpeed_ax,self.windU_ax,self.windV_ax)

            loadEndTime = time.time()

            print("Results loaded successfully")
            print("Time elapsed: " + repr(loadEndTime-loadStartTime))
            
            messagebox.showinfo("Load Successful", "Results loaded successfully.")
            
        else:
            messagebox.showinfo("Load File", "Please choose and load an input file.")
            
        return

###################################################################
###################################################################

    def refreshTimeSeriesPlots(self):
        
        startDate = self.startDateString.get()
        startTime = self.startTimeString.get()
        endDate = self.endDateString.get()
        endTime = self.endTimeString.get()
        
        self.plotTimeSeriesData(self.timeSeries_canvas,self.windDir_ax,self.windSpeed_ax,self.windU_ax,self.windV_ax)
        
        return

            
###################################################################
###################################################################

    def plotTimeSeriesDataPop(self):
        
        timeSeriesPlotsWidth = 7.8
        timeSeriesPlotsHeight = 6
        
        timeSeries_fig = plt.figure(figsize=(self.timeSeriesPlotsWidth,self.timeSeriesPlotsHeight), dpi = 100)
        windDir_ax = timeSeries_fig.add_subplot(411)
        windSpeed_ax = timeSeries_fig.add_subplot(412, sharex=windDir_ax)
        windU_ax = timeSeries_fig.add_subplot(413, sharex=windDir_ax)
        windV_ax = timeSeries_fig.add_subplot(414, sharex=windDir_ax)
        timeSeries_canvas = timeSeries_fig.canvas
        self.plotTimeSeriesData(timeSeries_canvas, windDir_ax, windSpeed_ax, windU_ax, windV_ax, True)

        return

###################################################################
###################################################################
    
    def plotTimeSeriesData(self,canvas,windDir_ax,windSpeed_ax,windU_ax,windV_ax,pop=False):

        startDate = self.startDateString.get()
        startTime = self.startTimeString.get()
        endDate = self.endDateString.get()
        endTime = self.endTimeString.get()  
        
        startDateTimeString = startDate + " " + startTime
        endDateTimeString = endDate + " " + endTime
        
        startDateTimeObj = dt.datetime.strptime(startDateTimeString,'%Y-%m-%d %H:%M')
        endDateTimeObj = dt.datetime.strptime(endDateTimeString,'%Y-%m-%d %H:%M')
        
        dateString = startDateTimeString + " - " + endDateTimeString
        
        dateTimeArray_filt = []
        Dir_10Min_filt = []
        Speed_10Min_filt = []
        U_10Min_filt = []
        V_10Min_filt = []
        
        for i in range(0,len(self.DateTimeArray)):
            if (self.DateTimeArray[i] <= endDateTimeObj + dt.timedelta(hours=1)) and (self.DateTimeArray[i] > startDateTimeObj):
                dateTimeArray_filt.append(self.DateTimeArray[i])
                Dir_10Min_filt.append(self.Dir_10Min[i])
                Speed_10Min_filt.append(self.Speed_10Min[i])
                U_10Min_filt.append(self.U_10Min[i])
                V_10Min_filt.append(self.V_10Min[i])
        
        hourly_dateTimeArray_filt = []
        hourly_Dir_filt = []
        hourly_Speed_filt = []
        hourly_U_filt = []
        hourly_V_filt = []
        
        for i in range(0,len(self.hourlyDateTimeArray)):
            if (self.hourlyDateTimeArray[i] <= endDateTimeObj + dt.timedelta(hours=1)) and (self.hourlyDateTimeArray[i] >= startDateTimeObj):
                hourly_dateTimeArray_filt.append(self.hourlyDateTimeArray[i])
                hourly_Dir_filt.append(self.hourlyDirArray[i])
                hourly_Speed_filt.append(self.hourlySpeedArray[i])
                hourly_U_filt.append(self.hourlyUArray[i])
                hourly_V_filt.append(self.hourlyVArray[i])
        
        daily_dateTimeArray_filt = []
        daily_Dir_filt = []
        daily_Speed_filt = []
        daily_U_filt = []
        daily_V_filt = []
        
        for i in range(0,len(self.dailyDateTimeArray)):
            if (self.dailyDateTimeArray[i] <= endDateTimeObj + dt.timedelta(hours=1)) and (self.dailyDateTimeArray[i] >= startDateTimeObj):
                daily_dateTimeArray_filt.append(self.dailyDateTimeArray[i])
                daily_Dir_filt.append(self.dailyDirArray[i])
                daily_Speed_filt.append(self.dailySpeedArray[i])
                daily_U_filt.append(self.dailyUArray[i])
                daily_V_filt.append(self.dailyVArray[i])
        
        windDir_ax.clear()
        windSpeed_ax.clear()
        windU_ax.clear()
        windV_ax.clear()
        
        windDir_ax.get_xaxis().set_visible(False)
        windSpeed_ax.get_xaxis().set_visible(False)
        windU_ax.get_xaxis().set_visible(False)

        windDir_ax.set_title(self.windDir_Title, fontsize=self.timeSeries_subPlotTitleSize)
        windSpeed_ax.set_title(self.windSpeed_Title, fontsize=self.timeSeries_subPlotTitleSize)
        windU_ax.set_title(self.windU_Title, fontsize=self.timeSeries_subPlotTitleSize)
        windV_ax.set_title(self.windV_Title, fontsize=self.timeSeries_subPlotTitleSize)
        
        windDir_ax.set_yticks(np.arange(0,360,100))
        
        if self.Check_10Min.get():
            windDir_ax.plot(dateTimeArray_filt, Dir_10Min_filt, color='green', label='10 min')
            windSpeed_ax.plot(dateTimeArray_filt, Speed_10Min_filt, color='green', label='10 min')
            windU_ax.plot(dateTimeArray_filt,  U_10Min_filt, color='green', label='10 min')
            windV_ax.plot(dateTimeArray_filt,  V_10Min_filt, color='green', label='10 min')
            
        if self.Check_Hourly.get():
            windDir_ax.plot(hourly_dateTimeArray_filt, hourly_Dir_filt, color='blue', label='Hourly Avg')
            windSpeed_ax.plot(hourly_dateTimeArray_filt, hourly_Speed_filt, color='blue', label='Hourly Avg')
            windU_ax.plot(hourly_dateTimeArray_filt, hourly_U_filt, color='blue', label='Hourly Avg')
            windV_ax.plot(hourly_dateTimeArray_filt, hourly_V_filt, color='blue', label='Hourly Avg')
            
        if self.Check_Daily.get():
            windDir_ax.plot(daily_dateTimeArray_filt, daily_Dir_filt, color='red', label='Daily Avg')
            windSpeed_ax.plot(daily_dateTimeArray_filt, daily_Speed_filt, color='red', label='Daily Avg')
            windU_ax.plot(daily_dateTimeArray_filt, daily_U_filt, color='red', label='Daily Avg')
            windV_ax.plot(daily_dateTimeArray_filt, daily_V_filt, color='red', label='Daily Avg')
            
        windDir_ax.legend()
        windSpeed_ax.legend()
        windU_ax.legend()
        windV_ax.legend()
        
        canvas.figure.autofmt_xdate()
        canvas.figure.subplots_adjust(left=self.leftMargin,right=self.rightMargin,bottom=self.bottomMargin,top=self.topMargin)
        
        if pop==False:
            canvas.draw()
        else:
            canvas.set_window_title(dateString)
        
        return

###################################################################
###################################################################
    
    def loadFiles(self):
        
        if path.exists(self.rawFilePathBox.get()):
            self.rawDataFileName = self.rawFilePathBox.get()
        else:
            messagebox.showinfo("Path Invalid", "Path to raw data file is invalid")
            return False
        
        return True
    
###################################################################
###################################################################
    
    def getFileArray(self, inputFile, delimiter):
    # Converts contents of input file in formats similar to CSVs into a string array

        # Open input file
        processFile = open(inputFile, 'r')

        # Read all the lines in the file
        lines = processFile.readlines()

        # Initialize output array
        contentArray = []

        # Loop through the lines
        for i in range(0,len(lines)):

            # Strip the regex line dividers from each single line
            line = repr(lines[i].rstrip('\r\n'))

            # Split the single line with the input delimited into an array
            arrayLine = line.split(delimiter)

            # Loop though each value of the line array and remove unnecessary strings
            for i in range(0,len(arrayLine)):
                arrayLine[i] = arrayLine[i].replace("'", "")
                arrayLine[i] = arrayLine[i].replace("[", "")
                arrayLine[i] = arrayLine[i].replace("]", "")

            # Append to output array
            contentArray.append(arrayLine)

        processFile.close()

        return contentArray

###################################################################
###################################################################

    def plotHourlyDataPop(self):
        
        hourlyAVG_fig = plt.figure(figsize=(6,6))
        hourlyAVG_ax = hourlyAVG_fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        hourlyAVG_ax.set_theta_zero_location("N")
        hourlyAVG_ax.set_theta_direction(-1)
        hourlyAVG_canvas = hourlyAVG_fig.canvas
        self.plotHourlyData(hourlyAVG_canvas, hourlyAVG_ax, True)
        
        return
    
###################################################################
###################################################################

    def plotHourlyData(self, canvas, ax, pop=False):
        
        self.HourlyAVG_dateListBoxList = self.HourlyAVG_dateListBox.curselection()
        self.HourlyAVG_hourListBoxList = self.HourlyAVG_hourListBox.curselection()
        
        if len(self.HourlyAVG_dateListBoxList) > 0 and len(self.HourlyAVG_hourListBoxList) > 0:
            dateString = self.HourlyAVG_dateListBox.get(self.HourlyAVG_dateListBoxList[0]) #String
            hourMinString = self.HourlyAVG_hourListBox.get(self.HourlyAVG_hourListBoxList[0]) #String
            hourString = hourMinString.split(":")[0]
            minString = hourMinString.split(":")[1]
            if hourString == '23':
                nextHourString = '00'
            else :
                nextHourMinString = self.HourlyAVG_hourListBox.get(self.HourlyAVG_hourListBoxList[0]+1) #String
                nextHourString = nextHourMinString.split(":")[0]
            dateTimeString = dateString + " " + hourMinString
            
            deg = -9999
            speed = -9999
            
            for i in range(0,len(self.hourlyDateTimeArray)):
                if dateTimeString == self.hourlyDateTimeArray[i].strftime('%Y-%m-%d %H:%M'):
                    deg = self.hourlyDirArray[i]
                    speed = self.hourlySpeedArray[i]
        
            if deg != -9999 or speed != -9999:
                c = ['r','b','g']  # plot marker colors
                ax.clear()         # clear axes from previous plot
                if speed > 0:
                    title_obj = ax.set_title('Direction from: ' + repr(round(deg,2)) + ' Speed: ' + repr(round(speed,2)), color="green")
                else:
                    title_obj = ax.set_title('Direction from: ' + repr(round(deg,2)) + ' Speed: ' + repr(round(speed,2)), color="red")
                ax.set_theta_zero_location("N")
                ax.set_theta_direction(-1)
                
                maxSpeed_10min = 0.0
                
                for i in range(0,len(self.DateTimeArray)):
                    dateString_10min = self.DateTimeArray[i].strftime('%Y-%m-%d')
                    hourMinString_10min = self.DateTimeArray[i].strftime('%H:%M')
                    hourString_10min = hourMinString_10min.split(":")[0]
                    minString_10min = hourMinString_10min.split(":")[1]
                    if (dateString == dateString_10min and hourString == hourString_10min and minString_10min != '00') or (dateString == dateString_10min and nextHourString == hourString_10min and minString_10min == '00'):
                        deg_10min = self.Dir_10Min[i]
                        speed_10min = self.Speed_10Min[i]
                        if deg_10min < 180:
                            flippedDeg_10min = deg_10min + 180.0
                        else:
                            flippedDeg_10min = deg_10min - 180.0
                        if speed_10min > maxSpeed_10min:
                            maxSpeed_10min = speed_10min
                        if speed_10min > 0:
                            arr = ax.arrow(flippedDeg_10min/180.*np.pi, 0, 0, speed_10min*0.8, alpha = 1, width = speed_10min*0.1,#arrowhead,
                                     head_width=speed_10min*0.2, head_length=speed_10min*0.2, edgecolor = 'white', facecolor = 'yellow', lw = 2, zorder = 50)
                
                if speed > 0:
                    if deg < 180:
                        flippedDeg = deg + 180.0
                    else:
                        flippedDeg = deg - 180.0
                    arr = ax.arrow(flippedDeg/180.*np.pi, 0, 0, speed*0.8, alpha = 1, width = speed*0.1,#arrowhead,
                             head_width=speed*0.2, head_length=speed*0.2, edgecolor = 'black', facecolor = 'green', lw = 2, zorder = 50)

                if maxSpeed_10min*1.0 > 1:
                    ax.set_ylim(0,maxSpeed_10min*1.0)
                    ax.set_yticks(np.arange(0,maxSpeed_10min*1.0,0.5)) 
                elif maxSpeed_10min < 0.5:
                    ax.set_ylim(0,maxSpeed_10min)
                    ax.set_yticks(np.arange(0,maxSpeed_10min,0.1)) 
                else:
                    ax.set_ylim(0,1.0)
                    ax.set_yticks(np.arange(0,1.0,0.2))
                    
                if pop==False:
                    canvas.draw()
                else:
                    canvas.set_window_title(dateTimeString)

            return
        
###################################################################
###################################################################

    def plotDailyDataPop(self):
        
        dailyAVG_fig = plt.figure(figsize=(6,6))
        dailyAVG_ax = dailyAVG_fig.add_axes([0.1,0.1,0.8,0.8],polar=True)
        dailyAVG_ax.set_theta_zero_location("N")
        dailyAVG_ax.set_theta_direction(-1)
        #dailyAVG_canvas = FigureCanvasTkAgg(dailyAVG_fig)
        dailyAVG_canvas = dailyAVG_fig.canvas
        self.plotDailyData(dailyAVG_canvas, dailyAVG_ax, True)
        
        return
###################################################################
###################################################################

    def plotDailyData(self, canvas, ax, pop=False):
        self.DailyAVG_dateListBoxList = self.DailyAVG_dateListBox.curselection()
        
        if len(self.DailyAVG_dateListBoxList) > 0:
            for i in range(0, len(self.DailyAVG_dateListBoxList)):
                #print self.dateListBoxList[i] # index
                dateString = self.DailyAVG_dateListBox.get(self.DailyAVG_dateListBoxList[i]) #String
                #print self.dailyDirArray[self.DailyAVG_dateListBoxList[i]]
                deg = self.dailyDirArray[self.DailyAVG_dateListBoxList[i]]
                #print self.dailySpeedArray[self.DailyAVG_dateListBoxList[i]]
                speed = self.dailySpeedArray[self.DailyAVG_dateListBoxList[i]]
        
            c = ['r','b','g']  # plot marker colors
            ax.clear()         # clear axes from previous plot
            if speed > 0:
                title_obj = ax.set_title('Direction from: ' + repr(round(deg,2)) + ' Speed: ' + repr(round(speed,2)), color="green")
            else:
                title_obj = ax.set_title('Direction from: ' + repr(round(deg,2)) + ' Speed: ' + repr(round(speed,2)), color="red")
            ax.set_theta_zero_location("N")
            ax.set_theta_direction(-1)

            maxSpeed_hourly = 0.0
            
            for i in range(0,len(self.hourlyDateTimeArray)):
                hourlyDateString = self.hourlyDateTimeArray[i].strftime('%Y-%m-%d')
                hourlyHourMinString = self.hourlyDateTimeArray[i].strftime('%H:%M')
                hourlyHourString = hourlyHourMinString.split(":")[0]
                hourlyMinString = hourlyHourMinString.split(":")[1]
                lastDayDateTimeObject = self.hourlyDateTimeArray[i] - dt.timedelta(days=1)
                lastDayDateTimeString = lastDayDateTimeObject.strftime('%Y-%m-%d')
                deg_hourly = self.hourlyDirArray[i]
                speed_hourly = self.hourlySpeedArray[i]
                
                if ((dateString == hourlyDateString and hourlyHourString != '00') or (dateString == lastDayDateTimeString and hourlyHourString == '00')) and self.hourlySpeedArray[i] > 0:
                    if deg_hourly < 180:
                        flippedDeg_hourly = deg_hourly + 180.0
                    else:
                        flippedDeg_hourly = deg_hourly - 180.0                    
                    arr = ax.arrow(flippedDeg_hourly/180.*np.pi, 0, 0, speed_hourly*0.8, alpha = 1, width = speed_hourly*0.1,#arrowhead,
                             head_width=speed_hourly*0.2, head_length=speed_hourly*0.2, edgecolor = 'white', facecolor = 'yellow', lw = 2, zorder = 50)
                    if speed_hourly > maxSpeed_hourly:
                        maxSpeed_hourly = speed_hourly

            if speed > 0:
                if deg < 180:
                    flippedDeg = deg + 180.0
                else:
                    flippedDeg = deg - 180.0
                arr = ax.arrow(flippedDeg/180.*np.pi, 0, 0, speed*0.8, alpha = 1, width = speed*0.1,#arrowhead,
                         head_width=speed*0.2, head_length=speed*0.2, edgecolor = 'black', facecolor = 'green', lw = 2, zorder = 50)

            if maxSpeed_hourly*1.1 > 1:
                ax.set_ylim(0,maxSpeed_hourly*1.1)
                ax.set_yticks(np.arange(0,maxSpeed_hourly*1.1,0.5))
            elif maxSpeed_hourly < 0.5:
                ax.set_ylim(0,0.5)
                ax.set_yticks(np.arange(0,0.5,0.1)) 
            else:
                ax.set_ylim(0,1.0)
                ax.set_yticks(np.arange(0,1.0,0.2))
                
            if pop==False:
                canvas.draw()
            else:
                canvas.set_window_title(dateString)

            return

###################################################################
###################################################################

    def chooseFile(self,textEntryBox):

        currentStringlength = len(textEntryBox.get())
        filename = askopenfilename()
        textEntryBox.delete(0,currentStringlength)
        textEntryBox.insert(0,filename)
        
        return

###################################################################
###################################################################

    def chooseSaveFile(self,textEntryBox):

        currentStringlength = len(textEntryBox.get())
        filename = asksaveasfilename(filetypes=[('XLS File', '*.xls'),('CSV File', '*.csv'),('TXT File', '*.txt')])
        textEntryBox.delete(0,currentStringlength)
        textEntryBox.insert(0,filename)
        
        return
    
###################################################################
###################################################################
    
    def chooseDir(self,textEntryBox):

        currentStringlength = len(textEntryBox.get())
        dirname = askdirectory()
        textEntryBox.delete(0,currentStringlength)
        textEntryBox.insert(0,dirname)
        
        return

###################################################################
###################################################################

    def messageWindow(self, title, message, geometry):
        win = tkinter.Toplevel()
        win.title(title)
        win.geometry(geometry)
        tkinter.Label(win, text=message, font=(None, 10,'bold')).pack()
        tkinter.Button(win, text='OK', command=win.destroy).pack()
    
###################################################################
###################################################################
    
    def on_closing(self):

        if messagebox.askokcancel("Quit", "Sure you want to quit?"):
            self.master.destroy()
            sys.exit()

        return
    
###################################################################
###################################################################
###################################################################
###################################################################
        
# Set plot style
#plt.style.use('ggplot')
sns.set_style("darkgrid")
    
# Paint the GUI
GUI = tkinter.Tk()

my_GUI = WindAnalysis_GUI(GUI)

# Run the whole GUI
GUI.mainloop()