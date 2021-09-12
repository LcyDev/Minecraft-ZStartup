:start
@ECHO OFF
::##################
::# CONFIGURATION  #
::##################

:: TITLE: Sets the Console Title.
SET TITLE=Minecraft: Server Instance
:: ALWAYS_RESTART: This enables a loop that will maintain the server open, will restart on crash and on /restart or /stop.
::                 You can only exit by closing the console window. (I would recommend configuring the spigot.yml restart)
::                 ("spigot.yml" "restart-script: ZStart.bat -restart"
::                 Valid Values: 'TRUE' or 'FALSE'
SET ALWAYS_RESTART=FALSE
:: EULA: Skips the eula.txt = true.
:: 		 Valid Values: 'TRUE' or 'FALSE'
SET EULA=TRUE
:: ADVANCEDSTART: Enables "IReallyKnowWhatIAmDoingISwear" flag.
::                Removes warning of outdated server build and other things..
::                Valid Values: 'TRUE' or 'FALSE'
SET ADVANCEDSTART=FALSE
:: EXIT_MODE: Select between 'WAIT' or 'PAUSE' to select how the console will close.
:: 	          (PAUSE REQUIRES USER INPUT).
SET EXIT_MODE=WAIT
:: WAIT_TIME: How many seconds to wait before the console closes.
SET WAIT_TIME=20



:: JAR_NAME: The name of your server's JAR file. The default is
::           "paperclip.jar".
::
::           Side note: if you're not using Paper (http://papermc.io) or one of it's forks,
::           (https://purpur.pl3x.net) then you should really switch. 
SET JAR_NAME=paperclip.jar
:: JAVA_BINARY: Here you can specify a folder path directly to '..\bin\java.exe'.
::            The default is "java", Example: JAVA_BINARY="C:\Program Files\Oracle\Java 16\bin\java.exe"
::            Consider using java 11 or latest if possible. (Change to OpenJDK here! https://adoptopenjdk.net/)	
SET JAVA_BINARY="java"
:: HEAP_SIZE: This is the maximum and minimum memory you plan the server will allocate.
::            By default, this is set to 4096MB, or 4GB. If you wish to allocate more than 4GB, you will need Java x64.
::            (1024M,2048M,3072M.. / 1G,2G,3G)
SET HEAP_MAX=4096
SET HEAP_MIN=1024
:: HEAP_UNIT: Selects the memory unit to be used along with heap_sizes.
::            (KB,MB,GB)
SET HEAP_UNIT=MB
:: NURSERY: Sets the nursery memory to twice heap_size and divided by 5.
::          Valid values: 'TRUE' or 'FALSE'
::          (REQUIRES OPENJ9) (IF DISABLED, JAVA AUTOMATICALLY SETS THE NURSERY TO OPTIMAL.)
SET NURSERY=FALSE


:: JVM_FLAGS: Here you can customize the JVM Flags, you should be using Aikar Flags (https://mcflags.emc.gs) for G1GC,
::            or the experimental ZGC. (From J11 up to latest) (Please consider using at least J14)
::            (Please do not put flags already set below in the "CMD".)
:: Choses JVM FLAGS MODE to use from below. Default=G1GC
SET JVM_MODE=G1GC
:: BELOW YOU CAN ADD, EDIT AND REMOVE. EJ: SET FLAGS_(NAME)=(FLAGS)
SET FLAGS_G1GC=-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:InitiatingHeapOccupancyPercent=15 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:MaxGCPauseMillis=200 -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true
SET FLAGS_ZGC=-XX:+UseZGC -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:InitiatingHeapOccupancyPercent=15 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:-UseG1GC -XX:-UseParallelGC -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true
SET FLAGS_CUSTOM=
SET FLAGS_CUSTOM2=

:: ALWAYS FLAGS (Independant of JVM_MODE)
SET DEFAULTS=-XX:+DisableExplicitGC
:: SERVER_JAR flags. (-jar paperclip.jar ->"-nogui"<-)
SET POSTJAR=-nogui
:::: END CONFIGURATION -- DON'T TOUCH ANYTHING BELOW THIS LINE!
::SCRIPT Setup
if '%1'=='-restart' GOTO restart
set MODE=%HEAP_UNIT:~0,1%
set agree=-Dcom.mojang.eula.agree=false
set advanced=-DIReallyKnowWhatIAmDoingISwear=false
if '%EULA%'=='TRUE' set agree=-DCom.mojang.eula.agree=true
if '%ADVANCEDSTART%'=='TRUE' set advanced=-DIReallyKnowWhatIAmDoingISwear=true
setlocal ENABLEDELAYEDEXPANSION
set "JVM_FLAGS=!FLAGS_%JVM_MODE%! %DEFAULTS% %agree% %advanced%"
setlocal DISABLEDELAYEDEXPANSION

if '%NURSERY%'=='TRUE' (
	set /A NURSE_MAX=%HEAP_MAX% * 2 / 5
	set /A NURSE_MIN=%HEAP_MAX% / 4
	set CMD=%JAVA_BINARY% -Xms%HEAP_MIN%%MODE% -Xmx%HEAP_MAX%%MODE% -Xmns%NURSE_MIN%%MODE% -Xmnx%NURSE_MAX%%MODE% %JVM_FLAGS% -jar %JAR_NAME% %POSTJAR%
) else set CMD=%JAVA_BINARY% -Xms%HEAP_MIN%%MODE% -Xmx%HEAP_MAX%%MODE% %JVM_FLAGS% -jar %JAR_NAME% %POSTJAR%
:: END OF SCRIPT

::Decoration
title %TITLE%
echo %DATE% - %TIME% 
echo.
echo Starting Server 
echo Loading startup parameters...
echo.
%CMD%
goto PAUSE
:PAUSE
echo.
if '%EXIT_MODE%'=='WAIT' TIMEOUT /T %WAIT_TIME%
if '%EXIT_MODE%'=='PAUSE' PAUSE
if '%ALWAYS_RESTART%'=='TRUE' ( goto restart
) else exit

:restart
echo.
echo Restarting server
echo.
cmd /c %0
cls
