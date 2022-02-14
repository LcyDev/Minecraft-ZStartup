package cona.hiromi;

import java.io.Console;
import java.io.File;
import java.io.FileNotFoundException;
import java.util.Objects;
import java.util.Scanner;

public class Storage {
/**
    public void eulat1; {
        Scanner fileScanner = null;
        try {
            // Check if eula.txt exists
            fileScanner = new Scanner(new File(eula));
            while (fileScanner.hasNext()) {
                String line = fileScanner.nextLine();
                if (line.equals("eula=false")) {
                    accept_eula();
                } else if (line.equals("eula=true")) {
                    break;
                } else {
                    accept_eula();
                }
            }
        } catch (
                FileNotFoundException e) {
            accept_eula();
        }
    }
 */
/**
File f = new File("ZStartup-config.yml");
    //Console
    String console = "general-config.console.";
    String title = Utils.Yaml(console+"title", f);
    File server_path = new File((String) Objects.requireNonNull(Utils.Yaml(console + "server-path", f)));
    server_path = new File(server_path.getCanonicalPath());
        out.println(server_path);
        System.setProperty("user.dir", server_path.getCanonicalPath());
    Boolean restart_loop = Utils.Yaml(console+"restart-loop", f);
    Boolean auto_eula = Utils.Yaml(console+"auto-eula", f);
    Boolean auto_start = Utils.Yaml(console+"auto-start", f);
    String wait_mode = Utils.Yaml(console+"wait-mode", f);
    Integer wait_timer = Utils.Yaml(console+"wait-timer", f);
    Boolean exit_on_stop = Utils.Yaml(console+"exit-on-stop", f);
        if (Boolean.TRUE.equals(auto_eula)) {
        accept_eula();
    }
        if (Boolean.TRUE.equals(auto_start)) {
        startServer();
    }
    Scanner scanner = new Scanner(System.in);
    Console c = System.console();
        if (c!=null) {
        boolean exit = false;
        while (!exit) {
            try {
                c.wait(20);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
        */
}
