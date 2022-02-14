package dev.conah;
import dev.conah.utilities.Functions;

import java.io.*;

import static java.lang.System.out;


public class ZStartup {
    public static void main (String [] args) throws IOException, InterruptedException  {
        Functions.accept_eula();

        String StartCMD = Functions.createRunCMD();
        out.println(StartCMD);
        Runtime runtime = Runtime.getRuntime();
        try {
            runtime.exec(StartCMD);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}