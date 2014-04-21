import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Server implements Runnable {   
    private final ConcurrentHashMap<Socket, WriterThread> writers = new ConcurrentHashMap<Socket, WriterThread>();
    private final ConcurrentHashMap<Socket, ReaderThread> readers = new ConcurrentHashMap<Socket, ReaderThread>();
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
        WriterThread w;
        ReaderThread r;
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
            w = new WriterThread(newClient, writers, readers);
            r = new ReaderThread(newClient, writers, readers);
            writers.put(newClient, w);
            readers.put(newClient, r);
            new Thread(w).start();
            new Thread(r).start();
        }
        
    }
        
        class WriterThread implements Runnable {
            private final Socket socket;
            private final ConcurrentHashMap<Socket, WriterThread> writers;
            private final ConcurrentHashMap<Socket, ReaderThread> readers;

            public WriterThread(Socket s, ConcurrentHashMap<Socket, WriterThread> writers, 
                    ConcurrentHashMap<Socket, ReaderThread> readers) {
                this.socket = s;
                this.writers = writers;
                this.readers = readers;
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
                        for (Socket w : this.writers.keySet()) {
                            out = w.getOutputStream();
                            out.write(command); 
                        }
                    } catch (SocketException socketE) {
                        writers.remove(this.socket);
                        readers.remove(this.socket);
                        return;
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
        
        class ReaderThread implements Runnable {
            private final Socket socket;
            private final ConcurrentHashMap<Socket, WriterThread> writers;
            private final ConcurrentHashMap<Socket, ReaderThread> readers;

            public ReaderThread(Socket s, ConcurrentHashMap<Socket, WriterThread> writers, 
                    ConcurrentHashMap<Socket, ReaderThread> readers) {
                this.socket = s;
                this.writers = writers;
                this.readers = readers;

            }

            @Override
            public void run() {
                InputStream in;
                OutputStream out;
                int command;
                while (true) {
                    try {
                        in = this.socket.getInputStream();
                        command = in.read(); // get input signal from raspi

                        if (command == -1) {
                            System.err.println("Socket broken, terminating connection.");
                            throw new SocketException();
                        }
                        else if (!((command == '0') || (command == '1'))) {
                            System.err.println("Invalid command " + command);
                            continue;
                        }
                        
                        //Write out to all sockets
                        for (Socket w : this.writers.keySet()) {
                            out = w.getOutputStream();
                            out.write(command); 
                        }
                    } catch (SocketException socketE) {
                        writers.remove(this.socket);
                        readers.remove(this.socket);
                        return;
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
}

