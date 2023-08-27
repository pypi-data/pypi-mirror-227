from logging import Logger as _Logger
from abc import ABC as _ABC
from datetime import datetime as _datetime, timedelta as _timedelta
from ..types.time import TimeSpan as _TimeSpan
from ..utility.linq import LINQ as _LINQ
from ..settingsproviders import SettingsManager_JSON as _SettingsManager_JSON
from ..utility.stopwatch import StopWatch as _StopWatch
from time import sleep as _sleep
import os as _os
from zlib import crc32 as _crc32
from ..utility import module as _module
from ..io import directory as _directory
from multiprocessing.pool import ThreadPool as _ThreadPool
import traceback as _traceback

class ITask(_ABC):
    '''
    Tasks needs to implement this interface to be loaded into task scheduler

    properties and methods for Derived classes:
        * task_Interval
        * On_StartUp
        * On_Schedule 
    '''
    task_Interval = None  # type: _TimeSpan
    '''Runs On_Schedule event per specified interval, example: TimeSpan(minute=2), would run the task once ever 2 minutes'''
    task_Ignore = False
    '''Can ignore a task from triggering'''

    def __init__(self) -> None:
        self.task_id = self.__class__.__module__ + "." + self.__class__.__name__
        self._task_nextSchedule = _datetime.min

    def On_StartUp(self) -> str|None:
        '''runs once per start of taskscheduler'''
        pass

    def On_Schedule(self) -> str|None:
        '''runs once per specified interval'''
        pass


class CommandTask(ITask):
    '''Premade task for running a simple command'''
    def __init__(self, interval:_TimeSpan, command:str) -> None:
        self.task_Interval = interval
        self.command = command
        super().__init__()

        from hashlib import md5
        self.task_id = md5(command.encode()).hexdigest()[:16]
    
    def On_Schedule(self):
        import subprocess
        result = subprocess.run(self.command, text=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        message = ""
        if(result.returncode != 0): #something went bad
            message += f"STDERR[{result.returncode}]: {result.stderr.rstrip()};"
        
        if(result.stdout):
            message += f"STDOUT: {result.stdout.rstrip()};"

        return message

class TaskSchedulerManager:
    def __init__(self, settingsPath: str, logger: _Logger) -> None:
        self.logger = logger
        self._settingsPath = settingsPath
        self._settingsManager = _SettingsManager_JSON(self._settingsPath)
        self._settingsManager.LoadSettings()
        self._tasks = {} #type: dict[str, ITask]
        '''all registered tasks'''
        self._FLAG_SAVESETTINGS = False
        self._FLAG_RUN = True
        self._config_RunIterationDelay = 1
        self._config_maxThreads = 10
        '''max threads to use for running tasks'''

    class _TaskResult:
        def __init__(self) -> None:
            self.stopwatch = _StopWatch()
            self.output = None #type:str
            self.error = None #type:str

        @property
        def ElapsedMS(self):
            return self.stopwatch.GetElapsedMilliseconds(decimalPrecision=2)

    def _RunTaskEvent_OnStartUp(self, task: ITask):
        taskResult = self._TaskResult()
        taskResult.stopwatch.Start()
        try:
            output = task.On_StartUp()
            taskResult.output = f"Event On_StartUp[{taskResult.ElapsedMS} MS]: {task.task_id}"
            if(output):
                taskResult.output += ", " + output
        except Exception as e:
            taskResult.error = f"Event On_StartUp failed[{taskResult.ElapsedMS} MS]: {task.task_id}, Error: {_traceback.format_exc()}"
        return taskResult

    def _RunTaskEvent_OnSchedule(self, task: ITask):
        taskResult = self._TaskResult()
        taskResult.stopwatch.Start()
        try:
            self._ScheduledTask_SetNextSchedule(task)
            output = task.On_Schedule()
            taskResult.output = f"Event On_Schedule[{taskResult.ElapsedMS} MS]: {task.task_id}"
            if(output):
                taskResult.output += ", " + output
        except Exception as e:
            taskResult.error = f"Event On_Schedule failed[{taskResult.ElapsedMS} MS]: {task.task_id}, Error: {_traceback.format_exc()}"
        return taskResult
    
    def Run(self):
        self._InitializeTasks()
        self.logger.info(f"Event Start")

        activeTaskList = _LINQ(self._tasks.values()) \
            .Where(lambda task: task.task_Ignore == False) \
            .ToList()

        self._config_maxThreads = min(len(activeTaskList), self._config_maxThreads)
        pool = _ThreadPool(processes=self._config_maxThreads)
        
        #skip none overriden ones
        tasksWithStartUp = _LINQ(activeTaskList).Where(lambda task: task.On_StartUp.__func__ is not ITask.On_StartUp)
        taskResults = pool.map(self._RunTaskEvent_OnStartUp, tasksWithStartUp)
        for taskRes in taskResults:
            if(taskRes.error):
                self.logger.error(taskRes.error)
            else:
                self.logger.info(taskRes.output)

        tasksWithSchedules = _LINQ(activeTaskList) \
            .Where(lambda task: task.task_Interval is not None) \
            .ToList()

        while self._FLAG_RUN:
            tasksNeedingScheduleRun = _LINQ(tasksWithSchedules) \
                .Where(self._ScheduledTask_ShouldRun)
            
            taskResults = pool.map(self._RunTaskEvent_OnSchedule, tasksNeedingScheduleRun)
            for taskRes in taskResults:
                if(taskRes.error):
                    self.logger.error(taskRes.error)
                else:
                    self.logger.info(taskRes.output)
            self.SaveSettingsIfNeeded() #save once per full iteration if needed
            _sleep(self._config_RunIterationDelay)
            
        pool.terminate()

    def SaveSettingsIfNeeded(self):
        '''instead of saving after each small modification, change when modifications are made'''
        if(self._FLAG_SAVESETTINGS): 
            self._settingsManager.SaveSettings()
            self._FLAG_SAVESETTINGS = False
            
    def _ScheduledTask_ShouldRun(self, task: ITask):
        if(_datetime.now() > task._task_nextSchedule):
            return True
        return False
    
    def _ScheduledTask_SetNextSchedule(self, task: ITask):
        '''sets the task directly to next scheduled interval'''
        task._task_nextSchedule = _datetime.now() + _timedelta(seconds=task.task_Interval.InSeconds())
        self._settingsManager.Settings["TaskSchedules"][task.task_id]["next"] = task._task_nextSchedule.isoformat()
        self._FLAG_SAVESETTINGS = True
        return

    def LoadTasks(self, tasks: list[ITask]):
        '''Load list of ITasks into memory'''
        for task in tasks:
            if not isinstance(task, ITask):
                raise TypeError(f"Task must be of type ITask, got {type(task)}")
            self._tasks[task.task_id] = task
        return self

    def LoadTasksFromFile(self, path:str):
        '''Scans a file for all ITask implementing classes and loads them into memory'''
        if(not _os.path.isfile(path)):
            raise FileNotFoundError(path)
        
        taskInstances = []
        
        dynamicModuleName = f"{_os.path.basename(path)}_{_crc32(path.encode())}"
        dynamicModule = _module.ImportModuleDynamically(dynamicModuleName, path)
        dynamicModuleInfo = _module.ModuleInfo(dynamicModule)
        classes = dynamicModuleInfo.GetDeclaredClasses(ITask, includeChildsOnly=True)
        for className,obj in classes.items():
            taskInstances.append(obj())

        self.LoadTasks(taskInstances)  

        return self

    def LoadTasksFromDirectory(self, path:str, recursive=True):
        '''Scans a directory for all ITask implementing classes and loads them into memory'''

        if(not _os.path.isdir(path)):
            raise NotADirectoryError(path)
        
        maxRecursionDepth = None if recursive == True else 1
        taskInstances = []
        pyFiles = _directory.List(path, 
                             includeDirs=False, 
                             includeFilter='/\.py$/i',
                             maxRecursionDepth=maxRecursionDepth)
        for filepath in pyFiles:
            self.LoadTasksFromFile(filepath)

        return self

    def _InitializeTasks(self):
        if("TaskSchedules" not in self._settingsManager.Settings):
            self._settingsManager.Settings["TaskSchedules"] = {}
            self._FLAG_SAVESETTINGS = True
            

        taskSchedulesSettings = self._settingsManager.Settings["TaskSchedules"]

        #clear invalid/old settings
        for key in list(taskSchedulesSettings.keys()):
            if(key not in self._tasks): #this includes ignored tasks aswell, since we dont want to reset it's schedule when its temporarily ignored
                del taskSchedulesSettings[key]
                self._FLAG_SAVESETTINGS = True

        #register tasks with schedules
        TasksWithSchedules = _LINQ(self._tasks.values()) \
            .Where(lambda task: task.task_Interval is not None)
        
        for task in TasksWithSchedules:
            #if this is a new task, or task interval has changed, then set to trigger them right away
            if(task.task_id not in taskSchedulesSettings) or (taskSchedulesSettings[task.task_id]["interval"] != task.task_Interval.InSeconds()):
                taskSchedulesSettings[task.task_id] = {
                    "interval": task.task_Interval.InSeconds(),
                    "next": _datetime.min.isoformat()
                }
                self._FLAG_SAVESETTINGS = True
            
            task._task_nextSchedule = _datetime.fromisoformat(taskSchedulesSettings[task.task_id]["next"])

        self.SaveSettingsIfNeeded()            
        return