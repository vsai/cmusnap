package server;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.concurrent.ConcurrentHashMap;

public class MainServer {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		ServerSocket ss;
		Socket s;
		InputStream in;
		OutputStream out;
		ReadHandler rh;
		WriteHandler wh;
		
		ConcurrentHashMap<Socket, ReadHandler> readMap = new ConcurrentHashMap<Socket, ReadHandler>();
		ConcurrentHashMap<Socket, WriteHandler> writeMap = new ConcurrentHashMap<Socket, WriteHandler>();
		
		int portnum = 5000;
		
		try {
			System.out.println("Running on hostname: " + InetAddress.getLocalHost().getHostAddress());
		} catch (UnknownHostException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		try {
			ss = new ServerSocket(portnum);
			while (true) {
				s = ss.accept();
				in = s.getInputStream();
				out = s.getOutputStream();
				rh = new ReadHandler(in, writeMap);
				wh = new WriteHandler(out);
				readMap.put(s, rh);
				writeMap.put(s, wh);
				rh.start();
				System.out.println("YOLO");
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
