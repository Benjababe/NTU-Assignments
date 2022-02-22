import java.io.IOException;
import java.io.InputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.io.OutputStream;

public class RfcTcpServer {
	static int PORT = 8082;

	public static void main(String[] args) {
		// 1. Open TCP socket at well-known port
		ServerSocket parentSocket = null;

		try {
			parentSocket = new ServerSocket(PORT);
		}

		catch (IOException e) {
			e.printStackTrace();
		}

		while (true) {
			try {
				// 2. Listen to establish TCP connection with client
				Socket childSocket = parentSocket.accept();

				// 3. Create new thread to handle client connection
				ClientHandler client = new ClientHandler(childSocket);
				Thread thread = new Thread(client);
				thread.start();
			}

			catch (IOException e) {
				e.printStackTrace();
				// wtf
				try {
					parentSocket.close();
				}

				catch (IOException ex) {
					ex.printStackTrace();
				}
			}
		}

	}
}

class ClientHandler implements Runnable {
	private Socket socket;

	ClientHandler(Socket socket) {
		this.socket = socket;
	}

	public void run() {
		try {
			// prepare memory buffer for message from client
			byte[] buffer = new byte[512];
			InputStream in = this.socket.getInputStream();

			// reads message received from client
			in.read(buffer);
			String message = new String(buffer);
			System.out.println("Received: " + message);

			// sets reply message to client
			String replyStr = "Hello client!";
			byte[] reply = replyStr.getBytes("UTF-8");

			// sends the reply to the client
			OutputStream out = this.socket.getOutputStream();
			out.write(reply);
			System.out.println("Reply sent!");
		}

		catch (IOException e) {
			e.printStackTrace();
		}
	}
}