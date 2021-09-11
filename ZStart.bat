@ECHO OFF
::##################
::# CONFIGURATION  #
::##################


:: TITLE: Set the Console Title.
SET TITLE=Minecraft: Server Instance

:: EXIT_MODE: Select between 'WAIT' or 'PAUSE' for when the server is closed/restarted.
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


:: HEAP_SIZE: This is the maxmimum memory you plan the server will allocate.
::            By default, this is set to 4096MB, or 4GB. If you wish to allocate more than 4GB, you will need Java x64.
::            (1024M, 2048M, 3072M..) or (1G, 2G, 3G..) 
:: HEAP_MIN: The minimum amount of ram that will be allocated.
SET HEAP_SIZE=4096
SET HEAP_MIN=1024
:: Select the memory mode. GB 'G' or MB 'M'. 
SET MODE=M
:: Requires MB mode. Valid values: 'TRUE' or 'FALSE' (REQUIRES OPENJ9)
SET NURSERY=FALSE

:: JVM_FLAGS: Here you can customize the JVM Flags, you should be using Aikar Flags (https://mcflags.emc.gs) for G1GC,
::            or the experimental ZGC. (From J11 up to latest) (Please consider using at least J14)
::            (Please do not put flags already set below in the "CMD".)
SET JVM_G1GC=-XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:InitiatingHeapOccupancyPercent=15 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:MaxGCPauseMillis=200 -XX:G1NewSizePercent=30 -XX:G1MaxNewSizePercent=40 -XX:G1HeapRegionSize=8M -XX:G1ReservePercent=20 -XX:G1HeapWastePercent=5 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1RSetUpdatingPauseTimePercent=5 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true
SET JVM_ZGC=-XX:+UseZGC -XX:+UnlockExperimentalVMOptions -XX:+ParallelRefProcEnabled -XX:+AlwaysPreTouch -XX:+PerfDisableSharedMem -XX:InitiatingHeapOccupancyPercent=15 -XX:SurvivorRatio=32 -XX:MaxTenuringThreshold=1 -XX:-UseG1GC -XX:-UseParallelGC -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true
:: JVM_MODE: Here you can choose to use between 'ZGC' or 'G1GC' flags.
SET JVM_MODE=G1GC



:::: END CONFIGURATION -- DON'T TOUCH ANYTHING BELOW THIS LINE!
:: SIDE NOTE: You can only change or add echos below 'title %TITLE%', or modify if you know what you are doing.
SET XMN=FALSE
if '%JVM_MODE%' == 'G1GC' SET JVM_XFLAGS=%JVM_G1GC%
if '%JVM_MODE%' == 'ZGC' SET JVM_XFLAGS=%JVM_ZGC%
if '%MODE%' == 'M' if '%NURSERY%' == 'TRUE' (
	SET XMN=TRUE
	SET /A NURSERY_MIN=%HEAP_SIZE% / 4
	SET /A NURSERY_MAX=%HEAP_SIZE% * 2 / 5
)
if '%XMN%' == 'TRUE' ( SET CMD=%JAVA_BINARY% -Xms%HEAP_MIN%M -Xmx%HEAP_SIZE%M -Xmns%NURSERY_MIN%M -Xmnx%NURSERY_MAX%M %JVM_XFLAGS% -XX:+DisableExplicitGC -Xgcpolicy:gencon -jar %JAR_NAME% -nogui
) else SET CMD=%JAVA_BINARY% -Xms%HEAP_MIN%%MODE% -Xmx%HEAP_SIZE%%MODE% %JVM_XFLAGS% -XX:+DisableExplicitGC -jar %JAR_NAMEY% -nogui

title %TITLE%
echo Starting Server
echo Loading startup parameters...
%CMD%
if '%EXIT_MODE%' == 'WAIT' TIMEOUT /T %WAIT_TIME%
if '%EXIT_MODE%' == 'PAUSE' PAUSE
exit