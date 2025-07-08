// PhantomRollUI.java
// High-Integrity Java Socket Client for PhantomRoll Control Interface
// Developed for Master's Level CS + Electrical/Electronics Engineering

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.net.Socket;

public class PhantomRollUI extends JFrame implements ActionListener {
    private static final String HOST = "127.0.0.1";
    private static final int PORT = 8879;

    private JTextArea logArea;
    private JButton startButton, stopButton, statusButton, exitButton;

    public PhantomRollUI() {
        super("幻影掷点 (PhantomRoll Control Panel)");
        initUI();
    }

    private void initUI() {
        setSize(500, 400);
        setLocationRelativeTo(null);
        setDefaultCloseOperation(EXIT_ON_CLOSE);

        JPanel panel = new JPanel();
        panel.setLayout(new GridLayout(2, 1));

        logArea = new JTextArea();
        logArea.setEditable(false);
        JScrollPane scrollPane = new JScrollPane(logArea);

        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new GridLayout(1, 4, 10, 10));

        startButton = new JButton("Start");
        stopButton = new JButton("Stop");
        statusButton = new JButton("Status");
        exitButton = new JButton("Exit");

        startButton.addActionListener(this);
        stopButton.addActionListener(this);
        statusButton.addActionListener(this);
        exitButton.addActionListener(e -> System.exit(0));

        buttonPanel.add(startButton);
        buttonPanel.add(stopButton);
        buttonPanel.add(statusButton);
        buttonPanel.add(exitButton);

        panel.add(scrollPane);
        panel.add(buttonPanel);

        add(panel);
    }

    private void sendCommand(String command) {
        try (Socket socket = new Socket(HOST, PORT);
             BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
             BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()))) {

            writer.write(command);
            writer.newLine();
            writer.flush();

            String response;
            while ((response = reader.readLine()) != null) {
                logArea.append("[SERVER] " + response + "\n");
            }

        } catch (IOException e) {
            logArea.append("[ERROR] Could not connect to PhantomRoll daemon.\n");
        }
    }

    @Override
    public void actionPerformed(ActionEvent e) {
        JButton src = (JButton) e.getSource();
        if (src == startButton) {
            logArea.append("[INFO] Sending START command...\n");
            sendCommand("start");
        } else if (src == stopButton) {
            logArea.append("[INFO] Sending STOP command...\n");
            sendCommand("stop");
        } else if (src == statusButton) {
            logArea.append("[INFO] Sending STATUS command...\n");
            sendCommand("status");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            PhantomRollUI ui = new PhantomRollUI();
            ui.setVisible(true);
        });
    }
}
