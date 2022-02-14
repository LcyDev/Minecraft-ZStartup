package dev.conah;
import dev.conah.utilities.Functions;
import dev.conah.utilities.Utils;

import java.io.*;
import java.util.Map;
import java.util.Objects;

import org.apache.commons.lang3.ArrayUtils;
import static java.lang.System.out;


public class ZStartup {
    public static void main (String [] args) throws IOException, InterruptedException  {
        Functions.accept_eula();
    }

    public static void readConfig() throws IOException {
        File f = new File("ZStartup-config.yml");
        //Server
        String server = "general-config.server.";
        String jar_name = Utils.Yaml(server+"jar-name", f);
        String jar_path = Utils.Yaml(server+"jar-path", f);
        Boolean eula_skip = Utils.Yaml(server+"eula-skip",f );
        String eula_flag = "";
        Boolean advanced_mode = Utils.Yaml(server+"advanced-mode", f);
        String adv_flag = "";
        String parameters = Objects.requireNonNull(Utils.Yaml(server+"parameters", f)).toString().replace("[", "").replace("]", "").replace(", ", " ");
        //Java
        String java = "general-config.java.";
        String java_binary = Utils.Yaml(java+"java-binary", f);
        Integer max_memory = Utils.Yaml(java+"max-memory", f);
        Integer min_memory = Utils.Yaml(java+"min-memory", f);
        String heap_unit = Utils.Yaml(java+"heap-unit", f);
        heap_unit = Objects.requireNonNull(heap_unit).substring(0, heap_unit.length() - 1);
        Boolean calc_nursery = Utils.Yaml(java+"calc-nursery", f);
        String nursery = "";
        Map<String, Object> flagsMap = Objects.requireNonNull(Utils.Yaml(java+"flags", f));
        String[] flags = flagsMap.keySet().toArray(new String[0]);
        flags = ArrayUtils.removeElement(flags, "DEFAULTS");
        String defaults = (Utils.Yaml(java+"flags.DEFAULTS", f));
        if (defaults!=null) {
            defaults = (" "+defaults);
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
        if (Boolean.TRUE.equals(calc_nursery) & max_memory!=null) {
            nursery = (" -Xmnx"+(max_memory * 2 / 5)+heap_unit+" -Xmns"+(max_memory / 4)+heap_unit);
        }
        // Startup variable
        String customflags = "";
        String strx;
        int i = 0;
        StringBuilder customflagsBuilder = new StringBuilder(customflags);
        while(i != flags.length) {
            Boolean str_ = Utils.Yaml(java+"flags."+flags[i]+".enable", f);
            if (Boolean.TRUE.equals(str_)) {
                strx = Utils.Yaml(java+"flags."+flags[i]+".list", f);
                if (strx!=null) {
                    strx = (" "+strx);
                } else {
                    strx = "";
                }
                customflagsBuilder.append(strx);
            }
            i++;
        }
        customflags = customflagsBuilder.toString();
        String Startup = ("\""+java_binary+"\""+" -Xmx"+max_memory+heap_unit+" -Xms"+min_memory+heap_unit+nursery+defaults+customflags+eula_flag+adv_flag+" -jar \""+jar_path+jar_name+"\" "+parameters);
        out.println(Startup);
        Runtime runtime = Runtime.getRuntime();
        try {
            runtime.exec(Startup);
        } catch (IOException e) {
        e.printStackTrace();
        }
    }
}