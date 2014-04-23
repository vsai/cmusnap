import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.concurrent.ConcurrentHashMap;

public class Server implements Runnable {   
    final ConcurrentHashMap<Integer, Socket> nicknames = new ConcurrentHashMap<Integer, Socket>();
    final ConcurrentHashMap<Integer, Socket> active = new ConcurrentHashMap<Integer, Socket>();
    private final int port = 5000;
    
    public static void main(String[] args) {
        Server s = new Server();
        s.run();
    }
    
    @Override
    public void run() {
        final ServerSocket serverSocket;
        try {
            serverSocket = new ServerSocket(port);
        } catch (IOException e) {
            System.err.println("Could not open server socket on port: " + port);
            e.printStackTrace();
            return;
        }

        /*
         * Keep accepting connections to a map server while tablets remain to
         * map
         */
        ClientData d = new ClientData(nicknames, active);
        int count = 0;
        while (true) {
            Socket newClient = null;
            try {
                // Wait for an incoming client connection
                System.err
                        .println("Server waiting for incoming connections...");
                newClient = serverSocket.accept();
                System.err.println("Server received incoming connection from " + newClient.getInetAddress().toString());
            } catch (IOException e) {
                System.err
                        .println("Server received IOException while listening for clients...");
                e.printStackTrace();
                break;
            }
            nicknames.put(count, newClient);
            active.put(count, newClient);
            new Thread(new WriterThread(count, d)).start();
            new Thread(new ReaderThread(count, d)).start();
            count += 1;
        }
        
    }
        // Encapsulates all data required by the reader/writer threads
        class ClientData {
            final ConcurrentHashMap<Integer, Socket> nicknames;
            final ConcurrentHashMap<Integer, Socket> active;
            
            ClientData(ConcurrentHashMap<Integer, Socket> nicknames,
                       ConcurrentHashMap<Integer, Socket> active) {
                this.nicknames = nicknames;
                this.active = active;
            }

            void deleteSocket(int s) {
                this.nicknames.remove(s);
                this.active.remove(s);
            }
        }
        
        class WriterThread implements Runnable {
            private final int nickname;
            private final Socket s;
            private final ClientData data;
            private final String ip;

            public WriterThread(int nickname, ClientData d) {
                this.nickname = nickname;
                this.data = d;
                this.s = d.nicknames.get(nickname);
                this.ip = this.s.getInetAddress().toString();
            }

            @Override
            public void run() {
                int command;
                OutputStream out;
                while (true) {
                    try {
                        //Read from stdin
                        command = System.in.read();
                        if (command == -1) {
                            System.err.println("Socket broken, terminating connection.");
                            throw new SocketException();
                        }

                        else if (!((command == '0') || (command == '1'))) {
                            System.err.println("Invalid command " + command);
                            continue;
                        }
                        
                        // Write out to all output streams
                        for (Socket w : this.data.active.values()) {
                            out = w.getOutputStream();
                            out.write(command); 
                        }
                    } catch (SocketException socketE) {
                        this.data.deleteSocket(nickname);
                        return;
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        
        class ReaderThread implements Runnable {
            private final int nickname;
            private final Socket s;
            private final ClientData data;
            private final String ip;

            public ReaderThread(int nickname, ClientData d) {
                this.nickname = nickname;
                this.data = d;
                this.s = d.nicknames.get(nickname);
                this.ip = this.s.getInetAddress().toString();
            }

            @Override
            public void run() {
                InputStream in;
                OutputStream out;
                int command;
                while (true) {
                    try {
                        in = this.s.getInputStream();
                        command = in.read(); // get input signal from raspi

                        if (command == -1) {
                            System.err.println("Socket broken, terminating connection.");
                            throw new SocketException();
                        }
                        else if (command == '2') {
                            if (this.data.active.containsKey(nickname)) {
                                System.err.println("Removing pi " + nickname + " at " + ip + " from active.");
                                this.data.active.remove(nickname);
                            }
                            else {
                                System.err.println("Adding pi " + nickname + " at " + ip + "  to active.");
                                this.data.active.put(nickname, s);
                            }
                        }
                        else if (!((command == '0') || (command == '1'))) {
                            System.err.println("Invalid command " + command);
                            continue;
                        }
                        else {
                            System.err.println("Got command " + command + " from pi at " + ip);
                        }
                        
                        //Write out to all sockets
                        for (Socket w : this.data.active.values()) {
                            out = w.getOutputStream();
                            out.write(command); 
                        }
                    } catch (SocketException socketE) {
                        this.data.deleteSocket(nickname);
                        return;
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                    
                }
            }
        }
}



