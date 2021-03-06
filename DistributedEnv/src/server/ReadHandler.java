package server;

import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;
import java.util.concurrent.ConcurrentHashMap;

public class ReadHandler extends Thread {
	
	InputStream in;
	ConcurrentHashMap<Socket, WriteHandler> writes;
	
	public ReadHandler(InputStream in, ConcurrentHashMap<Socket, WriteHandler> writes){
		this.in = in;
		this.writes = writes;
	}
	
	public void run() {
		int messageNum;
		
		while(true){
			try {
				messageNum = in.read();
				System.out.printf("Received %d from socket\n", messageNum);
				if (messageNum == -1){
					System.out.println("SOCKET BROKEN PIPE");
					//MUST REMOVE THE READ AND WRITE HANDLERS FROM THE HASHMAP
					break;
				}
				for (WriteHandler w : writes.values()) {
					w.writeInt(messageNum);
				}
				System.out.println("Wrote to all sockets");
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

}
