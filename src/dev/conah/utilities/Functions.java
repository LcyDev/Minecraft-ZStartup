package dev.conah.utilities;

import org.apache.commons.lang3.ArrayUtils;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.Objects;
import java.util.Scanner;

import static java.lang.System.out;

public class Functions {

    public static void accept_eula() throws IOException {
        String eula = "eula.txt";
        PrintWriter writer = new PrintWriter(eula, String.valueOf(StandardCharsets.UTF_8));
        ZonedDateTime now = ZonedDateTime.now();
        String Day = DateTimeFormatter.ofPattern("EEE").format(now);
        String Month = DateTimeFormatter.ofPattern(" MMM ").format(now);
        DateTimeFormatter dtf = DateTimeFormatter.ofPattern("dd HH:mm:ss zzz yyyy");
        writer.println("#By changing the setting below to TRUE you are indicating your agreement to our EULA (https://account.mojang.com/documents/minecraft_eula).");
        writer.println("#You also agree that tacos are tasty, and the best food in the world.");
        writer.println("#" + Utils.Capitalize(Day) + Utils.Capitalize(Month) + dtf.format(now));
        writer.println("eula=true");
        writer.println("#Automatically accepted by ZStartup");
        writer.close();
        Scanner fileScanner = null;
        try {
            fileScanner = new Scanner(new FileReader(eula));
            LineNumberReader l = new LineNumberReader(new FileReader(eula));
            String n;
            while ((n = l.readLine()) != null) {
                String line = fileScanner.nextLine();
                if (!line.equals("#")) {
                    //l.read();
                    int lN = l.getLineNumber();
                    out.println(lN);
                    out.println(line);
                }
            }
        } catch (FileNotFoundException e) {
            out.println("ERROR: File \"eula.txt\" not found.");
        }
    }

    public static String createRunCMD() throws IOException {
        File f = new File("ZStartup-config.yml");
        //Server
        String server = "general-config.server.";
        String jar_name = Utils.Yaml(server + "jar-name", f);
        String jar_path = Utils.Yaml(server + "jar-path", f);
        Boolean eula_skip = Utils.Yaml(server + "eula-skip", f);
        String eula_flag = "";
        Boolean advanced_mode = Utils.Yaml(server + "advanced-mode", f);
        String adv_flag = "";
        String parameters = Objects.requireNonNull(Utils.Yaml(server + "parameters", f)).toString().replace("[", "").replace("]", "").replace(", ", " ");
        //Java
        String java = "general-config.java.";
        String java_binary = Utils.Yaml(java + "java-binary", f);
        Integer max_memory = Utils.Yaml(java + "max-memory", f);
        Integer min_memory = Utils.Yaml(java + "min-memory", f);
        String heap_unit = Utils.Yaml(java + "heap-unit", f);
        heap_unit = Objects.requireNonNull(heap_unit).substring(0, heap_unit.length() - 1);
        Boolean calc_nursery = Utils.Yaml(java + "calc-nursery", f);
        String nursery = "";
        Map<String, Object> flagsMap = Objects.requireNonNull(Utils.Yaml(java + "flags", f));
        String[] flags = flagsMap.keySet().toArray(new String[0]);
        flags = ArrayUtils.removeElement(flags, "DEFAULTS");
        String defaults = (Utils.Yaml(java + "flags.DEFAULTS", f));
        if (defaults != null) {
            defaults = (" " + defaults);
        } else {
            defaults = "";
        }
        // Code
        if (Boolean.TRUE.equals(eula_skip)) {
            eula_flag = " -DCom.mojang.eula.agree=true";
        }
        if (Boolean.TRUE.equals(advanced_mode)) {
            adv_flag = " -DIReallyKnowWhatIAmDoingISwear=true";
        }
        if (Boolean.TRUE.equals(calc_nursery) & max_memory != null) {
            nursery = (" -Xmnx" + (max_memory * 2 / 5) + heap_unit + " -Xmns" + (max_memory / 4) + heap_unit);
        }
        // Startup variable
        String customflags = "";
        String strx;
        int i = 0;
        StringBuilder customflagsBuilder = new StringBuilder(customflags);
        while (i != flags.length) {
            Boolean str_ = Utils.Yaml(java + "flags." + flags[i] + ".enable", f);
            if (Boolean.TRUE.equals(str_)) {
                strx = Utils.Yaml(java + "flags." + flags[i] + ".list", f);
                if (strx != null) {
                    strx = (" " + strx);
                } else {
                    strx = "";
                }
                customflagsBuilder.append(strx);
            }
            i++;
        }
        customflags = customflagsBuilder.toString();
        String CMD = ("\"" + java_binary + "\"" + " -Xmx" + max_memory + heap_unit + " -Xms" + min_memory + heap_unit + nursery + defaults + customflags + eula_flag + adv_flag + " -jar \"" + jar_path + jar_name + "\" " + parameters);
        return CMD;
    }
}
