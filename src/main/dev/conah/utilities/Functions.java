package dev.conah.utilities;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
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
}
