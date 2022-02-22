import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetAddress;
import java.net.Socket;

public class RfcTcpClient {
	static int PORT = 8082;
	// localhost because I'm testing with my own TCP server
	static String SERVER_NAME = "localhost";

	public static void main(String[] args) {
		// 1. Establish TCP connection with server
		Socket socket = null;

		try {
			InetAddress serverAddr = InetAddress.getByName(SERVER_NAME);
			socket = new Socket(serverAddr, PORT);
		} catch (IOException e) {
			e.printStackTrace();
		}

		try {
			// 1.5 Prepare message to send
			String messageStr = "Hello TCP/IP server!";
			byte[] message = messageStr.getBytes("UTF-8");

			// 2. Send TCP request to server
			OutputStream os = socket.getOutputStream();
			System.out.println("Sending message...");
			os.write(message);
			System.out.println("Sent message!");

			// 3. Receive TCP reply from server
			byte[] reply = new byte[512];
			InputStream is = socket.getInputStream();
			is.read(reply);

			String replyStr = new String(reply);
			System.out.println("Received reply: " + replyStr);
		}

		catch (IOException e) {
			e.printStackTrace();
		}
	}

}
