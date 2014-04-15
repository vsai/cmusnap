package server;

import java.io.IOException;
import java.io.OutputStream;

public class WriteHandler {
	
	OutputStream out;
	public WriteHandler(OutputStream out){
		this.out = out;
	}
	
	public void writeInt(int messageNum) throws IOException {
		out.write(messageNum);
	}
}
