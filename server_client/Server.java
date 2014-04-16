import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.net.SocketTimeoutException;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Server implements Runnable {   
    private final ConcurrentHashMap<Socket, WriterThread> writers = new ConcurrentHashMap<Socket, WriterThread>();
    private final ConcurrentHashMap<Socket, ReaderThread> readers = new ConcurrentHashMap<Socket, ReaderThread>();
    private final int port = 5000;
    
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
                System.err.println("Server received incoming connection!");
            } catch (IOException e) {
                System.err
                        .println("Server received IOException while listening for clients...");
                e.printStackTrace();
                break;
            }
            w = new WriterThread(newClient, writers);
            r = new ReaderThread(newClient, writers);
            writers.put(newClient, w);
            readers.put(newClient, r);
            new Thread(w).start();
            new Thread(r).start();
        }
        
    }
        public static void main(String[] args) {
            Server s = new Server();
            s.run();
        }
        
        class WriterThread implements Runnable {
            private final Socket socket;
            private final ConcurrentHashMap<Socket, WriterThread> writers;

            public WriterThread(Socket s, ConcurrentHashMap<Socket, WriterThread> writers) {
                this.socket = s;
                this.writers = writers;
            }

            @Override
            public void run() {
                while (true) {
                    try {
                        int x = System.in.read();
                        OutputStream out;
                        for (Socket w : this.writers.keySet()) {
                            out = w.getOutputStream();
                            out.write(x); // Write out to all output streams
                        }
                    } catch (SocketException socketE) {
                        writers.remove(this.socket);
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

            public ReaderThread(Socket s, ConcurrentHashMap<Socket, WriterThread> writers) {
                this.socket = s;
                this.writers = writers;
            }

            @Override
            public void run() {
                while (true) {
                    try {
                        InputStream input = (this.socket.getInputStream());
                        int x = input.read(); // get input signal from raspi
                        OutputStream out;
                        for (Socket w : this.writers.keySet()) {
                            out = w.getOutputStream();
                            out.write(x); // Write out to all sockets
                        }
                    } catch (SocketException socketE) {
                        writers.remove(this.socket);
                        return;
                    } catch (Exception e) {
                        e.printStackTrace();
                    }
                }
            }
        }
}

    

