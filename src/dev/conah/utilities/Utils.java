package dev.conah.utilities;

import org.yaml.snakeyaml.Yaml;

import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;
import java.util.Map;

public class Utils {


    public static String Capitalize(String str) {
        // Get first letter using substring
        String firstLetStr = str.substring(0, 1);
        // Get remaining letter using substring
        String remLetStr = str.substring(1);
        // Put together the first letter and remaining string;
        return (firstLetStr.toUpperCase() + remLetStr);
    }


    public static <T> T Yaml(String keypath, File file) throws IOException {
        Yaml yaml = new Yaml();
        Reader yamlFile = new FileReader(file.getCanonicalPath());
        Map<?, ?> data = yaml.load(yamlFile);
        String[] parts = keypath.split("\\.");
        Object strz;
        // Initialize strx.
        try {
            Map<?, ?> strx = (Map<?, ?>) data.get(parts[0]);
            strz = strx;
            int i = 1;
            while (i != (parts.length)) {
                // Loop through all string indexs and try to get map.
                try {
                    strx = (Map<?, ?>) strx.get(parts[i]);
                    strz = strx;
                    i++;
                } catch (ClassCastException e) {
                    // Catch if strx can't get a map and return a value instead.
                    strz = strx.get(parts[i]);
                    break;
                }
            }
        } catch (ClassCastException e) {
            strz = data.get(parts[0]);
        } catch (NullPointerException e){
            return null;
        }
        if (strz != null) {
            return (T) strz;
        } else {
            return null;
        }
    }
}
