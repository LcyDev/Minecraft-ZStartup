@ECHO OFF
title ZStart
::##################
::# CONFIGURATION  #
::##################

:: RULES: In string sensitive configs, there will be "" set. 
:: In some cases, this will be removed after, so if you need some of them to stay, use instead ''
:: DO NOT REMOVE DEFAULT "", can cause issues.
:: Example: PARAMETERS="--nogui --config 'server properties.yml'"
:: Toggle configs valid values: TRUE or FALSE. (CAPS DON'T MATTER)

::--CONSOLE--::
::# Sets the console title.
SET TITLE="Minecraft: Server Instance"
::# Sets the server location.
SET SERVER_PATH="./"
::# Loop the server, no matter how the server closes, it will restart.
::# Exit ZStart to stop this loop.
::# (Consider rather configuring spigot.yml restart-script.)
SET RESTART_LOOP=false
::# Automatically creates and accepts eula.txt.
SET AUTO-EULA=true
::# What will happen when the server is stopped.
::# Values: WAIT, PAUSE, NONE
SET WAIT-MODE=WAIT
::# Sets how long to WAIT.
SET WAIT-TIMER=30 
::# Enables exiting after wait-mode.
SET EXIT=true


::--SERVER--::
::# The name of your server's JAR file.
::# Side note: if you're not using Paper (http://papermc.io) or one of it's forks,
::# (https://purpur.pl3x.net) then you should really switch. 
SET JAR_NAME="server.jar"
::# The location of your server's JAR.
SET JAR_PATH="./"
::# Skips the need of eula.txt = true.
SET EULA-SKIP=false
::# Removes warnings about outdated server builds.
SET ADVANCED-MODE=true
::# Your server's JAR parameters.
::# In order to see all of the parameters, set below --help.
::# (This wont let the server start, but will show all parameters aviable)
::# More info:
::#   https://minecraft.fandom.com/wiki/Tutorials/Setting_up_a_server
::#   https://bukkit.gamepedia.com/CraftBukkit_Command_Line_Arguments
::#   https://www.spigotmc.org/wiki/start-up-parameters
SET PARAMETERS="--nogui"


::--JAVA--::
::# Sets the path of the java binary. (bin\java.exe)
::# You can use this to determine which java you want to use.
::# Consider using java 11 or latest if possible, and changing to OpenJDK.
::# (Change to OpenJDK here! https://adoptopenjdk.net/)
SET JAVA_BINARY="java"
::# Allocate the server's max&min heap-memory.
::# If you want to allocate more than 4GB you will need Java 64 bits.
SET MAX-MEMORY=4096
SET MIN-MEMORY=1024
::# Select the memory unit to be used.
::# Values: KB, MB, GB.
SET HEAP_UNIT=MB
::# This attemps to self-calculate the nursery max&min memory based on max-heap-memory.
::# Java already sets this itself. OpenJ9 is needed.
SET NURSERY=false

::--FLAGS--::
::# DEFAULTS: Always enabled, independant of other group flags.
::# G1GC: Aikar's G1GC flags. (https://mcflags.emc.gs)
::# ZGC: Aikar based ZGC flags. (Exists from J11, decent from J14, Latest is always better.)

::# Enable one flag group per mode.
SET FLAGS_MODE=F_G1GC
::# Enables using more flag groups.
SET MULTI_FLAGS=false
::SET FLAGS_MODE1=
::SET FLAGS_MODE2=
::SET FLAGS_MODE3=

SET DEFAULTS="-XX:+DisableExplicitGC"
::# Instructions:
::#   Be sure to remove any flag that is already on DEFAULTS
::#   You can modify this as you please, remove or add new group flags.
::#   Group Format: "F_(NAME)=(FLAGS)"
::#   To toggle a group flag, just add it in FLAGS_MODE
::#   If your memory is set more than 12GB be sure to try and change the flags as explained in Aikar's flags.
::#    G1GC: -XX:G1NewSizePercent=40 -XX:G1MaxNewSizePercent=50 -XX:G1HeapRegionSize=16M -XX:G1ReservePercent=15
::#    OTHER: -XX:InitiatingHeapOccupancyPercent=20
::#    (If this generates problems, revert back)
SET F_G1GC=-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:InitiatingHeapOccupancyPercent=15 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:MaxGCPauseMillis=200 -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true
SET F_ZGC=-XX:+UseZGC -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:InitiatingHeapOccupancyPercent=15 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:-UseG1GC -XX:-UseParallelGC -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true
:: 
::# More info:
::   # Timezone flag: -Duser.timezone="America/New_York" (https://garygregory.wordpress.com/2013/06/18/what-are-the-java-timezone-ids/)
::   #   https://www.oracle.com/technical-resources/articles/java/g1gc.html
::   #   https://forums.spongepowered.org/t/optimized-startup-flags-for-consistent-garbage-collection/13239
::   #   https://wiki.openjdk.java.net/display/zgc/Main



::##########################
:: AUTO_START CONFIGURATION
::##########################
:: !WARNING!, BEFORE CHANGING THE SERVICE NAME, SET STARTS ON "NONE", RUN IT TO DELETE THE PREVIOUS TASK 
:: AND BEFORE THE SERVER STARTS, CLOSE WINDOW AND NOW CHANGE NAME.
::
:: ServiceName: Name of the service/task, no spaces.
SET ServiceName=mcserverbatch01
::::
:: Start_TASK: Sets the mode of the task.
::  DAILY=EVERYDAY, ONSTART=WINDOWS STARTS, ONLOGON=USER LOGINS, NONE=NO TASK_AUTOSTART
:: 			   (DAILY, ONSTART, ONLOGON, NONE)
SET Start_TASK=NONE
:: TaskTime: Sets to start the server at certain time.
::			 (NEEDS DAILY) (hh:ss)
SET TaskTime=13:05
::::
:: Start_SERVICE:
::  AUTO=WINDOWS STARTS, DELAYED=USER LOGINS, NONE= NO SERVICE_AUTOSTART
::        (AUTO, DELAYED-AUTO, DISABLED, NONE)
SET Start_SERVICE=NONE
::##########################

:::: END CONFIGURATION -- DON'T TOUCH ANYTHING BELOW THIS LINE!
::other
set TITLE=%TITLE:~1,-1%
set JAR_PATH=%JAR_PATH:~1,-1%
set DEFAULTS=%DEFAULTS:~1,-1%
set MODE=%HEAP_UNIT:~0,1%
::console-server
title %TITLE%
cd %SERVER_PATH%
if /I '%AUTO-EULA%'=='true' (
	@echo eula=true>"%JAR_PATH%eula.txt"
)
if /I '%1'=='-restart' GOTO restart
if /I '%EULA-SKIP%'=='true' set agree=-DCom.mojang.eula.agree=true
if /I '%ADVANCED-MODE%'=='true' set advanced=-DIReallyKnowWhatIAmDoingISwear=true
::TASKS&SERVICES 
if %Start_TASK%'=='NONE' SCHTASKS /DELETE /TN %ServiceName%
if %Start_SERVICE%'=='NONE' sc delete %ServiceName%
if NOT '%Start_TASK%'=='NONE' if '%Start_SERVICE%'=='NONE' SCHTASKS /CREATE /TN %ServiceName% /SC %Start_TASK% /ST %TaskTime% /TR %0 
if NOT '%Start_SERVICE%'=='NONE' if '%Start_TASK%'=='NONE' sc create '%ServiceName%' start=%Start_SERVICE% binpath=%0
::FLAGS
setlocal ENABLEDELAYEDEXPANSION
set "JVM_FLAGS=!%FLAGS_MODE%! %JVM_MF% %DEFAULTS% %agree% %advanced%"
if /I '%MULTI_FLAGS%'=='true' set JVM_MF=!%FLAGS_MODE1%! !%FLAGS_MODE2%! !%FLAGS_MODE3%! !%FLAGS_MODE4%! !%FLAGS_MODE5%!
FOR /F delims^=^"^ tokens^=* %%a in (%JVM_FLAGS%) do set JVM_FLAGS=%%a
FOR /F delims^=^"^ tokens^=* %%a in (%JVM_MF%) do set JVM_MF=%%a
setlocal DISABLEDELAYEDEXPANSION
)
:: NURSERY
if '%NURSERY%'=='TRUE' (
	set /A NURSE_MAX=%MAX-MEMORY% * 2 / 5
	set /A NURSE_MIN=%MAX-MEMORY% / 4
	set CMD=%JAVA_BINARY% -Xmx%MAX-MEMORY%%MODE% -Xms%MIN-MEMORY%%MODE% -Xmns%NURSE_MIN%%MODE% -Xmnx%NURSE_MAX%%MODE% %JVM_FLAGS% %12flags% "%JAR_PATH%%JAR_NAME%" %PARAMETERS%
) else set CMD=%JAVA_BINARY% -Xmx%MAX-MEMORY%%MODE% -Xms%MIN-MEMORY%%MODE% %JVM_FLAGS% %12flags% "%JAR_PATH%%JAR_NAME%" %PARAMETERS%

::Start server
echo %DATE% - %TIME% 
echo.
echo Starting Server 
echo Loading startup parameters...
echo.
%CMD%
goto stop

:stop
echo.
if /I '%WAIT-MODE%'=='WAIT' TIMEOUT /T %WAIT-TIMER%
if /I '%WAIT-MODE%'=='PAUSE' PAUSE
if /I '%RESTART_LOOP%'=='true' ( goto restart
)
goto exit

:exit
if /I '%EXIT%'=='true' exit

:restart
echo.
echo Restarting server
echo.
cmd /c %0
cls
